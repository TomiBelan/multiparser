
# USAGE: python3 runparser.py somepackage.somemodule input_data.txt
#
# "somepackage.somemodule" corresponds to "somepackage/somemodule.py"
#
# E.g.:
# python3 runparser.py toypython.grammar_out mgr/makeparser.py | less

import sys
import context
import importlib


def print_line(content, level, indent):
    before = '\u2502' + ' ' * (indent-1)
    final = '\u251C' + '\u2500' * (indent-1)
    for i in range(level):
        print('\033[%dm%s' % (31 + i%7, final if i == level-1 else before), end='')
    print('\033[0m', end='')
    print(content)

def print_color_tree(value, label='', level=0, indent=2):
    """Shows a parse tree with pretty colors.

    The colors don't mean anything, they just make it easier to see which
    line is which.
    """
    if isinstance(value, tuple) and hasattr(value, '_asdict'):
        print_line(label + value.__class__.__module__ + '.' + value.__class__.__name__, level, indent)
        value = value._asdict()
    elif isinstance(value, dict):
        print_line(label + 'dict', level, indent)

    if isinstance(value, dict):
        for k, v in value.items():
            print_color_tree(v, k + ': ', level + 1, indent)
    elif isinstance(value, list):
        print_line(label + 'list', level, indent)
        for i, v in enumerate(value):
            print_color_tree(v, str(i) + ': ', level + 1, indent)
    else:
        print_line(label + repr(value), level, indent)


if __name__ == '__main__':
    parser = importlib.import_module(sys.argv[1])
    with open(sys.argv[2]) as f:
        content = f.read()
    try:
        if hasattr(parser, 'parse_text'):
            # it is a composite parser
            result = parser.parse_text(content)
        else:
            # it is a standalone parser
            ctx = context.ParserContext(content)
            result = parser.parse(ctx)
    except context.ParseError as e:
        print('Error:', e)
    else:
        print_color_tree(result)
