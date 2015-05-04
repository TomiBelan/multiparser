
# USAGE: python3 -m mgr.dump my_grammar_file.mgr

import sys
from mgr.read import read_grammar

if __name__ == '__main__':
    g = read_grammar(sys.argv[1])
    print('PROPERTIES:')
    print(g.properties)
    print('RULES:')
    for nt in sorted(g.rules):
        for r,a in sorted(g.rules[nt]):
            print('   ', nt, '->', (r, a))
