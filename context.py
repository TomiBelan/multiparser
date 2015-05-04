
import bisect
import re
import string


digits = list(string.digits)
alnum = list(string.ascii_letters + string.digits + '_')
whitespace = list(string.whitespace)


class Token:
    def __init__(self, location, type, value=None):
        self.location = location
        self.type = type
        self.value = value

    def __repr__(self):
        return 'Token' + repr((self.type,self.value) if self.value is not None else (self.type,))


class ParserContext:
    def __init__(self, input):
        self.input = input
        self.pos = 0
        self.regexes = {}

        self.newlines = []
        current_line_start = 0
        while True:
            self.newlines.append(current_line_start)
            current_line_start = input.find('\n', current_line_start) + 1
            if current_line_start == 0: break

    @property
    def location(self):
        line = bisect.bisect(self.newlines, self.pos) - 1
        column = self.pos - self.newlines[line]
        return (line + 1, column + 1)

    @property
    def current(self):
        return self.input[self.pos : self.pos + 1]

    def peek(self, n=1):
        return self.input[self.pos : self.pos + n]

    def advance(self, n=1):
        self.pos = min(self.pos + n, len(self.input))

    def match(self, regex):
        if isinstance(regex, str):
            if regex not in self.regexes:
                self.regexes[regex] = re.compile(regex)
            regex = self.regexes[regex]
        obj = regex.match(self.input, self.pos)
        if obj:
            self.matched = obj
            self.advance(obj.end() - obj.start())
        return obj

    def embed_token(self, outer_language):
        pass


class ParseError(Exception):
    pass


def flatten(a, rv=None):
    if rv is None: rv = []
    if isinstance(a, list):
        for item in a:
            flatten(item, rv)
    elif a:
        rv.append(a)
    return rv


def combine_action(root, user, normal_vars, list_vars):
    normal_vars = set(normal_vars)
    list_vars = set(list_vars)

    def combined_action(ctx, *direct_values):
        labeled_values = root(ctx, *direct_values)
        flat_values = flatten(labeled_values)

        arguments = { '_ctx': ctx, '_loc': None, '_all': [] }
        for var in normal_vars: arguments[var] = None
        for var in list_vars: arguments[var] = []

        for label, value in flat_values:
            if isinstance(value, Token):
                arguments['_loc'] = value.location
                break

        for label, value in flat_values:
            if label in normal_vars: arguments[label] = value
            if label in list_vars: arguments[label].append(value)
            arguments['_all'].append(value)

        return user(**arguments)

    return combined_action
