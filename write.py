import numpy as np
class g:
    pass
g.names = "Backward_X", "Forward_X", "Backward_Y", "Forward_Y", "Plus"
# input, maximum node, otuput, arity, parameters
g.i = 1
g.n = 10
g.o = 1
g.a = 2
g.p = 0
gene = np.zeros((g.i + g.n + g.o, 1 + g.a + g.p), dtype=np.uint8)
