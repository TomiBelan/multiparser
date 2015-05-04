
from context import ParseError, Token


def tokenizer(ctx, close_with=None):
    in_preface = True

    while True:
        loc = ctx.location

        if in_preface:
            if ctx.match(r'(|[\s\S]*?\n)---'):
                yield Token(loc, 'PREFACE', ctx.matched.group(1))
                in_preface = False
                continue

            raise ParseError(loc, '"---" not found')

        if ctx.match(r'\s'):
            continue

        if ctx.match(r'#[^\n]*'):
            continue

        if ctx.current == '':
            yield Token(loc, 'EOF', None)
            continue

        if ctx.match(r'\\(\d+)'):
            yield Token(loc, 'SUBRULEREF', int(ctx.matched.group(1)))
            continue

        if ctx.match(r'[()=+*?:|]'):
            yield Token(loc, ctx.matched.group(), None)
            continue

        if ctx.match(r'"([^"]+)"'):
            yield Token(loc, 'NAME', ctx.matched.group(1))
            continue

        if ctx.match(r"'([^']+)'"):
            yield Token(loc, 'NAME', ctx.matched.group(1))
            continue

        if ctx.match(r'[A-Za-z0-9_]+'):
            yield Token(loc, 'NAME', ctx.matched.group())
            continue

        if ctx.match(r'`([^`]+)`'):
            yield Token(loc, 'ACTION', ctx.matched.group(1))
            continue

        raise ParseError(loc, "Unexpected %r" % ctx.current)
