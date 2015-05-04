
from context import ParseError, Token

def tokenizer(ctx, close_with=None):
    while True:
        loc = ctx.location

        if ctx.match(r'\s'):
            continue

        if ctx.current == '':
            yield Token(loc, 'EOF', None)
            continue

        if close_with and ctx.peek(len(close_with)) == close_with:
            ctx.advance(len(close_with))
            yield Token(loc, close_with, None)
            continue

        e = ctx.embed_token('toycalc')
        if e:
            yield e
            continue

        if ctx.current in ('+', '-', '*', '/', '^', '(', ')', ';'):
            token_type = ctx.current
            ctx.advance()
            yield Token(loc, token_type, None)
            continue

        if ctx.match(r'[0-9]+'):
            value = ctx.matched.group()
            yield Token(loc, 'NUMBER', int(value))
            continue

        if ctx.match(r'[A-Za-z]+'):
            token_type = ctx.matched.group()
            yield Token(loc, token_type, None)
            continue

        raise ParseError(loc, "Unexpected %r" % ctx.current)
