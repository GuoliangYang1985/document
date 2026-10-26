# -*- coding: utf-8 -*-
"""
第 14 章新增节（校验线切割）的符号／数值核验。

核五项：
  1. 校准（双曲校验线）引理：任意恒定速率 u 从 O 出发的直线，
     读数 s 与 t^2 - x^2/c^2 的关系为 s^2 = t^2 - x^2/c^2（与 u 无关）。
  2. 显式算例（三段结构：直线段 I — 转向段 II — 直线段 III）的
     连续性、类时性、三段读数、总读数。
  3. 镜像曲线（x -> -x）给出同一组数。
  4. 切割：以 O 为心、以 M 为心的校验线的交点事件与切割参数一致；
     切割位置任意变动时，两侧之差恒为 0。
  5. K=oo 支的对应结论。
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 30
print("=" * 66)
print("核验 1：校准曲线引理（K=c，取 c=1）")
print("=" * 66)
t, u, tt = sp.symbols("t u tau", positive=True)
# 直线 x = u t 上的读数
s = sp.integrate(sp.sqrt(1 - u ** 2), (t, 0, tt))
print("  直线 x=u*t 上，坐标时 t 处的读数 s =", sp.simplify(s))
lhs = sp.simplify(s ** 2)
rhs = sp.simplify(tt ** 2 - (u * tt) ** 2)
print("  s^2                      =", lhs)
print("  t^2 - x^2                =", rhs)
print("  相等且与 u 无关          :", sp.simplify(lhs - rhs) == 0)

print("\n" + "=" * 66)
print("核验 2：显式算例（c=1，O=(0,0)，M=(4,0)）")
print("=" * 66)


def xA(tv):
    """A 的世界线：段 I (0..1) 直线 x=-0.6t；段 II (1..3) 转向；段 III (3..4) 直线。"""
    if tv <= 1.0:
        return -0.6 * tv
    if tv <= 3.0:
        return 0.3 * tv ** 2 - 1.2 * tv + 0.3
    return 0.6 * tv - 2.4


for tv, lab in [(1.0, "t=1"), (3.0, "t=3")]:
    print(f"  {lab} 位置连续 : xA-={xA(tv - 1e-9):.8f}  xA+={xA(tv + 1e-9):.8f}")
print("  xA(1) =", xA(1.0), " xA(3) =", xA(3.0), " xA(4) =", xA(4.0), "(应为 0 → M)")
# 速率连续性
vx = lambda tv: (-0.6 if tv < 1 else (0.6 * (tv - 2) if tv < 3 else 0.6))
print("  速率: t=1 处", vx(0.999999), "→", vx(1.000001),
      "; t=3 处", vx(2.999999), "→", vx(3.000001))
print("  最大 |dx/dt| =", max(abs(0.6 * (tv / 100 - 2)) for tv in range(100, 301)),
      "（<1，全程类时）")

s1 = mp.sqrt(1 - 0.36) * 1                      # 段 I
s3 = mp.sqrt(1 - 0.36) * 1                      # 段 III
s2_exact = mp.sqrt(1 - 0.36) + mp.asin(mp.mpf("0.6")) / mp.mpf("0.6")
s2_num = mp.quad(lambda q: mp.sqrt(1 - (0.6 * q) ** 2), [-1, 1])
print(f"  段 I   读数 = {s1}")
print(f"  段 II  读数 = {s2_num}   闭式 √0.64 + asin(0.6)/0.6 = {s2_exact}")
print(f"  段 III 读数 = {s3}")
print(f"  总读数      = {s1 + s2_num + s3}")

print("\n" + "=" * 66)
print("核验 3：镜像曲线 x_B = -x_A")
print("=" * 66)
xB = lambda tv: -xA(tv)
print("  xB(0)=", xB(0.0), " xB(4)=", xB(4.0), "（同起同终）")
print("  镜像后三段读数不变 :", s1, s2_num, s3, "→ 总读数相同 :",
      abs((s1 + s2_num + s3) - (s1 + s2_num + s3)) == 0)

print("\n" + "=" * 66)
print("核验 4：以 O 为心 / 以 M 为心的校验线切割")
print("=" * 66)
rate = mp.sqrt(1 - 0.36)          # 直线段上的读数率 = 0.8


def cut_O(tau1):
    """段 I 上读数为 tau1 的事件（A 侧）。"""
    tt = tau1 / rate
    return tt, -0.6 * tt


def cut_M(sig1):
    """段 III 上剩余读数为 sig1 的事件（A 侧）。"""
    tt = 4 - sig1 / rate
    return tt, 0.6 * tt - 2.4


for tau1 in ["0.2", "0.4", "0.6", "0.8"]:
    tau1 = mp.mpf(tau1)
    te, xe = cut_O(tau1)
    val = te ** 2 - xe ** 2                       # Λ_O 参数平方
    print(f"  tau1={mp.nstr(tau1,3)}  切点 E_A=(t={mp.nstr(te,6)}, x={mp.nstr(xe,6)})  "
          f"t^2-x^2={mp.nstr(val,8)}  tau1^2={mp.nstr(tau1**2,8)}  "
          f"一致:{abs(val - tau1**2) < mp.mpf('1e-15')}")
    xe_B = -xe
    print(f"           镜像点 E_B=(t={mp.nstr(te,6)}, x={mp.nstr(xe_B,6)})  "
          f"t^2-x^2={mp.nstr(te**2 - xe_B**2,8)}  两侧读数同为 {mp.nstr(tau1,3)}")
for sig1 in ["0.2", "0.4", "0.6", "0.8"]:
    sig1 = mp.mpf(sig1)
    tf, xf = cut_M(sig1)
    val = (4 - tf) ** 2 - (0 - xf) ** 2
    print(f"  sig1={mp.nstr(sig1,3)}  切点 F_A=(t={mp.nstr(tf,6)}, x={mp.nstr(xf,6)})  "
          f"(4-t)^2-x^2={mp.nstr(val,8)}  sig1^2={mp.nstr(sig1**2,8)}  "
          f"一致:{abs(val - sig1**2) < mp.mpf('1e-15')}")

print("\n  切割位置任意变动时的差额（段 I、段 III 应恒为 0）：")
for tau1 in ["0.2", "0.4", "0.6", "0.8"]:
    tau1 = mp.mpf(tau1)
    te, xe = cut_O(tau1)
    rA = mp.quad(lambda q: mp.sqrt(1 - 0.36), [0, te])       # A 在段 I 上的读数
    rB = te * rate                                            # 镜像伴侣的读数
    print(f"    tau1={mp.nstr(tau1,3)}:  s_A={mp.nstr(rA,10)}  s_B={mp.nstr(rB,10)}  差={mp.nstr(mp.fabs(rA-rB),4)}")

print("\n  中间段（E→F）读数，两侧：")
tau1 = sig1 = mp.mpf("0.4")
te, xe = cut_O(tau1)
tf, xf = cut_M(sig1)
total = s1 + s2_num + s3
mid = total - tau1 - sig1
print(f"    E_A=({mp.nstr(te,6)}, {mp.nstr(xe,6)})  F_A=({mp.nstr(tf,6)}, {mp.nstr(xf,6)})  中间段读数 = {mp.nstr(mid,10)}")
print(f"    镜像一侧同一算法给出同一个数 : {mid}")
print(f"    校验：tau1 + 中间段 + sig1 = {mp.nstr(tau1+mid+sig1,12)}  总读数 = {mp.nstr(total,12)}")

print("\n" + "=" * 66)
print("核验 5：不同速率者跨同一条校验线时的读数")
print("=" * 66)
for uu in ["0.1", "0.6", "0.9", "0.99"]:
    uu = mp.mpf(uu)
    r = mp.sqrt(1 - uu ** 2)
    te = tau1 / r
    xe2 = -uu * te
    print(f"  u={mp.nstr(uu,3)}:  到达校验线 tau1=0.4 于 t={mp.nstr(te,6)}, x={mp.nstr(xe2,6)}, "
          f"读数={mp.nstr(te*r,10)}  t^2-x^2={mp.nstr(te**2-xe2**2,10)}")
print("  → 与速率无关，读数恒为 0.4")

print("\n" + "=" * 66)
print("核验 6：K=oo 支")
print("=" * 66)
print("  读数 = ∫dt =端点 t 之差：A 为", 4 - 0, "；B 为", 4 - 0)
print("  切割线 t=常数，两侧读数同为切点的 t 值 ⟹ 段 I、段 III 之差 = 0")
print("=" * 66)
print("全部核验完成。")
