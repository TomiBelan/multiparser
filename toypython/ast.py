
from collections import namedtuple

def convert_to_real_ast(obj):
    """Converts 'obj' to an object from the 'ast' standard library. Untested."""
    if isinstance(obj, list):
        return [convert_to_real_ast(item) for item in obj]
    if isinstance(obj, tuple) and hasattr(obj, '_replace'):
        import ast
        name = obj.__class__.__name__
        real_class = getattr(ast, name)
        fields = obj[:]
        extra = {}
        if hasattr(obj, 'location'):
            fields = obj[1:]
            extra = { 'lineno': obj.location[0], 'col_offset': 0 }   # TODO: col_offset
        fields = [convert_to_real_ast(item) for item in fields]
        return real_class(*fields, **extra)
    if isinstance(obj, (int, str, bytes)) or obj is None:
        return obj
    raise TypeError(obj.__class__.__name__)

# mod

Module = namedtuple('Module', 'body')
Interactive = namedtuple('Interactive', 'body')
Expression = namedtuple('Expression', 'body')

# stmt

FunctionDef = namedtuple('FunctionDef', 'location name args body decorator_list returns')
ClassDef = namedtuple('ClassDef', 'location name bases keyword starargs kwargs body decorator_list')
Return = namedtuple('Return', 'location value')

Delete = namedtuple('Delete', 'location targets')
Assign = namedtuple('Assign', 'location targets value')
AugAssign = namedtuple('AugAssign', 'location target op value')
For = namedtuple('For', 'location target iter body orelse')
While = namedtuple('While', 'location test body orelse')
If = namedtuple('If', 'location test body orelse')
With = namedtuple('With', 'location items body')

Raise = namedtuple('Raise', 'location exc cause')
Try = namedtuple('Try', 'location body handlers orelse finalbody')
Assert = namedtuple('Assert', 'location test msg')

Import = namedtuple('Import', 'location names')
ImportFrom = namedtuple('ImportFrom', 'location module names level')

Global = namedtuple('Global', 'location names')
Nonlocal = namedtuple('Nonlocal', 'location names')
Expr = namedtuple('Expr', 'location value')
Pass = namedtuple('Pass', 'location')
Break = namedtuple('Break', 'location')
Continue = namedtuple('Continue', 'location')

EmbedStat = namedtuple('EmbedStat', 'location value')

# expr

BoolOp = namedtuple('BoolOp', 'location op values')
BinOp = namedtuple('BinOp', 'location left op right')
UnaryOp = namedtuple('UnaryOp', 'location op operand')
Lambda = namedtuple('Lambda', 'location args body')
IfExp = namedtuple('IfExp', 'location test body orelse')
Dict = namedtuple('Dict', 'location keys values')
Set = namedtuple('Set', 'location elts')
ListComp = namedtuple('ListComp', 'location elt generators')
SetComp = namedtuple('SetComp', 'location elt generators')
DictComp = namedtuple('DictComp', 'location key value generators')
GeneratorExp = namedtuple('GeneratorExp', 'location elt generators')
Yield = namedtuple('Yield', 'location value')
YieldFrom = namedtuple('YieldFrom', 'location value')
Compare = namedtuple('Compare', 'location left ops comparators')
Call = namedtuple('Call', 'location func args keywords starargs kwargs')
Num = namedtuple('Num', 'location n')
Str = namedtuple('Str', 'location s')
Bytes = namedtuple('Bytes', 'location s')
NameConstant = namedtuple('NameConstant', 'location value')
Ellipsis = namedtuple('Ellipsis', 'location')

EmbedExp = namedtuple('EmbedExp', 'location value')

Attribute = namedtuple('Attribute', 'location value attr ctx')
Subscript = namedtuple('Subscript', 'location value slice ctx')
Starred = namedtuple('Starred', 'location value ctx')
Name = namedtuple('Name', 'location id ctx')
List = namedtuple('List', 'location elts ctx')
Tuple = namedtuple('Tuple', 'location elts ctx')

# expr_context

Load = namedtuple('Load', '')
Store = namedtuple('Store', '')
Del = namedtuple('Del', '')
AugLoad = namedtuple('AugLoad', '')
AugStore = namedtuple('AugStore', '')
Param = namedtuple('Param', '')

# slice

Slice = namedtuple('Slice', 'lower upper step')
ExtSlice = namedtuple('ExtSlice', 'dims')
Index = namedtuple('Index', 'value')

# boolop

And = namedtuple('And', '')
Or = namedtuple('Or', '')

# operator

Add = namedtuple('Add', '')
Sub = namedtuple('Sub', '')
Mult = namedtuple('Mult', '')
Div = namedtuple('Div', '')
Mod = namedtuple('Mod', '')
Pow = namedtuple('Pow', '')
LShift = namedtuple('LShift', '')
RShift = namedtuple('RShift', '')
BitOr = namedtuple('BitOr', '')
BitXor = namedtuple('BitXor', '')
BitAnd = namedtuple('BitAnd', '')
FloorDiv = namedtuple('FloorDiv', '')

# unaryop

Invert = namedtuple('Invert', '')
Not = namedtuple('Not', '')
UAdd = namedtuple('UAdd', '')
USub = namedtuple('USub', '')

# cmpop

Eq = namedtuple('Eq', '')
NotEq = namedtuple('NotEq', '')
Lt = namedtuple('Lt', '')
LtE = namedtuple('LtE', '')
Gt = namedtuple('Gt', '')
GtE = namedtuple('GtE', '')
Is = namedtuple('Is', '')
IsNot = namedtuple('IsNot', '')
In = namedtuple('In', '')
NotIn = namedtuple('NotIn', '')

# misc

comprehension = namedtuple('comprehension', 'target iter ifs')
ExceptHandler = namedtuple('ExceptHandler', 'location type name body')
arguments = namedtuple('arguments', 'args vararg kwonlyargs kw_defaults kwarg defaults')
arg = namedtuple('arg', 'location arg annotation')
keyword = namedtuple('keyword', 'arg value')
alias = namedtuple('alias', 'name asname')
withitem = namedtuple('withitem', 'context_expr optional_vars')
