# -*- coding: utf-8 -*-
"""
第 14 章配图：地球版双生子，在两支公设下的世界线对照。

同一个设定：弟弟留在 x=0，哥哥以 v 飞离到 d 后折返，在 R 重逢（v=0.6, T=100, d=30）。
  左 K=c   : 纸面长度与线长分离；两条世界线线长不同（100 与 80）
  右 K=oo  : 等长线成为水平直线；两条世界线线长相同（都是 100）
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sympy as sp

# ------------------------------------------------------------------ 符号核验
K, v = sp.symbols("K v", positive=True)
gam = 1 / sp.sqrt(1 - v ** 2 / K ** 2)
print("gamma(K) =", gam, "   K -> oo :", sp.limit(gam, K, sp.oo))

vn = 0.6                 # c = 1
T = 100.0                # 地球系往返总时间
d = vn * T / 2           # 单程距离 30

euclid_bro = 2 * np.hypot(T / 2, d)              # 纸面长度
mink_bro_c = 2 * np.sqrt((T / 2) ** 2 - d ** 2)  # 线长（K=c）
print("弟弟：纸面 %.1f，线长(K=c) %.1f，线长(K=oo) %.1f" % (T, T, T))
print("哥哥：纸面 %.1f，线长(K=c) %.1f，线长(K=oo) %.1f" % (euclid_bro, mink_bro_c, T))

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

BLUE, RED, GREY = "#1f6fb5", "#c0392b", "#7f7f7f"

fig, axes = plt.subplots(1, 2, figsize=(12.4, 6.8))


def frame(ax, title):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-9, 38)
    ax.set_ylim(-9, 114)
    ax.set_title(title, fontsize=13)
    ax.annotate("", xy=(0, 110), xytext=(0, -6),
                arrowprops=dict(arrowstyle="-|>", color="k", lw=1.25), zorder=3)
    ax.annotate("", xy=(36, 0), xytext=(-6, 0),
                arrowprops=dict(arrowstyle="-|>", color="k", lw=1.25), zorder=3)
    ax.text(1.2, 109, "$t$", fontsize=13)
    ax.text(34.6, -5.5, "$x$", fontsize=13)
    ax.plot([0, 0], [0, T], "-", color=BLUE, lw=2.4, zorder=4)
    ax.plot([0, d, 0], [0, T / 2, T], "-", color=RED, lw=2.4, zorder=4)
    ax.text(-1.2, 70, "弟弟", fontsize=12, color=BLUE, ha="right")
    ax.text(d + 1.4, 46, "哥哥", fontsize=12, color=RED)
    ax.text(-1.4, -4.0, "$O$", fontsize=12)
    ax.text(2.0, 106, "$R$", fontsize=12)
    ax.plot([0], [T], "o", color="k", ms=8, zorder=6)


# ============================================================ 左：K = c
ax = axes[0]
frame(ax, "$K=c$：两条世界线的线长不同")
ax.text(14, 96, "弟弟：线长 $100$\n哥哥：纸面 $116.6$，线长 $80$",
        fontsize=11.5, color="0.15")
ax.text(13, 16, "纸面更长的一条，\n线长反而更短", fontsize=11.5, color="0.15")
ax.text(14, 5, "线长 $=\\int\\!\\sqrt{\\mathrm{d}t^2-\\mathrm{d}x^2/c^2}$",
        fontsize=11, color="0.25")

# ============================================================ 右：K = 无穷
ax = axes[1]
frame(ax, "$K=\\infty$：两条世界线的线长相同")
for tt in [25.0, 50.0, 75.0, 100.0]:
    ax.plot([-5.5, 34.5], [tt, tt], "--", color=GREY, lw=1.1, zorder=1)
    ax.text(35.2, tt, "%d" % int(tt), fontsize=11, va="center", color="0.25")
for tt, xg in [(25.0, vn * 25.0), (50.0, d), (75.0, vn * 25.0)]:
    ax.plot([0], [tt], "o", color=BLUE, ms=6, zorder=5)
    ax.plot([xg], [tt], "o", color=RED, ms=6, zorder=5)
ax.plot([-5.5, 34.5], [50.0, 50.0], "--", color=GREY, lw=1.8, zorder=1,
        label="等长线（水平线）")
ax.text(14, 90, "弟弟：线长 $100$\n哥哥：线长 $100$", fontsize=11.5, color="0.15")
ax.text(13, 14, "每条水平线上，两人线长相同", fontsize=11.5, color="0.15")
ax.text(14, 4, "线长 $=\\int\\!\\mathrm{d}t=\\Delta t$（与形状无关）",
        fontsize=11, color="0.25")
ax.text(8.5, 42.5, "等长线（水平线）", fontsize=10.5, color=GREY)

plt.tight_layout()
plt.savefig("twins-earth-two-branches.png", dpi=200, facecolor="white")
print("saved twins-earth-two-branches.png")
