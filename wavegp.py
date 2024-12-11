import collections
import numpy as np
import re
import struct
import io


class UnknownFormatString(Exception):
    pass


dtype = np.dtype("uint8")
max_val = 256

def as_string(g, gen, All=False):
    o = io.StringIO()
    rn = reachable_nodes(g, gen)
    for i in range(g.i):
        o.write("%3d: input\n" % i)
    for i in range(g.n):
        if All or g.i + i in rn:
            o.write("%3d: %s" % (g.i + i, g.names[gen[g.i + i, 0]]))
            p = io.StringIO()
            args = g.args[gen[g.i + i, 0]]
            for j in range(args):
                if j > 0:
                    p.write(", ")
                p.write("%d" % gen[g.i + i, 1 + g.a + j])
            o.write(" [%s]" % p.getvalue())
            for j in range(g.arity[gen[g.i + i, 0]]):
                o.write(" %d" % gen[g.i + i, 1 + j])
            if g.i + i in rn:
                o.write(" *")
            o.write("\n")
    for i in range(g.o):
        o.write("%3d: output %d\n" % (g.i + g.n + i, gen[g.i + g.n + i, 1]))
    return o.getvalue()


def build(g, verts, edgs, params):
    Names = {name: index for index, name in enumerate(g.names)}
    gen = np.zeros((g.i + g.n + g.o, 1 + g.a + g.p), dtype=np.uint8)
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
    for i, param in enumerate(params):
        for k, p in enumerate(param):
            gen[D[i], 1 + g.a + k] = p
    return gen


def reachable_nodes(g, gen):
    q = {x for x in gen[g.i + g.n:, 1]}
    ans = set()
    while q:
        n = q.pop()
        if n >= g.i:
            ans.add(n)
            arity = g.arity[gen[n, 0]]
            adj = gen[n, 1:1 + arity]
            q.update(adj)
    return sorted(ans)


def serial(fmt, *args):
    assert len(fmt) == len(args)
    buf = bytearray()
    for f, a in zip(fmt, args):
        if f == "i":
            buf.extend(struct.pack("<i", a))
        elif f == "S":
            buf.extend(struct.pack("<i", len(a)))
            for s in a:
                buf.extend(struct.pack("<i", len(s)))
                buf.extend(s.encode("utf-8"))
        elif f == "I":
            buf.extend(struct.pack("<i", len(a)))
            for s in a:
                buf.extend(struct.pack("<i", s))
        elif f == "y":
            buf.extend(struct.pack("<i", len(a)))
            for s in a:
                assert s.dtype == dtype
                buf.extend(struct.pack("<i", s.ndim))
                buf.extend(struct.pack("<%ii" % s.ndim, *s.shape))
                buf.extend(s.tobytes())
        else:
            raise UnknownFormatString("Unknown format string: %s" % f)
    return buf


def deserial(fmt, buf):
    offset = 0
    ans = []
    for f in fmt:
        if f == "i":
            a, = struct.unpack_from("<i", buf, offset)
            offset += struct.calcsize("<i")
            ans.append(a)
        elif f == "S":
            n_strings, = struct.unpack_from("<i", buf, offset)
            offset += struct.calcsize("<i")
            strings = []
            for i in range(n_strings):
                size, = struct.unpack_from("<i", buf, offset)
                offset += struct.calcsize("<i")
                value, = struct.unpack_from("%ds" % size, buf, offset)
                offset += struct.calcsize("%ds" % size)
                strings.append(value.decode("utf-8"))
            ans.append(strings)
        elif f == "I":
            size, = struct.unpack_from("<i", buf, offset)
            offset += struct.calcsize("<i")
            value = struct.unpack_from("<%di" % size, buf, offset)
            offset += struct.calcsize("<%di" % size)
            ans.append(value)
        elif f == "y":
            n_arrays, = struct.unpack_from("<i", buf, offset)
            offset += struct.calcsize("<i")
            arrays = []
            for i in range(n_arrays):
                ndim, = struct.unpack_from("<i", buf, offset)
                offset += struct.calcsize("<i")
                shape = []
                for i in range(ndim):
                    d, = struct.unpack_from("<i", buf, offset)
                    offset += struct.calcsize("<i")
                    shape.append(d)
                array = np.ndarray(shape, dtype, buf, offset)
                arrays.append(array)
                offset += array.size
            ans.append(arrays)
        else:
            raise UnknownFormatString("Unknown format string: %s" % f)
    return ans
