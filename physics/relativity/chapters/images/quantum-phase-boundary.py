# -*- coding: utf-8 -*-
"""第 7 章配图：量子相态与引力相态的分界，以及静能的分离。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

M_ = 1.0
p = 1.0
Kv = np.linspace(0.25, 6.0, 3000)
E = np.sqrt(M_ ** 2 * Kv ** 4 + p ** 2 * Kv ** 2)   # 完整色散
Enr = E - M_ * Kv ** 2                              # 扣除静能后的残余
rest = M_ * Kv ** 2                                 # 静能（发散）

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 4.4))

# ---------- 左：相态图 ----------
ax1.fill_between([-0.02, 1.02], 0.0, 3.0, color="#f6ded9", alpha=0.85, zorder=0)
ax1.fill_between([-0.02, 1.02], -0.22, 0.0, color="#e3efe2", alpha=0.9, zorder=0)
ax1.plot([-0.02, 1.02], [0.0, 0.0], color="#333333", lw=1.8)
ax1.plot([0.0, 0.0], [-0.22, 3.0], color="#1f4e79", lw=1.4, ls="--")
ax1.scatter([0.0], [0.0], s=150, color="#2e6b3e", zorder=5)
ax1.annotate("量子相态\n$K=\\infty,\\ \\nabla K=0$", xy=(0.0, 0.0),
             xytext=(0.16, 0.55), fontsize=11, color="#2e6b3e",
             arrowprops=dict(arrowstyle="->", color="#2e6b3e", lw=1.4))
ax1.text(0.52, -0.14, "恒速群相态：波动方程（$K$ 有限）",
         fontsize=10.5, color="#1f4e79", ha="center")
ax1.text(0.50, 1.90, "引力相态：$\\nabla K\\neq 0$\n（无全局群 $\\Rightarrow$ 无中央扩张）",
         fontsize=11.5, color="#8c2f2c", ha="center", va="center")
ax1.text(0.50, 2.72, "$\\uparrow\\ |\\nabla K|\\to\\infty$（黑洞视界）",
         fontsize=10, color="#8c2f2c", ha="center")
ax1.set_xlim(-0.02, 1.02)
ax1.set_ylim(-0.22, 3.0)
ax1.set_xlabel(r"$1/K$", fontsize=12)
ax1.set_ylabel(r"$|\nabla K|$", fontsize=12)
ax1.set_title("相态图：量子相态是一个零测集", fontsize=13)
ax1.set_xticks([0.0, 0.5, 1.0])
ax1.set_xticklabels([r"$0$", r"$0.5$", r"$1$"])
ax1.set_yticks([0.0, 1.0, 2.0, 3.0])
ax1.grid(alpha=0.0)

# ---------- 右：静能的分离 ----------
ax2.plot(Kv, rest, color="#c0504d", lw=2.0, ls="--",
         label=r"静能 $mK^2\to\infty$")
ax2.plot(Kv, Enr, color="#1f4e79", lw=2.4,
         label=r"$E-mK^2\ \to\ p^2/(2m)$")
ax2.axhline(p ** 2 / (2 * M_), color="#2e6b3e", lw=1.4, ls=":")
ax2.text(3.2, 0.53, r"$p^2/(2m)=0.5$", fontsize=10.5, color="#2e6b3e")
ax2.annotate("静能发散，被相位\n$e^{-imK^2t/\\hbar}$ 精确扣除",
             xy=(4.4, M_ * 4.4 ** 2), xytext=(2.2, 12.0),
             fontsize=10, color="#8c2f2c",
             arrowprops=dict(arrowstyle="->", color="#8c2f2c", lw=1.2))
ax2.set_xlim(0.25, 6.0)
ax2.set_ylim(-0.4, 17.0)
ax2.set_xlabel(r"$K$", fontsize=12)
ax2.set_ylabel(r"能量（$m=p=1$）", fontsize=12)
ax2.set_title("重整化收缩：发散与 $1/K^2$ 相抵", fontsize=13)
ax2.legend(loc="upper left", fontsize=10, framealpha=0.95)
ax2.grid(alpha=0.28, ls=":")

fig.tight_layout()
fig.savefig("quantum-phase-boundary.png", dpi=170, bbox_inches="tight")
print("saved quantum-phase-boundary.png")
print("E-mK^2 at K=6 :", Enr[-1], "  -> p^2/(2m) =", p ** 2 / (2 * M_))
