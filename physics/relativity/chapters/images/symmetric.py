import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 创建画布，宽高比调整为横向
fig, ax = plt.subplots(figsize=(11, 4))
# 设置坐标轴范围，确保左右半圆完整显示
ax.set_xlim(-7.8, 7.8)
ax.set_ylim(-3.0, 3.0)
ax.axis('off')  # 隐藏坐标轴

# 手动调整边距，减少空白
plt.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.15)

# --- 基础几何参数 ---
track_width = 10      # 跑道直道长度
track_height = 4      # 跑道上下半圆的直径
radius = track_height / 2
straight_y_top = radius
straight_y_bottom = -radius
left_x = -track_width / 2
right_x = track_width / 2
center_x = 0
a_color = '#ff0000'
b_color = '#0000ff'

# 2. 高亮第一阶段研究对象：纯匀速直线段
# A的直线段 (从 P 向右到 M)
ax.plot([left_x, center_x], [straight_y_top, straight_y_top], color=a_color, linewidth=6, solid_capstyle='round', label='A的轨迹 (速度 v)')
# B的直线段 (从 Q 向左到 M)
ax.plot([right_x, center_x], [straight_y_top, straight_y_top], color=b_color, linewidth=6, solid_capstyle='round', label='B的轨迹 (速度 -v)')

# 3. 绘制剩余轨迹 (细线表示闭环)
# B的剩余部分 (右侧半圆弧，从底部直道转向 Q 点)
right_arc_B = patches.Arc((right_x, 0), track_height, track_height, angle=0, theta1=-90, theta2=90, color=b_color, linewidth=2)
ax.add_patch(right_arc_B)
ax.plot([0, left_x], [straight_y_bottom, straight_y_bottom], color=a_color, linewidth=2)
left_arc_A = patches.Arc((left_x, 0), track_height, track_height, angle=0, theta1=90, theta2=270, color=a_color, linewidth=2)
ax.add_patch(left_arc_A)

# B的剩余部分 (逆时针)
ax.plot([0, right_x], [straight_y_bottom, straight_y_bottom], color=b_color, linewidth=2)

# 4. 标记关键点
# P 点
ax.plot(left_x, straight_y_top, 'o', markersize=8, color='orange')
ax.text(left_x, straight_y_top + 0.4, r'P', fontsize=16, fontweight='bold', ha='center')

# Q 点
ax.plot(right_x, straight_y_top, 'o', markersize=8, color='orange')
ax.text(right_x, straight_y_top + 0.4, r'Q', fontsize=16, fontweight='bold', ha='center')

# M 点 (相遇点)
ax.plot(center_x, straight_y_top, '*', markersize=15, color='gold', markeredgecolor='orange', markeredgewidth=1.5)
ax.text(center_x, straight_y_top + 0.4, r'M', fontsize=14, ha='center', color='black', fontweight='bold')

# O 点 (起点)
ax.plot(center_x, straight_y_bottom, '*', markersize=15, color='gold', markeredgecolor='orange', markeredgewidth=1.5)
ax.text(center_x, straight_y_bottom - 0.6, r'O', fontsize=14, ha='center', color='black')

# 4.5 两条对称轴与镜像对应点（便于严谨表述"逐点对应"）
# --- 竖轴 OM：左右镜像对称（A 与 B 互换） ---
ax.plot([center_x, center_x], [straight_y_bottom, straight_y_top], '--', color='#888888', linewidth=1.4, zorder=1)
ax.text(center_x + 0.20, -1.15, '镜像轴 OM（左右对称）', fontsize=11, color='#666666', ha='left', va='center')

# --- 横轴：上下镜像对称（P 与 S、Q 与 S′、M 与 O） ---
ax.plot([-7.4, 7.4], [0, 0], '--', color='#888888', linewidth=1.4, zorder=1)
ax.text(-4.55, 0.30, '对称横轴（上下对称）', fontsize=11, color='#666666', ha='left', va='bottom')

# 左右对称的一对：R / R′（两点都落在横轴上）
r_pair_y = 0.0
ax.plot([-7.0], [r_pair_y], 'o', markersize=7, color='#444444', zorder=5)
ax.plot([7.0], [r_pair_y], 'o', markersize=7, color='#444444', zorder=5)
ax.text(-7.45, r_pair_y, r"R", fontsize=15, ha='center', va='center', color='#333333', fontweight='bold')
ax.text(7.45, r_pair_y, r"R'", fontsize=15, ha='center', va='center', color='#333333', fontweight='bold')

# 上下对称的两对：P 与 S、Q 与 S′（竖虚线为各自的对称连线）
for xv in (left_x, right_x):
    ax.plot([xv, xv], [straight_y_bottom, straight_y_top], '--', color='#bbbbbb', linewidth=1.2, zorder=1)
ax.plot([left_x], [straight_y_bottom], 'o', markersize=7, color='#444444', zorder=5)
ax.plot([right_x], [straight_y_bottom], 'o', markersize=7, color='#444444', zorder=5)
ax.text(left_x, straight_y_bottom - 0.55, r"S", fontsize=15, ha='center', color='#333333', fontweight='bold')
ax.text(right_x, straight_y_bottom - 0.55, r"S'", fontsize=15, ha='center', color='#333333', fontweight='bold')

# 5. 添加速度箭头
ax.arrow(-4, straight_y_top, 1.5, 0, head_width=0.3, head_length=0.4, fc=a_color, ec=a_color, linewidth=2)
ax.arrow(4, straight_y_top, -1.5, 0, head_width=0.3, head_length=0.4, fc=b_color, ec=b_color, linewidth=2)

# 6. 添加图例，放在底部中央，不遮挡图形
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2, fontsize=12, frameon=False)

plt.tight_layout()
plt.savefig(r"symmetric.png", dpi=200, bbox_inches="tight", facecolor="white")