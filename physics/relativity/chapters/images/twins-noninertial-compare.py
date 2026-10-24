# -*- coding: utf-8 -*-
"""
第 14 章配图：非惯性（加速观者自带）坐标下，两支的读数尺度对照。

左 K=c   : Rindler 坐标。t' = const 是过 (-1/a,0) 的斜线，x' = const 是双曲线；
           ds^2 = (1+a x')^2 dt'^2 - dx'^2 —— 度规带位置因子。
右 K=oo  : 加速观者坐标（只平移空间）。t' = const 仍是水平线，x' = const 是抛物线；
           ds^2 = dt'^2 —— 度规不变，加速轨迹不进入。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sympy as sp

# ------------------------------------------------------------------ 符号核验
t1, x1, a = sp.symbols("t1 x1 a", positive=True)
dt1, dx1 = sp.symbols("dt1 dx1")

tL = (1 / a + x1) * sp.sinh(a * t1)
xL = (1 / a + x1) * sp.cosh(a * t1) - 1 / a
dtL = sp.diff(tL, t1) * dt1 + sp.diff(tL, x1) * dx1
dxL = sp.diff(xL, t1) * dt1 + sp.diff(xL, x1) * dx1
ds2L = sp.simplify(sp.expand(dtL ** 2 - dxL ** 2))
print("洛伦兹支 Rindler : ds^2 =", ds2L)
print("   等于 (1+a x1)^2 dt1^2 - dx1^2 :", sp.simplify(
    ds2L - ((1 + a * x1) ** 2 * dt1 ** 2 - dx1 ** 2)) == 0)

f = sp.Function("f")
tG = t1
xG = x1 + f(t1)
dtG = sp.diff(tG, t1) * dt1 + sp.diff(tG, x1) * dx1
print("伽利略支加速坐标 : ds^2 = dt^2 =", sp.simplify(dtG ** 2))
print("   加速轨迹 f(t1) 是否进入 :", sp.diff(sp.simplify(dtG ** 2), f(t1)) == 0)

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

GREY, BLUE, RED = "#7f7f7f", "#1f6fb5", "#c0392b"
fig, axes = plt.subplots(1, 2, figsize=(12.4, 6.4))

# ============================================================ 左：Rindler
ax = axes[0]
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(-1.45, 2.0)
ax.set_ylim(-0.15, 2.25)
ax.set_title("$K=c$：匀加速观者的坐标（Rindler）", fontsize=13)
ax.annotate("", xy=(0, 2.15), xytext=(0, -0.1),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.2), zorder=3)
ax.annotate("", xy=(1.9, 0), xytext=(-1.35, 0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.2), zorder=3)
ax.text(0.10, 2.14, "$t$", fontsize=13)
ax.text(1.80, -0.13, "$x$", fontsize=13)

aa = 1.0
tt = np.linspace(-1.5, 1.5, 400)
for xp in [0.0, 0.4, 0.8, 1.2]:                       # x' = 常数：双曲线
    R = 1 / aa + xp
    ax.plot(R * np.cosh(aa * tt) - 1 / aa, R * np.sinh(aa * tt),
            "-", color=BLUE, lw=1.5, zorder=2)
for tp in [0.35, 0.70, 1.05, 1.40]:                   # t' = 常数：斜线
    xs = np.linspace(-1 / aa, 1.95, 100)
    ax.plot(xs, (xs + 1 / aa) * np.tanh(aa * tp), "--", color=RED, lw=1.3, zorder=2)
ax.plot([-1 / aa, -1 / aa], [-0.1, 2.2], ":", color="0.6", lw=1.0, zorder=1)

ax.plot([-1 / aa + 0.02], [0.02], "o", color="k", ms=5, zorder=5)
ax.text(-1 / aa + 0.08, 0.10, "$-1/a$", fontsize=11, color="0.35")
ax.text(1.62, 1.62, "$x'=$常数", fontsize=11.5, color=BLUE, rotation=38)
ax.text(0.62, 0.92, "$t'=$常数", fontsize=11.5, color=RED, rotation=38)
ax.text(-1.40, 1.98, "$\\mathrm{d}s^2=(1+a x')^2\\,\\mathrm{d}t'^2-\\mathrm{d}x'^2$",
        fontsize=12)
ax.text(-1.40, -0.05, "度规随位置变化", fontsize=11.5, color="0.15")

# ============================================================ 右：伽利略加速坐标
ax = axes[1]
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(-1.0, 2.4)
ax.set_ylim(-0.15, 2.25)
ax.set_title("$K=\\infty$：同一加速观者的坐标", fontsize=13)
ax.annotate("", xy=(0, 2.15), xytext=(0, -0.1),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.2), zorder=3)
ax.annotate("", xy=(2.3, 0), xytext=(-0.9, 0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.2), zorder=3)
ax.text(0.10, 2.14, "$t$", fontsize=13)
ax.text(2.20, -0.13, "$x$", fontsize=13)

acc = 0.5
tv = np.linspace(0, 2.15, 300)
for xp in [-0.4, 0.0, 0.4, 0.8, 1.2]:                 # x' = 常数：抛物线
    ax.plot(xp + 0.5 * acc * tv ** 2, tv, "-", color=BLUE, lw=1.5, zorder=2)
for tp in [0.5, 1.0, 1.5, 2.0]:                       # t' = 常数：水平线
    ax.plot([-0.85, 2.25], [tp, tp], "--", color=RED, lw=1.3, zorder=2)

ax.text(1.86, 1.72, "$x'=$常数", fontsize=11.5, color=BLUE, rotation=62)
ax.text(-0.80, 1.06, "$t'=$常数", fontsize=11.5, color=RED)
ax.text(-0.95, 1.98, "$\\mathrm{d}s^2=\\mathrm{d}t'^2$", fontsize=12)
ax.text(-0.95, -0.05, "度规不含位置因子", fontsize=11.5, color="0.15")

plt.tight_layout()
plt.savefig("twins-noninertial-compare.png", dpi=200, facecolor="white")
print("saved twins-noninertial-compare.png")
