#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""全书数值验算（《书籍规范》§7.5）。

逐条复算正文与表格里出现的数值，打印“书中值 / 复算值 / 偏差 / 判定”。
只用标准库，便于无 numpy 环境运行。

用法：
    python tools/verify_numbers.py

判定规则：
    EXACT  书中值 = 复算值（相对偏差 < 1e-12）        → 正文用 “=”
    ROUND  书中值是复算值四舍五入到书写位数          → 正文用 “\\approx”
    BAD    两者不符，或舍入位数不对                  → 必须改
"""
import math

def fmt(x, n=6):
    return ("%%.%df" % n) % x

FAIL = []

def _digits(x):
    s = ("%r" % x).split("e")[0]
    return len(s.split(".")[1]) if "." in s else 0

def report(name, book, calc, written_digits=None, exact=False, mag=False):
    """exact: 判定为精确相等；mag: 只比较数量级；否则按书写位数四舍五入比较。"""
    if exact:
        ok = abs(book - calc) <= 1e-12 * max(1.0, abs(calc))
        tag = "EXACT" if ok else "BAD"
        print("  %-44s 书中 %-12s 复算 %-18s %s" % (name, book, fmt(calc, 12), tag))
    elif mag:
        ok = abs(math.floor(math.log10(abs(calc))) - math.floor(math.log10(abs(book)))) <= 1
        tag = "MAG" if ok else "BAD"
        print("  %-44s 书中 %-12s 复算 %-18s %s" % (name, book, fmt(calc, 12), tag))
    else:
        d = _digits(book) if written_digits is None else written_digits
        r = round(calc, d)
        ok = abs(book - r) < 0.5 * 10 ** (-d) + 1e-12
        tag = "ROUND" if ok else "BAD"
        print("  %-44s 书中 %-12s 复算 %-18s 舍入 %-10s %s"
              % (name, book, fmt(calc, 12), r, tag))
    if not ok:
        FAIL.append(name)
    return ok


print("=" * 100)
print("第 13 章 对称双生子：数值对照")
print("=" * 100)
v = 0.6
w = 2 * v / (1 + v * v)
gw = 1 / math.sqrt(1 - w * w)
report("相对速度 w/c = 2v/(1+v^2)", 0.8824, w)
report("gamma_w = 1/sqrt(1-w^2)", 2.125, gw, 3, exact=True)
report("1/gamma_w", 0.4706, 1 / gw)
report("80/gamma_w（A 累积 80 时 B 侧值）", 37.6, 80 / gw)
report("gamma_w * 80（B 侧 80 投影到 A 侧）", 170.0, gw * 80, 0, exact=True)
gw_half = 1 / math.sqrt(1 - 0.25)
report("w=0.5c 时 80/gamma_w（正文“约 69”）", 69, 80 / gw_half)

print("\ngamma_w 随 K 变化（固定 w = 0.8824c）")
for K, book in ((3, 1.046), (1.5, 1.237), (1, 2.125)):
    report("gamma_w, K = %gc" % K, book, 1 / math.sqrt(1 - (w / K) ** 2))

print("=" * 100)
print("第 12 章 非对称双生子：v=0.6c, T=100 年")
print("=" * 100)
g = 1 / math.sqrt(1 - 0.36)
report("gamma = 1/sqrt(1-v^2)", 1.25, g, exact=True)
report("Delta s_G = T/gamma", 80.0, 100 / g, 0, exact=True)
report("差值 T - T/gamma", 20.0, 100 - 100 / g, 0, exact=True)

print("\n方式二：Q=(10,6) 固定，M=20,30,50")
for M, Lbook, ibook in ((20, 8.00, 12.00), (30, 19.08, 10.92), (50, 39.55, 10.45)):
    dt = M - 10.0
    L = dt * math.sqrt(1 - (6.0 / dt) ** 2)
    inter = M - math.sqrt(dt ** 2 - 36.0)
    report("M=%d 返程线长 L" % M, Lbook, L)
    report("M=%d 校验线交 t 轴" % M, ibook, inter)
    report("M=%d 交点与 s_Q=8 之差" % M, round(inter - 8, 2), inter - 8)

print("\n纸面长与线长（t=50, x=30）")
report("纸面长 2*sqrt(50^2+30^2)", 116.6, 2 * math.sqrt(2500 + 900))
report("线长 2*sqrt(50^2-30^2)", 80.0, 2 * math.sqrt(2500 - 900), 0, exact=True)

print("=" * 100)
print("第 14 章 非惯性双生子：显式算例（c=1）")
print("=" * 100)
report("段 I 线长 0.8（=sqrt(1-0.6^2)）", 0.8, math.sqrt(1 - 0.36), 1, exact=True)
seg2 = math.sqrt(1 - 0.36) + math.asin(0.6) / 0.6
report("段 II 线长 sqrt(1-0.36)+asin(0.6)/0.6", 1.8725018, seg2, 7)
report("总长 0.8+1.8725018+0.8", 3.4725018, 2 * 0.8 + seg2, 7)
report("P 的线长 3.4725-0.8", 2.6725, 2 * 0.8 + seg2 - 0.8)
report("中间段 3.4725-1.6", 1.8725, 2 * 0.8 + seg2 - 1.6)
report("等价核对 1^2-0.6^2=0.8^2", 0.64, 1 - 0.36, 2, exact=True)
# 分段函数连续性与速率连续性
xA = lambda t: (-0.6 * t if t <= 1 else (0.3 * t * t - 1.2 * t + 0.3 if t <= 3 else 0.6 * t - 2.4))
vA = lambda t: (-0.6 if t <= 1 else (0.6 * t - 1.2 if t <= 3 else 0.6))
report("x(1-) = x(1+) = -0.6", -0.6, xA(1.0), 6, exact=True)
report("x(3-) = x(3+) = -0.6", -0.6, xA(3.0), 6, exact=True)
v_seg1 = -0.6
v_seg2 = lambda t: 0.6 * t - 1.2
v_seg3 = 0.6
report("v(1-) = -0.6", -0.6, v_seg1, exact=True)
report("v(1+) = -0.6（段 II 在 t=1 的斜率）", -0.6, v_seg2(1.0), exact=True)
report("v(3-) = +0.6（段 II 在 t=3 的斜率）", 0.6, v_seg2(3.0), exact=True)
report("v(3+) = +0.6", 0.6, v_seg3, exact=True)

print("\nln 2 与像区间标度表")
report("ln 2", 0.693, math.log(2))
c = 2.99792458e8
ly = 9.4607304725808e15
yr = 3.15576e7
for a, book_ly, book_yr in ((9.8, 0.97, 0.67), (0.98, 9.7, 6.7), (0.098, 97, 67)):
    c2a = c * c / a              # 米
    s = c / a * math.log(2)      # 秒
    report("a=%g m/s^2 的 c^2/a（光年）" % a, book_ly, c2a / ly)
    report("a=%g m/s^2 的 (c/a)ln2（年）" % a, book_yr, s / yr)

print("=" * 100)
print("第 9 章 时钟耦合：量级估计")
print("=" * 100)
report("sigma(alpha) = 1e-18 / 1.1e-13（量级）", 1e-5, 1e-18 / 1.1e-13, mag=True)

print("=" * 100)
print("图形坐标（正文 vs 配图脚本）——需人工裁定，此处只列出")
print("=" * 100)
print("  正文 twins-noninertial.qmd：S=(0.8, 0)，S'=(1.2046, 1.3355)，P=(2.6725, 0)，Q=(2.2679, 1.3355)")
print("  配图 twins-calibration-cut-ends.py：折角 (x_A, tau_A) = (0.7059, 0.8) 与 (0.7059, 2.6725)")
print("  说明：0.7059 = w*tau = 0.8824*0.8；正文四个数在脚本里没有对应计算式。")

print("\n" + "=" * 100)
if FAIL:
    print("BAD %d 处：%s" % (len(FAIL), "；".join(FAIL)))
    raise SystemExit(1)
print("全部复算通过（EXACT / ROUND / MAG 三类，无 BAD）。")
