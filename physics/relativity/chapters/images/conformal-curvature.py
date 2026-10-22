# -*- coding: utf-8 -*-
"""对共形（tetrad）约定 g_{μν} = K^2 η_{μν} 严格符号推导曲率。
签名 η = diag(1,-1,-1,-1)。
"""
import sympy as sp

t, x, y, z = sp.symbols('t x y z')
X = [t, x, y, z]
K = sp.Function('K')(t, x, y, z)

eta = sp.diag(1, -1, -1, -1)
g = K ** 2 * eta
ginv = (1 / K ** 2) * eta


def d(f, m):
    return sp.diff(f, X[m])


# ---------- Christoffel ----------
Gam = {}
for r in range(4):
    for m in range(4):
        for v in range(4):
            expr = 0
            for s in range(4):
                expr += ginv[r, s] * (d(g[v, s], m) + d(g[m, s], v) - d(g[m, v], s))
            Gam[(r, m, v)] = sp.simplify(expr / 2)

print("=== Christoffel 非零样本 ===")
for key in [(0, 0, 0), (0, 0, 1), (1, 0, 0), (1, 1, 1), (1, 2, 2), (0, 1, 1)]:
    print("Gamma^%d_{%d%d} = %s" % (key[0], key[1], key[2], Gam[key]))

# 与闭式 Gamma^ρ_{μν} = (δ^ρ_ν ∂_μ K + δ^ρ_μ ∂_ν K - η_{μν} ∂^ρ K)/K 比对
dK = [d(K, m) for m in range(4)]
dKup = [sum(eta[r, s] * dK[s] for s in range(4)) for r in range(4)]
ok_all = True
for r in range(4):
    for m in range(4):
        for v in range(4):
            closed = (sp.KroneckerDelta(r, v) * dK[m]
                      + sp.KroneckerDelta(r, m) * dK[v]
                      - eta[m, v] * dKup[r]) / K
            diff = sp.simplify(sp.expand(Gam[(r, m, v)] - closed))
            if diff != 0:
                ok_all = False
                print("MISMATCH", r, m, v, diff)
print("Christoffel 闭式校验:", "OK" if ok_all else "FAIL")

# ---------- Ricci ----------
Ric = {}
for s in range(4):
    for v in range(4):
        e1 = sum(d(Gam[(r, v, s)], r) for r in range(4))
        e2 = sum(d(Gam[(r, r, s)], v) for r in range(4))
        e3 = sum(Gam[(r, r, l)] * Gam[(l, v, s)] for r in range(4) for l in range(4))
        e4 = sum(Gam[(r, v, l)] * Gam[(l, r, s)] for r in range(4) for l in range(4))
        Ric[(s, v)] = sp.simplify(e1 - e2 + e3 - e4)

# ---------- Ricci 标量 ----------
Rs = sp.simplify(sum(ginv[m, n] * Ric[(m, n)] for m in range(4) for n in range(4)))
print("\n=== Ricci 标量 ===")
sp.pprint(sp.simplify(Rs))

# 闭式 R = -6 (∂_t^2 K - ∇^2 K)/K^3
lapK = d(d(K, 1), 1) + d(d(K, 2), 2) + d(d(K, 3), 3)
boxK = d(d(K, 0), 0) - lapK
print("R 闭式校验:", sp.simplify(sp.expand(Rs - (-6 * boxK / K ** 3))) == 0)

# ---------- Einstein 张量 ----------
G = {}
for m in range(4):
    for n in range(4):
        G[(m, n)] = sp.simplify(Ric[(m, n)] - Rs * g[m, n] / 2)

grad2 = d(K, 1) ** 2 + d(K, 2) ** 2 + d(K, 3) ** 2
print("\n=== G_00 ===")
sp.pprint(sp.simplify(G[(0, 0)]))

G00_closed = (3 * dK[0] ** 2 + grad2) / K ** 2 - 2 * lapK / K
print("G_00 闭式校验:", sp.simplify(sp.expand(G[(0, 0)] - G00_closed)) == 0)

print("\n=== G_00 (静态 ∂_t K = 0) ===")
G00_static = G00_closed.subs(dK[0], 0)
sp.pprint(sp.simplify(G00_static))

print("\n=== G_0i ===")
for i in range(1, 4):
    print("G_0%d =" % i, sp.simplify(G[(0, i)]))

# ---------- u = ln K 形式 ----------
u = sp.log(K)
du = [sp.simplify(sp.diff(u, X[m])) for m in range(4)]
lapu = sp.simplify(sum(sp.diff(u, X[i], 2) for i in range(1, 4)))
grad2u = sum(du[i] ** 2 for i in range(1, 4))
G00_u = sp.simplify(3 * du[0] ** 2 - grad2u - 2 * lapu)
print("\nG_00 用 u=lnK 表达校验:",
      sp.simplify(sp.expand(G[(0, 0)] - G00_u)) == 0)

# 一般分量闭式（u 形式）
print("\n=== 一般分量闭式校验 G_{μν} = -2∂_μ∂_ν u + 2∂_μ u ∂_ν u + η_{μν}(2□u + |∇u|^2_η) ===")
boxu = sp.simplify(sum(eta[m, n] * sp.diff(u, X[m], X[n]) for m in range(4) for n in range(4)))
norm2u = sp.simplify(sum(eta[m, n] * du[m] * du[n] for m in range(4) for n in range(4)))
allok = True
for m in range(4):
    for n in range(4):
        closed = (-2 * sp.diff(u, X[m], X[n]) + 2 * du[m] * du[n]
                  + eta[m, n] * (2 * boxu + norm2u))
        diff = sp.simplify(sp.expand(G[(m, n)] - closed))
        if diff != 0:
            allok = False
            print("MISMATCH", m, n, diff)
print("Einstein 张量闭式校验:", "OK" if allok else "FAIL")
