#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""数值体例体检（《书籍规范》§7.5）。

用法：
    python tools/check_numeric.py        # 只报告
    python tools/check_numeric.py -v     # 附带上下文

退出码：0 = 无违规；1 = 有违规。数值本身的算术正确性由 tools/verify_numbers.py 负责，
本脚本只管“该用 \\approx 的地方有没有用 \\approx”。

检查项：
    A. 等号右侧是四舍五入后的十进制，而左侧含根式／对数／分数／π —— 应为 \\approx；
    B. 同一句里“约”与 \\approx 并用 —— 双标记；
    C. 表格含十进制数而题注未声明“近似值”；
    D. \\approx 右侧被写成整数（如 \\approx80）—— 多半是精确值，误加了 \\approx。
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = sorted(glob.glob(os.path.join(ROOT, "chapters", "*.qmd")))
FILES.append(os.path.join(ROOT, "index.qmd"))
VERBOSE = "-v" in sys.argv

IRRATIONAL = r"\\(?:sqrt|arcsin|arccos|arctan|ln|log|pi|frac|dfrac|tfrac)"
# 等号右侧：小数（可能带科学计数法）
NUM_EQ = re.compile(r"=\s*[-+]?\d+\.\d+(?!\d*\.?\d*\{)")
APPROX_EQ = re.compile(r"\\approx\s*[-+]?\d+\.\d")
APPROX_INT = re.compile(r"\\approx\s*[-+]?[1-9]\d{1,}(?![\d.^])")
# “约”与 \approx 贴得太近（同一个小句内）
DOUBLE_MARK = re.compile(r"约[^，。；]{0,10}\\approx|\\approx[^，。；]{0,10}约")

hits = []


def add(rule, path, lineno, detail=""):
    hits.append((rule, os.path.relpath(path, ROOT).replace("\\", "/"), lineno, detail))


for path in FILES:
    lines = io.open(path, encoding="utf-8").read().split("\n")

    for i, line in enumerate(lines, 1):
        code = re.sub(r"`[^`\n]*`", "", line)

        # A. 精确算式配了四舍五入的结果
        for m in NUM_EQ.finditer(code):
            head = code[: m.start()]
            if re.search(IRRATIONAL, head):
                add("提示：A 根式/对数/分数后用了 =（核对是否应为 \\approx）", path, i, head[-40:].strip()[-36:])

        # B. “约”与 \approx 并用（同一个小句内才算）
        for m in DOUBLE_MARK.finditer(code):
            add("B “约”与 \\approx 并用", path, i, m.group(0)[:40])

        # D. \approx 后接整数
        for m in APPROX_INT.finditer(code):
            add("D \\approx 后接整数（疑为精确值）", path, i, code[max(0, m.start() - 20): m.end()].strip()[:60])

    # C. 表格内的十进制数，题注未声明近似
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|"):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            block = lines[i:j]
            k = j
            caption = ""
            while k < len(lines) and not lines[k].strip():
                k += 1
            if k < len(lines) and lines[k].lstrip().startswith(":"):
                caption = lines[k]
            has_dec = any(re.search(r"\d+\.\d", b) and "\\ldots" not in b for b in block)
            if has_dec and "近似" not in caption and "精确" not in caption:
                add("提示：C 表内有小数但题注未声明", path, i + 1, caption.strip()[:50])
            i = j
        else:
            i += 1

if not hits:
    print("数值体例：全部合规。")
    sys.exit(0)

blocking = [h for h in hits if not h[0].startswith("提示")]
for rule, path, lineno, detail in blocking + [h for h in hits if h[0].startswith("提示")]:
    print("%s:%s  %s%s" % (path, lineno, rule, ("  |  " + detail) if detail else ""))
print("\n违规 %d 处，提示 %d 处。" % (len(blocking), len(hits) - len(blocking)))
sys.exit(1 if blocking else 0)
