# -*- coding: utf-8 -*-
"""恒速场群配图：左栏 局部零锥 + 恒速曲线；右栏 K(x) 与 Ricci 标量 R=2K''/K。"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 12

L = 1.0
K0 = 1.0
alpha = 0.6

x = np.linspace(0.0, L, 4001)
K = K0 * (1.0 + alpha * np.sin(2 * np.pi * x / L))
Kpp = -K0 * alpha * (2 * np.pi / L) ** 2 * np.sin(2 * np.pi * x / L)
R = 2.0 * Kpp / K

# 恒速曲线 dx/dt = K(x)  =>  dt/dx = 1/K(x)
t = np.concatenate([[0.0], np.cumsum(0.5 * (1.0 / K[1:] + 1.0 / K[:-1]) * np.diff(x))])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.4, 5.4))

# ---------------- 左栏 ----------------
ax1.set_title("局部零锥与恒速曲线", fontsize=13, pad=10)

# K 常数对照（直线）
ax1.plot(x, x / K0, color="#B4B2A9", lw=2.0, ls="--",
         label="$K$ 为常数（对照）")

# 局部零锥：在若干位置画 V 形（朝 +t 张开）
cone_x = [0.06, 0.26, 0.46, 0.66, 0.86]
d = 0.075
for k, xc in enumerate(cone_x):
    idx = int(round(xc / L * (len(x) - 1)))
    x0, t0 = x[idx], t[idx]
    kk = K[idx]
    hl = d / kk  # dt 方向半长（K 越大越平，张角越宽）
    ax1.plot([x0 - d, x0], [t0 + hl, t0], color="#D85A30", lw=1.8, zorder=3)
    ax1.plot([x0, x0 + d], [t0, t0 + hl], color="#D85A30", lw=1.8, zorder=3)
    ax1.plot([x0], [t0], marker="o", ms=5, color="#993C1D", zorder=4)
    if k == 0:
        ax1.annotate("$K=1.22$", xy=(x0 + 0.02, t0 - 0.01),
                     xytext=(0.145, -0.16), fontsize=11.5, color="#993C1D",
                     ha="center",
                     arrowprops=dict(arrowstyle="-", color="#993C1D", lw=0.9))
    if k == 4:
        ax1.annotate("$K=0.53$", xy=(x0 - 0.03, t0 - 0.005),
                     xytext=(0.78, 0.52), fontsize=11.5, color="#993C1D",
                     ha="center",
                     arrowprops=dict(arrowstyle="-", color="#993C1D", lw=0.9))

# 恒速曲线（变 K）：三条平移副本
for off, lw in zip([0.0, 0.55, 1.10], [2.6, 2.2, 2.2]):
    ax1.plot(x, t + off, color="#185FA5", lw=lw,
             label="恒速曲线 $\\mathrm{d}x/\\mathrm{d}t=K(x)$" if off == 0 else None)

ax1.set_xlabel("$x/L$")
ax1.set_ylabel("$t$")
ax1.set_xlim(0.0, 1.0)
ax1.set_ylim(-0.28, 2.25)
ax1.legend(loc="lower right", fontsize=11, framealpha=0.95)
ax1.grid(alpha=0.25, ls=":")
ax1.set_axisbelow(True)

# ---------------- 右栏 ----------------
ax2.set_title("恒速场与 Ricci 标量", fontsize=13, pad=10)

ax2.axhline(0.0, color="#B4B2A9", lw=1.2, ls="-", zorder=1)
ax2.plot(x, K / K0, color="#0F6E56", lw=2.6, label="$K(x)/K_0$")
ax2.set_xlabel("$x/L$")
ax2.set_ylabel("$K/K_0$", color="#0F6E56")
ax2.tick_params(axis="y", labelcolor="#0F6E56")
ax2.set_xlim(0.0, 1.0)
ax2.set_ylim(0.30, 1.75)

ax2b = ax2.twinx()
ax2b.plot(x, R * L ** 2, color="#BA7517", lw=2.6, ls="--",
          label="$R=2\\,\\Delta K/K$")
ax2b.set_ylabel("$R\\,L^{2}$", color="#BA7517")
ax2b.tick_params(axis="y", labelcolor="#BA7517")
ax2b.axhline(0.0, color="#B4B2A9", lw=0.8, zorder=1)
ax2b.set_ylim(-150.0, 150.0)

lines1, lab1 = ax2.get_legend_handles_labels()
lines2, lab2 = ax2b.get_legend_handles_labels()
ax2.legend(lines1 + lines2, lab1 + lab2, loc="lower center",
           fontsize=11, framealpha=0.95)

ax2.grid(alpha=0.25, ls=":")
ax2.set_axisbelow(True)

fig.tight_layout()
fig.savefig("invariant-speed-field.png", dpi=150, bbox_inches="tight",
            facecolor="white")
print("saved invariant-speed-field.png")
