
from collections import namedtuple

Add = namedtuple('Add', 'location left right')
Sub = namedtuple('Sub', 'location left right')
Mul = namedtuple('Mul', 'location left right')
Div = namedtuple('Div', 'location left right')
Pow = namedtuple('Pow', 'location left right')
UnaryMin = namedtuple('UnaryMin', 'location operand')

Number = namedtuple('Number', 'location value')
Embedded = namedtuple('Embedded', 'location content')
