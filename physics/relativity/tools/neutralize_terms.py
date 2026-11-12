# -*- coding: utf-8 -*-
"""把带倾向词（退化/塌缩等）改为中性、可核对的描述。
每条替换都显式给出期望出现次数，不匹配即报错，不做静默跳过。
"""
import io, os, sys

PAIRS = [
    # 第 3 章 恒速群
    ("chapters/invariant-speed-group.qmd", "（$K$ 有限者彼此同构，$K=\\infty$ 与 $K=0$ 为两种退化情形）",
     "（$K$ 有限者彼此同构，$K=\\infty$ 与 $K=0$ 是参数区间的两个端点）", 1),
    ("chapters/invariant-speed-group.qmd", "变换退化为恒等。", "变换成为恒等变换。", 1),
    ("chapters/invariant-speed-group.qmd", "光锥退化为时间轴方向", "光锥成为时间轴方向", 1),
    ("chapters/invariant-speed-group.qmd", "且其不变量退化得更彻底。", "且其不变量的秩更低。", 1),
    ("chapters/invariant-speed-group.qmd", "选定 $K$ 之后才塌缩到其中一种", "选定 $K$ 之后才取其中一种形式", 1),
    ("chapters/invariant-speed-group.qmd", "$K\\to0$ 对应 Carroll 退化结构。", "$K\\to0$ 对应 Carroll 结构。", 1),
    ("chapters/invariant-speed-group.qmd", "Newton–Cartan 几何（退化度规：时间一形式与空间度规分离）",
     "Newton–Cartan 几何（度规不可逆：时间一形式与空间度规分离）", 1),
    ("chapters/invariant-speed-group.qmd", "于是“构成群”这件事本身退化为逐点成立、跨点不成立",
     "于是“构成群”这件事本身成为逐点成立、跨点不成立", 1),
    ("chapters/invariant-speed-group.qmd", "| $K=\\infty$ 下无事件视界 | 光锥退化，无单向膜 |",
     "| $K=\\infty$ 下无事件视界 | 光锥不界定因果范围，无单向膜 |", 1),
    ("chapters/invariant-speed-group.qmd", "| $0$ | 退化 | —— |", "| $0$ | Carroll 型 | —— |", 1),
    ("chapters/invariant-speed-group.qmd", "| $0$ | $t'=t-\\beta x,\\quad x'=x$ | 退化 | 无传播联系（Carroll 极限） |",
     "| $0$ | $t'=t-\\beta x,\\quad x'=x$ | Carroll 型 | 无传播联系（Carroll 极限） |", 1),
    ("chapters/invariant-speed-group.qmd", "| $0$ | Carroll 型 | 退化 | 退化 | 无 |",
     "| $0$ | Carroll 型 | 未列出 | Carroll 型几何 | 无 |", 1),

    # 第 2 章 平坦空间引力
    ("chapters/flat-space-gravity.qmd", "任一非退化的对称二阶张量", "任一可逆的对称二阶张量", 1),
    ("chapters/flat-space-gravity.qmd", "由于 $\\eta$ 与 $g$ 都非退化", "由于 $\\eta$ 与 $g$ 都可逆", 1),
    ("chapters/flat-space-gravity.qmd", "退化为单个标量方程 $R^{(1)}=0$", "成为单个标量方程 $R^{(1)}=0$", 1),
    ("chapters/flat-space-gravity.qmd", "（在非退化、且不退化到标量方程的意义下）",
     "（在算子可逆、且不落到标量方程的意义下）", 1),
    ("chapters/flat-space-gravity.qmd", "去掉退化情形后", "去掉这两类特殊情形后", 1),

    # 钟耦合
    ("chapters/clock-coupling.qmd", "并给出类别映射 $i\\mapsto f_i$ 的三种退化", "并给出类别映射 $i\\mapsto f_i$ 的三种情形", 1),
    ("chapters/clock-coupling.qmd", "（即 $\\Phi$ 为常数，静态场的退化解）", "（即 $\\Phi$ 为常数）", 1),
    ("chapters/clock-coupling.qmd", "**故除退化情形 $f_i\\equiv1$（等价地 $\\omega_i=dt$）外",
     "**故除 $f_i\\equiv1$（等价地 $\\omega_i=dt$）这一情形外", 1),
    ("chapters/clock-coupling.qmd", "## 三种退化情形 {#sec-cc-degenerations}", "## 三种特殊情形 {#sec-cc-degenerations}", 1),
    ("chapters/clock-coupling.qmd", "一切类别依赖的量都退化。", "一切依赖类别的量都取同一值。", 1),
    ("chapters/clock-coupling.qmd", ": 类别映射的三种退化 {#tbl-degenerations}", ": 类别映射的三种情形 {#tbl-degenerations}", 1),
    ("chapters/clock-coupling.qmd", "| 退化情形 | 余循环平凡性判据 |", "| 特殊情形 | 余循环平凡性判据 |", 1),
    ("chapters/clock-coupling.qmd", "本章的读数 $\\tau_i$ 退化为 $t$ 本身", "本章的读数 $\\tau_i$ 成为 $t$ 本身", 1),

    # 恒速场动力学
    ("chapters/invariant-speed-dynamics.qmd", "### 局域情形（$K$ 为常数）：严格退化", "### 局域情形（$K$ 为常数）：等式严格成立", 1),
    ("chapters/invariant-speed-dynamics.qmd", "**薛定谔方程。** 这一退化是严格的，未作任何近似。",
     "**薛定谔方程。** 这一步是严格的，未作任何近似。", 1),

    # 伽利略电动力学
    ("chapters/galilean-electrodynamics.qmd", "并在速度补偿对象为零时退化为标准麦克斯韦方程组？",
     "并在速度补偿对象为零时成为标准麦克斯韦方程组？", 1),
    ("chapters/galilean-electrodynamics.qmd", "- **(G3) 退化条件**：当补偿速度 $\\mathbf{w}=\\mathbf{0}$ 时，严格退化为 @eq-standard-maxwell。",
     "- **(G3) 取值条件**：当补偿速度 $\\mathbf{w}=\\mathbf{0}$ 时，方程组与 @eq-standard-maxwell 严格相同。", 1),
    ("chapters/galilean-electrodynamics.qmd", "$L$ 退化为纯空间算子", "$L$ 成为纯空间算子", 1),
    ("chapters/galilean-electrodynamics.qmd", "四条方程退化为 $\\mathbb{R}^{3}$ 上的纯空间约束",
     "四条方程成为 $\\mathbb{R}^{3}$ 上的纯空间约束", 1),
    ("chapters/galilean-electrodynamics.qmd", "极限的两个退化版本（电极限、磁极限）", "极限下的两个版本（电极限、磁极限）", 1),

    # 恒速场
    ("chapters/invariant-speed-field.qmd", "$K$ 常数时才退化为常系数方程", "$K$ 常数时才成为常系数方程", 1),
    ("chapters/invariant-speed-field.qmd", "## 退化曲面 {#sec-ifg-interface}", "## 度规不可逆的曲面 {#sec-ifg-interface}", 1),
    ("chapters/invariant-speed-field.qmd", "- $\\Sigma$ 是 $K$ 场的退化水平集；", "- $\\Sigma$ 是 $K$ 场的一个水平集，在其上 $K$ 取 $0$ 或 $\\infty$；", 1),
    ("chapters/invariant-speed-field.qmd", "度规退化；", "度规不可逆；", 1),
    ("chapters/invariant-speed-field.qmd", "**须说明**：这里说的是度规退化，不涉及任何物理判断。",
     "**须说明**：这里说的是度规不可逆（不满秩），不涉及任何物理判断。", 1),

    # 恒速场几何
    ("chapters/invariant-speed-geometry.qmd", "## 退化：回到全局洛伦兹变换 {#sec-isg2-degenerate}",
     "## $K$ 为常数时：回到全局恒速变换 {#sec-isg2-degenerate}", 1),
    ("chapters/invariant-speed-geometry.qmd", "对称群退化为全局的恒速群", "对称群成为全局的恒速群", 1),

    # 记号
    ("chapters/notation.qmd", "按退化边界理解", "按边界点理解", 1),
    ("chapters/notation.qmd", "$K=\\infty$ 时退化为 $\\mathrm{d}t^{2}$", "$K=\\infty$ 时取 $\\mathrm{d}t^{2}$", 1),

    # 导览
    ("chapters/reading-guide.qmd", "$K$ 无梯度时度规退化为 Minkowski", "$K$ 无梯度时度规成为 Minkowski 度规", 1),
    ("chapters/reading-guide.qmd", "当补偿速度取零时退化为标准麦克斯韦方程组", "当补偿速度取零时成为标准麦克斯韦方程组", 1),

    # 量子相位
    ("chapters/quantum-phase.qmd", "### 不变量的退化：从 $1$ 个到 $2$ 个", "### 不变量的个数：从 $1$ 个到 $2$ 个", 1),
    ("chapters/quantum-phase.qmd", "### 零锥的退化", "### 零锥的形状", 1),
    ("chapters/quantum-phase.qmd", "即：**零曲面退化为同时超曲面**", "即：**零曲面成为同时超曲面**", 1),
    ("chapters/quantum-phase.qmd", "取极限后 $\\hat C=m^{2}K^{2}\\to\\infty$ 退化，", "取极限后 $\\hat C=m^{2}K^{2}\\to\\infty$ 不给出有限值，", 1),
    ("chapters/quantum-phase.qmd", "这与第一部分“零锥退化为 $t=$ 常数”相呼应", "这与第一部分“零锥成为 $t=$ 常数”相呼应", 1),
    ("chapters/quantum-phase.qmd", "| 不变量退化为 $\\Delta t$ 与 $\\lvert\\Delta\\mathbf{x}\\rvert$ 两个 |",
     "| 不变量成为 $\\Delta t$ 与 $\\lvert\\Delta\\mathbf{x}\\rvert$ 两个 |", 1),
    ("chapters/quantum-phase.qmd", "| 零锥退化为 $t=$ 常数 |", "| 零锥成为 $t=$ 常数 |", 1),
    ("chapters/quantum-phase.qmd", "$\\hat M=0$ 时退化为 $0$", "$\\hat M=0$ 时为 $0$", 1),

    # 变换推导
    ("chapters/transform-derivation.qmd", "$v = 0$ 时变换退化为恒等", "$v = 0$ 时变换成为恒等变换", 1),
    ("chapters/transform-derivation.qmd", "连续地退化为恒等变换", "连续地趋于恒等变换", 3),
    ("chapters/transform-derivation.qmd", "逐项退化为 @eq-galilean-t 与 @eq-galilean-x", "逐项成为 @eq-galilean-t 与 @eq-galilean-x", 1),
    ("chapters/transform-derivation.qmd", "伽利略群是它在收缩极限下的退化结果", "伽利略群是它在收缩极限下的结果", 1),

    # 双源场
    ("chapters/two-source-field.qmd", "@eq-quadratic 退化为一次方程", "@eq-quadratic 成为一次方程", 1),

    # 配图脚本中的注释与打印（不进入正文）
    ("chapters/images/twins-earth-absolute.py", "退化为水平直线", "在 K->oo 时成为水平直线", 1),
    ("chapters/images/twins-earth-absolute.py", "在 K->oo 时退化为 t = tau（水平直线）", "在 K->oo 时成为 t = tau（水平直线）", 1),
    ("chapters/images/twins-earth-two-branches.py", "等读数线退化为水平直线", "等读数线成为水平直线", 1),
    ("chapters/images/twins-galilean-compare.py", "时双曲线退化为水平直线", "时双曲线成为水平直线", 1),
]

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []
done = 0
for rel, old, new, n in PAIRS:
    p = os.path.join(root, rel)
    s = io.open(p, encoding="utf-8").read()
    c = s.count(old)
    if c != n:
        errors.append("%s  期望 %d 处，实得 %d 处：%s" % (rel, n, c, old[:70]))
        continue
    s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    done += c

print("已替换 %d 处" % done)
for e in errors:
    print("未处理：" + e)
sys.exit(1 if errors else 0)
