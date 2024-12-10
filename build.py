import numpy as np
import wavegp
import sys
import re
import collections


def build(gen, *args):
    verts = [arg for arg in args if isinstance(arg, str)]
    edgs = [arg for arg in args if not isinstance(arg, str)]
    cnt = 0
    D = {}
    for i, v in enumerate(verts):
        if re.match("^o[0-9]+$", v):
            D[i] = g.i + g.n + int(v[1:])
        elif re.match("^i[0-9]+$", v):
            D[i] = int(v[1:])
        else:
            D[i] = g.i + cnt
            gen[D[i], 0] = Names[v]
            cnt += 1
    A = collections.defaultdict(int)
    for x, y in edgs:
        j0 = D[x]
        j1 = D[y]
        gen[j1, 1 + A[y]] = j0
        A[y] += 1


class g:
    pass


# random.seed(2)
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
gen = np.zeros((g.i + g.n + g.o, 1 + g.a + g.p), dtype=np.uint8)
'''
build(gen, "i0", "Backward_Y", "Backward_X", (0, 1), (0, 2), "Minus", (1, 3),
      (2, 3), "o0", (3, 4))
'''
build(gen, "i0", "Backward_Y", "Backward_Y", "Backward_Y", "o0", (0, 1),
      (1, 2), (2, 3), (3, 4))
genes = [gen]
print(wavegp.reachable_nodes(g, gen))
fmt = "iiiiiSIIy"
buf = wavegp.serial(fmt, g.i, g.n, g.o, g.a, g.p, g.names, g.arity, g.args,
                    genes)
with open(sys.argv[1], "wb") as f:
    f.write(buf)
