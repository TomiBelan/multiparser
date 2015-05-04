languages = {
    'toypython': 'toypython/grammar.mgr',
    'toylua': 'toylua/llgrammar.mgr',
    'toycalc': 'toycalc/llgrammar.mgr',
}

root = 'toypython'

embeds = [
    ('toypython', 'EMBEDEXPR', 'toylua', 'exp', '(:', ':)'),
    ('toylua', 'EMBEDEXPR', 'toycalc', None, '(:', ':)'),
    ('toycalc', 'EMBEDEXPR', 'toypython', 'eval_input', '(:', ':)'),
]
