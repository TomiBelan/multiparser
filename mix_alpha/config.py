languages = {
    'toypython': 'toypython/grammar.mgr',
    'toylua': 'toylua/lrgrammar.mgr',
    'toycalc': 'toycalc/peggrammar.ebnf',
}

root = 'toylua'

embeds = (
    [(outer, 'EMBEDSTAT', 'toylua', 'chunk', '<?lua', '?>')
     for outer in languages if outer != 'toylua'] +
    [(outer, 'EMBEDSTAT', 'toylua', 'chunk', '%lua{', '}')
     for outer in languages if outer != 'toylua'] +
    [(outer, 'EMBEDEXPR', 'toylua', 'exp', '%lua(', ')')
     for outer in languages if outer != 'toylua'] +

    [(outer, 'EMBEDSTAT', 'toypython', 'file_input', '<?py', '?>')
     for outer in languages if outer != 'toypython'] +
    [(outer, 'EMBEDSTAT', 'toypython', 'file_input', '%py{', '}')
     for outer in languages if outer != 'toypython'] +
    [(outer, 'EMBEDEXPR', 'toypython', 'eval_input', '%py(', ')')
     for outer in languages if outer != 'toypython'] +

    [(outer, 'EMBEDEXPR', 'toycalc', None, '%calc(', ')')
     for outer in languages if outer != 'toycalc'] +
[])
