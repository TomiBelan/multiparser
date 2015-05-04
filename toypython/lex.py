
from context import ParseError, Token


RESERVED = '''
    False None True and as assert break class continue def del elif else except
    finally for from global if import in is lambda nonlocal not or pass raise
    return try while with yield
'''.split()

OPS = '''
+       -       *       **      /       //      %
<<      >>      &       |       ^       ~
<       >       <=      >=      ==      !=
(       )       [       ]       {       }
,       :       .       ;       @       =       ->
+=      -=      *=      /=      //=     %=
&=      |=      ^=      >>=     <<=     **=
'''.split()
OPS = sorted(OPS, key=lambda o: -len(o))


def tokenizer(ctx, close_with=None):
    after_newline = True
    first_level = 1 if close_with is None else None
    in_parens = 0
    indent_stack = [0]

    while True:
        loc = ctx.location

        if ctx.match(r' '):
            continue

        if ctx.match(r'#[^\n]*'):
            continue

        if ctx.match(r'\\\n'):
            if after_newline:
                raise ParseError(loc,
                    "toypython doesn't support empty lines with trailing '\\'")
            continue

        if ctx.match(r'\n'):
            if not in_parens and not after_newline:
                yield Token(loc, 'NEWLINE', None)
                after_newline = True
            continue

        if ctx.match(r'\t'):
            raise ParseError(loc, "toypython doesn't support tabs")

        if ctx.current == '':   # EOF
            if not in_parens and not after_newline:
                yield Token(loc, 'NEWLINE', None)
                after_newline = True
            while len(indent_stack) > 1:
                indent_stack.pop()
                yield Token(loc, 'DEDENT')
            yield Token(loc, 'EOF')
            continue

        # ------------------- no more whitespace -------------------

        if first_level is None:
            line, column = ctx.location
            first_level = column
        if after_newline:
            after_newline = False
            line, column = ctx.location
            my_indent = column - first_level
            if my_indent > indent_stack[-1]:
                indent_stack.append(my_indent)
                yield Token(loc, 'INDENT')
            elif my_indent < indent_stack[-1]:
                ending = close_with and ctx.peek(len(close_with)) == close_with
                if ending and my_indent < 0:
                    my_indent = 0
                if my_indent not in indent_stack:
                    raise ParseError(loc, "bad dedent")
                while my_indent != indent_stack[-1]:
                    indent_stack.pop()
                    yield Token(loc, 'DEDENT')

        e = ctx.embed_token('toypython')
        if e:
            yield e
            continue

        if ctx.match(r'[A-Za-z_][A-Za-z0-9_]*'):
            value = ctx.matched.group()
            if value in RESERVED:
                yield Token(loc, value)
            else:
                yield Token(loc, 'NAME', value)
            continue

        if ctx.match(r'[0-9]+(?![A-Za-z_])'):
            yield Token(loc, 'NUMBER', int(ctx.matched.group()))
            # TODO: other numeric literals
            continue

        if ctx.match(r'"[^"\\]*"'):
            yield Token(loc, 'STRING', ctx.matched.group()[1:-1])
            continue
        if ctx.match(r'\'[^\'\\]*\''):
            yield Token(loc, 'STRING', ctx.matched.group()[1:-1])
            continue
        # TODO: other string literals

        m = False
        for op in ([close_with] if close_with else []) + OPS:
            if ctx.peek(len(op)) == op:
                if op in ['(', '{', '[']: in_parens += 1
                if op in [')', '}', ']']: in_parens -= 1
                ctx.advance(len(op))
                yield Token(loc, op, None)
                m = True
                break
        if m: continue

        raise ParseError(loc, "Unexpected %r" % ctx.current)
