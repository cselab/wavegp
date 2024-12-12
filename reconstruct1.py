import wavegp
import sys
import numpy as np
import random
import subprocess
import statistics
import collections


class g:
    pass


def rand():
    while True:
        gen = wavegp.rand(g)
        if good(gen):
            return gen


def good(gen):
    rn = wavegp.reachable_nodes(g, gen)
    j = gen[g.i + g.n + 0, 1]
    return j > g.i and Names[gen[j, 0]] == "Merge"


def fun(forward, backward):
    loss = []
    for x0 in xx:
        y, = wavegp.execute(g, forward, [x0])
        i, j, *rest = np.argsort(y[1::2])
        y[2 * i + 1] = 0
        y[2 * j + 1] = 0
        x, = wavegp.execute(g, backward, [y])
        l = diff(x, x0)
        loss.append(l)
    ans = statistics.mean(loss)
    return ans


def example():
    p = 2
    q = 10
    x = [random.randint(-p, p)]
    for i in range(N - 1):
        x.append(x[-1] + random.randint(-p, p))
        p, q = q, p
    return np.array(x, dtype=float)


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
N = 1 << 3
g.nodes = Even, Odd, Plus, Minus, U, Merge
g.names = "Even", "Odd", "Plus", "Minus", "U", "Merge"
Names = dict(enumerate(g.names))
g.arity = 1, 1, 2, 2, 1, 2
g.args = 0, 0, 0, 0, 0, 0
# input, maximum node, output, arity, parameters
g.i = 1
g.n = 6
g.o = 1
g.a = 2
g.p = 0
forward0 = wavegp.build(
    g,
    #  0      1       2        3    4    5        6     7
    ["i0", "Odd", "Even", "Minus", "U", "Plus", "Merge", "o0"],
    [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (2, 5), (4, 5), (5, 6), (3, 6),
     (6, 7)],
    [])

backward0 = wavegp.build(
    g,
    #  0      1       2    3        4       5        6     7
    ["i0", "Odd", "Even", "U", "Minus", "Plus", "Merge", "o0"],
    [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 4), (1, 5), (4, 5), (4, 6),
     (5, 6), (6, 7)],
    [])

xx = [example() for i in range(5)]
sys.stdout.write("loss: %g\n" % fun(forward0, backward0))
loss0 = fun(forward0, backward0)

best = sys.float_info.max, None, None

i = 0
while True:
    forward = rand()
    backward = rand()
    loss = fun(forward, backward)
    if i % 10000 == 0:
        print("epoch: ", i)
    i += 1
    if loss < best[0]:
        wavegp.as_image(g, forward, "best.forward.png")
        wavegp.as_image(g, backward, "best.backward.png")
        print(wavegp.as_string(g, forward))
        print(wavegp.as_string(g, backward))
        best = loss, forward, backward
        print(loss, loss0)
