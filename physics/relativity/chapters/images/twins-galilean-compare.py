# -*- coding: utf-8 -*-
"""
第 13 章配图：洛伦兹（K=c）与伽利略（K=∞）的闵氏几何对照。

同一构造（A 视角，B 以 w 运动，A 读 tau）：
  等固有读数轨迹  t^2 - x^2/K^2 = tau^2
  对称点坐标时    t = tau / sqrt(1 - w^2/K^2) = gamma_w * tau
K -> 无穷 时双曲线退化为水平直线 t = tau，gamma_w -> 1，各配对重合。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sympy as sp

# ------------------------------------------------------------------ 符号核验
K, w, tau = sp.symbols("K w tau", positive=True)
gw = 1 / sp.sqrt(1 - w ** 2 / K ** 2)
print("gamma_w(K) =", gw)
print("K->oo       =", sp.limit(gw, K, sp.oo))
print("K 扫描（w=0.8824）:")
for Kv in [sp.oo, sp.Integer(3), sp.Rational(3, 2), sp.Integer(1)]:
    print("  K=%-6s gamma_w=%.4f" % (Kv, float(gw.subs({K: Kv, w: sp.Rational(15, 17)}))))

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

BLUE, RED = "#1f6fb5", "#c0392b"
wn = 2 * 0.6 / (1 + 0.6 ** 2)               # 0.8824（与本章 v=0.6c 一致）
gwn = (1 + 0.6 ** 2) / (1 - 0.6 ** 2)       # 2.125

fig, axes = plt.subplots(1, 2, figsize=(11.6, 5.6))


def frame(ax, title, xlim, ylim):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_title(title, fontsize=12.5)
    ax.annotate("", xy=(0, ylim[1] * 0.97), xytext=(0, ylim[0] + 0.12),
                arrowprops=dict(arrowstyle="-|>", color="k", lw=1.25), zorder=3)
    ax.annotate("", xy=(xlim[1] * 0.93, 0), xytext=(xlim[0] + 0.12, 0),
                arrowprops=dict(arrowstyle="-|>", color="k", lw=1.25), zorder=3)
    ax.text(0.10, ylim[1] * 0.955, "$t$", fontsize=12)
    ax.text(xlim[1] * 0.88, -0.16, "$x$", fontsize=12)
    L = ylim[1]
    ax.plot([0, L], [0, L], color="0.88", lw=0.8, zorder=0)
    ax.plot([0, -L], [0, L], color="0.88", lw=0.8, zorder=0)


xlim, ylim = (-2.35, 1.05), (-0.45, 2.55)

# ============================================================ 左：洛伦兹 K=c
ax = axes[0]
frame(ax, "洛伦兹（$K=c$）：双曲线，配对分离", xlim, ylim)

tt = np.linspace(0, 2.40, 50)
ax.plot(-wn * tt, tt, "-", color="k", lw=1.6, zorder=3)
ax.text(-wn * 2.40 - 0.28, 2.34, "$B$", fontsize=12)

tt = np.linspace(1.0, 2.30, 400)
ax.plot(-np.sqrt(tt ** 2 - 1), tt, "--", color=BLUE, lw=2.0, zorder=2,
        label="等读数轨迹 $t^2-x^2/K^2=\\tau^2$（双曲线）")

ax.plot([-wn * gwn, 0.05], [gwn, gwn], "--", color=RED, lw=1.2, zorder=2,
        label="本系同时线（水平）")
ax.plot([-wn, 0.05], [1.0, 1.0], "--", color=RED, lw=1.2, zorder=2)

ax.plot(0, 1, "o", color="k", ms=6, zorder=5)
ax.plot(-wn * gwn, gwn, "o", color=RED, ms=6, zorder=5)
ax.plot(0, gwn, "s", color=RED, mfc="white", mec=RED, ms=7, zorder=5)
ax.plot(-wn, 1.0, "o", mfc="white", mec="0.35", ms=6.5, zorder=5)

ax.text(0.10, 0.80, "A 读 $\\tau$", fontsize=11)
ax.text(0.10, 2.14, "投影 $=2.125\\,\\tau$", fontsize=11, color=RED)
ax.text(-wn * gwn - 0.06, gwn - 0.22, "B 读 $\\tau$（对称点）",
        fontsize=11, color=RED, ha="right")
ax.text(-wn - 0.08, 0.70, "B 读 $0.47\\tau$", fontsize=10.5,
        color="0.30", ha="right")
ax.text(-0.17, -0.20, "$O$", fontsize=11)
ax.legend(loc="lower left", fontsize=9.5, framealpha=0.96)

# ============================================================ 右：伽利略 K=∞
ax = axes[1]
frame(ax, "伽利略（$K=\\infty$）：水平线，配对重合", xlim, ylim)

tt = np.linspace(0, 2.40, 50)
ax.plot(-wn * tt, tt, "-", color="k", lw=1.6, zorder=3)
ax.text(-wn * 2.40 - 0.28, 2.34, "$B$", fontsize=12)

ax.plot([-2.1, 0.05], [1, 1], "-", color=BLUE, lw=2.0, zorder=2,
        label="等读数轨迹 $t=\\tau$（水平直线，绝对）")
ax.plot([-2.1, 0.05], [1, 1], "--", color=RED, lw=1.4, zorder=3,
        label="本系同时线（与前者重合）")

ax.plot(0, 1, "o", color="k", ms=6, zorder=5)
ax.plot(-wn, 1.0, "o", color=RED, ms=6, zorder=5)

ax.text(0.10, 0.80, "A 读 $\\tau$", fontsize=11)
ax.text(-wn - 0.08, 1.12, "B 读 $\\tau$（同一点）", fontsize=11, color=RED,
        ha="right")
ax.text(-0.17, -0.20, "$O$", fontsize=11)
ax.text(-2.15, 1.85, "$\\gamma_w=1$：投影 $=$ 对称读数\n无钟慢，无双生子分歧",
        fontsize=11)
ax.legend(loc="lower left", fontsize=9.5, framealpha=0.96)

plt.tight_layout()
plt.savefig("twins-galilean-compare.png", dpi=200, facecolor="white")
print("saved twins-galilean-compare.png")
