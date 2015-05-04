
from collections import defaultdict, namedtuple

from context import ParserContext
from grammar import Grammar
from mgr.parser_out import parse, SimpleRule, ExtendedRule, Symbol, Subrule, SubruleReference


# A helper class that keeps track of everything we need while converting a rule.
RuleData = namedtuple('RuleData',
    'rules normal_vars list_vars make_nonterminal mgr_left')


def _convert_items(items, data):
    """Converts 'items' (a list of symbols etc) into a lambda function which can
    be used either as a subrule action or as the main action's root= argument.
    """
    converted_items = []
    action_args = ['ctx']
    action_body = []

    for i, item in enumerate(items):
        i += 1
        action_args.append('v%d' % i)
        if isinstance(item, Symbol):
            if item.label and item.append:
                data.list_vars.add(item.label)
            elif item.label:
                data.normal_vars.add(item.label)
            converted_items.append(item.value)
            action_body.append('(%r, v%d)' % (item.label, i))
        elif isinstance(item, Subrule):
            converted_items.append(_convert_subrule(item, data))
            action_body.append('v%d' % i)
        elif isinstance(item, SubruleReference):
            converted_items.append('%s__%d' % (data.mgr_left, item.index))
            action_body.append('v%d' % i)

    action = 'lambda %s: [%s]' % (', '.join(action_args), ', '.join(action_body))
    return (tuple(converted_items), action)


def _convert_subrule(subrule, data):
    """Converts the subrule into a new nonterminal. Returns its name."""
    left, srindex = data.make_nonterminal(data.mgr_left)
    for branch in subrule.branches:
        if subrule.type == '*':
            data.rules[left].append(_convert_items(branch.items + [SubruleReference(srindex)], data))
        else:
            data.rules[left].append(_convert_items(branch.items, data))
    if subrule.type == '?' or subrule.type == '*':
        data.rules[left].append(_convert_items([], data))
    return left


def _convert_rule(rule, rules, make_nonterminal):
    """Converts the given SimpleRule or ExtendedRule to Grammar rules."""

    if isinstance(rule, SimpleRule):
        rules[rule.left].append((tuple(rule.right), rule.action))
        return

    normal_vars = set()
    list_vars = set()
    meta_vars = set(('_ctx', '_loc', '_all'))
    data = RuleData(rules, normal_vars, list_vars, make_nonterminal, rule.left)

    right, root_action = _convert_items(rule.right, data)
    if normal_vars & list_vars:
        raise ValueError("Normal var and list var cannot have the same name")
    if (normal_vars | list_vars) & meta_vars:
        raise ValueError("Label cannot have reserved name")
    user_args = ', '.join(normal_vars | list_vars | meta_vars)
    full_action = ('combine_action(root=%s, user=lambda %s: (\n%s\n), normal_vars=%r, list_vars=%r)' %
        (root_action, user_args, rule.action, sorted(normal_vars), sorted(list_vars)))
    rules[rule.left].append((right, full_action))


def convert_grammar(mgr_grammar, initial_states=None):
    """Converts the given MgrGrammar (an AST representation of a .mgr file) into
    a grammar.Grammar object (a generic context-free grammar).
    """
    preface = mgr_grammar.preface
    rules = { rule.left: [] for rule in mgr_grammar.rules }

    helper_counters = defaultdict(lambda: 0)

    def make_nonterminal(prefix):
        while True:
            helper_counters[prefix] += 1
            proposed_name = '%s__%d' % (prefix, helper_counters[prefix])
            if proposed_name in rules: continue
            rules[proposed_name] = []
            return proposed_name, helper_counters[prefix]

    for rule in mgr_grammar.rules:
        _convert_rule(rule, rules, make_nonterminal)

    if any(isinstance(rule, ExtendedRule) for rule in mgr_grammar.rules):
        preface += '\nfrom context import combine_action\n'

    return Grammar(preface, mgr_grammar.properties, rules, initial_states)


def read_grammar(filename, initial_states=None):
    """Reads the mgr grammar from the given file and returns a Grammar."""
    with open(filename) as f:
        content = f.read()
    ctx = ParserContext(content)
    mgr_grammar = parse(ctx)
    return convert_grammar(mgr_grammar, initial_states)

