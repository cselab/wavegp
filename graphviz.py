import wavegp
import sys


class g:
    pass


Colors = "red", "blue", "green", "orange", "purple", "brown", "pink", "cyan", "magenta"


def stopo(gen):
    q = {x for x in gen[g.i + g.n:, 1]}
    topo = set()
    while q:
        n = q.pop()
        if n >= g.i:
            topo.add(n)
            arity = g.arity[gen[n, 0]]
            adj = gen[n, 1:1 + arity]
            q.update(adj)
    return sorted(topo)


def graph(gen, path):
    with open(path, "w") as f:
        f.write("digraph {\n")
        for j in range(g.i):
            f.write(f"  {j} [label = i{j}]\n")
        for n in stopo(gen):
            arity = g.arity[gen[n, 0]]
            args = g.args[gen[n, 0]]
            f.write(f'  {n} [label = "{g.names[gen[n, 0]]}')
            for j in range(args):
                f.write(f", {gen[n, 1 + g.a + j]}")
            f.write('"]\n')
            for j in range(arity):
                if arity == 1:
                    f.write(f"  {gen[n, 1 + j]} -> {n}\n")
                else:
                    k = j % len(Colors)
                    f.write(
                        f"  {gen[n, 1 + j]} -> {n} [color = {Colors[j]}]\n")
        for j in range(g.o):
            f.write(f"  {g.i + g.n + j} [label = o{j}]\n")
            f.write(f"  {gen[g.i + g.n + j, 1]} -> {g.i + g.n + j}\n")
        f.write("}\n")


fmt = "iiiiiSIIy"
with open(sys.argv[1], "rb") as f:
    buf = f.read()
    g.i, g.n, g.o, g.a, g.p, g.names, g.arity, g.args, genes = wavegp.deserial(
        fmt, buf)

for i, gen in enumerate(genes):
    path = "%s.%08d.gv" % (sys.argv[2], i)
    graph(gen, path)
    sys.stderr.write("graphviz.py: %s\n" % path)
