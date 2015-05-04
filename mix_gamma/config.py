languages = {
    'toypython': 'toypython/grammar.mgr',
    'toylua': 'toylua/llgrammar.mgr',
    'toycalc': 'toycalc/lrgrammar.mgr',
}

root = 'toypython'

embeds = (
    [(outer, 'EMBEDEXPR', 'toylua', 'exp', '@@lua', '@@@')
     for outer in languages if outer != 'toylua'] +
    [(outer, 'EMBEDSTAT', 'toylua', 'chunk', '<lua>', '</lua>')
     for outer in languages if outer != 'toylua'] +
    [(outer, 'EMBEDEXPR', 'toypython', 'eval_input', '@@python', '@@@')
     for outer in languages if outer != 'toypython'] +
    [(outer, 'EMBEDSTAT', 'toypython', 'file_input', '<python>', '</python>')
     for outer in languages if outer != 'toypython'] +
    [(outer, 'EMBEDEXPR', 'toycalc', None, '@@calc', '@@@')
     for outer in languages if outer != 'toycalc'] +
[])
