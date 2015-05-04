
from .peggrammar_ebnf_out import peggrammarSemantics as BaseSemantics
from .ast import *

handlers = {
    "+": Add,
    "-": Sub,
    "*": Mul,
    "/": Div,
}

def left_associative(location, l, ops, rs):
    for op, r in zip(ops, rs):
        handler = handlers[op]
        l = handler(location, l, r)
    return l

def get_location(ast):
    parseinfo = ast.parseinfo
    lineinfo = parseinfo.buffer.line_info(parseinfo.pos)
    return (lineinfo.line + 1, lineinfo.col + 1)

class Semantics(BaseSemantics):
    def sum(self, ast):
        return left_associative(get_location(ast), ast['l'], ast['ops'], ast['rs'])

    def product(self, ast):
        return left_associative(get_location(ast), ast['l'], ast['ops'], ast['rs'])

    def factor(self, ast):
        if ast['m']: return UnaryMin(get_location(ast), ast['m'])
        return ast['p']

    def power(self, ast):
        if not ast['r']: return ast['l']
        return Pow(get_location(ast), ast['l'], ast['r'])

    def number(self, ast):
        return Number(get_location(ast), int(ast['n']))

    def embedloc(self, ast):
        return Embedded(get_location(ast), ast['e'])
