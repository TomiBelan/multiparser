
TARGETS = \
	mgr/parser_out.py \
	toylua/llgrammar_out.py \
	toylua/lrgrammar_out.py \
	toypython/grammar_out.py \
	toycalc/llgrammar_out.py \
	toycalc/lrgrammar_out.py \
	toycalc/peggrammar_out.py \
	example_basicrules_out.py \
	example_extrules_out.py \
	mix_alpha/composite_out.py \
	mix_beta/composite_out.py \
	mix_gamma/composite_out.py \

all: $(TARGETS)

PYTHON = python3
BASE_DEPS = \
	Makefile \
	compose.py \
	compose_template \
	context.py \
	grammar.py \
	makell.py \
	makell_template \
	makelr.py \
	makelr_template \
	makepeg.py \
	makepeg_template \
	mgr/lex.py \
	mgr/parser_out.py \
	mgr/read.py \

%_out.py: %.mgr $(BASE_DEPS)
	$(PYTHON) compose.py $<

%/composite_out.py: %/config.py $(BASE_DEPS)
	$(PYTHON) compose.py $*

%_out.py: %.ebnf $(BASE_DEPS)
	$(PYTHON) makepeg.py $< $@

mgr/parser_out.py: mgr/makeparser.py mgr/metagrammar.py makelr.py grammar.py
	$(PYTHON) -m mgr.makeparser $@

clean:
	rm -f *_out.py */*_out.py

.PHONY: all clean
.DELETE_ON_ERROR:
