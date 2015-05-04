#!/bin/sh
for t in ll lr; do
  for c in a b; do
    python3 test1.py toylua.${t}grammar_out toylua/example2$c.lua | grep -v location: > tmp_2$t$c
  done
done
sha1sum tmp_2*
