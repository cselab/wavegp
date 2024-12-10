import serial
import sys


class g:
    pass


def stopo(gen):
    q = {x for x in gen[g.i + g.n:, 1]}
    topo = set()
    while q:
        n = q.pop()
        if n >= g.i:
            topo.add(n)
            arity = g.nodes[gen[n, 0]].arity
            adj = gen[n, 1:1 + arity]
            q.update(adj)
    return sorted(topo)


def graph(gen, path):
    with open(path, "w") as f:
        f.write("digraph {\n")
        for j in range(g.i):
            f.write(f"  {j} [label = i{j}]\n")
        for n in stopo(gen):
            arity = 1  # g.nodes[gen[n, 0]].arity
            args = 1  # g.nodes[gen[n, 0]].args
            f.write(f'  {n} [label = "{names[gen[n, 0]]}')
            for j in range(args):
                f.write(f", {gen[n, 1 + g.a + j]}")
            f.write('"]\n')
            for j in range(arity):
                f.write(f"  {gen[n, 1 + j]} -> {n}\n")
        for j in range(g.o):
            f.write(f"  {g.i + g.n + j} [label = o{j}]\n")
            f.write(f"  {gen[g.i + g.n + j, 1]} -> {g.i + g.n + j}\n")
        f.write("}\n")


fmt = "iiiiiSy"
with open(sys.argv[1], "rb") as f:
    buf = f.read()
    g.i, g.n, g.o, g.a, g.p, g.names, genes = serial.deserial(fmt, buf)

for i, gen in enumerate(genes):
    graph(gen, "q.%08d.gv" % i)
