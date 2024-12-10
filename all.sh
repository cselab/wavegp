#!/bin/sh
python write.py a.raw
python read.py a.raw
python graphviz.py a.raw a
for i in a.*.gv; do dot $i -T png -o ${i%.gv}.png; done
