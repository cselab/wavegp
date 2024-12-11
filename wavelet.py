import wavegp
import sys
import numpy as np
import random


class g:
    pass


def diff(a, b):
    diff = np.subtract(a, b)
    return np.mean(diff**2)


def Even(inp, args):
    x, = inp
    y = np.zeros(N)
    for i in range(N // 2):
        y[i] = x[2 * i]
    return y


def Odd(inp, args):
    x, = inp
    y = np.zeros(N)
    for i in range(N // 2):
        y[i] = x[2 * i + 1]
    return y


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


def Merge(inp, args):
    x, y = inp
    z = np.empty(N)
    for i in range(N // 2):
        z[2 * i] = x[i]
        z[2 * i + 1] = y[i]
    return z


random.seed(2)
N = 8
Y, X = np.meshgrid(range(N), range(N))
x0 = 1, 2, 3, 4, 5, 6, 7, 8
y0 = 1, 2, 3, 4, 5, 6, 7, 8

g.nodes = Even, Odd, Plus, Minus, P, U, Merge
g.names = "Even", "Odd", "Plus", "Minus", "P", "U", "Merge"
g.arity = 1, 1, 2, 2, 1, 1, 2
g.args = 0, 0, 0, 0, 0, 0, 0
# input, maximum node, output, arity, parameters
g.i = 1
g.n = 11
g.o = 1
g.a = 2
g.p = 0
gen0 = wavegp.rand(g)
gen1 = wavegp.build(g,
                    ["i0", "Odd", "Even", "Minus", "Plus", "U", "Merge", "o0"],
                    [(0, 1), (0, 2), (1, 3), (2, 3), (1, 4), (2, 4), (4, 5),
                     (3, 6), (5, 6), (6, 7)], [])

for gen in [gen1]:
    sys.stdout.write(wavegp.as_string(g, gen))
    y, = wavegp.execute(g, gen, [x0])
    sys.stdout.write("loss: %g\n\n" % diff(y, y0))
