from random import randrange
import numpy as np
import random
import wavegp
import sys
import re
import collections


def init():
    gen = np.zeros((g.i + g.n + g.o, 1 + g.a + g.p), dtype=np.uint8)
    for j in range(g.n):
        gen[g.i + j, 0] = randrange(len(g.names))
        for k in range(g.a):
            gen[g.i + j, 1 + k] = randrange(g.i + j)
        for k in range(g.p):
            gen[g.i + j, 1 + g.a + k] = randrange(wavegp.max_val)
    for j in range(g.o):
        gen[g.i + g.n + j, 1] = randrange(g.i + g.n)
    return gen


def build(gen, *args):
    cnt = 0
    verts = {arg for arg in args if isinstance(arg, str)}
    edgs = {arg for arg in args if not isinstance(arg, str)}

    cnt = 0
    D = {}
    for i, v in enumerate(verts):
        if re.match("^o[0-9]+$", v):
            ty = "o"
            j = int(v[1:])
        elif re.match("^i[0-9]+$", v):
            ty = "i"
            j = int(v[1:])
        else:
            ty = "n"
            j = cnt
            gen[g.i + j, 0] = Names[v]
            cnt += 1
        D[i] = ty, j

    A = collections.defaultdict(int)
    for x, y in edgs:
        ty0, j0 = D[x]
        ty1, j1 = D[y]


#        if ty1 == "n":
#            gen[g.i + j1] =


class g:
    pass


random.seed(2)
g.names = "Backward_X", "Forward_X", "Backward_Y", "Forward_Y", "Plus", "Minus"
Names = {name: index for index, name in enumerate(g.names)}
g.arity = 1, 1, 1, 1, 2, 2
g.args = 0, 0, 0, 0, 0, 0
# input, maximum node, output, arity, parameters
g.i = 1
g.n = 10
g.o = 1
g.a = 2
g.p = 0

gen = init()
genes = [gen]

build(gen, "i0", "Backward_Y", (0, 1), "Minus", (0, 2), (1, 2), "o0", (2, 3))

fmt = "iiiiiSIIy"
buf = wavegp.serial(fmt, g.i, g.n, g.o, g.a, g.p, g.names, g.arity, g.args,
                    genes)
with open(sys.argv[1], "wb") as f:
    f.write(buf)
