
from collections import namedtuple

Block = namedtuple('Block', 'statements')

Assignment = namedtuple('Assignment', 'location lhs rhs')
Label = namedtuple('Label', 'location name')
Break = namedtuple('Break', 'location')
Goto = namedtuple('Goto', 'location name')
BlockStatement = namedtuple('BlockStatement', 'location block')
While = namedtuple('While', 'location condition body')
Repeat = namedtuple('Repeat', 'location body condition')
If = namedtuple('If', 'location conditions bodies')
NumericFor = namedtuple('NumericFor', 'location var initial limit step body')
GenericFor = namedtuple('GenericFor', 'location vars explist body')
Function = namedtuple('Function', 'location funcname params body')
LocalFunction = namedtuple('LocalFunction', 'location funcname params body')
Local = namedtuple('Local', 'location lhs rhs')
EmbedStatement = namedtuple('EmbedStatement', 'location content')
Return = namedtuple('Return', 'location explist')

FuncName = namedtuple('FuncName', 'dotnames colonname')

Name = namedtuple('Name', 'location name')
Dot = namedtuple('Dot', 'location left name')
Brackets = namedtuple('Brackets', 'location left right')
FunctionCall = namedtuple('FunctionCall', 'location left methodname arglist')
BinOp = namedtuple('BinOp', 'location left op right')
UnaryOp = namedtuple('UnaryOp', 'location op right')

LuaNil = namedtuple('LuaNil', 'location')
LuaFalse = namedtuple('LuaFalse', 'location')
LuaTrue = namedtuple('LuaTrue', 'location')
Number = namedtuple('Number', 'location value')
String = namedtuple('String', 'location value')
EmbedExpression = namedtuple('EmbedExpression', 'location content')
LuaEllipsis = namedtuple('LuaEllipsis', 'location')
TableConstructor = namedtuple('TableConstructor', 'location fields')
Field = namedtuple('Field', 'location key value')
