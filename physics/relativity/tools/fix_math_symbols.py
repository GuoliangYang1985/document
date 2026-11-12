# -*- coding: utf-8 -*-
"""数学符号体例统一（对应《书籍规范.md》§7.1）。

六类修正：
  1. \\vec\\nabla / \\boldsymbol{\\nabla}  ->  \\nabla        （nabla 不加粗，ISO 80000-2）
  2. \\epsilon -> \\varepsilon                            （与全书 118 处 \\varepsilon 统一）
  3. \\mathrm{i} -> i                                     （虚数单位统一斜体）
  4. 数学片段内裸微分 d -> \\mathrm{d}（dt/ds/dx/dy/dz/d\\tau/d^4x/dS/d\\Omega）
  5. \\Gamma^{a}_{bc} -> \\Gamma^{a}{}_{bc}                （Christoffel 错位指标）
  6. X^{a}_{\\ b} -> X^{a}{}_{b}                          （张量手动空格错位 -> 空组错位）

用法：python tools/fix_math_symbols.py --dry   先看 diff 计数
      python tools/fix_math_symbols.py --apply 落盘
幂等：apply 后重跑命中为 0。
"""
import glob
import io
import os
import re
import sys

APPLY = "--apply" in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = sorted(glob.glob(os.path.join(ROOT, "chapters", "*.qmd"))) + [os.path.join(ROOT, "index.qmd")]

STAT = {}

def bump(k, n=1):
    STAT[k] = STAT.get(k, 0) + n

RX_VEC = re.compile(r"\\vec\s*\{?\\nabla\}?|\\boldsymbol\s*\{\\nabla\}")
RX_EPS = re.compile(r"\\epsilon(?![a-zA-Z])")
RX_MI = re.compile(r"\\mathrm\{i\}")
RX_MDS = re.compile(r"\\mathrm d(?![a-zA-Z])")
# 裸微分：d 后跟 t/s/x/y/z（后界非字母）、\tau、或 d^2/d^3/d^4 微分元；前面不是字母/反斜杠
RX_BARE_D = re.compile(
    r"(?<![\\A-Za-z])d(?=[tsxyz](?![A-Za-z])|\\tau(?![A-Za-z])|\^\{?[234]\}?(?![A-Za-z0-9]))")
# \frac{d}{d...} 孤立微分（固定串，避免误伤 aligned/标签/变量 d）
RX_FRAC_D = re.compile(
    r"\\frac\{d(\^\{2\})?\}\{(d\\tau(?:\^\{[^{}]+\})?|ds|dt)\}")
RX_GAMMA = re.compile(r"(\\Gamma\^\{[^{}]+\})_\{")
RX_STAG = re.compile(r"\^\{([A-Za-z0-9]+)\}_\{\\ +([^{}]+)\}")

def fix_text(t):
    # 1. nabla 不加粗
    t, n = RX_VEC.subn(r"\\nabla", t)
    bump("nabla 去粗（vec/boldsymbol）", n)
    # 2. epsilon -> varepsilon
    t, n = RX_EPS.subn(r"\\varepsilon", t)
    bump("epsilon -> varepsilon", n)
    # 3. mathrm{i} -> i
    t, n = RX_MI.subn("i", t)
    bump("mathrm{i} -> i", n)
    # 3b. mathrm d -> mathrm{d}
    t, n = RX_MDS.subn(r"\\mathrm{d}", t)
    bump("mathrm d -> mathrm{d}", n)
    # 4b. \frac{d}{d...} 孤立微分
    t, n = RX_FRAC_D.subn(r"\\frac{\\mathrm{d}\1}{\\mathrm{d}\2}", t)
    bump("frac 孤立 d -> mathrm{d}", n)
    # 5. Gamma 错位
    t, n = RX_GAMMA.subn(r"\1{}_{", t)
    bump("Gamma 错位指标", n)
    # 6. 手动空格错位 -> 空组
    t, n = RX_STAG.subn(r"^\{\1\}_\{\2\}", t)
    bump("手动空格错位 -> 空组", n)
    # 4. 裸微分（只在数学片段内）
    n_total = 0
    out = []
    i = 0
    L = len(t)
    while i < L:
        ch = t[i]
        if ch == "`":  # 行内代码原样保留
            j = t.find("`", i + 1)
            j = L - 1 if j < 0 else j
            out.append(t[i:j + 1])
            i = j + 1
            continue
        if ch == "$":
            if t.startswith("$$", i):
                j = t.find("$$", i + 2)
                j = L if j < 0 else j + 2
            else:
                # 行内 $：到下一个未转义的 $
                j = i + 1
                while j < L:
                    if t[j] == "\\":
                        j += 2
                        continue
                    if t[j] == "$":
                        break
                    j += 1
                j = min(j + 1, L)
            seg = t[i:j]
            seg, n = RX_BARE_D.subn(r"\\mathrm{d}", seg)
            n_total += n
            out.append(seg)
            i = j
            continue
        out.append(ch)
        i += 1
    bump("裸微分 d -> mathrm{d}", n_total)
    return "".join(out)

for fp in FILES:
    raw = io.open(fp, encoding="utf-8", newline="").read()
    fixed = fix_text(raw)
    if fixed != raw:
        print("%-46s" % os.path.relpath(fp, ROOT), end=" ")
        if APPLY:
            io.open(fp, "w", encoding="utf-8", newline="\n").write(fixed)
            print("written")
        else:
            print("pending")
    else:
        print("%-46s (no change)" % os.path.relpath(fp, ROOT))

print()
for k in sorted(STAT):
    print("%6d  %s" % (STAT[k], k))
