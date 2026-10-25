# -*- coding: utf-8 -*-
"""
第 14 章配图：对称双生子的「校验线切割」。

左：$K=c$，切割线为以 O 为心 / 以 M 为心的双曲校验线
      t^2 - x^2/c^2 = tau1^2、(t_M-t)^2 - (x-x_M)^2/c^2 = sigma1^2
右：$K=oo$，切割线为水平线 t = 常数

两条互为镜像的世界线（同一Start O、同一重逢 M）由三段组成：
段 I 直线 → 段 II 转向 → 段 III 直线。
"""
import numpy as np
import sympy as sp
import mpmath as mp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

mp.mp.dps = 25

# ------------------------------------------------------------------ 符号核验
t, x, u, tt = sp.symbols("t x u tau", positive=True)
s_expr = sp.integrate(sp.sqrt(1 - u ** 2), (t, 0, tt))
check1 = sp.simplify(s_expr ** 2 - (tt ** 2 - (u * tt) ** 2)) == 0
print("校准引理  s^2 = t^2 - x^2（与速率 u 无关）:", check1)

rate = mp.sqrt(1 - mp.mpf("0.36"))        # 直线段读数率 0.8
tau1 = sig1 = mp.mpf("0.4")
tE = tau1 / rate                          # 0.5
tF = 4 - sig1 / rate                      # 3.5
xAtE = float(-0.6 * tE)                   # -0.3
xAtF = float(0.6 * tF - 2.4)              # -0.3
print(f"  切点 E_A=({tE}, {xAtE})  F_A=({tF}, {xAtF})")
print("  Λ_O 参数核对:", mp.nstr(tE ** 2 - (-xAtE) ** 2, 8), "= tau1^2 =", mp.nstr(tau1 ** 2, 8))
print("  Λ_M 参数核对:", mp.nstr((4 - tF) ** 2 - (0 - xAtF) ** 2, 8), "= sig1^2 =", mp.nstr(sig1 ** 2, 8))

# ------------------------------------------------------------------ 路径
def xA(tv):
    tv = np.asarray(tv, dtype=float)
    out = np.empty_like(tv)
    m1 = tv <= 1.0
    m2 = (tv > 1.0) & (tv <= 3.0)
    m3 = tv > 3.0
    out[m1] = -0.6 * tv[m1]
    out[m2] = 0.3 * tv[m2] ** 2 - 1.2 * tv[m2] + 0.3
    out[m3] = 0.6 * tv[m3] - 2.4
    return out

ts_I = np.linspace(0, 1, 120)
ts_II = np.linspace(1, 3, 240)
ts_III = np.linspace(3, 4, 120)

BLUE, RED, GREY, GREEN = "#1f4e79", "#b03a2e", "#555555", "#2e7d32"
fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.4), sharey=True)

for kinf, ax in zip([False, True], axes):
    # ---- 切割窗口（填充）
    xs = np.linspace(-0.42, 0.42, 200)
    if kinf:
        y_top = np.full_like(xs, float(tF))
        y_bot = np.full_like(xs, float(tE))
    else:
        y_bot = np.sqrt(0.16 + xs ** 2)
        y_top = 4 - np.sqrt(0.16 + xs ** 2)
    ax.fill_between(xs, y_bot, y_top, color="#d9d9d9", alpha=0.45, zorder=0)

    # ---- 两条世界线（互为镜像；A 在左侧，B = ι(A) 在右侧）
    for sgn, col, lab in [(1, BLUE, "A 的世界线"), (-1, RED, "B 的世界线")]:
        ax.plot(sgn * xA(ts_I), ts_I, color=col, lw=2.6, zorder=4)
        ax.plot(sgn * xA(ts_II), ts_II, color=col, lw=2.6, ls="-", zorder=4)
        ax.plot(sgn * xA(ts_III), ts_III, color=col, lw=2.6, zorder=4)

    # ---- 切割线
    if kinf:
        for tv, lab in [(float(tE), r"$\Lambda_O$：$t=0.5$"),
                        (float(tF), r"$\Lambda_M$：$t=3.5$")]:
            ax.plot(xs, np.full_like(xs, tv), color=GREEN, lw=1.8, ls="--", zorder=3)
        ax.text(0.46, float(tE) + 0.06, r"$\Lambda_O$: $t=$常数", fontsize=9.5, color=GREEN)
        ax.text(0.46, float(tF) + 0.06, r"$\Lambda_M$: $t=$常数", fontsize=9.5, color=GREEN)
    else:
        ax.plot(xs, np.sqrt(0.16 + xs ** 2), color=GREEN, lw=1.8, ls="--", zorder=3)
        ax.plot(xs, 4 - np.sqrt(0.16 + xs ** 2), color=GREEN, lw=1.8, ls="--", zorder=3)
        ax.text(0.50, 0.62, r"$\Lambda_O$: $t^2-x^2/c^2=\tau_1^2$", fontsize=9.5, color=GREEN)
        ax.text(0.50, 3.16, r"$\Lambda_M$: $(t_M-t)^2-x^2/c^2=\sigma_1^2$",
                fontsize=9.5, color=GREEN)

    # ---- 切点
    for sgn, nm in [(-1, "A"), (1, "B")]:
        ax.plot([sgn * (-0.3)], [0.5], "o", color=GREEN, ms=8, zorder=6)
        ax.plot([sgn * (-0.3)], [3.5], "o", color=GREEN, ms=8, zorder=6)
    ax.text(-0.30, 0.30, "$E_A$", fontsize=10, color=GREEN, ha="center")
    ax.text(0.30, 0.30, "$E_B$", fontsize=10, color=GREEN, ha="center")
    ax.text(-0.30, 3.72, "$F_A$", fontsize=10, color=GREEN, ha="center")
    ax.text(0.30, 3.72, "$F_B$", fontsize=10, color=GREEN, ha="center")

    # ---- O、M
    ax.plot([0], [0], "o", color="black", ms=7, zorder=6)
    ax.plot([0], [4], "o", color="black", ms=7, zorder=6)
    ax.text(0.08, -0.22, "$O$", fontsize=11)
    ax.text(0.08, 4.06, "$M$（重逢）", fontsize=11)

    # ---- 分段标注
    ax.text(-0.98, 0.62, "段 I\n惯性段", fontsize=9.5, color=BLUE, ha="left")
    ax.text(-1.06, 1.90, "段 II\n转向段", fontsize=9.5, color=BLUE, ha="left")
    ax.text(-0.98, 3.30, "段 III\n惯性段", fontsize=9.5, color=BLUE, ha="left")

    # ---- 读数标注
    lab1 = "0.5" if kinf else str(tau1)
    ax.annotate(f"读数 $\\tau_1={lab1}$\n两侧相同", xy=(-0.3, 0.5),
                xytext=(-0.05, 1.15), fontsize=9.5, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.0))
    ax.annotate(f"剩余读数 $\\sigma_1={lab1}$\n两侧相同", xy=(-0.3, 3.5),
                xytext=(-0.05, 2.62), fontsize=9.5, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.0))

    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-0.45, 4.55)
    ax.set_xlabel("$x$", fontsize=11)
    ax.grid(alpha=0.2)

axes[0].set_ylabel("$ct$", fontsize=11)
axes[0].set_title("$K=c$：双曲校验线的切割", fontsize=12.5)
axes[1].set_title("$K=\\infty$：校验线为 $t=$常数", fontsize=12.5)

# 图例（共用）
from matplotlib.lines import Line2D
leg = [Line2D([0], [0], color=BLUE, lw=2.6, label="曲线 $\\gamma_A$"),
       Line2D([0], [0], color=RED, lw=2.6, label="曲线 $\\gamma_B=\\iota(\\gamma_A)$"),
       Line2D([0], [0], color=GREEN, lw=1.8, ls="--", label="校验线（切割）")]
fig.legend(handles=leg, loc="lower center", ncol=3, fontsize=10.5, frameon=False)
fig.tight_layout(rect=[0, 0.06, 1, 1])
fig.savefig("twins-calibration-cut.png", dpi=155)
print("  已输出 twins-calibration-cut.png")
