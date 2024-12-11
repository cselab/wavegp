import wavegp
import sys


class g:
    pass


fmt = "iiiiiSIIy"
with open(sys.argv[1], "rb") as f:
    buf = f.read()
    g.i, g.n, g.o, g.a, g.p, g.names, g.arity, g.args, genes = wavegp.deserial(
        fmt, buf)
print("n_genes = ", len(genes))
print("node names:", *g.names)
print("node arity:", *g.arity)
print("number of parameters:", *g.args)
print("input:", g.i)
print("output:", g.o)


