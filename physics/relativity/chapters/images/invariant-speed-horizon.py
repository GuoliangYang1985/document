# -*- coding: utf-8 -*-
"""第 6 章配图：恒速场 K(r) 与 Schwarzschild 视界。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

M = 1.0
rs = 2.0 * M
r = np.linspace(rs + 1e-4, 10.0 * M, 4000)

F = 1.0 - 2.0 * M / r          # g_00 = K^2
K = np.sqrt(F)                 # 恒速场
dK = M / (r ** 2 * np.sqrt(F)) # dK/dr
I = 48.0 * M ** 2 / r ** 6     # C_abcd C^abcd

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 4.3))

# ---- 左图：K(r) 与 g_00(r)，视界位置 ----
ax1.plot(r, K, color="#1f4e79", lw=2.2, label=r"$K(r)=\sqrt{1-2M/r}$")
ax1.plot(r, F, color="#c0504d", lw=2.0, ls="--", label=r"$g_{00}=1-2M/r$")
ax1.axvline(rs, color="#333333", lw=1.4, ls=":")
ax1.axhspan(-0.09, 0.0, color="#d9d9d9", alpha=0.55, zorder=0)
ax1.fill_betweenx([-0.09, 1.09], 1.6, rs, color="#f2dcdb", alpha=0.55, zorder=0)
ax1.text(rs + 0.12, 1.00, r"$r_s=2M$", fontsize=11, color="#333333")
ax1.text(1.62, 0.92, r"$r<r_s$" "\n" r"$K$ 无定义", fontsize=9.5,
         color="#8c2f2c", va="top", ha="left")
ax1.set_xlim(1.6, 10.0)
ax1.set_ylim(-0.09, 1.12)
ax1.set_xlabel(r"$r/M$", fontsize=12)
ax1.set_ylabel(r"$K,\ \ g_{00}$", fontsize=12)
ax1.set_title("恒速场与视界", fontsize=13)
ax1.legend(loc="lower right", fontsize=10, framealpha=0.95)
ax1.grid(alpha=0.28, ls=":")

# ---- 右图：Weyl 不变量与 K 的梯度（对数刻度）----
ax2.semilogy(r, I, color="#2e6b3e", lw=2.2,
             label=r"$C_{abcd}C^{abcd}=48M^2/r^6$")
ax2.semilogy(r, dK, color="#7f4fbf", lw=2.0, ls="--",
             label=r"$|\partial_r K|=M/(r^2K)$")
ax2.axvline(rs, color="#333333", lw=1.4, ls=":")
ax2.fill_betweenx([1e-3, 2e2], 1.6, rs, color="#f2dcdb", alpha=0.55, zorder=0)
ax2.set_xlim(1.6, 10.0)
ax2.set_ylim(1e-3, 2e2)
ax2.set_yticks([1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2])
ax2.set_yticklabels([r"$10^{-3}$", r"$10^{-2}$", r"$10^{-1}$",
                     r"$10^{0}$", r"$10^{1}$", r"$10^{2}$"])
ax2.set_xlabel(r"$r/M$", fontsize=12)
ax2.set_ylabel("量值（对数刻度）", fontsize=12)
ax2.set_title("潮汐曲率非零 · 视界处梯度发散", fontsize=13)
ax2.legend(loc="upper right", fontsize=10, framealpha=0.95)
ax2.grid(alpha=0.28, ls=":", which="both")

fig.tight_layout()
fig.savefig("invariant-speed-horizon.png", dpi=170, bbox_inches="tight")
print("saved invariant-speed-horizon.png")
print("K(2M+eps) ->", K[0], " ; I(rs) =", 48 * M ** 2 / rs ** 6)
