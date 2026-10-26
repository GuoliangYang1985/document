# -*- coding: utf-8 -*-
"""
第 14 章配图（修订版）：镜像弯曲曲线对中，gamma_B 在 **A 视角坐标纸面** 中的像。

旧图把这张图画在惯性坐标 (t,x) 上——那张纸属于第三方；本图的横轴是
A 自己的空间坐标 x_A、纵轴是 A 自己的读数坐标 tau_A。

像的参数方程（c=1，A 的曲率取 a=1，参数 u = a*tau_B 为 B 自己的读数）：
    x_A(u)  = sqrt(5 - 4 cosh u) - 1
    tau_A(u)= arctanh( sinh u / (2 - cosh u) )
像存在当且仅当 u < ln 2。u -> ln2 时 x_A -> -1（域边界）而 tau_A -> 无穷。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

for f, s in (("font.sans-serif", ["Microsoft YaHei", "SimHei", "DejaVu Sans"]),
             ("axes.unicode_minus", False)):
    plt.rcParams[f] = s

BLUE, RED, GREEN, GREY, BLACK = "#1f4e79", "#b03a2e", "#2e7d32", "#666666", "#111111"

# ---------------------------------------------------------------- 数值核验
print("=== 像的点检验（a=1）===")
for u in [0.0, 0.2, 0.4, 0.6, 0.69]:
    rho = np.sqrt(max(5 - 4 * np.cosh(u), 0.0))
    xA = rho - 1
    tA = np.arctanh(np.sinh(u) / (2 - np.cosh(u)))
    # 反代回惯性坐标验证 = B 的世界线 at=sinh u, ax=1-cosh u
    at = rho * np.sinh(tA)
    ax_ = rho * np.cosh(tA) - 1
    print(f"  u={u:.2f}  x_A={xA:+.5f}  tau_A={tA:.4f}  "
          f"反代 at={at:.5f} (应={np.sinh(u):.5f})  ax={ax_:+.5f} (应={1-np.cosh(u):+.5f})")

# ---------------------------------------------------------------- 图
fig, ax = plt.subplots(figsize=(6.2, 5.4))

# 域外
ax.axvspan(-1.85, -1.0, color="#eeeeee", zorder=0, hatch="///")
ax.text(-1.42, 2.75, "不在 A 的坐标域中", fontsize=10, color=GREY,
        ha="center", rotation=90)

# 域边界
ax.axvline(-1.0, color=GREY, ls="--", lw=1.6)
ax.text(-0.92, -0.14, "$x_A=-c^{2}/a$", fontsize=10.5, color=GREY)

# A 的世界线（自己的坐标里是纵轴）
ax.plot([0, 0], [0, 6.0], color=BLACK, lw=2.6)
ax.text(0.10, 5.35, "A：$x_A=0$", fontsize=11, color=BLACK)

# B 的像
us = np.linspace(0, np.log(2) - 1e-9, 2000)
rho = np.sqrt(np.maximum(5 - 4 * np.cosh(us), 0))
xA = rho - 1.0
tA = np.arctanh(np.sinh(us) / (2 - np.cosh(us)))
ax.plot(xA, tA, color=RED, lw=2.6)
ax.text(-0.62, 4.65, "B 的像\n（$a\\tau_B<\\ln2$ 的部分）", fontsize=11, color=RED)

# B 自己的读数 a*tau_B 的刻度点
for u in [0.2, 0.4, 0.6]:
    rho = np.sqrt(5 - 4 * np.cosh(u))
    xA1 = rho - 1
    tA1 = np.arctanh(np.sinh(u) / (2 - np.cosh(u)))
    ax.plot([xA1], [tA1], "o", color=GREEN, ms=6, zorder=5)
    ax.annotate(f"$a\\tau_B={u}$", xy=(xA1, tA1), xytext=(xA1 + 0.22, tA1 + 0.18),
                fontsize=9.5, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.0))

# 渐近行为
ax.annotate("当 $a\\tau_B\\to\\ln2$：\n$x_A\\to-c^{2}/a$，$a\\tau_A\\to\\infty$",
            xy=(-0.97, 4.9), xytext=(0.55, 4.15), fontsize=10.5, color=BLACK,
            arrowprops=dict(arrowstyle="->", color=BLACK, lw=1.2))

ax.set_xlim(-1.85, 2.2)
ax.set_ylim(-0.2, 6.0)
ax.set_xlabel("$a\\,x_A\\,/\\,c^{2}$（A 自己的空间坐标）", fontsize=11)
ax.set_ylabel("$a\\,\\tau_A\\,/\\,c$（A 自己的读数坐标）", fontsize=11)
ax.set_title("镜像弯曲曲线对：$\\gamma_B$ 在 A 视角纸面上的像", fontsize=12.5)
ax.grid(alpha=0.18)
fig.tight_layout()
fig.savefig("twins-a-view-domain.png", dpi=155)
print("\n  已输出 twins-a-view-domain.png")
