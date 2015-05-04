from demo_out import parse
from context import ParserContext

print(parse(ParserContext("HELLO")))

print(parse(ParserContext("IF FALSE THEN HELLO")))

print(parse(ParserContext("IF TRUE THEN IF FALSE THEN HELLO ELSE HELLO")))

print(parse(ParserContext("IF HELLO THEN TRUE")))
