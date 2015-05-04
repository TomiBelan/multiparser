
# USAGE: python3 makepeg.py <file>.ebnf <file>_out.py
#
# makepeg.py creates two output files. The first output file is always named
# <file>_ebnf_out.py. The second output file can be renamed, but it is
# generally called <file>_out.py.

import os
import re
import sys
import subprocess


with open(__file__[:-3] + '_template') as f:
    parser_template, method_template, choice_template = f.read().split('\n---\n')


def run_grako(input_filename, output_filename, force=False):
    """Runs Grako to create the base PEG parser (foo_ebnf_out.py)."""

    if input_filename.startswith('-'): raise ValueError('bad input filename')
    if output_filename.startswith('-'): raise ValueError('bad output filename')

    try:
        input_mtime = os.path.getmtime(input_filename)
        output_mtime = os.path.getmtime(output_filename)
        if output_mtime > input_mtime and not force: return
    except OSError:
        pass

    subprocess.check_call([sys.executable, '-m', 'grako',
                           input_filename, '-o', output_filename])


def make_peg_parser(input_filename, embeds, module_name=None):
    """Creates the secondary PEG parser file which overrides Grako's defaults
    with Multiparser's own customizations.
    """

    with open(input_filename, 'r', encoding='utf8') as f:
        grammar = f.read()

    match = re.search(r'\(\*multiparser_options\(([\s\S]*?)\)\*\)', grammar)
    options = match.group(1) if match else ''

    parser_name = os.path.splitext(os.path.basename(input_filename))[0]
    module_name = module_name or '.%s_ebnf_out' % parser_name

    choices = {}
    for (outer, token_type, inner, start, opener, closer) in embeds:
        choices.setdefault(token_type, []).append(choice_template %
            dict(inner=inner, start=start, opener=opener, closer=closer))

    methods = []
    for token_type, choice_list in choices.items():
        methods.append(method_template %
            dict(token_type=token_type, choices=''.join(choice_list)))

    return parser_template % dict(
        parser_name=parser_name, module_name=module_name,
        methods=''.join(methods), options=options)


def main(input_filename, output_filename):
    """Creates both the _ebnf_out.py file and the second _out.py file for
    the given EBNF grammar.
    """

    if not input_filename.endswith('.ebnf'): raise ValueError(input_filename)
    if not output_filename.endswith('.py'): raise ValueError(output_filename)

    grako_output_filename = input_filename[:-5] + '_ebnf_out.py'

    run_grako(input_filename, grako_output_filename)

    parser = make_peg_parser(input_filename, [])
    with open(output_filename, 'w') as f:
        f.write(parser)


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
