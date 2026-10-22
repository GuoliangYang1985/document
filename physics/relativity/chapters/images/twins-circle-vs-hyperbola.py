# -*- coding: utf-8 -*-
"""
第 13 章配图核查：对称双生子闵氏图中「圆弧法」的适用范围。

左图：A 视角（标准闵氏图）。等固有读数点的轨迹是双曲线 t^2-x^2=tau^2；
      以 OM_t 为半径的欧氏圆弧与 t' 轴的交点偏低（B 读 0.686 tau，不是 tau）。
右图：双框架同比例的对称画法。两轴每格 = 各自读数，圆弧法严格成立。

参数：v = 0.6, gamma = 1.25, tau = 1。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sympy as sp

# ------------------------------------------------------------------ 符号核验
vs, ts = sp.symbols("v tau", positive=True)
gs = 1 / sp.sqrt(1 - vs ** 2)

t_c = ts / sp.sqrt(1 + vs ** 2)                 # 圆弧交点的 A 坐标时
read_c = sp.simplify(t_c * sp.sqrt(1 - vs ** 2))  # B 在该点的读数
print("圆弧交点 B 读数 =", sp.simplify(read_c))
print("  是否等于 tau :", sp.simplify(read_c - ts) == 0)

t_h, x_h = gs * ts, -vs * gs * ts               # boost 像（真对称点）
print("boost 像在双曲线 t^2-x^2=tau^2 上 :", sp.simplify(t_h ** 2 - x_h ** 2 - ts ** 2) == 0)
print("boost 像的 B 读数 = tau :", sp.simplify(t_h * sp.sqrt(1 - vs ** 2) - ts) == 0)
print("A 的洛伦兹投影读数 = gamma*tau =", sp.simplify(gs * ts))

# ------------------------------------------------------------------ 数值参数
vn = 0.6
gn = 1.0 / np.sqrt(1 - vn ** 2)      # 1.25
t_cn = 1.0 / np.sqrt(1 + vn ** 2)    # 圆弧交点处 A 坐标时 0.8571
read_cn = t_cn * np.sqrt(1 - vn ** 2)  # B 读数 0.686
print("v=0.6: 圆弧交点 B 读数 =", round(read_cn, 4))

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 6.2))

# ================================================================ 左图：A 视角
ax = ax1
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(-2.35, 1.75)
ax.set_ylim(-0.55, 2.62)

ax.annotate("", xy=(0, 2.55), xytext=(0, -0.30),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.3), zorder=3)
ax.annotate("", xy=(1.62, 0), xytext=(-1.55, 0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.3), zorder=3)
ax.annotate("", xy=(-vn * 2.2, 2.2), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.3), zorder=3)
ax.text(0.08, 2.48, "$t$", fontsize=13)
ax.text(1.58, -0.22, "$x$", fontsize=13)
ax.text(-1.62, 2.10, "$t'$", fontsize=13)
ax.text(-0.17, -0.24, "$O$", fontsize=12)

# 等固有读数轨迹：双曲线
tt = np.linspace(1.0, 1.80, 400)
ax.plot(-np.sqrt(tt ** 2 - 1), tt, "--", color="#1f6fb5", lw=1.9,
        label="等固有读数轨迹 $t^2-x^2=\\tau^2$", zorder=2)

# 半径 OM_t 的圆弧
th = np.linspace(np.deg2rad(84), np.deg2rad(148), 300)
ax.plot(np.cos(th), np.sin(th), ":", color="0.40", lw=1.7,
        label="圆弧：以 $O$ 为心、$OM_t$ 为半径", zorder=2)

# A 的洛伦兹同时线（水平）
ax.plot([-vn * gn, 0.06], [gn, gn], "--", color="#c0392b", lw=1.2,
        label="A 的洛伦兹同时线（水平投影）", zorder=2)

ax.plot(0, 1, "o", color="k", ms=6, zorder=5)
ax.plot(-vn * gn, gn, "o", color="#c0392b", ms=6, zorder=5)
ax.plot(0, gn, "s", color="#1f6fb5", ms=6, zorder=5)
ax.plot(-vn * t_cn, t_cn, "o", mfc="white", mec="0.35", ms=6.5, zorder=5)

ax.text(0.10, 0.80, "$M_t$（A 读 $\\tau$）", fontsize=11)
ax.text(0.09, 1.22, "$M'$（A 的投影，读 $\\gamma\\tau$）", fontsize=11, color="#1f6fb5")
ax.text(-0.86, 1.33, "$M_{t'}$（B 读 $\\tau$，真对称点）", fontsize=11,
        color="#c0392b", ha="right")
ax.text(-0.60, 0.58, "圆弧交点（B 读 $0.69\\tau$）", fontsize=10,
        color="0.30", ha="right")

ax.legend(loc="lower left", fontsize=9.5, framealpha=0.96)
ax.set_title("A 视角（标准闵氏图）：等读数点在双曲线上", fontsize=12)

# ======================================================== 右图：对称画法
ax = ax2
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(-1.30, 1.85)
ax.set_ylim(-0.80, 1.72)

aa = (gn + 1) / (gn * vn)          # a
cc = gn * vn / (gn + 1)            # c = 1/a
alpha = np.arctan((1 + cc) / 4)    # 取光锥呈 45 度的对称画法
ut = np.array([np.sin(alpha), np.cos(alpha)])
utp = np.array([-np.sin(alpha), np.cos(alpha)])
ux = np.array([aa * np.sin(alpha), cc * np.cos(alpha)])
uxp = np.array([aa * np.sin(alpha), -cc * np.cos(alpha)])

# 一致性核验：同一事件用两套坐标画到纸面同一点
Lam = np.array([[gn, gn * vn], [gn * vn, gn]])
MA = np.column_stack([ut, ux])
MB = np.column_stack([utp, uxp])
print("对称画法一致性（M_A = M_B * Lambda）:", np.allclose(MA, MB @ Lam))

L = 1.55
for uu, lab, off in [(ut, "$t$", (0.07, 0.01)), (utp, "$t'$", (-0.30, 0.01)),
                     (ux, "$x$", (0.03, 0.10)), (uxp, "$x'$", (0.03, -0.24))]:
    ax.annotate("", xy=L * uu, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="k", lw=1.3), zorder=3)
    ax.text(L * uu[0] + off[0], L * uu[1] + off[1], lab, fontsize=13)
ax.text(-0.26, -0.10, "$O$", fontsize=12)

th = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(th), np.sin(th), ":", color="0.40", lw=1.7,
        label="等读数圆（两轴同比例）", zorder=1)

Mt, Mtp = ut.copy(), utp.copy()
Mp, Mpb = gn * ut, gn * utp

ax.plot([Mtp[0], Mtp[0] + 0.85 * ux[0]], [Mtp[1], Mtp[1] + 0.85 * ux[1]],
        "--", color="#c0392b", lw=1.2, label="A 的同时线（$\\parallel\\,x$）", zorder=2)
ax.plot([Mt[0], Mt[0] - 0.85 * uxp[0]], [Mt[1], Mt[1] - 0.85 * uxp[1]],
        "--", color="#2e8b57", lw=1.2, label="B 的同时线（$\\parallel\\,x'$）", zorder=2)

ax.plot(*Mt, "o", color="k", ms=6, zorder=5)
ax.plot(*Mtp, "o", color="#c0392b", ms=6, zorder=5)
ax.plot(*Mp, "s", color="#c0392b", mfc="white", mec="#c0392b", ms=7, zorder=5)
ax.plot(*Mpb, "s", color="#2e8b57", mfc="white", mec="#2e8b57", ms=7, zorder=5)

ax.text(Mt[0] + 0.06, Mt[1] - 0.14, "$M_t$（A 读 $\\tau$）", fontsize=11)
ax.text(Mtp[0] - 0.06, Mtp[1] - 0.14, "$M_{t'}$（B 读 $\\tau$）",
        fontsize=11, color="#c0392b", ha="right")
ax.text(Mp[0] + 0.07, Mp[1] - 0.02, "$M'$（A 读 $\\gamma\\tau$）",
        fontsize=11, color="#c0392b")
ax.text(Mpb[0] - 0.07, Mpb[1] - 0.02, "$B$ 的投影（读 $\\gamma\\tau$）",
        fontsize=11, color="#2e8b57", ha="right")

ax.legend(loc="lower left", fontsize=9.5, framealpha=0.96)
ax.set_title("对称画法（两框架同比例）：圆弧法成立", fontsize=12)

plt.tight_layout()
plt.savefig("twins-circle-vs-hyperbola.png", dpi=200, facecolor="white")
print("saved twins-circle-vs-hyperbola.png")
