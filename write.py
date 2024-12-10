from random import randrange
import numpy as np
import random
import serial
import sys


def init():
    gen = np.zeros((g.i + g.n + g.o, 1 + g.a + g.p), dtype=np.uint8)
    for j in range(g.n):
        gen[g.i + j, 0] = randrange(len(g.names))
        for k in range(g.a):
            gen[g.i + j, 1 + k] = randrange(g.i + j)
        for k in range(g.p):
            gen[g.i + j, 1 + g.a + k] = randrange(serial.max_val)
    for j in range(g.o):
        gen[g.i + g.n + j, 1] = randrange(g.i + g.n)
    return gen


class g:
    pass


random.seed(2)
g.names = "Backward_X", "Forward_X", "Backward_Y", "Forward_Y", "Plus"
# input, maximum node, otuput, arity, parameters
g.i = 1
g.n = 10
g.o = 1
g.a = 2
g.p = 1
g.lmb = 10
genes = [init() for i in range(g.lmb)]
fmt = "iiiiiSy"
buf = serial.serial(fmt, g.i, g.n, g.o, g.a, g.p, g.names, genes)
with open(sys.argv[1], "wb") as f:
    f.write(buf)
