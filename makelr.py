
# USAGE: python3 makelr.py file.mgr file_out.py
# But you may want to use compose.py instead.

from grammar import ReprWrap

with open(__file__[:-3] + '_template') as f:
    parser_template = f.read()


class State:
    def __init__(self, kernel):
        self.kernel = kernel
        self.items = None
        self.actions = None


def build_closure(grammar, kernel):
    items = set(kernel)

    while True:
        new_items = set()

        for nt, (rule, action), index, lookahead in items:
            rest = rule[index:]
            if not rest: continue
            symbol = rest[0]
            if symbol not in grammar.rules: continue

            lookaheads = grammar.get_first(rest[1:] + (lookahead,))

            for rule2, action2 in grammar.rules[symbol]:
                for beta in lookaheads:
                    item = (symbol, (rule2, action2), 0, beta)
                    if item not in items: new_items.add(item)

        if not new_items: break
        items.update(new_items)

    return items


def resolve_conflict(grammar, symbol, kernel, shifts, reduces):
    ignore_reduces = grammar.properties.get('ignore_reduces')
    if len(reduces[symbol]) != 1:
        new_reduces = set()
        for (nt, rule, action) in reduces[symbol]:
            if (nt, rule, symbol) not in ignore_reduces:
                new_reduces.add((nt, rule, action))

        if new_reduces:
            reduces[symbol] = new_reduces
        else:
            del reduces[symbol]
            return

    precedence_rules = grammar.properties.get('precedence')
    if precedence_rules and symbol in shifts and len(reduces[symbol]) == 1:
        reduce_nt, reduce_rule, reduce_action = list(reduces[symbol])[0]
        terminals = [s for s in reduce_rule if s not in grammar.rules]
        last_terminal = terminals[-1] if terminals else None

        for precedence_rule in precedence_rules:
            shift_index = reduce_index = None

            for i, precedence_level in enumerate(precedence_rule):
                type, symbols = precedence_level
                if symbol in symbols: shift_index = i
                if last_terminal in symbols: reduce_index = i
                if (reduce_nt, reduce_rule) in symbols: reduce_index = i

            if shift_index != None and reduce_index != None:
                if reduce_index > shift_index:
                    del shifts[symbol]
                    return
                if reduce_index < shift_index:
                    del reduces[symbol]
                    return

                type, symbols = precedence_rule[shift_index]
                if type == 'left':
                    del shifts[symbol]
                    return
                elif type == 'right':
                    del reduces[symbol]
                    return
                elif type == 'nonassoc':
                    del shifts[symbol]
                    del reduces[symbol]
                    return
                elif type == 'precedence':
                    pass
                else:
                    raise ValueError('Unknown precedence rule type: %r' % type)

    if symbol in shifts:
        msg = []
        msg.append('SHIFT-REDUCE CONFLICT')
        msg.append('Lookahead symbol: %r' % symbol)
        msg.append('Rules that can be shifted:')
        distinct_shifts = set((nt, rule, shifted_index - 1)
                              for nt, (rule, action), shifted_index, lookahead in shifts[symbol])
        for nt, rule, index in distinct_shifts:
            msg.append('  %s -> %s <*> %s' % (nt, ' '.join(rule[:index]), ' '.join(rule[index:])))
        msg.append('Rules that can be reduced:')
        for nt, rule, action in reduces[symbol]:
            msg.append('  %s -> %s' % (nt, ' '.join(rule)))
        raise ValueError('\n'.join(msg))

    if len(reduces[symbol]) != 1:
        msg = []
        msg.append('REDUCE-REDUCE CONFLICT')
        msg.append('Lookahead symbol: %r' % symbol)
        msg.append('Rules that can be reduced:')
        for nt, rule, action in reduces[symbol]:
            msg.append('  %s -> %s' % (nt, ' '.join(rule)))
        raise ValueError('\n'.join(msg))


def build_actions(grammar, ordered_rules_map, kernel, items):
    shifts = {}
    reduces = {}

    for nt, (rule, action), index, lookahead in items:
        if index < len(rule):
            symbol = rule[index]
            if symbol not in shifts:
                shifts[symbol] = set()
            shifts[symbol].add((nt, (rule, action), index+1, lookahead))
        else:
            if lookahead not in reduces:
                reduces[lookahead] = set()
            reduces[lookahead].add((nt, rule, action))

    for symbol in shifts:
        shifts[symbol] = frozenset(shifts[symbol])

    for symbol in list(reduces):
        if symbol in shifts or len(reduces[symbol]) != 1:
            resolve_conflict(grammar, symbol, kernel, shifts, reduces)

    for symbol in reduces:
        reduces[symbol] = (False, ordered_rules_map[reduces[symbol].pop()])

    return shifts, reduces


def dump_items(items):
    by_rule = {}
    for nt, (rule, action), index, lookahead in items:
        by_rule.setdefault((nt, rule, index), set()).add(lookahead)
    for (nt, rule, index), lookaheads in by_rule.items():
        print(nt, '->', ' '.join(rule[:index]), '<*>', ' '.join(rule[index:]), '~~~', sorted(lookaheads))


def make_lr_table(grammar):
    ordered_rules = []
    ordered_rules_map = {}
    initial_states_map = {}

    for nt in grammar.rules:
        for rule, action in grammar.rules[nt]:
            ordered_rules_map[(nt, rule, action)] = len(ordered_rules)
            ordered_rules.append((nt, rule, ReprWrap(action)))

    table = []
    queue = set()
    kernels_map = {}

    for nt, close_with in grammar.initial_states:
        ordered_rules_map[(None, (nt,), None)] = None
        initial_item = (None, ((nt,), None), 0, close_with)
        kernel = frozenset([initial_item])

        initial_states_map[(nt, close_with)] = len(table)
        kernels_map[kernel] = len(table)
        table.append(State(kernel))
        queue.add(table[-1])

    while queue:
        state = queue.pop()
        print(len(table), end='\r')

        state.items = build_closure(grammar, state.kernel)

        shifts, reduces = build_actions(grammar, ordered_rules_map, state.kernel, state.items)
        state.actions = {}

        for symbol, kernel in shifts.items():
            if kernel not in kernels_map:
                kernels_map[kernel] = len(table)
                table.append(State(kernel))
                queue.add(table[-1])
            state.actions[symbol] = (True, kernels_map[kernel])

        state.actions.update(reduces)

    table = [state.actions for state in table]
    return initial_states_map, ordered_rules, table


def generate_parser(grammar, initial_states_map, ordered_rules, table):
    return grammar.preface + parser_template % dict(
        start=grammar.properties['default_start'],
        initial=initial_states_map, rules=ordered_rules, table=table)


def make_lr_parser(grammar):
    initial_states_map, ordered_rules, table = make_lr_table(grammar)
    return generate_parser(grammar, initial_states_map, ordered_rules, table)


def main(input_filename, output_filename):
    from mgr.read import read_grammar
    grammar = read_grammar(input_filename)
    parser = make_lr_parser(grammar)
    if not output_filename.endswith('.py'): raise ValueError(output_filename)
    with open(output_filename, 'w') as f:
        f.write(parser)


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
