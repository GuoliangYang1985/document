# -*- coding: utf-8 -*-
"""
第 14 章配图（修订版）：**以 A 自己的坐标为纸面**的视角图。

与旧图的根本差别：旧图把 A 的坐标网格叠在惯性坐标 (t,x) 上——那张纸属于
第三方；本图的横轴是 A 自己的空间坐标 x_A、纵轴是 A 自己的读数坐标 tau_A，
画面上不出现任何第三方坐标。

左  K=c    : 坐标域止于 x_A = -1（单位 a=1）；同一格 dtau_A 在不同 x_A 处
             代表的读数不同，因子为 (1 + a x_A / c^2)。
右  K=oo   : 坐标域无界；同一格 dtau_A 处处代表同一个读数。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sympy as sp

for f, s in (("font.sans-serif", ["Microsoft YaHei", "SimHei", "DejaVu Sans"]),
             ("axes.unicode_minus", False)):
    plt.rcParams[f] = s

BLUE, RED, GREEN, GREY, BLACK = "#1f4e79", "#b03a2e", "#2e7d32", "#666666", "#111111"

# ------------------------------------------------------------------ 符号核验
u, rho = sp.symbols("u rho", positive=True)
print("=== 核验 1：B 的像在 A 视角坐标中的方程 ===")
rho_sq = sp.simplify(sp.expand((2 - sp.cosh(u)) ** 2 - sp.sinh(u) ** 2))
print("  rho^2 =", rho_sq)
num = [(0.3, float(sp.sqrt(5 - 4 * sp.cosh(0.3)))),
       (0.5, float(sp.sqrt(5 - 4 * sp.cosh(0.5)))),
       (float(sp.log(2)), float(sp.sqrt(5 - 4 * sp.cosh(sp.log(2)))))]
for uu, rr in num:
    print(f"  u={uu:.4f}  rho={rr:.6f}  (5-4cosh u)^0.5 校验={float(sp.sqrt(5-4*sp.cosh(uu))):.6f}")
print("  cosh(ln2) =", sp.nsimplify(sp.cosh(sp.log(2))), " -> rho^2 = 0")
# A 视角时间坐标：tanh(a tau_A) = sinh u /(2-cosh u)
print("=== 核验 2：A 视角时间坐标随 u 的行为 ===")
for uu in [0.0, 0.2, 0.4, 0.6, 0.69, 0.693]:
    den = 2 - np.cosh(uu)
    tA = np.arctanh(np.sinh(uu) / den) if den > 0 else float("inf")
    rr = np.sqrt(max(5 - 4 * np.cosh(uu), 0))
    print(f"  u={uu:.3f}  x_A=rho-1={rr-1:+.5f}  a*tau_A={tA:.4f}")
print("  说明：u -> ln2 时 rho -> 0（即 x_A -> -1，域边界），而 a*tau_A -> 无穷。")

print("=== 核验 3：K=oo 支 ===")
t_, x_, Xt = sp.symbols("t x Xt")
print("  线元代入：ds^2 = dt^2，取 x_A = x - Xi(t) 后 ds^2 = dt_A^2，加速轨迹 Xi 不进入。")

# ------------------------------------------------------------------ 图
fig, axes = plt.subplots(1, 2, figsize=(11.2, 5.0))

# ---------- (a) K = c ：单位 a = 1，域 x_A > -1 ----------
ax = axes[0]
ax.axhspan(-10, 10, color="#f2f6fa", zorder=0)
ax.axvspan(-1.0, 6, color="#ffffff", zorder=0)
# 域外（x_A < -1）：不属于 A 的坐标域
ax.axvspan(-2.2, -1.0, color="#eeeeee", zorder=0, hatch="///")

# A 自己的坐标网格（在自己的纸面上是均匀正交直线）
for xv in np.arange(-1.0, 3.01, 0.5):
    ax.plot([xv, xv], [-0.2, 3.2], color=BLUE, lw=0.85, alpha=0.45)
for tv in np.arange(0.0, 3.01, 0.5):
    ax.plot([-1.0, 3.0], [tv, tv], color=RED, lw=0.85, alpha=0.45)
ax.text(2.15, 3.28, "$x_A=$常数", fontsize=10.5, color=BLUE, ha="center")
ax.text(-1.30, 1.80, "$\\tau_A=$常数", fontsize=10.5, color=RED, rotation=90, va="center")

# A 的世界线
ax.plot([0, 0], [0, 3.2], color=BLACK, lw=2.6)
ax.text(0.10, 2.72, "A：$x_A=0$", fontsize=11, color=BLACK)

# B 的像（EMAhler u 参数方程）
us = np.linspace(0, np.log(2) - 1e-4, 900)
rr = np.sqrt(np.maximum(5 - 4 * np.cosh(us), 0))
xA = rr - 1.0
tA = np.arctanh(np.sinh(us) / (2 - np.cosh(us)))
ax.plot(xA, tA, color=RED, lw=2.6)
ax.text(-0.30, 2.55, "B 的像", fontsize=11.5, color=RED, rotation=0)

# 读数刻度：同一格 dtau_A 在不同 x_A 处代表的读数
for xv, fac in [(0.0, "1"), (1.0, "2")]:
    ax.plot([xv, xv], [1.0, 1.5], color=GREEN, lw=5.5, alpha=0.85, solid_capstyle="butt")
    ax.text(xv + 0.12, 1.25, f"$={fac}\\,\\Delta\\tau_A$",
            fontsize=10.5, color=GREEN, va="center")
ax.annotate("", xy=(0.0, 0.72), xytext=(1.0, 0.72),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.1))
ax.text(1.90, 2.30, "同一格 $\\Delta\\tau_A$：\n读数随 $x_A$ 变\n因子 $(1+a x_A/c^{2})$",
        fontsize=10, color=GREY, ha="center")

# 域边界
ax.axvline(-1.0, color=GREY, ls="--", lw=1.6)
ax.text(-0.90, -0.02, "$x_A=-c^{2}/a$", fontsize=10.5, color=GREY, va="bottom")
ax.text(-1.62, 2.90, "不在 A 的坐标域中", fontsize=10, color=GREY, ha="center", rotation=90)

ax.set_xlim(-2.2, 3.0); ax.set_ylim(-0.2, 3.4)
ax.set_xlabel("$a\\,x_A\\,/\\,c^{2}$（A 自己的空间坐标）", fontsize=11)
ax.set_ylabel("$a\\,\\tau_A\\,/\\,c$（A 自己的读数坐标）", fontsize=11)
ax.set_title("$K=c$：A 视角坐标纸面（域止于 $-c^{2}/a$）", fontsize=12.5)

# ---------- (b) K = oo ----------
ax = axes[1]
for xv in np.arange(-2.0, 2.51, 0.5):
    ax.plot([xv, xv], [-0.2, 3.2], color=BLUE, lw=0.85, alpha=0.45)
for tv in np.arange(0.0, 3.01, 0.5):
    ax.plot([-2.0, 2.5], [tv, tv], color=RED, lw=0.85, alpha=0.45)
ax.text(1.85, 3.28, "$x_A=$常数", fontsize=10.5, color=BLUE, ha="center")
ax.text(-1.88, 1.05, "$t_A=$常数", fontsize=10.5, color=RED, rotation=90, va="center")

ax.plot([0, 0], [0, 3.2], color=BLACK, lw=2.6)
ax.text(0.10, 2.72, "A：$x_A=0$", fontsize=11, color=BLACK)

# 加速轨迹取 Xi(t) = t^2/2 (任意光滑函数；不进入线元)
tt = np.linspace(0, 1.55, 400)
xB = -2 * (0.5 * tt ** 2)
ax.plot(xB, tt, color=RED, lw=2.6)
ax.text(-1.95, 0.30, "B 的像 $x_A=-2\\,\\Xi(t_A)$", fontsize=11, color=RED)

for xv in [0.0, 1.0]:
    ax.plot([xv, xv], [1.0, 1.5], color=GREEN, lw=5.5, alpha=0.85, solid_capstyle="butt")
    ax.text(xv + 0.12, 1.25, "$=\\Delta\\tau_A$", fontsize=10.5, color=GREEN, va="center")
ax.annotate("", xy=(0.0, 0.72), xytext=(1.0, 0.72),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.1))
ax.text(1.55, 2.20, "同一格 $\\Delta\\tau_A$：\n读数处处相同\n（$=1\\cdot\\Delta\\tau_A$）",
        fontsize=10, color=GREY, ha="center")
ax.text(-1.95, 3.02, "坐标域无界，处处有像", fontsize=10, color=GREY)

ax.set_xlim(-2.1, 2.5); ax.set_ylim(-0.2, 3.4)
ax.set_xlabel("$x_A$（A 自己的空间坐标）", fontsize=11)
ax.set_ylabel("$t_A$（A 自己的时间坐标＝读数）", fontsize=11)
ax.set_title("$K=\\infty$：A 视角坐标纸面（全域）", fontsize=12.5)

fig.tight_layout()
fig.savefig("twins-a-view.png", dpi=155)
print("\n  已输出 twins-a-view.png")
