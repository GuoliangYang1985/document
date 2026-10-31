# -*- coding: utf-8 -*-
"""
第 13 章配图：对称双生子的闵氏几何图（三视角对照）。

左：A 视角（A 静止，B 以相对速度 w 向 -x 运动）
中：B 视角（身份互换的镜像）
右：地球视角（本章的镜像对称系：A、B 各以 ±v 运动）

统一结论：等线长点的轨迹是校准双曲线 t^2 - x^2/K^2 = s_0^2，不是欧氏圆。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sympy as sp

# ------------------------------------------------------------------ 符号核验
K, w, tau = sp.symbols("K w tau", positive=True)
gw = 1 / sp.sqrt(1 - w ** 2 / K ** 2)

# 对称点：B 读 tau 的事件在 A 系中的坐标时
t_s = gw * tau
x_s = -w * gw * tau
print("核验 1 对称点在等线长双曲线上 t^2-x^2/K^2=s_0^2:",
      sp.simplify(t_s ** 2 - x_s ** 2 / K ** 2 - tau ** 2) == 0)
print("核验 2 对称点处 B 的线长 = tau:",
      sp.simplify(t_s * sp.sqrt(1 - w ** 2 / K ** 2) - tau) == 0)
# 圆弧（欧氏圆）交点的线长
t_c = tau / sp.sqrt(1 + w ** 2 / K ** 2)
print("核验 3 圆弧交点处 B 的线长 = tau*sqrt((1-w^2/K^2)/(1+w^2/K^2)):",
      sp.simplify(t_c * sp.sqrt(1 - w ** 2 / K ** 2)
                  - tau * sp.sqrt((1 - w ** 2 / K ** 2) / (1 + w ** 2 / K ** 2))) == 0)
# 伽利略极限
print("核验 4 伽利略极限 K->oo: gamma_w ->",
      sp.limit(gw, K, sp.oo), "；等线长曲线 t^2-x^2/K^2=s_0^2 -> t^2=tau^2")

# ------------------------------------------------------------------ 数值参数
vn = 0.6                                   # 地球系中 A、B 各自速率（c=1）
gv = 1 / np.sqrt(1 - vn ** 2)              # 1.25
wn = 2 * vn / (1 + vn ** 2)                # 0.8823529
gwn = (1 + vn ** 2) / (1 - vn ** 2)        # 2.125
print("v=%.4f  w=%.4f  gamma_v=%.4f  gamma_w=%.4f" % (vn, wn, gv, gwn))

# 地球视角下「A 系配对」给出的线长增量比（含出发间隔 d 的偏移项）
rv = sp.Rational(3, 5)                       # v = 0.6c
ts_, ds_ = sp.symbols("t d", positive=True)
r_lim = (ts_ * (1 - rv ** 2) + 2 * rv * ds_) / (ts_ * (1 + rv ** 2))
print("地球视角 A 系配对的增量比（有限 t）:", sp.simplify(r_lim))
print("  t->oo 极限 =", sp.limit(r_lim, ts_, sp.oo),
      "；1/gamma_w =", sp.Rational(1, 1) * (1 - rv ** 2) / (1 + rv ** 2))

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

BLUE, RED, GREEN = "#1f6fb5", "#c0392b", "#2e8b57"
fig, axes = plt.subplots(1, 3, figsize=(15.0, 5.6))


def frame(ax, title, xlim, ylim, xlab="$x$", ylab="$t$", cone=True):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_title(title, fontsize=12.5)
    ax.annotate("", xy=(0, ylim[1] * 0.97), xytext=(0, ylim[0] + 0.12),
                arrowprops=dict(arrowstyle="-|>", color="k", lw=1.25), zorder=3)
    ax.annotate("", xy=(xlim[1] * 0.93, 0), xytext=(xlim[0] + 0.12, 0),
                arrowprops=dict(arrowstyle="-|>", color="k", lw=1.25), zorder=3)
    ax.text(0.10, ylim[1] * 0.955, ylab, fontsize=12)
    ax.text(xlim[1] * 0.90, -0.16, xlab, fontsize=12)
    if cone:
        L = max(ylim[1], abs(xlim[0]))
        ax.plot([0, L], [0, L], color="0.88", lw=0.8, zorder=0)
        ax.plot([0, -L], [0, L], color="0.88", lw=0.8, zorder=0)


# ================================================================= 左：A 视角
ax = axes[0]
frame(ax, "A 视角（A 静止，B 以 $w$ 运动）", (-2.35, 1.05), (-0.45, 2.55))

# B 世界线
tt = np.linspace(0, 2.40, 50)
ax.plot(-wn * tt, tt, "-", color="k", lw=1.6, zorder=3)
ax.annotate("", xy=(-wn * 2.40, 2.40), xytext=(-wn * 2.30, 2.30),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.4), zorder=3)
ax.text(-wn * 2.40 - 0.30, 2.34, "$B$", fontsize=12)

# 等线长双曲线
tt = np.linspace(1.0, 2.30, 400)
ax.plot(-np.sqrt(tt ** 2 - 1), tt, "--", color=BLUE, lw=1.9, zorder=2,
        label="等线长轨迹 $t^2-x^2/K^2=s_0^2$")

# A 系同时线（水平）
ax.plot([-wn * gwn, 0.05], [gwn, gwn], "--", color=RED, lw=1.2, zorder=2,
        label="本系同时线（水平）")
ax.plot([-wn, 0.05], [1.0, 1.0], "--", color=RED, lw=1.2, zorder=2)

ax.plot(0, 1, "o", color="k", ms=6, zorder=5)
ax.plot(-wn * gwn, gwn, "o", color=RED, ms=6, zorder=5)
ax.plot(0, gwn, "s", color=RED, mfc="white", mec=RED, ms=7, zorder=5)
ax.plot(-wn, 1.0, "o", mfc="white", mec="0.35", ms=6.5, zorder=5)

ax.text(0.10, 0.80, "$M_t$：A 侧累积 $s_0$", fontsize=11)
ax.text(-0.06, 2.14, "$M'$：该处累积 $=2.125\,s_0$", fontsize=11, color=RED, ha="right")
ax.text(-wn * gwn - 0.06, gwn - 0.20, "$M_{t'}$：B 侧累积 $s_0$",
        fontsize=11, color=RED, ha="right")
ax.text(-wn - 0.08, 0.72, "B 侧累积 $0.47s_0$", fontsize=10.5,
        color="0.30", ha="right")
ax.text(-0.17, -0.20, "$O$", fontsize=11)

# ================================================================= 中：B 视角
ax = axes[1]
frame(ax, "B 视角（B 静止，A 以 $w$ 运动）", (-1.05, 2.35), (-0.45, 2.55))

tt = np.linspace(0, 2.40, 50)
ax.plot(wn * tt, tt, "-", color="k", lw=1.6, zorder=3)
ax.annotate("", xy=(wn * 2.40, 2.40), xytext=(wn * 2.30, 2.30),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.4), zorder=3)
ax.text(wn * 2.40 + 0.10, 2.34, "$A$", fontsize=12)

tt = np.linspace(1.0, 2.30, 400)
ax.plot(np.sqrt(tt ** 2 - 1), tt, "--", color=BLUE, lw=1.9, zorder=2)

ax.plot([-0.05, wn * gwn], [gwn, gwn], "--", color=GREEN, lw=1.2, zorder=2)
ax.plot([-0.05, wn], [1.0, 1.0], "--", color=GREEN, lw=1.2, zorder=2)

ax.plot(0, 1, "o", color="k", ms=6, zorder=5)
ax.plot(wn * gwn, gwn, "o", color=GREEN, ms=6, zorder=5)
ax.plot(0, gwn, "s", color=GREEN, mfc="white", mec=GREEN, ms=7, zorder=5)
ax.plot(wn, 1.0, "o", mfc="white", mec="0.35", ms=6.5, zorder=5)

ax.text(-0.10, 0.80, "$M_t$：B 侧累积 $s_0$", fontsize=11, ha="right")
ax.text(-0.10, 2.14, "$M'$：该处累积 $=2.125\,s_0$", fontsize=11,
        color=GREEN, ha="right")
ax.text(wn * gwn + 0.06, gwn - 0.20, "$M_{t'}$：A 侧累积 $s_0$",
        fontsize=11, color=GREEN)
ax.text(wn + 0.08, 0.72, "A 侧累积 $0.47s_0$", fontsize=10.5, color="0.30")
ax.text(0.05, -0.20, "$O$", fontsize=11)

# ============================================================== 右：地球视角
ax = axes[2]
d = 1.0
tM = d / vn                                 # 1.6667
tt = np.linspace(0, tM, 60)
ax.plot(-d + vn * tt, tt, "-", color="k", lw=1.6, zorder=3, label="A 的世界线")
ax.plot(d - vn * tt, tt, "-", color="k", lw=1.6, zorder=3, label="B 的世界线")

t0 = 0.8
xA, xB = -d + vn * t0, d - vn * t0          # -0.52, +0.52
# A 系同时线：dt/dx = v ；与 B 世界线交于 tBp
tBp = (t0 * (1 - vn ** 2) + 2 * vn * d) / (1 + vn ** 2)
xBp = d - vn * tBp
# 以 P、Q 为心的等线长双曲线（增量 s = t0/gamma_v）
s = t0 / gv                                 # 0.64
tp = np.linspace(s, s * 1.42, 300)
ax.plot(-d + np.sqrt(tp ** 2 - s ** 2), tp, "--", color=BLUE, lw=1.6, zorder=2)
ax.plot(d - np.sqrt(tp ** 2 - s ** 2), tp, "--", color=BLUE, lw=1.6, zorder=2)

frame(ax, "地球视角（镜像对称系，A、B 各以 $\\pm v$ 运动）",
      (-1.45, 1.45), (-0.35, 2.05), cone=False)
ax.plot([xA, xB], [t0, t0], "-", color="k", lw=1.1, zorder=2)
ax.plot([xA, xBp], [t0, tBp], "--", color=RED, lw=1.2, zorder=2,
        label="A 系同时线（倾斜）")

ax.plot(xA, t0, "o", color="k", ms=6, zorder=5)
ax.plot(xB, t0, "o", color="k", ms=6, zorder=5)
ax.plot(xBp, tBp, "s", color=RED, mfc="white", mec=RED, ms=7, zorder=5)
ax.plot(-d, 0, "o", color="k", ms=5, zorder=5)
ax.plot(d, 0, "o", color="k", ms=5, zorder=5)
ax.plot(0, tM, "o", color="k", ms=5, zorder=5)

ax.text(-d - 0.06, -0.20, "$P$", fontsize=11)
ax.text(d + 0.02, -0.20, "$Q$", fontsize=11)
ax.text(0.05, tM + 0.04, "$M$", fontsize=11)
ax.text(0.0, t0 + 0.06, "对称对（水平）", fontsize=10.5, ha="center")
ax.text(xBp + 0.14, tBp - 0.34, "A 的配对", fontsize=10.5, color=RED, ha="left")
ax.text(-d - 0.30, 1.30, "A 线长增量 $=t/\\gamma_v$", fontsize=10.5)
ax.text(d + 0.05, 1.30, "B 线长增量 $=t/\\gamma_v$", fontsize=10.5)

handles, labels = axes[0].get_legend_handles_labels()
h2, l2 = axes[2].get_legend_handles_labels()
fig.legend(handles + h2[:3], labels + l2[:3], loc="lower center", ncol=3,
           fontsize=10, frameon=False)

plt.tight_layout(rect=(0, 0.10, 1, 1))
plt.savefig("twins-three-views.png", dpi=200, facecolor="white")
print("saved twins-three-views.png")
