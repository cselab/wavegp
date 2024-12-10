import wavegp
import sys


class g:
    pass


fmt = "iiiiiSIIy"
with open(sys.argv[1], "rb") as f:
    buf = f.read()
    g.i, g.n, g.o, g.a, g.p, g.names, g.arity, g.args, genes = wavegp.deserial(
        fmt, buf)
print(g.names)
print(g.arity)
print(g.args)
