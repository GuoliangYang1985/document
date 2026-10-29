# -*- coding: utf-8 -*-
"""
第 14 章配图（方式二）：转向事件 Q 固定，只把重逢事件沿 t 轴推后（返程变慢）。
Q 固定在 (6,10)（t1=10、v=0.6，c=1，tau_Q=8）；
重逢 M=20/30/50，返程速率依次 0.6/0.3/0.15；
返程段读数 L=sqrt((M-tQ)^2-xQ^2)=8.00/19.08/39.55；
以各 M 为心、过同一个 Q 的校验线与 t 轴的交点 = M-L = 12.00/10.92/10.45，
读数差 = 交点 - tau_Q = 4.00/2.92/2.45，随返程拉长而缩小，趋于 t_Q-tau_Q=2。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

for f, s in (("font.sans-serif", ["Microsoft YaHei", "SimHei", "DejaVu Sans"]),
             ("axes.unicode_minus", False)):
    plt.rcParams[f] = s

BLUE, RED, GREEN, GREY = "#1f4e79", "#b03a2e", "#2e7d32", "#666666"

xQ, tQ = 6.0, 10.0
tauQ = 8.0   # 外出段 O->Q 的读数（径向直线）

cases = [("M_1", 20.0, BLUE), ("M_2", 30.0, GREEN), ("M_3", 50.0, RED)]

fig, ax = plt.subplots(figsize=(9.2, 8.0))
ax.axhline(0, color="#bbbbbb", lw=0.8)
ax.axvline(0, color="#555555", lw=1.4)

# 外出段 O -> Q
ax.plot([0, xQ], [0, tQ], color="#888888", lw=2.0)
ax.plot(xQ, tQ, "o", color="#8c1d18", ms=8, zorder=6)
ax.annotate("$Q$ (6, 10) 固定", (xQ, tQ), textcoords="offset points",
            xytext=(10, -24), color="#8c1d18", fontsize=11)

# tau_Q 的刻度（外出段读数）
ax.plot([-0.12, 0.12], [tauQ, tauQ], color="#555555", lw=2.0)
ax.annotate(rf"$\tau_Q={tauQ:.0f}$（外出段读数）", (0, tauQ),
            textcoords="offset points", xytext=(-12, -4), ha="right",
            color="#555555", fontsize=10.5)

for name, tM, col in cases:
    L = np.sqrt((tM - tQ) ** 2 - xQ ** 2)     # 返程段 Q->M 的读数
    cut = tM - L                               # 校验线（以 M 为心、过 Q）与 t 轴的交点
    ax.plot([xQ, 0], [tQ, tM], color=col, lw=1.9)               # 返程惯性段
    ax.plot(0, tM, "o", color=col, ms=7, zorder=6)
    x = np.linspace(0, 10.2, 300)                               # 校验线（下支）
    ax.plot(x, tM - np.sqrt(L ** 2 + x ** 2), color=col, lw=2.1, ls="--")
    ax.plot(0, cut, "s", color=col, ms=8, zorder=6)             # 交点
    ax.annotate(rf"${name}={tM:.0f}$", (0, tM), textcoords="offset points",
                xytext=(9, 5), color=col, fontsize=11.5)
    ax.annotate(rf"$L={L:.2f}$", (xQ / 2, (tQ + tM) / 2),
                textcoords="offset points", xytext=(8, 0), color=col, fontsize=10.5)

ax.annotate("交点 12.00", (0, 12.0), textcoords="offset points",
            xytext=(-10, 4), ha="right", color=BLUE, fontsize=10.5)
ax.annotate("O", (0, 0), textcoords="offset points", xytext=(-12, -8),
            color="#333333", fontsize=12)

ax.text(1.8, 51.4,
        "三条校验线都以落点为心、都过同一个 $Q$：\n"
        "交点 $12.00\\to10.92\\to10.45$\n"
        "落点推高（返程变慢）时交点下移、\n越来越贴近 $t_Q=10$；\n"
        "返程无限慢的极限是交点 $=t_Q$。\n\n"
        "读数差 $=$ 交点 $-\\ \\tau_Q$：\n"
        "$4.00\\to2.92\\to2.45$，随返程拉长而缩小，\n趋于 $t_Q-\\tau_Q=2$",
        fontsize=11, color="0.15", va="top",
        bbox=dict(boxstyle="round,pad=0.45", fc="#f4f0fa", ec=BLUE, lw=0.9))

ax.set_xlim(-4.8, 10.6)
ax.set_ylim(-1.5, 53)
ax.set_xlabel("x")
ax.set_ylabel("t")
ax.set_title("转向事件 $Q$ 固定、重逢事件沿 $t$ 轴推后（返程变慢）\n"
             "过同一个 $Q$ 的三条校验线：交点下移、趋于 $t_Q$，读数差缩小",
             fontsize=12.5)
fig.tight_layout()
fig.savefig("twins-asym-fixq.png", dpi=200, facecolor="white")
for name, tM, col in cases:
    L = np.sqrt((tM - tQ) ** 2 - xQ ** 2)
    print(f"{name}={tM:.0f}  L={L:.2f}  交点={tM-L:.2f}  差={tM-L-tauQ:.2f}")
print("saved")
