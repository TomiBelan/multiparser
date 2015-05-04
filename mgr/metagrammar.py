
from grammar import Grammar

preface = '''

from mgr.lex import tokenizer
from collections import namedtuple
from context import flatten

MgrGrammar = namedtuple('MgrGrammar', 'preface properties rules')
# rules is a list of (SimpleRule|ExtendedRule)

SimpleRule = namedtuple('SimpleRule', 'left right action')
# right is a list of str

ExtendedRule = namedtuple('ExtendedRule', 'left right action')
# right is a list of (Symbol|Subrule|SubruleReference)

Symbol = namedtuple('Symbol', 'label append value')

Subrule = namedtuple('Subrule', 'branches type')
# branches is a list of SubruleBranch

SubruleBranch = namedtuple('SubruleBranch', 'items')
# items is a list of (Symbol|Subrule|SubruleReference)

SubruleReference = namedtuple('SubruleReference', 'index')

'''

condensed_rules = '''

start = PREFACE properties rules `lambda ctx,p,d,r: MgrGrammar(p.value, d, flatten(r))`

properties = ACTION `lambda ctx,a: eval(a.value)`
properties = `lambda ctx: {}`

rules = rule rules `lambda ctx,x,xs: [x,xs]`
rules = `lambda ctx: []`

rule = NAME = names ACTION `lambda ctx,l,_,rs,a: SimpleRule(l.value, flatten(rs), a.value)`
rule = NAME : ebranch ebranches `lambda ctx,l,_,b,bs: [ExtendedRule(l.value, r, a) for r, a in flatten([b,bs])]`

names = NAME names `lambda ctx,n,ns: [n.value,ns]`
names = `lambda ctx: []`

ebranches = | ebranch ebranches `lambda ctx,_,b,bs: [b,bs]`
ebranches = `lambda ctx: []`

ebranch = eitems ACTION `lambda ctx,r,a: (flatten(r), a.value)`

eitems = eitem eitems `lambda ctx,e,es: [e,es]`
eitems = `lambda ctx: []`

eitem = NAME `lambda ctx,v: Symbol(None, False, v.value)`
eitem = NAME = NAME `lambda ctx,l,_,v: Symbol(l.value, False, v.value)`
eitem = NAME + = NAME `lambda ctx,l,_,__,v: Symbol(l.value, True, v.value)`
eitem = ( subbranch subbranches ) suffix `lambda ctx,_,b,bs,__,s: Subrule(flatten([b,bs]), s)`
eitem = SUBRULEREF `lambda ctx,r: SubruleReference(r.value)`

suffix = ? `lambda ctx,a: "?"`
suffix = * `lambda ctx,a: "*"`
suffix = `lambda ctx: None`

subbranches = | subbranch subbranches `lambda ctx,_,b,bs: [b,bs]`
subbranches = `lambda ctx: []`

subbranch = eitems `lambda ctx,es: SubruleBranch(flatten(es))`

'''


rules = {}
for line in condensed_rules.split('\n'):
    line = line.strip()
    if not line: continue
    nt, _, line = line.partition('=')
    rule, action, _ = line.split('`')
    rule = tuple([r.strip() for r in rule.split()])
    rules.setdefault(nt.strip(), []).append((rule, action))

grammar = Grammar(preface, {}, rules)
