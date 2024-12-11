# wavegp

```
$ python write.py a.raw
$ python read.py a.raw
n_genes =  8
['Backward_X', 'Forward_X', 'Backward_Y', 'Forward_Y', 'Plus', 'Minus']
(1, 1, 1, 1, 2, 2)
(0, 0, 0, 0, 0, 0)
$ python graphviz.py a.raw a
graphviz.py: a.00000000.gv
graphviz.py: a.00000001.gv
graphviz.py: a.00000002.gv
graphviz.py: a.00000003.gv
graphviz.py: a.00000004.gv
graphviz.py: a.00000005.gv
graphviz.py: a.00000006.gv
graphviz.py: a.00000007.gv
```

Convert to images

```
$ for i in a.*.gv; do dot $i -T png -o ${i%.gv}.png; done
```

Build

```
$ python build.py a.raw
$ python graphviz.py a.raw a
graphviz.py: a.00000000.gv
graphviz.py: a.00000001.gv
```

# References

- <https://www.kartezio.com>
- <https://zenodo.org/records/3889163>
- <https://www.cgplibrary.co.uk>
- <https://github.com/paul-kaufmann/cgp>
- <https://github.com/um-tech-evolution/CartesianGP.jl>

- Miller, J. F. (2020). Cartesian genetic programming: its status and
  future. Genetic Programming and Evolvable Machines, 21(1), 129-168
  [10.1007/s10710-019-09360-6](https://doi.org/10.1007/s10710-019-09360-6)

