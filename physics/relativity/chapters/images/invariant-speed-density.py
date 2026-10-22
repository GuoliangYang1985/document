# -*- coding: utf-8 -*-
"""第 5 章配图：球对称静态例 K(r)=K0+alpha/r 与 G_00(r)=alpha^2/(r^2(K0 r+alpha)^2)。"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 12

K0 = 1.0
alpha = 0.5

r = np.linspace(0.30, 3.2, 3000)
K = K0 + alpha / r
G00 = alpha ** 2 / (r ** 2 * (K0 * r + alpha) ** 2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.6, 4.9))

ax1.set_title("恒速场 $K(r)=K_0+\\dfrac{\\alpha}{r}$", fontsize=13, pad=10)
ax1.plot(r, K, color="#0F6E56", lw=2.8)
ax1.axhline(K0, color="#B4B2A9", lw=1.6, ls="--")
ax1.annotate("$K_0$", xy=(2.75, K0), xytext=(2.55, K0 - 0.13),
             fontsize=12, color="#5F5E5A")
ax1.set_xlabel("$r$")
ax1.set_ylabel("$K/K_0$")
ax1.set_xlim(0.30, 3.2)
ax1.set_ylim(0.95, 2.55)
ax1.grid(alpha=0.25, ls=":")
ax1.set_axisbelow(True)

ax2.set_title("Einstein 张量 $G_{00}(r)=\\dfrac{\\alpha^{2}}{r^{2}(K_0r+\\alpha)^{2}}$",
              fontsize=13, pad=10)
ax2.semilogy(r, G00, color="#A32D2D", lw=2.8)
ax2.set_xlabel("$r$")
ax2.set_ylabel("$G_{00}$（对数刻度）")
ax2.set_xlim(0.30, 3.2)
ax2.set_yticks([1e-3, 1e-2, 1e-1, 1e0, 1e1])
ax2.set_yticklabels(["$10^{-3}$", "$10^{-2}$", "$10^{-1}$", "$10^{0}$", "$10^{1}$"])
ax2.grid(alpha=0.25, ls=":", which="both")
ax2.set_axisbelow(True)

ymin, ymax = ax2.get_ylim()
ax2.fill_between(r, ymin, G00, color="#F09595", alpha=0.35)
ax2.set_ylim(ymin, ymax)
ax2.annotate("$G_{00}>0$ 处处成立\n（能量密度非零）",
             xy=(0.95, 1e-1), xytext=(1.25, 1.0),
             fontsize=12, color="#791F1F", ha="left",
             arrowprops=dict(arrowstyle="->", color="#791F1F", lw=1.2))

fig.tight_layout()
fig.savefig("invariant-speed-density.png", dpi=150, bbox_inches="tight",
            facecolor="white")
print("saved invariant-speed-density.png")
print("G00 range: %.4g .. %.4g" % (G00.min(), G00.max()))
