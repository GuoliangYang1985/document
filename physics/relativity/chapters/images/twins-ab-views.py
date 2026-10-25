# -*- coding: utf-8 -*-
"""
第 14 章配图：对称双生子的 A 视角与 B 视角时空图，$K=c$ 与 $K=\infty$ 对照。

2x2 面板：
  上行 K=c   ：A 视角（A 静止）/ B 视角（B 静止）
  下行 K=oo  ：A 视角（A 静止）/ B 视角（B 静止）

每个面板画：
  · 静止者的世界线（纵轴）
  · 运动者的世界线 x = -w t
  · 等读数线（K=c：校准双曲线；K=oo：水平直线）
  · 本系同时线（水平线），并标出它与运动者世界线的交点

全程只用 A、B 两者的坐标，不出现第三个坐标系。
"""
import numpy as np
import sympy as sp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

# ------------------------------------------------------------------ 符号核验
t, x, w, tau, c, K = sp.symbols("t x w tau c K", positive=True)
gam = 1 / sp.sqrt(1 - w ** 2 / c ** 2)
# 运动者世界线 x = -w t 上，本系坐标时 t 处的读数
tau_moving = sp.simplify(sp.sqrt(t ** 2 - (w * t) ** 2 / c ** 2))
print("K=c  运动者世界线上、本系坐标时 t 处的读数 :", tau_moving,
      "  == t/gamma_w :", sp.simplify(tau_moving - t / gam) == 0)
# 运动者读数为 tau 的事件，本系坐标时
t_at_tau = sp.simplify(tau / sp.sqrt(1 - w ** 2 / c ** 2))
print("K=c  运动者读数为 tau 的事件，本系坐标时 :", t_at_tau,
      "  == gamma_w*tau :", sp.simplify(t_at_tau - gam * tau) == 0)
# 等读数线：t^2 - x^2/K^2 = tau^2
print("K=c  等读数线 t^2 - x^2/c^2 = tau^2 ；代入 (gamma_w tau, -w gamma_w tau) 残差 :",
      sp.simplify((gam * tau) ** 2 - (w * gam * tau) ** 2 / c ** 2 - tau ** 2))
# K -> oo 的极限
print("K->oo  等读数线 t^2 - x^2/K^2 = tau^2 的极限 :",
      sp.limit(t ** 2 - x ** 2 / K ** 2, K, sp.oo), "= tau^2  ==>  t = tau（水平直线）")
print("K->oo  gamma_w(K) =", sp.limit(1 / sp.sqrt(1 - w ** 2 / K ** 2), K, sp.oo))

# ------------------------------------------------------------------ 绘图
W = 0.6                      # 相对速率 w/c
GAM = 1 / np.sqrt(1 - W ** 2)   # 1.25
TMAX = 1.35
TAUS = [0.45, 0.80, 1.15]

fig, axes = plt.subplots(2, 2, figsize=(10.4, 8.6))
BLUE, RED, GREY, BLACK = "#1f4e79", "#b03a2e", "#666666", "#111111"


def panel(ax, K_inf, view, title):
    """view: 'A' 表示所画坐标系中 A 静止（A 视角），'B' 则 B 静止。"""
    sgn = -1.0 if view == "A" else 1.0      # 运动者世界线的斜率方向（镜像）
    tt = np.linspace(0, TMAX, 200)
    ax.plot(np.zeros_like(tt), tt, color=BLACK, lw=3.0, zorder=4)
    ax.plot(sgn * W * tt, tt, color=RED, lw=2.6, zorder=4)

    if K_inf:                                # K = oo：等读数线 = 水平线
        for tv in TAUS:
            xs = np.linspace(-1.0, 1.0, 50)
            ax.plot(xs, np.full_like(xs, tv), color=BLUE, lw=1.6, ls="-", alpha=0.95)
        ax.text(0.10 if view == "A" else -0.98, TAUS[0] + 0.05,
                "等读数线＝同时线\n$t=\\tau$", fontsize=9.5, color=BLUE, ha="left")
    else:                                    # K = c：等读数线为校准双曲线
        for tv in TAUS:
            xs = np.linspace(-1.0, 1.0, 400)
            yy = np.sqrt(tv ** 2 + xs ** 2)
            ax.plot(xs, yy, color=BLUE, lw=1.5, alpha=0.95)
        ax.text(-0.98 if view == "A" else 0.02, 0.06,
                "等读数线\n$t^{2}-x^{2}/c^{2}=\\tau^{2}$",
                fontsize=9.5, color=BLUE, ha="left")
        # 本系同时线（水平）示例
        tv = TAUS[1]
        xs = np.linspace(-1.0, 1.0, 50)
        ax.plot(xs, np.full_like(xs, tv), color=GREY, lw=1.5, ls="--")
        ax.text(0.10 if view == "A" else -0.98, tv + 0.05, "同时线 $t=$常数",
                fontsize=9, color=GREY, ha="left")

    # 两个标定点：静止者读 tau 与运动者读 tau
    tv = TAUS[1]
    ax.plot([0], [tv], "o", color=BLACK, ms=7, zorder=5)
    if K_inf:
        ax.plot([sgn * W * tv], [tv], "o", color=RED, ms=7, zorder=5)
        ax.annotate("读数相同", xy=(sgn * W * tv, tv), xytext=(-0.98, tv + 0.28),
                    fontsize=9.5, color="#2e7d32", ha="left",
                    arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=1.0))
    else:
        tmv = GAM * tv
        ax.plot([sgn * W * tmv], [tmv], "o", color=RED, ms=7, zorder=5)
        ax.annotate("读数相同\n$t=\\gamma_w\\tau$", xy=(sgn * W * tmv, tmv),
                    xytext=(-0.98, tmv + 0.10), fontsize=9.5, color="#2e7d32",
                    ha="left",
                    arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=1.0))

    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(0, TMAX + 0.12)
    ax.set_title(title, fontsize=12)
    ax.set_xlabel("$x$（长度）", fontsize=10.5)
    ax.set_ylabel("$ct$（长度）", fontsize=10.5)
    ax.grid(alpha=0.22)


panel(axes[0, 0], False, "A", "$K=c$　A 视角（A 静止，B 沿 $x=-wt$）")
panel(axes[0, 1], False, "B", "$K=c$　B 视角（B 静止，A 沿 $x=+wt$）")
panel(axes[1, 0], True, "A", "$K=\\infty$　A 视角（A 静止，B 沿 $x=-wt$）")
panel(axes[1, 1], True, "B", "$K=\\infty$　B 视角（B 静止，A 沿 $x=+wt$）")

fig.suptitle("对称双生子的 A 视角与 B 视角（$w=0.6c$，$\\gamma_w=1.25$；只含 A、B 两套坐标）",
             fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.975])
fig.savefig("twins-ab-views.png", dpi=150)
print("已输出 twins-ab-views.png")
