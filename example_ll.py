from grammar import Grammar
from makell import make_ll_parser

preface = "from toycalc.lex import tokenizer"

rules = {
    # stat -> HELLO | IF cond THEN stat optional_else
    "stat": [(("HELLO",), "lambda ctx, a: 'hello'"),
             (("IF", "cond", "THEN", "stat", "optional_else"),
              "lambda ctx, a, b, c, d, e: ('if', b, d, e)")],

    # cond -> TRUE | FALSE
    "cond": [(("TRUE",), "lambda ctx, a: True"),
             (("FALSE",), "lambda ctx, a: False")],

    # optional_else -> ELSE stat | epsilon
    "optional_else": [(("ELSE", "stat"), "lambda ctx, a, b: b"),
                      ((), "lambda ctx: None")],
}

properties = {
    "default_start": "stat",
    "llconflicts": {
        ("optional_else", "ELSE"): ("ELSE", "stat"),
    },
}

my_grammar = Grammar(preface, properties, rules)
print(make_ll_parser(my_grammar))
