
# USAGE: python3 makell.py file.mgr file_out.py
# But you may want to use compose.py instead.

from grammar import ReprWrap

with open(__file__[:-3] + '_template') as f:
    parser_template = f.read()


def make_ll_table(grammar):
    ordered_rules = []
    table = { nt: {} for nt in grammar.rules }
    llconflicts = grammar.properties.get('llconflicts') or {}

    for (nt, tok), rule in llconflicts.items():
        if nt not in grammar.rules:
            raise Exception("Unknown nonterminal in llconflicts: %r" % nt)
        if not any(irule == rule for irule, iaction in grammar.rules[nt]):
            raise Exception("Unknown rule in llconflicts: %r -> %r" % (nt, rule))

    had_conflicts = False

    for nt in grammar.rules:
        for rule, action in grammar.rules[nt]:
            index = len(ordered_rules)
            ordered_rules.append((rule, ReprWrap(action)))

            want = grammar.get_first(rule)
            if grammar.get_nullable(rule):
                want.update(grammar.follow[nt])

            for tok in want:
                if llconflicts.get((nt, tok), rule) != rule: continue
                if tok in table[nt]:
                    print("LL CONFLICT on nt %r token %r: rule %r vs rule %r\n" %
                        (nt, tok, ordered_rules[table[nt][tok]][0], rule))
                    had_conflicts = True
                table[nt][tok] = index

    if had_conflicts:
        raise Exception("conflicts in grammar")

    return ordered_rules, table


def generate_parser(grammar, rules, table):
    return grammar.preface + parser_template % dict(
        start=grammar.properties['default_start'],
        rules=rules,
        table=table)


def make_ll_parser(grammar):
    rules, table = make_ll_table(grammar)
    return generate_parser(grammar, rules, table)


def main(input_filename, output_filename):
    from mgr.read import read_grammar
    grammar = read_grammar(input_filename)
    parser = make_ll_parser(grammar)
    if not output_filename.endswith('.py'): raise ValueError(output_filename)
    with open(output_filename, 'w') as f:
        f.write(parser)


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
