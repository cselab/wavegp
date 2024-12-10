import serial
import sys


class g:
    pass


fmt = "iiiiiSy"
with open(sys.argv[1], "rb") as f:
    buf = f.read()
    g.i, g.n, g.o, g.a, g.p, g.names, genes = serial.deserial(fmt, buf)
print(g.names)
