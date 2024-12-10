from random import randrange
import numpy as np
import random
import wavegp
import sys


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


class g:
    pass


random.seed(2)
g.names = "Backward_X", "Forward_X", "Backward_Y", "Forward_Y", "Plus"
g.arity = 1, 1, 1, 1, 2
g.args = 0, 0, 0, 0, 0
# input, maximum node, otuput, arity, parameters
g.i = 1
g.n = 10
g.o = 1
g.a = 2
g.p = 1
g.lmb = 3
genes = [init() for i in range(g.lmb)]
fmt = "iiiiiSIIy"
buf = wavegp.wavegp(fmt, g.i, g.n, g.o, g.a, g.p, g.names, g.arity, g.args,
                    genes)
with open(sys.argv[1], "wb") as f:
    f.write(buf)
