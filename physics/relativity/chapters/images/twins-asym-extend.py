# -*- coding: utf-8 -*-
"""
第 14 章配图（方式一）：速率不变、飞行距离变长。
三次飞行 v=0.6（c=1，gamma=1.25）不变，t1=5/10/20，即 tbl-at-scan 的三行。
转向事件 Q 沿外出直线外移 (3,5)->(6,10)->(12,20)，重逢事件 M=10/20/40；
以各 M 为心、过该次 Q 的校验线与 t 轴的交点 = 6/12/24，tau=t1/gamma=4/8/16，
长度差 = 交点 - s = 2t1(1-1/gamma) = 2/4/8。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

for f, s in (("font.sans-serif", ["Microsoft YaHei", "SimHei", "DejaVu Sans"]),
             ("axes.unicode_minus", False)):
    plt.rcParams[f] = s

BLUE, RED, GREEN, GREY = "#1f4e79", "#b03a2e", "#2e7d32", "#666666"
v, gam = 0.6, 1.25

trips = [dict(idx=1, t1=5.0,  col=BLUE),
         dict(idx=2, t1=10.0, col=RED),
         dict(idx=3, t1=20.0, col=GREEN)]
for tr in trips:
    tr["Q"] = (v * tr["t1"], tr["t1"])   # 转向事件
    tr["M"] = 2 * tr["t1"]               # 重逢事件高度
    tr["tau"] = tr["t1"] / gam           # 外出段线长 = 返程段线长（速率不变）
    tr["cut"] = tr["M"] - tr["tau"]      # 校验线（以 M 为心、过 Q）与 t 轴的交点
    tr["diff"] = tr["cut"] - tr["tau"]   # 长度差

fig, ax = plt.subplots(figsize=(9.6, 8.4))
ax.axhline(0, color="#bbbbbb", lw=0.8)
ax.axvline(0, color="#555555", lw=1.4)

# 外出段：速率相同，三次共用同一条直线，只画一次
ax.plot([0, v * trips[-1]["t1"]], [0, trips[-1]["t1"]], color="#888888", lw=2.0)
ax.annotate("外出段（速率 0.6 不变，\n三次共用同一条直线）",
            (0.75 * v * trips[-1]["t1"], 0.75 * trips[-1]["t1"]),
            textcoords="offset points", xytext=(12, -20),
            color=GREY, fontsize=10.5)

for tr in trips:
    Qx, Qt = tr["Q"]
    col, i = tr["col"], tr["idx"]
    ax.plot([Qx, 0], [Qt, tr["M"]], color=col, lw=1.9)          # 返程惯性段
    ax.plot(0, tr["M"], "o", color=col, ms=7, zorder=6)
    x = np.linspace(0, 12.6, 500)                                # 校验线（下支）
    t = tr["M"] - np.sqrt(tr["tau"] ** 2 + x ** 2)
    m = t >= -0.2
    ax.plot(x[m], t[m], color=col, lw=2.1, ls="--")
    ax.plot(*tr["Q"], "o", color=col, ms=7, zorder=6)
    ax.plot(0, tr["cut"], "s", color=col, ms=8, zorder=6)        # 交点
    ax.plot([-0.18, -0.18], [tr["tau"], tr["cut"]], color=col, lw=3.0)  # 缺口
    ax.plot([-0.3, 0.3], [tr["tau"], tr["tau"]], color=col, lw=1.5)

    ax.annotate(rf"$\tau_{i}={tr['tau']:.0f}$", (0, tr["tau"]),
                textcoords="offset points", xytext=(-14, -4),
                ha="right", color=col, fontsize=11)
    ax.annotate(rf"交点 ${tr['cut']:.0f}$", (0, tr["cut"]),
                textcoords="offset points", xytext=(-40, -4),
                ha="right", color=col, fontsize=11)
    ax.annotate(rf"$M_{i}={tr['M']:.0f}$", (0, tr["M"]),
                textcoords="offset points", xytext=(-84, -4),
                ha="right", color=col, fontsize=11)
    ax.annotate(rf"$Q_{i}$", tr["Q"], textcoords="offset points",
                xytext=(9, -13), color=col, fontsize=11.5)

ax.annotate("O", (0, 0), textcoords="offset points", xytext=(-13, -7),
            color="#333333", fontsize=12)

ax.text(4.6, 41.6,
        "飞行距离 $t_1$ 变长、速率不变：\n"
        "$Q$ 沿外出直线外移 $(3,5)\\to(6,10)\\to(12,20)$\n"
        "交点随之上移：$6\\to12\\to24$\n"
        "$s$ 也上移：$4\\to8\\to16$\n\n"
        "长度差 $=$ 交点 $-\ s$：\n"
        "$6-4=2$，$12-8=4$，$24-16=8$\n"
        "即 $2t_1(1-1/\\gamma)$，随惯性飞行变长而变大",
        fontsize=11, color="0.15", va="top",
        bbox=dict(boxstyle="round,pad=0.45", fc="#f4f0fa", ec=GREEN, lw=0.9))

ax.set_xlim(-6.2, 13.2)
ax.set_ylim(-1.5, 43)
ax.set_xlabel("x")
ax.set_ylabel("t")
ax.set_title("速率不变、飞行距离变长：三次飞行各有自己的 $Q$ 与自己的校验线\n"
             "交点上移，交点与 $s$ 之间的缺口就是长度差", fontsize=12.5)
fig.tight_layout()
fig.savefig("twins-asym-extend.png", dpi=200, facecolor="white")
for tr in trips:
    print(f"t1={tr['t1']:>4.0f}  Q={tr['Q']}  M={tr['M']:>4.0f}  tau={tr['tau']:>4.0f}  "
          f"交点={tr['cut']:>4.0f}  差={tr['diff']:>4.0f}")
print("saved")
