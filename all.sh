#!/bin/sh
python build.py a.raw
python read.py a.raw
python graphviz.py a.raw a
for i in a.*.gv; do dot $i -T svg -o ${i%.gv}.svg; done
cp a.00000000.svg a.00000001.svg img/
