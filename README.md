
Multiparser
===========

This is my master's thesis. It is a parser that can read multiple languages embedded within each
other in one file (a bit like HTML and PHP, or LINQ in C#, etc). The languages can use different
lexical analysis rules or even different parsing models (LL, LR, PEG), and Multiparser's output
combines them into one abstract syntax tree.

I am open sourcing the code. But please keep in mind that this is academic software, and using it in
practice may be painful. It's not nearly as polished as "big" parser generators like flex/bison or
ANTLR.

The thesis itself is written in Slovak. You can find it in the file "[BelanDP.pdf][pdf]".

[pdf]: https://cdn.rawgit.com/TomiBelan/multiparser/master/BelanDP.pdf



Requirements
------------

Multiparser needs:

* Python 3
  (tested with version 3.4, might also work with older 3.x versions and PyPy 3)

* make

* Grako
  (python library -- tested with version 3.5.1)
  (needed only when using PEG parsers)


Ways to install Grako:

* With "pip" a "virtualenv" (see online tutorials)

* With "pip": `sudo pip install grako`

* Download https://pypi.python.org/packages/source/g/grako/grako-3.5.1.tar.gz, extract it to a
  temporary location and copy the directory "grako-3.5.1/grako" to this directory

Test: the command `python3 -m grako` should output `usage: grako ...`.



How to use
----------

`make` generates parsers for all demo languages. It can take a while.

The script runparser.py runs a given parser on a given output and shows the result. Such as:

- `python3 runparser.py toylua.lrgrammar_out toylua/example1.lua`
- `python3 runparser.py toypython.grammar_out toypython/example_goodindent.py`
- `python3 runparser.py mix_alpha.composite_out mix_alpha/example1.lua`
- `python3 runparser.py mix_beta.composite_out mix_beta/example1.py`
- `python3 runparser.py mix_gamma.composite_out mix_gamma/example1.py`

(runparser.py currently assumes that you use a UNIX-like color terminal. I should fix that one day.)

It's possible to add your own languages and your own composite language settings. The scripts
compose.py, makell.py, makelr.py, makepeg.py are used to generate executable code from them. See the
Makefile.

The `example_*` files contain examples from the thesis.

