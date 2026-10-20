import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

GMAX = 4.0                                   # 绘图时 gamma 的截断上限
RATIO_MAX = np.sqrt(1.0 - 1.0 / GMAX**2)      # gamma = GMAX 对应的 v/K ≈ 0.9682

# ================= 图 1：不同 K 下的 gamma 曲线族 =================
fig, ax = plt.subplots(figsize=(8.0, 5.6))

beta = np.linspace(0.0, 3.2, 8000)

cases = [
    (1.0,  '#c0392b', r'$K=c$'),
    (2.0,  '#e67e22', r'$K=2c$'),
    (3.0,  '#2980b9', r'$K=3c$'),
    (None, '#1e8449', r'$K=\infty$'),
]

for K, col, lab in cases:
    if K is None:
        b = beta
        g = np.ones_like(b)
        lw = 3.0
        z = 5
    else:
        b = beta[beta < K * RATIO_MAX]
        g = 1.0 / np.sqrt(1.0 - (b / K) ** 2)
        lw = 2.2
        z = 4
    ax.plot(b, g, color=col, lw=lw, label=lab, zorder=z,
            solid_capstyle='round')

# 有限 K 的发散位置（渐近线）
for K, col, _ in cases:
    if K is not None and K <= 3.2:
        ax.axvline(K, color=col, ls=(0, (4, 4)), lw=1.4, alpha=0.9, zorder=2)
        ax.text(K + 0.07, 3.74, r'$v=K$', fontsize=11, color=col,
                 ha='left', va='center')

# gamma = 1 的水平线（伽利略）：单独用箭头文字标注，与横轴分开
ax.annotate(r'$\gamma_K\equiv 1$（伽利略变换）',
            xy=(1.30, 1.0), xytext=(1.62, 0.58),
            fontsize=11.5, color='#1e8449', ha='center',
            arrowprops=dict(arrowstyle='->', color='#1e8449',
                            lw=1.3, shrinkA=1, shrinkB=3))

# y < 1 区域：实数域无定义（该带内留白，仅用于与横轴区分）
ax.axhspan(0.0, 1.0, color='#95a5a6', alpha=0.12, zorder=0)
ax.text(2.70, 0.72, r'$\gamma_K<1$ 无实数解', fontsize=10.5,
        color='#7f8c8d', ha='center', va='center')

ax.set_xlim(0.0, 3.2)
ax.set_ylim(0.0, 4.2)
ax.set_xticks([0, 1, 2, 3])
ax.set_yticks([0, 1, 2, 3, 4])
ax.set_xlabel(r'$v/c$', fontsize=13)
ax.set_ylabel(r'$\gamma_K(v)=\dfrac{1}{\sqrt{1-v^{2}/K^{2}}}$', fontsize=13)
ax.grid(alpha=0.25, lw=0.7, zorder=1)
ax.legend(loc='lower center', ncol=2, fontsize=11.5,
          frameon=False, bbox_to_anchor=(0.5, 0.02))
ax.set_title(r'不同恒速 $K$ 下的 $\gamma_K(v)$ 曲线族', fontsize=13.5, pad=10)

plt.tight_layout()
plt.savefig(r"invariant-speed.png", dpi=200, bbox_inches="tight", facecolor="white")