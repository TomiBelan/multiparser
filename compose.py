
# USAGE 1: python3 compose.py path.to.package
#
#   Creates a composite parser in the given python package.
#   compose.py will use "import path.to.package.config" to find config.py.
#   To process "foo/bar/config.py", run "python3 compose.py foo.bar".
#
# USAGE 2: python3 compose.py <file>.mgr
#
#   Makes an LL or LR parser from <file>.mgr, depending on its "type" property.
#   Writes the result to <file>_out.py.

import os
from importlib import import_module
import makell
import makelr
import makepeg
import mgr.read


with open(__file__[:-3] + '_template') as f:
    composite_parser_template = f.read()


def make_mgr_parser(input_file, initial_states, output_file):
    """Creates a parser from a .mgr grammar file."""

    print("=====", input_file, "->", output_file, "=====")

    grammar = mgr.read.read_grammar(input_file, initial_states)

    type = grammar.properties.get('type')
    if type == 'LL':
        output = makell.make_ll_parser(grammar)
    elif type == 'LR':
        output = makelr.make_lr_parser(grammar)
    elif type:
        raise Exception('File %r specifies unknown "type"' % input_file)
    else:
        raise Exception('File %r does not specify "type"' % input_file)

    with open(output_file, 'w') as f:
        f.write(output)


def make_peg_parser(input_file, embeds, output_file):
    """Creates the _ebnf_out.py and _out.py files from an .ebnf grammar file."""

    grako_output_file = input_file[:-5] + '_ebnf_out.py'
    grako_module_name = grako_output_file[:-3].replace('/', '.')
    print("=====", input_file, "->", grako_output_file, "=====")
    makepeg.run_grako(input_file, grako_output_file)

    print("=====", input_file, "->", output_file, "=====")
    output = makepeg.make_peg_parser(input_file, embeds, grako_module_name)
    with open(output_file, 'w') as f:
        f.write(output)


def make_composite_parser(config, output_file):
    """Creates the main composite_out.py file for a composite parser."""

    print("=====", output_file, "=====")

    imports = '\n'.join(
        'from .%s_out import parse as parse_%s\nparsers[%r] = parse_%s' % (language, language, language, language)
        for language in config.languages)

    # sort by opener length
    embeds = sorted(config.embeds, key=lambda e: -len(e[4]))

    output = composite_parser_template % dict(imports=imports, embeds=embeds, root=config.root)

    with open(output_file, 'w') as f:
        f.write(output)


def compose(package_name):
    """Loads a config.py file from the given package and creates all files
    needed for the composite parser to run.
    """

    config = import_module(package_name + '.config')
    path = os.path.dirname(config.__file__)

    initial_map = { language: set() for language in config.languages }
    initial_map[config.root].add((None, 'EOF'))
    embeds_map = { language: [] for language in config.languages }
    for embed in config.embeds:
        (outer, token_type, inner, start, opener, closer) = embed
        initial_map[inner].add((start, closer))
        embeds_map[outer].append(embed)

    for language, input_file in config.languages.items():
        output_file = os.path.join(path, language + '_out.py')
        if input_file.endswith('.mgr'):
            make_mgr_parser(input_file, initial_map[language], output_file)
        elif input_file.endswith('.ebnf'):
            make_peg_parser(input_file, embeds_map[language], output_file)
        else:
           raise Exception('Unknown grammar file type: %r' % language_file)

    make_composite_parser(config, os.path.join(path, 'composite_out.py'))


if __name__ == '__main__':
    import sys
    if sys.argv[1].endswith('.mgr'):
        make_mgr_parser(sys.argv[1], None, sys.argv[1][:-4] + '_out.py')
    else:
        compose(sys.argv[1])
