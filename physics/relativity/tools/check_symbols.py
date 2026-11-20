# -*- coding: utf-8 -*-
"""数学符号体例检查（对应《书籍规范.md》§7.1）。

十一查（全部机器可判，输出 0 即通过）：
  1. \\vec —— nabla 与向量一律不用箭头体例（向量用 \\mathbf，nabla 不加粗）；
  2. \\boldsymbol{\\nabla} —— nabla 不加粗（Latin Modern Math 下该命令无效）；
  3. \\boldsymbol{拉丁字母} —— \\boldsymbol 对拉丁字母不出粗体，属无效写法；
  4. \\epsilon —— 统一为 \\varepsilon；
  5. \\mathrm{i} —— 虚数单位统一斜体 i；
  6. \\mathrm d —— 须写 \\mathrm{d}；
  7. 数学片段内裸微分 d（dt/ds/dx/dy/dz/d^2/d^3/d^4/d\\tau）—— 须 \\mathrm{d}；
  8. \\Gamma^{a}_{bc} —— Christoffel 须用错位指标 \\Gamma^{a}{}_{bc}；
  9. 文本模式的 ⟹ ⟸ ⇒ ⇔ → ← 等符号 —— 正文字体（Latin Modern Roman）无此字形，
     渲染为空白；改用数学模式 $\\Longrightarrow$ $\\rightarrow$ 等；
 10. 对号（$\\checkmark$ / ✓ / ✔ / ☑ / ✗ / ✘）—— 全书不使用，核验结论写成完整陈述句；
 11. 工程验收腔（符号计算／符号核验／simplify／脚本／逐项…相符／与解析式相符／
     输出：／差值…为零／未省略任何项／未引入…近似／验证了…程序的正确性）——
     专著不为自己的闭式作验算声明；闭式的推导链与一致性条件集中列于书末
     「符号与约定」附录的「曲率闭式的推导与一致性」，正文只陈述数学，
     不出现脚本与核验输出。
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = sorted(glob.glob(os.path.join(ROOT, "chapters", "*.qmd"))) + [os.path.join(ROOT, "index.qmd")]

CHECKS = [
    ("vec", re.compile(r"\\vec(?![a-zA-Z])"), r"\\vec —— 向量不用箭头，改 \\mathbf；nabla 改裸 \\nabla"),
    ("boldsymbol nabla", re.compile(r"\\boldsymbol\s*\{?\\nabla\}?"), "nabla 不加粗，改裸 \\nabla"),
    ("boldsymbol 拉丁", re.compile(r"\\boldsymbol\s*\{([a-zA-Z])\}"), r"\boldsymbol 对拉丁字母无效，改 \mathbf"),
    ("epsilon", re.compile(r"\\epsilon(?![a-zA-Z])"), r"统一为 \varepsilon"),
    ("mathrm{i}", re.compile(r"\\mathrm\{i\}"), "虚数单位统一斜体 i"),
    ("mathrm d", re.compile(r"\\mathrm d(?![a-zA-Z])"), r"写 \mathrm{d}"),
    ("Gamma 未错位", re.compile(r"\\Gamma\^\{[^{}]+\}_\{"), r"Christoffel 用错位指标 \Gamma^{a}{}_{bc}"),
]
RX_BARE_D = re.compile(
    r"(?<![\\A-Za-z])d(?=[tsxyz](?![A-Za-z])|\\tau(?![A-Za-z])|\^\{?[234]\}?(?![A-Za-z0-9]))")
RX_TEXT_SYMBOL = re.compile(r"[⟹⟸⟺⇒⇐⇔→←↔]")
RX_CHECKMARK = re.compile(r"\\checkmark|[✓✔☑✗✘]")
RX_CODE = re.compile(r"`[^`]*`")
# 第十一查：工程验收腔。专著不为闭式作验算声明，正文只陈述数学；
# 闭式推导链与一致性条件集中在书末「符号与约定」附录。
RX_VERIFY_BOILERPLATE = re.compile(
    r"符号(?:计算|核验)|simplify|脚本|"
    r"(?:逐项|符号|全部|16 个分量).{0,8}(?:核验)?相符|"
    r"与解析式相符|输出：|"
    r"差值.{0,6}为零|未省略任何项|未引入.{0,2}近似|"
    r"验证了.{0,12}程序的正确性")

hits = []
for fp in FILES:
    t = io.open(fp, encoding="utf-8").read()
    rel = os.path.relpath(fp, ROOT)
    lines = t.split("\n")
    for i, line in enumerate(lines, 1):
        for tag, rx, msg in CHECKS:
            m = rx.search(line)
            if m:
                hits.append("%s:%d  %s  | %s" % (rel, i, msg, line.strip()[:60]))
    # 裸微分只在数学片段内查
    depth_math = False
    for i, line in enumerate(lines, 1):
        s = line
        while s:
            if not depth_math:
                j = s.find("$")
                if j < 0:
                    break
                depth_math = True
                s = s[j + 2:] if s.startswith("$$", j) else s[j + 1:]
            else:
                j = s.find("$")
                seg = s if j < 0 else s[:j]
                for m in RX_BARE_D.finditer(seg):
                    hits.append("%s:%d  裸微分 d 须 \\mathrm{d}  | %s" % (rel, i, seg[max(0, m.start() - 18):m.end() + 10].strip()))
                if j < 0:
                    break
                depth_math = False
                s = s[j + 2:] if s.startswith("$$", j) else s[j + 1:]

    # 第九查：文本模式（数学片段与代码 span 之外）的特殊符号 —— 正文字体缺字
    depth_math = False
    for i, line in enumerate(lines, 1):
        s = line
        while s:
            if not depth_math:
                j = s.find("$")
                seg = s if j < 0 else s[:j]
                seg = RX_CODE.sub("", seg)
                for m in RX_TEXT_SYMBOL.finditer(seg):
                    hits.append(
                        "%s:%d  文本模式符号 %s 缺字（正文字体无此字形），改数学模式 $\\Longrightarrow$/ $\\rightarrow$  | %s"
                        % (rel, i, m.group(), seg[max(0, m.start() - 15):m.end() + 12].strip()))
                if j < 0:
                    break
                depth_math = True
                s = s[j + 2:] if s.startswith("$$", j) else s[j + 1:]
            else:
                j = s.find("$")
                if j < 0:
                    break
                depth_math = False
                s = s[j + 2:] if s.startswith("$$", j) else s[j + 1:]

    # 第十查：对号一律不使用（含数学模式 $\checkmark$）—— 核验结论写成完整陈述句
    for i, line in enumerate(lines, 1):
        for m in RX_CHECKMARK.finditer(line):
            hits.append("%s:%d  不使用对号 %s，核验结论写成完整陈述句  | %s"
                        % (rel, i, m.group(), line.strip()[:60]))

    # 第十一查：工程验收腔 —— 符号计算/脚本/核验输出/逐项相符等一律不出现在正文
    for i, line in enumerate(lines, 1):
        for m in RX_VERIFY_BOILERPLATE.finditer(line):
            hits.append("%s:%d  工程验收腔 %s，改陈述数学（推导链见书末附录）  | %s"
                        % (rel, i, m.group(), line.strip()[:60]))

for h in hits:
    print(h)
print("\n合计 %d 处。" % len(hits))
sys.exit(1 if hits else 0)
