import wavegp
import sys
import numpy as np
import random
import subprocess


class g:
    pass


def execute(gen, x0):
    xe = x0
    xo = x0
    ye, yo = wavegp.execute(g, gen, [xe, xo])
    return ye


def diff(a, b):
    diff = np.subtract(a, b)
    return np.mean(diff**2)


def Plus(inp, args):
    x, y = inp
    z = np.zeros(N)
    for i in range(N):
        z[i] = x[i] + y[i]
    return z


def Minus(inp, args):
    x, y = inp
    z = np.zeros(N)
    for i in range(N):
        z[i] = x[i] - y[i]
    return z


def P(inp, args):
    x, = inp
    return x


def U(inp, args):
    x, = inp
    return x / 2


random.seed(2)
N = 8
x0 = 56, 40, 8, 24, 48, 48, 40, 16
y0 = 48, -16, 16, 16, 48, 0, 28, -24

g.nodes = Plus, Minus, P, U
g.names = "Plus", "Minus", "P", "U"
g.arity = 2, 2, 1, 1
g.args = 0, 0, 0, 0
# input, maximum node, output, arity, parameters
g.i = 2
g.n = 6
g.o = 2
g.a = 2
g.p = 0
gen0 = wavegp.rand(g)
gen1 = wavegp.rand(g)
gen2 = wavegp.build(
    g,
    #        0    1        2    3       4     5     6
    ["i0", "i1", "Minus", "U", "Plus", "o0", "o1"],
    [(0, 2), (1, 2), (2, 3), (0, 4), (3, 4), (4, 5), (2, 6)],
    [])

for gen in gen0, gen1, gen2:
    sys.stdout.write(wavegp.as_string(g, gen))
    y = execute(gen, x0)
    sys.stdout.write("cost: %g\n\n" % diff(y, y0))
    with open("split.gv", "w") as f:
        f.write(wavegp.as_graphviz(g, gen))
