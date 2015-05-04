
# USAGE: python3 -m mgr.makeparser mgr/parser_out.py
#
# This is usually called from the Makefile.

import sys

from mgr.metagrammar import grammar
from makelr import make_lr_table, generate_parser


def main(output_filename):
    stuff = make_lr_table(grammar)
    parser = generate_parser(grammar, *stuff)
    if not output_filename.endswith('.py'): raise ValueError(output_filename)
    with open(output_filename, 'w') as f:
        f.write(parser)

if __name__ == '__main__':
    main(*sys.argv[1:])
