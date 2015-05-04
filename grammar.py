
class ReprWrap:
    """Utility class used to embed runnable code in repr().

    repr(ReprWrap(s)) == "\n(" + s + ")\n"

    This is used for the RULES table in generated parsers. For the most part,
    it is a static literal, but actions wrapped in ReprWrap will be evaluated
    when the generated parser is imported.
    """
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '\n(' + str(self.value) + ')\n'


class Grammar:
    """A context-free grammar."""

    def __init__(self, preface, properties, rules, initial_states=None):
        self.preface = preface
        self.properties = properties.copy()
        self.rules = rules

        default_start = self.properties.setdefault('default_start', 'start')

        self.initial_states = set()
        for start_nt, close_with in (initial_states or { (None, 'EOF') }):
            self.initial_states.add((start_nt or default_start, close_with))

    @property
    def nullable(self):
        """Set of nullable nonterminals."""
        if getattr(self, '_nullable', None): return self._nullable
        nullable = self._nullable = set()

        while True:
            changed = False

            for nt in self.rules:
                if nt in nullable: continue
                for rule, action in self.rules[nt]:
                    if all(symbol in nullable for symbol in rule):
                        nullable.add(nt)
                        changed = True
                        break

            if not changed: break

        return nullable

    def get_nullable(self, word):
        """Find whether all symbols in 'word' are nullable."""
        return all(symbol in self.nullable for symbol in word)

    @property
    def first(self):
        """Map from nonterminals to their FIRST sets."""
        if getattr(self, '_first', None): return self._first
        first = self._first = { nt: set() for nt in self.rules }

        while True:
            changed = False

            for nt in self.rules:
                old_len = len(first[nt])

                for rule, action in self.rules[nt]:
                    for symbol in rule:
                        if symbol in self.rules:
                            first[nt].update(first[symbol])
                            if symbol in self.nullable: continue
                        else:
                            first[nt].add(symbol)
                        break

                if len(first[nt]) != old_len: changed = True

            if not changed: break

        return first

    def get_first(self, word):
        """Computes the FIRST set for any word (not just a nonterminal)."""
        result = set()
        for symbol in word:
            if symbol in self.rules:
                result.update(self.first[symbol])
                if symbol in self.nullable: continue
            else:
                result.add(symbol)
            break
        return result

    @property
    def follow(self):
        """Map from nonterminals to their FOLLOW sets."""
        if getattr(self, '_follow', None): return self._follow
        follow = self._follow = { nt: set() for nt in self.rules }
        edges = { nt: set() for nt in self.rules }

        for nt, symbol in self.initial_states:
            follow[nt].add(symbol)

        for nt in self.rules:
            for rule, action in self.rules[nt]:
                for i, symbol in enumerate(rule):
                    if symbol not in self.rules: continue
                    rest = rule[i+1:]
                    follow[symbol].update(self.get_first(rest))
                    if self.get_nullable(rest):
                        edges[symbol].add(nt)

        while True:
            changed = False

            for nt in self.rules:
                old_len = len(follow[nt])

                for nt2 in edges[nt]:
                    follow[nt].update(follow[nt2])

                if len(follow[nt]) != old_len: changed = True

            if not changed: break

        return follow
