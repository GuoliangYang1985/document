# -*- coding: utf-8 -*-
"""
第 14 章配图：把两刀落在转向段的两端（A 视角纸面）。

本图是第 14 章切割构造唯一的配图：两刀落在转向段两端，中间段就是转向段本身，
惯性段对惯性段、转向段对转向段，两侧对应段的线长各自相等。

K=c 支：切点线长为 0.8（= 段 I 的线长），双曲线参数 0.8：
        E_A=(1,-0.6)、E_B=(1,0.6)，核对 1^2-0.6^2=0.64=0.8^2；
        F_A=(3,-0.6)、F_B=(3,0.6)，核对 (4-3)^2-0.6^2=0.64。
K=oo 支：切点为 t=1 与 t=3（该支线长即 t 之差，段 I 的线长为 1）。

字母：A 的转向段两端为 S（下，线长 0.8）与 P（上，线长 2.6725）；
      B 的转向段两端为 S'（下）与 Q（上）。

B 的像上的两个方形标记：位于 (x_A, tau_A) = (0.7059, 0.8) 与 (0.7059, 2.6725)，
那里 B 仍在匀速运动；折角来自 A 自己的坐标构造——A 的加速度在这两个线长处
由 0 跳变到非零、再由非零跳回 0（本算例的加速度是分段常数），A 的同时面族
倾角随之突变。折角属于 A，不属于 B。x_A 的解析值 = 1.5 * 0.8 / 1.7 = 0.7059。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scipy.interpolate as si
from scipy.optimize import brentq
from matplotlib.lines import Line2D

for f, s in (("font.sans-serif", ["Microsoft YaHei", "SimHei", "DejaVu Sans"]),
             ("axes.unicode_minus", False)):
    plt.rcParams[f] = s

BLUE, RED, GREEN, GREY, BLACK = "#1f4e79", "#b03a2e", "#2e7d32", "#666666", "#111111"
ORANGE = "#e08214"

# ================================================== A 的轨迹（显式算例, c=1）
def A_x(t):
    if t <= 1: return -0.6 * t
    if t <= 3: return 0.3 * t * t - 1.2 * t + 0.3
    return 0.6 * t - 2.4

def A_v(t):
    if t <= 1: return -0.6
    if t <= 3: return 0.6 * t - 1.2
    return 0.6

ts = np.linspace(0, 4, 8001)
vs = np.array([A_v(t) for t in ts])
dtau = 0.5 * (np.sqrt(1 - vs[1:] ** 2) + np.sqrt(1 - vs[:-1] ** 2)) * np.diff(ts)
taus = np.concatenate([[0], np.cumsum(dtau)])

TAU_M = float(taus[-1])
TAU_1 = float(np.interp(1, ts, taus))       # 段 I 末端（= 变速段起点）
TAU_2 = float(np.interp(3, ts, taus))       # 变速段末端（= 段 III 起点）
X_KINK = 1.5 * TAU_1 / 1.7                  # 折角处的 x_A（解析值）
print("核验0: tau(1)=%.4f tau(3)=%.4f tau(4)=%.6f" % (TAU_1, TAU_2, TAU_M))
print("核验1: 中间段线长 = %.4f（应等于段 II 的 1.8725）" % (TAU_M - TAU_1 - TAU_1))
print("核验2: 折角位置 (%s, %s) 与 (%s, %s)" %
      (round(X_KINK, 4), round(TAU_1, 4), round(X_KINK, 4), round(TAU_2, 4)))

theta_of_tau = si.interp1d(taus, np.arctanh(vs))
T_of_tau = si.interp1d(taus, ts)
X_of_tau = si.interp1d(taus, [A_x(t) for t in ts])
a_of_tau = si.interp1d(0.5 * (taus[:-1] + taus[1:]),
                       np.diff(np.arctanh(vs)) / np.diff(taus))

def _root(t, x, lo, hi):
    return brentq(lambda u: (t - float(T_of_tau(u))) * np.cosh(float(theta_of_tau(u)))
                  - (x - float(X_of_tau(u))) * np.sinh(float(theta_of_tau(u))), lo, hi)

def fermi_solve(t, x):
    tt = taus[1:-1]
    th = theta_of_tau(tt); T = T_of_tau(tt); X = X_of_tau(tt)
    F = (t - T) * np.cosh(th) - (x - X) * np.sinh(th)
    F[np.abs(F) < 1e-11] = 0.0
    s = np.sign(F)
    cross = np.where(s[:-1] * s[1:] < 0)[0]
    zero = np.where(s == 0)[0]
    roots = []
    for i in cross:
        roots.append(_root(t, x, tt[i], tt[i + 1]))
    for i in zero:
        lo = max(tt[max(i - 1, 0)], 1e-9); hi = min(tt[min(i + 1, len(tt) - 1)], taus[-1] - 1e-9)
        roots.append(_root(t, x, lo, hi))
    roots.sort()
    uniq = []
    for r in roots:
        if not uniq or r - uniq[-1] > 1e-6:
            uniq.append(r)
    if len(uniq) != 1: return None
    tau = uniq[0]
    xA = (x - float(X_of_tau(tau))) / np.cosh(float(theta_of_tau(tau)))
    if 1 + float(a_of_tau(min(max(tau, taus[1]), taus[-2]))) * xA <= 0: return None
    return tau, xA

def curve_to_A(pair_t, pair_x):
    out_t, out_x = [], []
    for t, x in zip(pair_t, pair_x):
        r = fermi_solve(t, x)
        out_t.append(r[0] if r else np.nan)
        out_x.append(r[1] if r else np.nan)
    return np.array(out_t), np.array(out_x)

# ================================================== 切点与核验
print("=== 核验 3：四个切点的 A 视角坐标（线长应两两相同）===")
pts = {}
for nm, t, x in [("E_A", 1.0, -0.6), ("E_B", 1.0, 0.6),
                 ("F_A", 3.0, -0.6), ("F_B", 3.0, 0.6)]:
    r = fermi_solve(t, x)
    pts[nm] = r
    print("  %-4s (t=%.1f, x=%+.1f) -> (tau_A=%.4f, x_A=%+.4f)" % (nm, t, x, r[0], r[1]))
print("  E 两点线长之和应对称：tau(E_A)+tau(F_A)=%.4f（总线长 %.4f）"
      % (pts["E_A"][0] + pts["F_A"][0], TAU_M))
print("  E 两点 x_A 之和应为 0：%.6f；F 两点：%.6f"
      % (pts["E_A"][1] + pts["E_B"][1], pts["F_A"][1] + pts["F_B"][1]))

# ================================================== 曲线数据
ts_B = np.linspace(0, 4, 700)
tB_img, xB_img = curve_to_A(ts_B, -np.array([A_x(t) for t in ts_B]))
tB_img[0], xB_img[0] = 0.0, 0.0
tB_img[-1], xB_img[-1] = TAU_M, 0.0
tau_B_pts = np.interp(ts_B, ts, taus)

x_hi = 0.62
x_lo1 = np.linspace(-x_hi, x_hi, 320)
L1_t, L1_x = curve_to_A(np.sqrt(0.64 + x_lo1 ** 2), x_lo1)
L2_t, L2_x = curve_to_A(4 - np.sqrt(0.64 + x_lo1 ** 2), x_lo1)

ts_inf = np.linspace(0, 4, 500)
xB_inf = -2 * np.array([A_x(t) for t in ts_inf])

# ================================================== 图（1x2，都是 A 视角）
fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.9))

def split_plot(ax, X, T, mask, color, lw, label=None, z=4):
    """把被 mask 挖去的曲线分成两段画，避免前后段之间出现假的连线。"""
    idx = np.where(mask)[0]
    ax.plot(X[:idx[0]], T[:idx[0]], color=color, lw=lw, zorder=z, label=label)
    ax.plot(X[idx[-1] + 1:], T[idx[-1] + 1:], color=color, lw=lw, zorder=z)

def band(ax, lo, hi):
    ax.plot([0, 0], [lo, hi], color=ORANGE, lw=7, alpha=0.35,
            solid_capstyle="butt", zorder=2)

def corners(ax):
    for tv in (TAU_1, TAU_2):
        ax.plot([X_KINK], [tv], "s", ms=6.5, mfc="none", mec=GREY, mew=1.4, zorder=6)

def panel_c(ax):
    ax.plot([0, 0], [0, TAU_M], color=BLUE, lw=2.8, zorder=4)
    band(ax, TAU_1, TAU_2)
    mask_mid = (tau_B_pts > TAU_1 + 1e-6) & (tau_B_pts < TAU_2 - 1e-6)
    split_plot(ax, xB_img, tB_img, mask_mid, RED, 2.4)
    ax.plot(xB_img[mask_mid], tB_img[mask_mid], color=ORANGE, lw=4.2,
            ls=(0, (5, 1.6, 1.2, 1.6)), zorder=5)
    ax.plot(L1_x, L1_t, "--", color=GREEN, lw=1.8, zorder=3)
    ax.plot(L2_x, L2_t, "--", color=GREEN, lw=1.8, zorder=3)
    corners(ax)
    for k in ["E_A", "E_B", "F_A", "F_B"]:
        tau, xA = pts[k]
        ax.plot([xA], [tau], "o", color=GREEN, ms=7.5, zorder=6)
    # 字母：A 的转向段两端 S、P；B 的转向段两端 S'、Q
    ax.text(-0.11, 0.86, "$S$", fontsize=13, color=BLACK, ha="right", va="center", zorder=6)
    ax.text(-0.11, 2.62, "$P$", fontsize=13, color=BLACK, ha="right", va="center", zorder=6)
    ax.text(1.44, 1.17, "$S'$", fontsize=13, color=BLACK, ha="left", va="center", zorder=6)
    ax.text(1.44, 2.30, "$Q$", fontsize=13, color=BLACK, ha="left", va="center", zorder=6)
    ax.text(-0.44, (TAU_1 + TAU_2) / 2, "A 的变速段", fontsize=8.8, color="#8a5a00",
            rotation=90, ha="center", va="center")
    ax.annotate("线长 $s_1=0.8$\n两侧相同", xy=pts["E_B"],
                xytext=(1.45, 0.66), fontsize=9.5, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.1))
    ax.annotate("线长 $s_2=0.8$\n两侧相同", xy=pts["F_B"],
                xytext=(1.45, 2.78), fontsize=9.5, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.1))
    ax.text(0.40, 1.72, "B 的变速段\n线长 $0.8\to 2.6725$", fontsize=9.5,
            color=GREY, ha="left")
    ax.text(1.45, 0.30, "方形：B 的像上的折角\n（见讨论）", fontsize=9, color=GREY, ha="left")
    ax.set_xlim(-0.55, 2.35); ax.set_ylim(-0.15, 3.72)

def panel_inf(ax):
    ax.plot([0, 0], [0, 4.0], color=BLUE, lw=2.8, zorder=4)
    band(ax, 1.0, 3.0)
    mask_mid = (ts_inf > 1.0 + 1e-9) & (ts_inf < 3.0 - 1e-9)
    split_plot(ax, xB_inf, ts_inf, mask_mid, RED, 2.4)
    ax.plot(xB_inf[mask_mid], ts_inf[mask_mid], color=ORANGE, lw=4.2,
            ls=(0, (5, 1.6, 1.2, 1.6)), zorder=5)
    xE = -2 * float(A_x(1.0))
    for tv in (1.0, 3.0):
        ax.plot([-0.55, 2.35], [tv, tv], "--", color=GREEN, lw=1.8, zorder=3)
        for xv in (xE, 0.0):
            ax.plot([xv], [tv], "o", color=GREEN, ms=7.5, zorder=6)
    ax.text(-0.11, 1.08, "$S$", fontsize=13, color=BLACK, ha="right", va="center", zorder=6)
    ax.text(-0.11, 2.92, "$P$", fontsize=13, color=BLACK, ha="right", va="center", zorder=6)
    ax.text(1.44, 1.12, "$S'$", fontsize=13, color=BLACK, ha="left", va="center", zorder=6)
    ax.text(1.44, 2.92, "$Q$", fontsize=13, color=BLACK, ha="left", va="center", zorder=6)
    ax.text(-0.44, 2.00, "A 的变速段", fontsize=8.8, color="#8a5a00",
            rotation=90, ha="center", va="center")
    ax.annotate("线长 $s_1=1.0$\n两侧相同", xy=(-xE / 2, 1.0 + 0.02),
                xytext=(1.45, 0.55), fontsize=9.5, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.1))
    ax.annotate("线长 $s_2=1.0$\n两侧相同", xy=(-xE / 2, 3.0 - 0.02),
                xytext=(1.45, 3.42), fontsize=9.5, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.1))
    ax.text(0.40, 1.98, "B 的变速段\n线长 $1.0\to 3.0$", fontsize=9.5,
            color=GREY, ha="left")
    ax.text(1.45, 0.24, "这一支没有这种\n折角", fontsize=9, color=GREY, ha="left")
    ax.set_xlim(-0.55, 2.35); ax.set_ylim(-0.15, 4.15)

panel_c(axes[0]); panel_inf(axes[1])
for ax, ttl in zip(axes, ["$K=c$：刀落在转向段两端", "$K=\\infty$：刀落在转向段两端"]):
    ax.set_title(ttl, fontsize=12.5)
    ax.set_xlabel("$x_A$（A 自己的空间坐标）", fontsize=11)
    ax.set_ylabel("$\\tau_A$（A 自己的线长坐标）", fontsize=11)
    ax.grid(alpha=0.18)
handles = [
    Line2D([0], [0], color=BLUE, lw=2.8, label="$\\gamma_A$（纵轴 $=0$）"),
    Line2D([0], [0], color=RED, lw=2.4, label="$\\gamma_B$ 的像"),
    Line2D([0], [0], color=ORANGE, lw=4.0, ls=(0, (5, 1.6, 1.2, 1.6)),
           label="B 的变速段（两侧线长相同）"),
    Line2D([0], [0], color=GREEN, lw=1.8, ls="--", label="等线长线（校验线）"),
    Line2D([0], [0], marker="s", ms=6.5, mfc="none", mec=GREY, mew=1.4, lw=0,
           label="折角处（B 仍匀速）"),
]
fig.legend(handles=handles, loc="lower center", ncol=5, fontsize=9.8,
           frameon=False, bbox_to_anchor=(0.5, -0.004))
fig.tight_layout(rect=(0, 0.07, 1, 1))
fig.savefig("twins-calibration-cut-ends.png", dpi=155)
print("  已输出 twins-calibration-cut-ends.png（1x2，A 视角）")
