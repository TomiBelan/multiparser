
from context import ParseError, Token


RESERVED = '''
    and break do else elseif end false for function goto if in local nil not or
    repeat return then true until while
'''.split()

OPS = '+ - * / % ^ # == ~= <= >= < > = ( ) { } [ ] :: ; : , ... .. .'.split()

ESCAPES = {
    'a': '\a',
    'b': '\b',
    'f': '\f',
    'n': '\n',
    'r': '\r',
    't': '\t',
    'v': '\v',
    '\\': '\\',
    '"': '"',
    "'": "'",
    '\n': '\n',
}


def tokenizer(ctx, close_with=None):
    BASE = 0
    STRING = 1

    st = BASE
    string_val = string_loc = string_quote = None

    while True:
        loc = ctx.location

        if st == BASE:
            if ctx.match(r'\s'):
                continue
            if ctx.match(r'--\[(=*)\['):
                close_re = r'[\s\S]*?\]' + ctx.matched.group(1) + r'\]'
                if not ctx.match(close_re):
                    raise ParseError(ctx.location, "EOF in multiline comment")
                continue
            if ctx.match(r'--[^\n]*'):
                continue

            if ctx.current == '':   # EOF
                yield Token(loc, 'EOF', None)
                continue

            e = ctx.embed_token('toylua')
            if e:
                yield e
                continue

            if ctx.match(r'[0-9]+'):
                yield Token(loc, 'NUMBER', int(ctx.matched.group()))
                # TODO: floating point
                continue

            if ctx.match(r'[A-Za-z0-9_]+'):
                value = ctx.matched.group()
                if value in RESERVED:
                    yield Token(loc, value, None)
                else:
                    yield Token(loc, 'NAME', value)
                continue

            if ctx.match('["\']'):
                string_loc = loc
                string_quote = ctx.matched.group()
                string_value = []
                st = STRING
                continue

            if ctx.match(r'\[(=*)\['):
                close_re = r'([\s\S]*?)\]' + ctx.matched.group(1) + r'\]'
                if not ctx.match(close_re):
                    raise ParseError(ctx.location, "EOF in string")
                yield Token(loc, 'STRING', ctx.matched.group(1))
                continue

            m = False
            for op in ([close_with] if close_with else []) + OPS:
                if ctx.peek(len(op)) == op:
                    ctx.advance(len(op))
                    yield Token(loc, op, None)
                    m = True
                    break
            if m: continue

        if st == STRING:
            if ctx.current == '':   # EOF
                raise ParseError(loc, "EOF in string")
            if ctx.match(r'\n'):
                raise ParseError(loc, "Newline in string")
            if ctx.match(r'\\z\s*'):
                continue
            if ctx.current == '\\':
                ctx.advance()
                if ctx.current in ESCAPES:
                    string_value.append(ESCAPES[ctx.current])
                    ctx.advance()
                else:
                    # TODO: \xXX, \ddd
                    raise ParseError(loc, "Invalid escape sequence")
                continue
            if ctx.match(string_quote):
                yield Token(string_loc, 'STRING', ''.join(string_value))
                st = BASE
                continue

            string_value.append(ctx.current)
            ctx.advance()
            continue

        raise ParseError(loc, "Unexpected %r" % ctx.current)
