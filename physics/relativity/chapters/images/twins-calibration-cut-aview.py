# -*- coding: utf-8 -*-
"""
第 14 章配图（修订版）：校验线切割，画在 **A 视角坐标纸面** 上。

与旧图的根本差别：旧图的轴是 (x, ct)——(M1) 的承载坐标，属于第三方；
本图的横轴是 A 自己的空间坐标 x_A、纵轴是 A 自己的读数坐标 tau_A
（右面板为 B 视角，是左面板的镜像）。

做法：显式算例中 A 的全程 Fermi 坐标数值构造；gamma_B 与两条校验线
逐点解正交方程变换到 A 视角坐标。核验：
  1. gamma_B 的像全程存在（显式算例中 B 全程位于 A 的单射域内）；
  2. 切割点 E_A、E_B、F_A、F_B 的 A 视角坐标与读数；
  3. 两条校验线分别过 (tau_1, 0) 与 (tau_M - sigma_1, 0)。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scipy.interpolate as si
from scipy.optimize import brentq

for f, s in (("font.sans-serif", ["Microsoft YaHei", "SimHei", "DejaVu Sans"]),
             ("axes.unicode_minus", False)):
    plt.rcParams[f] = s

BLUE, RED, GREEN, GREY, BLACK = "#1f4e79", "#b03a2e", "#2e7d32", "#666666", "#111111"

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
print("核验0: tau(1)=%.4f(应0.8) tau(3)=%.4f(应2.6725) tau(4)=%.6f(应3.4725)"
      % (np.interp(1, ts, taus), np.interp(3, ts, taus), taus[-1]))

theta_of_tau = si.interp1d(taus, np.arctanh(vs))
T_of_tau = si.interp1d(taus, ts)
X_of_tau = si.interp1d(taus, [A_x(t) for t in ts])
a_of_tau = si.interp1d(0.5 * (taus[:-1] + taus[1:]),
                       np.diff(np.arctanh(vs)) / np.diff(taus))

def _root(t, x, lo, hi):
    return brentq(lambda u: (t - float(T_of_tau(u))) * np.cosh(float(theta_of_tau(u)))
                  - (x - float(X_of_tau(u))) * np.sinh(float(theta_of_tau(u))), lo, hi)

def fermi_solve(t, x):
    """惯性坐标 (t,x) -> A 视角 (tau_A, x_A)；无解或多解返回 None。"""
    tt = taus[1:-1]
    th = theta_of_tau(tt); T = T_of_tau(tt); X = X_of_tau(tt)
    F = (t - T) * np.cosh(th) - (x - X) * np.sinh(th)
    F[np.abs(F) < 1e-11] = 0.0
    s = np.sign(F)
    cross = np.where(s[:-1] * s[1:] < 0)[0]
    zero = np.where(s == 0)[0]
    roots = []
    step = taus[1] - taus[0]
    for i in cross:
        roots.append(_root(t, x, tt[i], tt[i + 1]))
    for i in zero:                       # 零点恰在网格上：邻域内精化
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

# ================================================== 核验
print("=== 核验 1：gamma_B 的像全程存在？ ===")
miss = [round(t, 3) for t in np.linspace(0, 4, 81) if fermi_solve(t, -A_x(t)) is None]
print("  无解的 t:", miss if miss else "无（B 的像全程存在）")

print("=== 核验 2：切割点与端点 ===")
for name, t, x in [("E_A", 0.5, -0.3), ("E_B", 0.5, 0.3),
                   ("F_A", 3.5, -0.3), ("F_B", 3.5, 0.3),
                   ("O", 0, 0), ("M", 4, 0)]:
    r = fermi_solve(t, x)
    print(f"  {name}: (t={t}, x={x}) -> A 视角 ({r[0]:.4f}, {r[1]:.4f})" if r
          else f"  {name}: 无解")

# 校验线过 γ_A 上的读数点
print("=== 核验 3：校验线在 γ_A 上交于读数点 ===")
print("  tau_1=0.4 处 E_A 的 A 视角时间坐标应为 0.4（见上）")
print("  F_A 的 A 视角时间坐标应为 tau(3.5)=%.4f" % np.interp(3.5, ts, taus))
print("  E_B 的 A 视角时间坐标=%.4f, F_B 的 A 视角时间坐标=%.4f（对称性：二者之和应=tau(4)=%.4f）"
        % (fermi_solve(0.5,0.3)[0], fermi_solve(3.5,0.3)[0], taus[-1]))

# ================================================== 曲线数据
# γ_A 的像 = 纵轴
tau_axis = np.linspace(0, 4, 200)
# γ_B 的像
ts_B = np.linspace(0, 4, 700)
tB_img, xB_img = curve_to_A(ts_B, -np.array([A_x(t) for t in ts_B]))
tB_img[0], xB_img[0] = 0.0, 0.0                     # O
tB_img[-1], xB_img[-1] = float(taus[-1]), 0.0       # M
# 校验线（惯性坐标双曲线，t>0 / t<tM 支）
x_lo1 = np.linspace(-0.45, 0.55, 300)
t_l1 = np.sqrt(0.16 + x_lo1 ** 2)                      # Λ_O: t^2-x^2=0.4^2
L1_t, L1_x = curve_to_A(t_l1, x_lo1)
x_lo2 = np.linspace(-0.45, 0.55, 300)
t_l2 = 4 - np.sqrt(0.16 + x_lo2 ** 2)                  # Λ_M: (4-t)^2-x^2=0.4^2
L2_t, L2_x = curve_to_A(t_l2, x_lo2)

# ================================================== K=oo 支（A 视角解析）
# K=oo：t_A = t，x_A = x - X_A(t)；读数 = t 之差；校验线 = 水平线 t = 常数
def XA(t):
    return A_x(t)

ts_inf = np.linspace(0, 4, 500)
xB_inf = -2 * np.array([XA(t) for t in ts_inf])       # γ_B 的像 x_A = -2 X_A(t)
T1_INF, S1_INF = 0.5, 0.5                             # 切割读数（正文：0.5）

# ================================================== 图（2x2：两支 × 两视角）
fig, axes = plt.subplots(2, 2, figsize=(12.4, 10.4))

def draw_cut(ax, kind="c", mirror=False):
    """kind='c'：K=c 支（数值 Fermi 变换）；kind='inf'：K=oo 支（解析）。"""
    sgn = -1 if mirror else 1
    cA, cB = (RED, BLUE) if mirror else (BLUE, RED)
    xa_lab = "$x_B$（B 自己的空间坐标）" if mirror else "$x_A$（A 自己的空间坐标）"
    tau_lab = "$\\tau_B$（B 自己的读数坐标）" if mirror else "$\\tau_A$（A 自己的读数坐标）"
    labA = "$\\gamma_B$（纵轴 $=0$）" if mirror else "$\\gamma_A$（纵轴 $=0$）"
    labB = "$\\gamma_A$ 的像" if mirror else "$\\gamma_B$ 的像"

    if kind == "c":
        tauM = float(taus[-1]); t1, s1 = 0.4, 0.4
        ax.plot([0, 0], [0, tauM], color=cA, lw=2.6, label=labA, zorder=4)
        ax.plot(sgn * xB_img, tB_img, color=cB, lw=2.6, label=labB, zorder=4)
        tau_B_pts = np.interp(ts_B, ts, taus)
        mask_mid = (tau_B_pts > t1 - 1e-6) & (tau_B_pts < tauM - s1 + 1e-6)
        ax.plot(sgn * xB_img[mask_mid], tB_img[mask_mid], color="#e08214", lw=4.0,
                zorder=3)
        ax.plot([], [], color="#e08214", lw=4.0, label="中间段（两侧读数相同）")
        coords = {"E_A": fermi_solve(0.5, -0.3), "E_B": fermi_solve(0.5, 0.3),
                  "F_A": fermi_solve(3.5, -0.3), "F_B": fermi_solve(3.5, 0.3)}
        # 校验线按全程画出（双曲线的两支都保留），两切割点落在同一条线上
        ax.plot(sgn * L1_x, L1_t, "--", color=GREEN, lw=1.8,
                label="校验线 $\\Lambda_O$、$\\Lambda_M$")
        ax.plot(sgn * L2_x, L2_t, "--", color=GREEN, lw=1.8)
        order = ["E_B", "E_A", "F_B", "F_A"] if mirror else ["E_A", "E_B", "F_A", "F_B"]
        for k in order:
            tau, xA = coords[k]
            ax.plot([sgn * xA], [tau], "o", color=GREEN, ms=7, zorder=6)
        tau_E = coords["E_A"][0]; tau_F = coords["F_A"][0]
        val_E, val_F = t1, tauM - tau_F
        pos_E = (sgn * coords["E_B"][1], coords["E_B"][0])
        pos_F = (sgn * coords["F_B"][1], coords["F_B"][0])
        ax.annotate("读数 $\\tau_1=%.1f$\n两侧相同" % val_E, xy=pos_E,
                    xytext=(-2.10, 0.50) if mirror else (1.45, 0.72), fontsize=10, color=GREEN,
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.1))
        ax.annotate("读数 $\\sigma_1=%.1f$\n两侧相同" % val_F, xy=pos_F,
                    xytext=(-2.10, 3.20) if mirror else (0.72, 3.20), fontsize=10, color=GREEN,
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.1))
        ax.text((-2.10 if mirror else 0.55), 1.95, "中间段读数\n两侧相同",
                fontsize=10, color=GREY, ha="center")
        ax.set_xlim((-2.35, 0.55) if mirror else (-0.55, 2.35)); ax.set_ylim(-0.15, 3.75)
    else:
        tauM = 4.0; t1, s1 = T1_INF, S1_INF
        ax.plot([0, 0], [0, tauM], color=cA, lw=2.6, label=labA, zorder=4)
        ax.plot(sgn * xB_inf, ts_inf, color=cB, lw=2.6, label=labB, zorder=4)
        mask_mid = (ts_inf > t1) & (ts_inf < tauM - s1)
        ax.plot(sgn * xB_inf[mask_mid], ts_inf[mask_mid], color="#e08214", lw=4.0,
                zorder=3)
        ax.plot([], [], color="#e08214", lw=4.0, label="中间段（两侧读数相同）")
        xE = -2 * float(XA(t1))
        # 水平校验线按全程画出（贯穿整个面板），两切割点落在同一条线上
        for tv, lab in [(t1, "$\\Lambda_O:\\ t=%s$（水平线）" % t1),
                        (tauM - s1, "$\\Lambda_M$")]:
            ax.plot((-2.35, 0.55) if mirror else (-0.55, 2.35), [tv, tv], "--",
                    color=GREEN, lw=1.8, label=lab if not mirror else None)
        for tt_, xv_ in [(t1, xE), (tauM - s1, xE)]:
            ax.plot([sgn * xv_, sgn * 0], [tt_, tt_], "o", color=GREEN, ms=7, zorder=6)
        ax.annotate("读数 $\\tau_1=%s$\n两侧相同" % t1, xy=(sgn * xE / 2, t1),
                    xytext=(-2.10, 0.08) if mirror else (1.00, 0.08), fontsize=10, color=GREEN,
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.1))
        ax.annotate("读数 $\\sigma_1=%s$\n两侧相同" % s1, xy=(sgn * xE / 2, tauM - s1),
                    xytext=(-2.10, 3.68) if mirror else (0.70, 3.68), fontsize=10, color=GREEN,
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.1))
        ax.text((-2.10 if mirror else 0.9), 2.0, "中间段读数\n两侧相同",
                fontsize=10, color=GREY, ha="center")
        ax.set_xlim((-2.35, 0.55) if mirror else (-0.55, 2.35)); ax.set_ylim(-0.15, 4.15)

    ax.plot([0], [0], "o", color=BLACK, ms=7, zorder=6)
    ax.plot([0], [tauM], "o", color=BLACK, ms=7, zorder=6)
    ax.text(0.09, 0.03, "$O$", fontsize=12, color=BLACK)
    ax.text(0.09, tauM - 0.24, "$M$", fontsize=12, color=BLACK)
    ax.set_xlabel(xa_lab, fontsize=11)
    ax.set_ylabel(tau_lab, fontsize=11)
    ax.legend(loc="center right" if mirror else "upper right", fontsize=8.5,
              framealpha=1.0)
    ax.grid(alpha=0.18)

draw_cut(axes[0][0], kind="c", mirror=False)
draw_cut(axes[0][1], kind="c", mirror=True)
draw_cut(axes[1][0], kind="inf", mirror=False)
draw_cut(axes[1][1], kind="inf", mirror=True)
axes[0][0].set_title("$K=c$：A 视角纸面", fontsize=12.5)
axes[0][1].set_title("$K=c$：B 视角纸面（镜像）", fontsize=12.5)
axes[1][0].set_title("$K=\\infty$：A 视角纸面", fontsize=12.5)
axes[1][1].set_title("$K=\\infty$：B 视角纸面（镜像）", fontsize=12.5)
fig.suptitle("校验线切割，画在视角自己的坐标纸面上", fontsize=13.5, y=0.995)
fig.tight_layout(rect=(0, 0, 1, 0.975))
fig.savefig("twins-calibration-cut-aview.png", dpi=150)
print("  xE(切点 x_A) =", -2*float(XA(T1_INF)), "  切点=(0,%s)与(%s,%s)" % (T1_INF, -2*float(XA(T1_INF)), T1_INF))
print("  已输出 twins-calibration-cut-aview.png（2x2）")

print("  四个切点的 A 视角坐标（tau_A, x_A）:")
for k, pt in [("E_A",(0.5,-0.3)),("E_B",(0.5,0.3)),("F_A",(3.5,-0.3)),("F_B",(3.5,0.3))]:
    r = fermi_solve(*pt)
    print("    %-4s -> (%s, %s)" % (k, round(float(r[0]),4), round(float(r[1]),4)))
