# -*- coding: utf-8 -*-
"""第 6 章 Weyl 部分：一般族（含拖曳 Omega）的分量 + Schwarzschild 特化的不变量。"""
import sympy as sp

t, r, th, ph = sp.symbols('t r theta phi')
X = [t, r, th, ph]
s = sp.sin(th)

F = sp.Function('F')(r)
A = sp.Function('A')(r)
Om = sp.Function('Omega')(r)


def build_metric(Fv, Av, Omv):
    gg = sp.zeros(4, 4)
    gg[0, 0] = Fv - r ** 2 * s ** 2 * Omv ** 2
    gg[0, 3] = -r ** 2 * s ** 2 * Omv
    gg[3, 0] = -r ** 2 * s ** 2 * Omv
    gg[1, 1] = -Av
    gg[2, 2] = -r ** 2
    gg[3, 3] = -r ** 2 * s ** 2
    return gg


def curvatures(gg):
    ginv = sp.simplify(gg.inv())

    def dd(f, m):
        return sp.diff(f, X[m])

    Gam = {}
    for a in range(4):
        for m in range(4):
            for v in range(4):
                e = 0
                for sg in range(4):
                    e += ginv[a, sg] * (dd(gg[v, sg], m) + dd(gg[m, sg], v) - dd(gg[m, v], sg))
                Gam[(a, m, v)] = sp.simplify(e / 2)

    Ric = {}
    for sg in range(4):
        for v in range(4):
            e1 = sum(dd(Gam[(a, v, sg)], a) for a in range(4))
            e2 = sum(dd(Gam[(a, a, sg)], v) for a in range(4))
            e3 = sum(Gam[(a, a, l)] * Gam[(l, v, sg)] for a in range(4) for l in range(4))
            e4 = sum(Gam[(a, v, l)] * Gam[(l, a, sg)] for a in range(4) for l in range(4))
            Ric[(sg, v)] = sp.simplify(e1 - e2 + e3 - e4)

    Rs = sp.simplify(sum(ginv[m, n] * Ric[(m, n)] for m in range(4) for n in range(4)))

    Rie = {}
    for a in range(4):
        for b in range(4):
            for m in range(4):
                for v in range(4):
                    Rie[(a, b, m, v)] = (
                        dd(Gam[(a, b, v)], m) - dd(Gam[(a, b, m)], v)
                        + sum(Gam[(a, m, l)] * Gam[(l, b, v)] for l in range(4))
                        - sum(Gam[(a, v, l)] * Gam[(l, b, m)] for l in range(4)))

    cache = {}

    def rlow(a, b, m, v):
        if (a, b, m, v) not in cache:
            cache[(a, b, m, v)] = sp.simplify(
                sum(gg[a, l] * Rie[(l, b, m, v)] for l in range(4)))
        return cache[(a, b, m, v)]

    def weyl(a, b, m, v):
        term = rlow(a, b, m, v)
        term += -(gg[a, m] * Ric[(b, v)] - gg[a, v] * Ric[(b, m)]
                  - gg[b, m] * Ric[(a, v)] + gg[b, v] * Ric[(a, m)])
        term += sp.Rational(1, 6) * Rs * (gg[a, m] * gg[b, v] - gg[a, v] * gg[b, m])
        return sp.simplify(term)

    return gg, ginv, Gam, Ric, Rs, weyl


# ================= 一般族 =================
print("########## 一般族（含拖曳 Omega(r)）##########")
g, ginv, Gam, Ric, Rs, weyl = curvatures(build_metric(F, A, Om))

keys = [(0, 1, 0, 1), (0, 2, 0, 2), (0, 3, 0, 3), (1, 3, 1, 3), (0, 1, 1, 3), (2, 3, 2, 3)]
for key in keys:
    val = weyl(*key)
    print("C_%d%d%d%d =" % key, sp.simplify(val))

print("\n只含 Omega' 的部分（令 Omega=const 后考察）：")
# 取 Omega 为常数时 C_0101 是否还依赖 Omega
Om0 = sp.Symbol('Omega0')
gg_c = build_metric(F, A, Om0)
_, _, _, _, _, weyl_c = curvatures(gg_c)
print("Omega=const 时 C_0101 =", sp.simplify(weyl_c(0, 1, 0, 1)))
print("Omega=const 时 C_0313 =", sp.simplify(weyl_c(0, 3, 1, 3)))

# ================= Schwarzschild =================
print("\n\n########## Schwarzschild 特化 ##########")
M = sp.Symbol('M', positive=True)
gg2 = build_metric(1 - 2 * M / r, 1 / (1 - 2 * M / r), 0)
g2, ginv2, Gam2, Ric2, Rs2, weyl2 = curvatures(gg2)

print("Ricci 全零:", all(sp.simplify(Ric2[(m, n)]) == 0 for m in range(4) for n in range(4)))
print("R =", Rs2)
print("Einstein 张量全零:",
      all(sp.simplify(Ric2[(m, n)] - Rs2 * g2[m, n] / 2) == 0
          for m in range(4) for n in range(4)))

print("\n非零 Weyl 分量：")
for key in [(0, 1, 0, 1), (0, 2, 0, 2), (0, 3, 0, 3), (1, 2, 1, 2), (1, 3, 1, 3), (2, 3, 2, 3)]:
    val = weyl2(*key)
    print("  C_%d%d%d%d =" % key, sp.simplify(val))

# 不变量（gi nv2 为对角，可大幅简化）
print("\nWeyl 不变量 C_{abcd} C^{abcd}：")
I2 = 0
for a in range(4):
    for b in range(4):
        for m in range(4):
            for v in range(4):
                cc = sp.simplify(weyl2(a, b, m, v))
                if cc == 0:
                    continue
                I2 += cc * cc * ginv2[a, a] * ginv2[b, b] * ginv2[m, m] * ginv2[v, v]
I2 = sp.simplify(I2)
print("  I =", I2)
print("  与 48 M^2/r^6 之差 =", sp.simplify(I2 - 48 * M ** 2 / r ** 6))

# 恒速场 K = sqrt(F)，及其梯度
Kv = sp.sqrt(1 - 2 * M / r)
print("\nK(r) =", Kv, " ; dK/dr =", sp.simplify(sp.diff(Kv, r)))
print("视界处 K ->", sp.limit(Kv, r, 2 * M))
