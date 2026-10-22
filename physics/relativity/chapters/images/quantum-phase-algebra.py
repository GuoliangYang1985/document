# -*- coding: utf-8 -*-
"""第 7 章（量子相态的代数生成）符号核验

核验六组断言：
A. 恒速代数 [B,P]=H/K^2、[B,H]=P、[H,P]=0，以及 K->oo 的收缩
B. 伽利略代数唯一非平凡中央扩张的分类（Jacobi + 上闭链/闭上链）
C. 相位抽取：常 K 时静能项相消、K->oo 得薛定谔方程
D. 变系数 K(x) 时残留项的显式形式与量级
E. 含相位 boost 变换下薛定谔方程的协变性
F. [K,P]=i hbar m、[q,P]=i hbar 的显式算子验证
"""
import itertools
import sympy as sp

t, x, K = sp.symbols('t x K', positive=True)
m, hbar, v = sp.symbols('m hbar v', positive=True)

print("=" * 68)
print("A. 恒速代数（1+1 维向量场）与其收缩")
print("=" * 68)


def comm(op1, op2):
    """两个一阶微分算子 (a,b) = a d/dt + b d/dx 的对易子。"""
    a1, b1 = op1
    a2, b2 = op2
    ct = (a1 * sp.diff(a2, t) + b1 * sp.diff(a2, x)
          - a2 * sp.diff(a1, t) - b2 * sp.diff(a1, x))
    cx = (a1 * sp.diff(b2, t) + b1 * sp.diff(b2, x)
          - a2 * sp.diff(b1, t) - b2 * sp.diff(b1, x))
    return sp.simplify(ct), sp.simplify(cx)


H = (sp.Integer(1), sp.Integer(0))
P = (sp.Integer(0), sp.Integer(1))
B = (-x / K ** 2, -t)

print("[B,P] =", comm(B, P), "   期望 (1/K^2, 0) -> H/K^2")
print("[B,H] =", comm(B, H), "   期望 (0, 1)      -> P")
print("[H,P] =", comm(H, P), "   期望 (0, 0)")
print("K->oo 后 boost 生成元 B =", tuple(sp.limit(c, K, sp.oo) for c in B),
      " 期望 (0, -t)")
print("K->oo 后 [B,P] =", tuple(sp.limit(c, K, sp.oo) for c in comm(B, P)),
      " 期望 (0, 0)")

print()
print("=" * 68)
print("B. 伽利略代数（3+1 维，10 个生成元）中央扩张的分类")
print("=" * 68)
# 基序：0=H, 1..3=P_i, 4..6=K_i(boost), 7..9=J_i(转动)
eps = lambda i, j, k: sp.Rational(int(
    (i - j) * (j - k) * (k - i) / 2))  # Levi-Civita，仅用于 3 个互异指标

n = 10
C = {}  # C[(a,b)] = {k: coeff}，仅存 a<b，取用时按反对称展开


def add(a, b, k, coeff):
    key = (min(a, b), max(a, b))
    s = 1 if (a, b) == key else -1
    C.setdefault(key, {})
    C[key][k] = C[key].get(k, 0) + s * coeff


# [K_i, H] = P_i
for i in range(3):
    add(4 + i, 0, 1 + i, 1)
# [J_i, P_j] = eps_ijk P_k ; [J_i, K_j] = eps_ijk K_k ; [J_i, J_j] = eps_ijk J_k
for i in range(3):
    for j in range(3):
        for k in range(3):
            e = int((i - j) * (j - k) * (k - i) / 2) if len({i, j, k}) == 3 else 0
            if e:
                add(7 + i, 1 + j, 1 + k, e)   # [J_i, P_j] = eps_ijk P_k
                add(7 + i, 4 + j, 4 + k, e)   # [J_i, K_j] = eps_ijk K_k
# [J_i, J_j] = eps_ijk J_k 只按 i<j 登记一次，避免同一对正反各加一次
for i in range(3):
    for j in range(3):
        if i < j:
            k = 3 - i - j
            e = int((i - j) * (j - k) * (k - i) / 2)
            add(7 + i, 7 + j, 7 + k, e)


def bracket(a, b):
    """返回 {k: coeff}，含反对称。"""
    if a == b:
        return {}
    key = (min(a, b), max(a, b))
    s = 1 if (a, b) == key else -1
    return {kk: s * cc for kk, cc in C.get(key, {}).items()}


# 未扩张代数的 Jacobi 自检
ok = True
bad = []
for a, b, c in itertools.combinations(range(n), 3):
    acc = {}
    for (p, q, r) in ((a, b, c), (b, c, a), (c, a, b)):
        for kk, cc in bracket(p, q).items():
            for ll, dd in bracket(kk, r).items():
                acc[ll] = acc.get(ll, 0) + cc * dd
    if any(sp.simplify(val) != 0 for val in acc.values()):
        ok = False
        bad.append((a, b, c, acc))
print("未扩张伽利略代数 Jacobi 自检:", ok)
if bad:
    print("  失败的三元组示例:", bad[:4])
    print("  结构常数样本: [H,K_0]=", bracket(0, 4),
          " [J_0,P_1]=", bracket(7, 2),
          " [J_0,J_1]=", bracket(7, 8),
          " [J_0,K_1]=", bracket(7, 5))

# 上闭链未知量 c[a][b] (a<b)
pairs = [(a, b) for a in range(n) for b in range(n) if a < b]
cs = sp.symbols('c0:45')
cidx = {pr: cs[i] for i, pr in enumerate(pairs)}


def ct(a, b):
    if a == b:
        return sp.Integer(0)
    return cidx[(min(a, b), max(a, b))] * (1 if (a, b) == (min(a, b), max(a, b)) else -1)


eqs = []
for a, b, c in itertools.combinations(range(n), 3):
    expr = 0
    for (p, q, r) in ((a, b, c), (b, c, a), (c, a, b)):
        for kk, cc in bracket(p, q).items():
            expr += cc * ct(kk, r)
    eqs.append(sp.expand(expr))

Amat = sp.Matrix([[sp.expand(e).coeff(c) for c in cs] for e in eqs])
rank = Amat.rank()
dim_cocycle = len(cs) - rank
print("2-闭上链空间维数:", dim_cocycle)

# 上边界空间：c_f(a,b) = f([a,b])，f 由 10 个分量 f_k 给出
fs = sp.symbols('f0:10')
cols = []
for k in range(n):
    col = []
    for (a, b) in pairs:
        col.append(bracket(a, b).get(k, 0))
    cols.append(sp.Matrix(col))
Bmat = sp.Matrix.hstack(*cols)
dim_boundary = Bmat.rank()
print("2-上边界空间维数:", dim_boundary)
print("H^2(galilei, R) 的维数 =", dim_cocycle - dim_boundary)

# 非平凡代表元：取 c(K_i, P_j) = delta_ij（其余为 0），检验它是闭上链而非上边界
test = {pr: sp.Integer(0) for pr in pairs}
for i in range(3):
    test[(1 + i, 4 + i)] = sp.Integer(1)  # (P_i, K_i) 有序对
res = [sp.expand(e).subs({cidx[pr]: test[pr] for pr in pairs}) for e in eqs]
print("代表元 c(P_i,K_j)=delta_ij 满足全部 Jacobi:", all(r == 0 for r in res))
# 上边界在该分量上必为 0，因为 [K_i,P_j]=0
print("上边界在 (K_i,P_j) 分量上的值 [K_i,P_j] =", bracket(4, 1),
      "-> 该分量恒为 0，故代表元非上边界")

print()
print("=" * 68)
print("C. 常系数 K：相位抽取与 K->oo 极限")
print("=" * 68)
K0 = sp.Symbol('K0', positive=True)
X, T = sp.symbols('X T')
phi = sp.Function('phi')(X, T)
th = m * K0 ** 2 * T / hbar
psi = sp.exp(-sp.I * th) * phi
L = sp.simplify(sp.expand(
    K0 ** (-2) * sp.diff(psi, T, 2) - sp.diff(psi, X, 2)
    + m ** 2 * K0 ** 2 / hbar ** 2 * psi))
core = sp.simplify(sp.expand(L * sp.exp(sp.I * th)))
print("L psi = e^{-i theta} * [", core, "]")
# 断言：core 应等于 K^{-2} phi_TT - (2 i m/hbar) phi_T - phi_XX（静能项相消）
claim = (K0 ** (-2) * sp.diff(phi, T, 2)
         - 2 * sp.I * m / hbar * sp.diff(phi, T)
         - sp.diff(phi, X, 2))
print("静能项 m^2K^2/hbar^2 是否相消（core - claim）:",
      sp.simplify(sp.expand(core - claim)))
# core = 0 乘以 (i hbar / 2m) 后即为目标方程
target = sp.expand(core * (sp.I * hbar / (2 * m)))
print("乘以 i hbar/(2m) 后（即 i hbar phi_T + ... = 0 的左端）:", sp.simplify(target))

print()
print("=" * 68)
print("D. 变系数 K(X)：残留项")
print("=" * 68)
Kf = sp.Function('K')(X)
thx = 2 * m * T * Kf * sp.diff(Kf, X) / hbar
thxx = m * T / hbar * sp.diff(Kf ** 2, X, 2)
psi2 = sp.exp(-sp.I * m * Kf ** 2 * T / hbar) * phi
L2 = sp.simplify(sp.expand(
    Kf ** (-2) * sp.diff(psi2, T, 2) - sp.diff(psi2, X, 2)
    + m ** 2 * Kf ** 2 / hbar ** 2 * psi2))
core2 = sp.simplify(sp.expand(L2 * sp.exp(sp.I * m * Kf ** 2 * T / hbar)))
guess = (Kf ** (-2) * sp.diff(phi, T, 2)
         - 2 * sp.I * m / hbar * sp.diff(phi, T)
         - sp.diff(phi, X, 2)
         + 2 * sp.I * thx * sp.diff(phi, X)
         + sp.I * thxx * phi
         + thx ** 2 * phi)
print("core2 - 预期形式 =", sp.simplify(sp.expand(core2 - guess)))
print("残留项 A（一阶导数，反 Hermite）= 2 i hbar T K K' phi_X")
print("残留项 B（零阶，反 Hermite）  = i hbar T (K'^2 + K K'') phi")
print("残留项 C（零阶，Hermite，发散）= 2 m T^2 K^2 K'^2 phi")
Kp = sp.Symbol('Kp')  # |nabla K| 视为与 K0 无关的量级
print("取 K -> K0 -> oo 且 K' 固定时残留项 C 的量级: K^2 * K'^2 ~ K0^2 -> oo")
print("残留项 A、B 的量级: K K' ~ K0 -> oo")

print()
print("=" * 68)
print("E. 含相位 boost 下薛定谔方程的协变性")
print("=" * 68)
V = sp.Symbol('V', real=True)
a0, a1, a2, aT = sp.symbols('psi psi_X psi_XX psi_T')  # psi, psi_xi, psi_xixi, psi_T
S_T = -m * V ** 2 / 2
S_X = m * V
# Phi_T / Phi_XX 的括号表达式
br_T = sp.I / hbar * S_T * a0 + aT - V * a1
br_XX = (sp.I / hbar * S_X) ** 2 * a0 + 2 * (sp.I / hbar * S_X) * a1 + a2
expr = sp.simplify(sp.expand(sp.I * hbar * br_T + hbar ** 2 / (2 * m) * br_XX))
print("i hbar Phi_T + (hbar^2/2m) Phi_XX = e^{iS/hbar} * [",
      sp.simplify(expr), "]")
print("若 psi 满足 i hbar psi_T = -(hbar^2/2m) psi_xx，则括号内 =",
      sp.simplify(expr.subs(aT, sp.I * hbar / (2 * m) * a2)))
# 对照组：去掉相位（S=0，即真表示）时的残留
br_T0 = aT - V * a1
br_XX0 = a2
expr0 = sp.simplify(sp.expand(sp.I * hbar * br_T0 + hbar ** 2 / (2 * m) * br_XX0))
print("无相位时：i hbar Phi_T + (hbar^2/2m) Phi_XX =", expr0,
      " -> 残留 =", sp.simplify(expr0.subs(aT, sp.I * hbar / (2 * m) * a2)))

print()
print("=" * 68)
print("F. 算子对易子 [K,P]、[q,P] 的显式验证")
print("=" * 68)
f = sp.Function('f')(X, T)
Kop = m * X * f + sp.I * hbar * T * sp.diff(f, X)          # K = m q - t P
Pop = -sp.I * hbar * sp.diff(f, X)                          # P = -i hbar d/dx
lhs = sp.expand(m * X * Pop + sp.I * hbar * T * sp.diff(Pop, X))
rhs = sp.expand(-sp.I * hbar * sp.diff(Kop, X))
print("[K,P] f =", sp.simplify(lhs - rhs), "   期望 i hbar m f")
qop = X * f
lhs2 = X * Pop
rhs2 = -sp.I * hbar * sp.diff(qop, X)
print("[q,P] f =", sp.simplify(lhs2 - rhs2), "   期望 i hbar f")
print()
print("=" * 68)
print("色散关系收缩：E^2 = m^2 K^4 + p^2 K^2, E = mK^2 + E_nr")
print("=" * 68)
p = sp.Symbol('p', real=True)
Enr = sp.Symbol('E_nr')
exprC = sp.expand((m * K ** 2 + Enr) ** 2 / K ** 2 - p ** 2 - m ** 2 * K ** 2)
print("展开 E^2/K^2 - p^2 - m^2K^2 =", sp.simplify(exprC))
print("K->oo 取极限:", sp.limit(sp.simplify(exprC), K, sp.oo),
      "  -> 2 m E_nr - p^2 = 0  ->  E_nr = p^2/(2m)")
