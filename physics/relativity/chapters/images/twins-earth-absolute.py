# -*- coding: utf-8 -*-
"""
第 14 章配图：地球版双生子，在绝对时间公设（K = 无穷）下的世界线。

设定：弟弟留在地球（x=0），哥哥以 v 飞离到 d 后折返，在 R 重逢。
K = 无穷 时：
  等读数轨迹   t^2 - x^2/K^2 = tau^2   在 K->oo 时成为水平直线  t = tau
  钟慢因子     gamma(K) = 1/sqrt(1-v^2/K^2) = 1
故两条形状完全不同的世界线，处处读数相同，重逢时同龄。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sympy as sp

# ------------------------------------------------------------------ 符号核验
K, v, tau = sp.symbols("K v tau", positive=True)
gam = 1 / sp.sqrt(1 - v ** 2 / K ** 2)
print("gamma(K)   =", gam)
print("K -> oo    =", sp.limit(gam, K, sp.oo))
print("等读数曲线 t^2 - x^2/K^2 = tau^2 在 K->oo 时成为 t = tau（水平直线）")

# 数值设定
vn = 0.6                 # 飞船速率（c=1）
T = 100.0                # 地球系往返总时间
d = vn * T / 2           # 单程距离 = 30（光年）
print("v=%.2f  往返 T=%.1f  单程距离 d=%.1f  单程用时=%.1f" % (vn, T, d, d / vn))
print("K=c    : 弟弟 %.1f 年，哥哥 %.1f 年（gamma=1.25）" % (T, T / 1.25))
print("K=oo   : 弟弟 %.1f 年，哥哥 %.1f 年（gamma=1）" % (T, T))

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

BLUE, RED, GREY = "#1f6fb5", "#c0392b", "#7f7f7f"

fig, ax = plt.subplots(figsize=(8.2, 7.4))
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(-9, 38)
ax.set_ylim(-9, 112)

# 坐标轴
ax.annotate("", xy=(0, 108), xytext=(0, -6),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.25), zorder=3)
ax.annotate("", xy=(36, 0), xytext=(-6, 0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.25), zorder=3)
ax.text(1.2, 107, "$t$", fontsize=13)
ax.text(35.0, -5.5, "$x$", fontsize=13)

# 等读数线（= 同时线）：水平直线 t = tau
for tt in [25.0, 50.0, 75.0, 100.0]:
    ax.plot([-5.5, 34.5], [tt, tt], "--", color=GREY, lw=1.1, zorder=1)
ax.plot([-5.5, 34.5], [25.0, 25.0], "--", color=GREY, lw=1.6, zorder=1,
        label="等读数线（= 同时线）$t=\\tau$")

# 读数标注（右侧）
for tt in [25.0, 50.0, 75.0, 100.0]:
    ax.text(35.2, tt, "%d" % int(tt), fontsize=11, va="center", color="0.25")

# 弟弟：竖直线
ax.plot([0, 0], [0, T], "-", color=BLUE, lw=2.4, zorder=4, label="弟弟（地球）")
# 哥哥：折线
ax.plot([0, d, 0], [0, T / 2, T], "-", color=RED, lw=2.4, zorder=4, label="哥哥（飞船）")

# 交点
for tt, xg in [(25.0, vn * 25.0), (50.0, d), (75.0, vn * 25.0), (100.0, 0.0)]:
    ax.plot([0], [tt], "o", color=BLUE, ms=6.5, zorder=5)
    if tt < 100.0:
        ax.plot([xg], [tt], "o", color=RED, ms=6.5, zorder=5)
ax.plot([0], [T], "o", color="k", ms=8, zorder=6)

# 文字标注
ax.text(-1.2, 66, "弟弟（地球）", fontsize=11.5, color=BLUE, ha="right")
ax.text(d + 1.4, 47, "哥哥（飞船）", fontsize=11.5, color=RED)
ax.text(-1.2, -4.0, "$O$", fontsize=12)
ax.text(2.0, 104, "$R$ 重逢", fontsize=12)
ax.text(-5.5, 88, "两条世界线在每条水平线上\n读数都相同", fontsize=11.5, color="0.15")
ax.text(-5.5, 8, "$\\gamma=1$：没有钟慢\n哥哥不会更年轻", fontsize=11.5, color="0.15")

ax.legend(loc="lower right", fontsize=10.5, framealpha=0.96)
plt.tight_layout()
plt.savefig("twins-earth-absolute.png", dpi=200, facecolor="white")
print("saved twins-earth-absolute.png")
