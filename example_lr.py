from grammar import Grammar
from makelr import make_lr_parser

preface = "from toycalc.lex import tokenizer"

rules = {
    # stat -> HELLO | IF cond THEN stat | IF cond THEN stat ELSE stat
    "stat": [(("HELLO",), "lambda ctx, a: 'hello'"),
             (("IF", "cond", "THEN", "stat"),
              "lambda ctx, a, b, c, d: ('if', b, d, None)"),
             (("IF", "cond", "THEN", "stat", "ELSE", "stat"),
              "lambda ctx, a, b, c, d, e, f: ('if', b, d, f)")],

    # cond -> cond AND cond | cond OR cond | TRUE | FALSE
    "cond": [(("cond", "AND", "cond"), "lambda ctx, a, b, c: (a, 'and', c)"),
             (("cond", "OR", "cond"), "lambda ctx, a, b, c: (a, 'or', c)"),
             (("TRUE",), "lambda ctx, a: True"),
             (("FALSE",), "lambda ctx, a: False")],
}

properties = {
    "default_start": "stat",
    "precedence": [
        [
            ("left", ["OR"]),
            ("left", ["AND"]),
        ],
        [
            ("precedence", [("stat", ("IF", "cond", "THEN", "stat"))]),
            ("precedence", ["ELSE"]),
        ],
    ],
}

my_grammar = Grammar(preface, properties, rules)
print(make_lr_parser(my_grammar))
