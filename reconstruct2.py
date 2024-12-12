import wavegp
import sys
import numpy as np
import random
import subprocess
import statistics
import collections
import multiprocessing
import copy


class g:
    pass


def rand():
    while True:
        gen = wavegp.rand(g)
        if good(gen):
            return gen


def mutate(i, genes):
    mutate_prob = 0.2
    genes[0], genes[i] = genes[i], genes[0]
    # topo = wavegp.reachable_nodes(g, genes[0])
    for i in range(1, g.lmb + 1):
        while True:
            genes[i] = copy.copy(genes[0])
            for m in range(n_mutations):
                j = random.randrange(g.n)
                k = random.randrange(1 + g.a + g.p)
                if k == 0:
                    genes[i][g.i + j, 0] = random.randrange(len(g.nodes))
                elif k <= g.a:
                    genes[i][g.i + j, k] = random.randrange(g.i + j)
                else:
                    genes[i][g.i + j, k] = random.randrange(g.max_val)
            for k in range(g.o):
                if random.random() < mutate_prob:
                    genes[i][g.i + g.n + k, 1] = random.randrange(g.i + g.n)
            if good(genes[i]):
                break


def good(gen):
    rn = wavegp.reachable_nodes(g, gen)
    j = gen[g.i + g.n + 0, 1]
    return j > g.i and Names[gen[j, 0]] == "Merge"


def fun(pair):
    forward, backward = pair
    cost = []
    for x0 in xx:
        y, = wavegp.execute(g, forward, [x0])
        i, j, *rest = np.argsort(y[1::2])
        y[2 * i + 1] = 0
        y[2 * j + 1] = 0
        x, = wavegp.execute(g, backward, [y])
        l = diff(x, x0)
        cost.append(l)
    ans = statistics.mean(cost)
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
g.lmb = 10000
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
cost0 = fun([forward0, backward0])
sys.stdout.write(f"reference cost {cost0:.16e}\n")

genes_forward = [rand() for i in range(g.lmb + 1)]
genes_backward = [rand() for i in range(g.lmb + 1)]
n_mutations = 50 * g.n * (1 + g.a + g.p) // 100
generation = 0
max_generation = 10000000000
while True:
    with multiprocessing.Pool() as pool:
        costs = pool.map(fun, zip(genes_forward, genes_backward))
    i = np.argmin(costs)
    if generation % 100 == 0:
        print(f"{generation:08} {costs[i]:.16e}")
    if generation == max_generation:
        break
    generation += 1
    mutate(i, genes_forward)
    mutate(i, genes_backward)
