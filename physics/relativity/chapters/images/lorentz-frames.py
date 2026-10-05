"""
洛伦兹变换示意图（《狭义相对论》第 2 章）
=======================================

生成坐标变换示意图 lorentz-frames.png：

惯性系 S 与 S' 的几何设置
    两系坐标轴对应平行，S' 系以速度 v 沿 x 轴正向相对 S 系运动；
    图中给出同一事件 P 在两系中的横坐标 x 与 x'（因横向坐标不变，y' = y）。

运行方式：python lorentz-frames.py
输出：与本脚本同目录的 lorentz-frames.png
"""

from pathlib import Path

import matplotlib.pyplot as plt

# ==================== 全局风格 ====================
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "cm"          # 数学符号使用 Computer Modern

C_S = "#1a1a1a"        # S 系：黑
C_SP = "#0f4c9c"       # S' 系：蓝
C_V = "#c00000"        # 相对速度：暗红
C_GRAY = "#8a8a8a"     # 辅助线：灰

OUT = Path(__file__).resolve().parent / "lorentz-frames.png"
DASH = (0, (5, 4))     # 虚线样式
DOTDASH = (0, (3, 3))  # 点划线样式


def arrow(ax, p_from, p_to, color, lw=1.8, ls="-", scale=12):
    """带箭头的直线段"""
    ax.annotate("", xy=p_to, xytext=p_from,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=ls, shrinkA=0, shrinkB=0,
                                mutation_scale=scale))


def double_arrow(ax, p_from, p_to, color, lw=1.2, scale=9):
    """双箭头（用于标注坐标跨度）"""
    ax.annotate("", xy=p_to, xytext=p_from,
                arrowprops=dict(arrowstyle="<|-|>", color=color, lw=lw,
                                linestyle=DOTDASH, shrinkA=0, shrinkB=0,
                                mutation_scale=scale))


fig, ax = plt.subplots(figsize=(6.4, 5.0))

# ==================== 惯性系 S 与 S' 的几何设置 ====================
ax.set_xlim(-0.9, 6.9)
ax.set_ylim(-1.75, 4.3)
ax.set_aspect("equal")
ax.axis("off")

# --- S 系 ---
arrow(ax, (0, 0), (5.8, 0), C_S)                 # x 轴
arrow(ax, (0, 0), (0, 3.9), C_S)                 # y 轴
ax.text(5.9, -0.02, "$x$", fontsize=15, color=C_S, va="center")
ax.text(-0.02, 4.02, "$y$", fontsize=15, color=C_S, ha="center")
ax.plot(0, 0, "o", ms=5, color=C_S)
ax.text(-0.30, -0.44, "$O$", fontsize=14, color=C_S)
ax.text(0.34, 1.15, "$S$", fontsize=16, color=C_S)

# --- S' 系 ---
xp = 2.5                                          # S' 系原点在 x 轴上的位置
arrow(ax, (xp, 0), (xp, 3.15), C_SP)              # y' 轴
ax.plot(xp, 0, "o", ms=5, color=C_SP)
ax.text(xp, -0.44, "$O'$", fontsize=14, color=C_SP, ha="center")
ax.text(xp + 0.06, 3.28, "$y'$", fontsize=15, color=C_SP)
ax.text(xp + 0.40, 1.15, "$S'$", fontsize=16, color=C_SP)

# --- 相对速度 v ---
arrow(ax, (0.25, 0.66), (2.24, 0.66), C_V)
ax.text(1.25, 0.80, "$v$", fontsize=15, color=C_V, ha="center")

# --- 事件 P 及其在两系中的横坐标 ---
Px, Py = 4.3, 2.5
ax.plot(Px, Py, "o", ms=6, color=C_S)
ax.text(Px + 0.16, Py + 0.04, "$P$", fontsize=15, color=C_S)
ax.plot([Px, Px], [0, Py], ls=DASH, lw=1.1, color=C_GRAY)       # 到 x 轴的垂线
ax.plot([0, Px], [Py, Py], ls=DASH, lw=1.1, color=C_GRAY)       # 到 y 轴的垂线
ax.text(0.32, Py + 0.14, "$y$", fontsize=14, color=C_S)          # 纵坐标读数

# x 跨度（自 O 量起）与 x' 跨度（自 O' 量起）
y1, y2 = -0.72, -1.24
double_arrow(ax, (0, y1), (Px, y1), C_S)
ax.text(Px / 2, y1 - 0.40, "$x$", fontsize=14, color=C_S, ha="center")
double_arrow(ax, (xp, y2), (Px, y2), C_SP)
ax.text((xp + Px) / 2, y2 - 0.40, "$x'$", fontsize=14, color=C_SP, ha="center")

plt.tight_layout()
fig.savefig(OUT, dpi=200, bbox_inches="tight", facecolor="white")
print(f"已输出：{OUT}")
