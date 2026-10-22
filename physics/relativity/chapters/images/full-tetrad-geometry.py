# -*- coding: utf-8 -*-
"""第 6 章：含拖曳与剪切的完整族
ds^2 = F(r) dt^2 - A(r) dr^2 - r^2 dtheta^2 - r^2 sin^2(theta) (dphi + Omega(r) dt)^2
其中 F = K^2, K 为恒速场（局部光速上限）。
严格计算 Christoffel / Ricci / R / Einstein / Weyl。
"""
import sympy as sp

t, r, th, ph = sp.symbols('t r theta phi')
X = [t, r, th, ph]
s = sp.sin(th)
c = sp.cos(th)

F = sp.Function('F')(r)      # F = K^2
A = sp.Function('A')(r)
Om = sp.Function('Omega')(r)

g = sp.zeros(4, 4)
g[0, 0] = F - r ** 2 * s ** 2 * Om ** 2
g[0, 3] = -r ** 2 * s ** 2 * Om
g[3, 0] = -r ** 2 * s ** 2 * Om
g[1, 1] = -A
g[2, 2] = -r ** 2
g[3, 3] = -r ** 2 * s ** 2

print("det g =", sp.simplify(g.det()))

ginv = sp.simplify(g.inv())
print("\n=== g^{mu nu} ===")
for m in range(4):
    for n in range(4):
        if ginv[m, n] != 0:
            print("g^%d%d =" % (m, n), sp.simplify(ginv[m, n]))


def d(f, m):
    return sp.diff(f, X[m])


# ---------- Christoffel ----------
Gam = {}
for a in range(4):
    for m in range(4):
        for v in range(4):
            e = 0
            for sg in range(4):
                e += ginv[a, sg] * (d(g[v, sg], m) + d(g[m, sg], v) - d(g[m, v], sg))
            Gam[(a, m, v)] = sp.simplify(e / 2)

print("\n=== Christoffel 非零分量 ===")
cnt = 0
for a in range(4):
    for m in range(4):
        for v in range(m, 4):
            if Gam[(a, m, v)] != 0:
                cnt += 1
                print("Gamma^%d_{%d%d} = %s" % (a, m, v, sp.simplify(Gam[(a, m, v)])))
print("非零个数:", cnt)

# ---------- Ricci ----------
Ric = {}
for sg in range(4):
    for v in range(4):
        e1 = sum(d(Gam[(a, v, sg)], a) for a in range(4))
        e2 = sum(d(Gam[(a, a, sg)], v) for a in range(4))
        e3 = sum(Gam[(a, a, l)] * Gam[(l, v, sg)] for a in range(4) for l in range(4))
        e4 = sum(Gam[(a, v, l)] * Gam[(l, a, sg)] for a in range(4) for l in range(4))
        Ric[(sg, v)] = sp.simplify(e1 - e2 + e3 - e4)

print("\n=== Ricci 张量非零分量 ===")
for m in range(4):
    for n in range(m, 4):
        if Ric[(m, n)] != 0:
            print("R_%d%d = %s" % (m, n, sp.simplify(Ric[(m, n)])))

Rs = sp.simplify(sum(ginv[m, n] * Ric[(m, n)] for m in range(4) for n in range(4)))
print("\nRicci 标量 R =", sp.simplify(Rs))

# ---------- Einstein ----------
G = {}
for m in range(4):
    for n in range(m, 4):
        G[(m, n)] = sp.simplify(Ric[(m, n)] - Rs * g[m, n] / 2)

print("\n=== Einstein 张量非零分量 ===")
for m in range(4):
    for n in range(m, 4):
        if G[(m, n)] != 0:
            print("G_%d%d = %s" % (m, n, sp.simplify(G[(m, n)])))

# ---------- Riemann (全下指标) ----------
Rie = {}
for a in range(4):
    for b in range(4):
        for m in range(4):
            for v in range(4):
                e = (d(Gam[(a, b, v)], m) - d(Gam[(a, b, m)], v)
                     + sum(Gam[(a, m, l)] * Gam[(l, b, v)] for l in range(4))
                     - sum(Gam[(a, v, l)] * Gam[(l, b, m)] for l in range(4)))
                Rie[(a, b, m, v)] = e

Rlow = {}
for a in range(4):
    for b in range(4):
        for m in range(4):
            for v in range(4):
                Rlow[(a, b, m, v)] = sp.simplify(
                    sum(g[a, l] * Rie[(l, b, m, v)] for l in range(4)))

print("\n=== Weyl 张量：关键分量 ===")


def weyl(a, b, m, v):
    term = Rlow[(a, b, m, v)]
    term += -(g[a, m] * Ric[(b, v)] - g[a, v] * Ric[(b, m)]
              - g[b, m] * Ric[(a, v)] + g[b, v] * Ric[(a, m)])
    term += sp.Rational(1, 6) * Rs * (g[a, m] * g[b, v] - g[a, v] * g[b, m])
    return sp.simplify(term)


for key in [(0, 1, 0, 1), (0, 2, 0, 2), (0, 3, 0, 3), (1, 3, 1, 3), (0, 1, 1, 3)]:
    print("C_%d%d%d%d = %s" % (key[0], key[1], key[2], key[3]), weyl(*key))

# ---------- Schwarzschild 特化 ----------
print("\n\n########## Schwarzschild 特化 ##########")
M = sp.Symbol('M', positive=True)
subs_sch = {F: 1 - 2 * M / r, A: 1 / (1 - 2 * M / r), Om: 0}

# 直接重建 Schwarzschild 度规计算（避免替换导数时的陷阱）
F_s = 1 - 2 * M / r
A_s = 1 / (1 - 2 * M / r)
g2 = sp.zeros(4, 4)
g2[0, 0] = F_s
g2[1, 1] = -A_s
g2[2, 2] = -r ** 2
g2[3, 3] = -r ** 2 * s ** 2
ginv2 = sp.simplify(g2.inv())


def d2(f, m):
    return sp.diff(f, X[m])


Gam2 = {}
for a in range(4):
    for m in range(4):
        for v in range(4):
            e = 0
            for sg in range(4):
                e += ginv2[a, sg] * (d2(g2[v, sg], m) + d2(g2[m, sg], v) - d2(g2[m, v], sg))
            Gam2[(a, m, v)] = sp.simplify(e / 2)

Ric2 = {}
for sg in range(4):
    for v in range(4):
        e1 = sum(d2(Gam2[(a, v, sg)], a) for a in range(4))
        e2 = sum(d2(Gam2[(a, a, sg)], v) for a in range(4))
        e3 = sum(Gam2[(a, a, l)] * Gam2[(l, v, sg)] for a in range(4) for l in range(4))
        e4 = sum(Gam2[(a, v, l)] * Gam2[(l, a, sg)] for a in range(4) for l in range(4))
        Ric2[(sg, v)] = sp.simplify(e1 - e2 + e3 - e4)

print("Schwarzschild Ricci 是否全零:",
      all(sp.simplify(Ric2[(m, n)]) == 0 for m in range(4) for n in range(4)))

Rs2 = sp.simplify(sum(ginv2[m, n] * Ric2[(m, n)] for m in range(4) for n in range(4)))
print("Schwarzschild R =", Rs2)

Rie2 = {}
for a in range(4):
    for b in range(4):
        for m in range(4):
            for v in range(4):
                e = (d2(Gam2[(a, b, v)], m) - d2(Gam2[(a, b, m)], v)
                     + sum(Gam2[(a, m, l)] * Gam2[(l, b, v)] for l in range(4))
                     - sum(Gam2[(a, v, l)] * Gam2[(l, b, m)] for l in range(4)))
                Rie2[(a, b, m, v)] = e

Rlow2 = {}
for a in range(4):
    for b in range(4):
        for m in range(4):
            for v in range(4):
                Rlow2[(a, b, m, v)] = sp.simplify(
                    sum(g2[a, l] * Rie2[(l, b, m, v)] for l in range(4)))


def weyl2(a, b, m, v):
    term = Rlow2[(a, b, m, v)]
    term += -(g2[a, m] * Ric2[(b, v)] - g2[a, v] * Ric2[(b, m)]
              - g2[b, m] * Ric2[(a, v)] + g2[b, v] * Ric2[(a, m)])
    term += sp.Rational(1, 6) * Rs2 * (g2[a, m] * g2[b, v] - g2[a, v] * g2[b, m])
    return sp.simplify(term)


print("\nSchwarzschild Weyl 分量：")
for key in [(0, 1, 0, 1), (0, 2, 0, 2), (0, 3, 0, 3), (1, 2, 1, 2), (2, 3, 2, 3)]:
    print("  C_%d%d%d%d = %s" % (key[0], key[1], key[2], key[3]), weyl2(*key))

# Weyl 不变量 C_{abcd} C^{abcd}
Cup = {}
for a in range(4):
    for b in range(4):
        for m in range(4):
            for v in range(4):
                Cup[(a, b, m, v)] = sp.simplify(sum(
                    ginv2[a, p] * ginv2[b, q] * ginv2[m, u] * ginv2[v, w] * weyl2(p, q, u, w)
                    for p in range(4) for q in range(4) for u in range(4) for w in range(4)))

I2 = sp.simplify(sum(weyl2(a, b, m, v) * Cup[(a, b, m, v)]
                     for a in range(4) for b in range(4)
                     for m in range(4) for v in range(4)))
print("\nSchwarzschild Weyl 不变量 C_abcd C^abcd =", sp.simplify(I2))
print("（标准值 48 M^2 / r^6；差值 =",
      sp.simplify(I2 - 48 * M ** 2 / r ** 6), ")")
