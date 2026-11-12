# -*- coding: utf-8 -*-
"""数学符号体例检查（对应《书籍规范.md》§7.1）。

八查（全部机器可判，输出 0 即通过）：
  1. \\vec —— nabla 与向量一律不用箭头体例（向量用 \\mathbf，nabla 不加粗）；
  2. \\boldsymbol{\\nabla} —— nabla 不加粗（Latin Modern Math 下该命令无效）；
  3. \\boldsymbol{拉丁字母} —— \\boldsymbol 对拉丁字母不出粗体，属无效写法；
  4. \\epsilon —— 统一为 \\varepsilon；
  5. \\mathrm{i} —— 虚数单位统一斜体 i；
  6. \\mathrm d —— 须写 \\mathrm{d}；
  7. 数学片段内裸微分 d（dt/ds/dx/dy/dz/d^2/d^3/d^4/d\\tau）—— 须 \\mathrm{d}；
  8. \\Gamma^{a}_{bc} —— Christoffel 须用错位指标 \\Gamma^{a}{}_{bc}。
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

for h in hits:
    print(h)
print("\n合计 %d 处。" % len(hits))
sys.exit(1 if hits else 0)
