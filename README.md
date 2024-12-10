# wavegp

```
$ python write.py a.raw
$ python read.py a.raw
['Backward_X', 'Forward_X', 'Backward_Y', 'Forward_Y', 'Plus']
(1, 1, 1, 1, 2)
(0, 0, 0, 0, 0)
$ python graphviz.py a.raw
$ python graphviz.py a.raw a
graphviz.py: a.00000000.gv
graphviz.py: a.00000001.gv
graphviz.py: a.00000002.gv
$ for i in a.*.gv; do dot $i -T png -o ${i/.gv/.png}; done
$ ls a.*.png
a.00000000.png	a.00000001.png	a.00000002.png
```
