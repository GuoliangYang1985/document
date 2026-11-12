#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""标点体例体检（《书籍规范》§8）。

用法：
    python tools/check_punct.py        # 只报告违规项
    python tools/check_punct.py -v     # 附带命中上下文

退出码：0 = 全部合规；1 = 有违规。
机器可判项见 §8.12。不可判项（括注句号归属、引号内外、引导语通顺度、
式末标点的句读归属（句号还是逗号）、复合专名连接号）需人工复核。
"""
import io
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = sorted(glob.glob(os.path.join(ROOT, "chapters", "*.qmd")))
FILES.append(os.path.join(ROOT, "index.qmd"))

HAN = r"\u4e00-\u9fff"
CJK = "，。；：、？！（）【】《》“”‘’"
VERBOSE = "-v" in sys.argv
hits = []


def add(rule, path, lineno, line="", detail=""):
    hits.append((rule, os.path.relpath(path, ROOT).replace("\\", "/"), lineno, detail, line.strip()[:70]))


def probe_of(line):
    """把行内代码、行内数学、链接目标换成占位符，保留其余字符位置关系。"""
    s = re.sub(r"`[^`\n]*`", "\u0001", line)
    s = re.sub(r"\$[^$\n]*\$", "\u0001", s)
    s = re.sub(r"\]\([^)\n]*\)", "]", s)
    return s


for path in FILES:
    raw = io.open(path, encoding="utf-8", newline="").read()
    lines = raw.split("\n")

    if "\r" in raw:
        add("CRLF 行尾", path, 0)
    if raw.startswith("\n"):
        add("首行空行", path, 1)

    in_code = False
    in_disp = False
    disp_start = 0
    disp_body = []
    quote_depth = 0

    for n, line in enumerate(lines, 1):
        # 行尾 ASCII 空格（不含 NBSP）
        if re.search(r"[ \t]+$", line):
            add("行尾空格", path, n, line)

        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        # ---- 显示公式块 ----
        if not in_disp and line.strip() == "$$":
            in_disp, disp_start, disp_body = True, n, []
            continue
        if in_disp:
            if line.strip().startswith("$$"):
                in_disp = False
                content = [x for x in disp_body if x.strip()]
                if any(not x.strip() for x in disp_body):
                    add("公式块内空行", path, disp_start, "",
                        "pandoc/Quarto 数学解析会在此断开")
                if content:
                    # 居中环境（aligned/cases/…）的 \end 之后标点会悬在块的中线，故标点在环境内末行；
                    # 矩阵（pmatrix 等）的 \end 与末行同基线，标点在其后，不跳过。
                    CENTERED = ("aligned", "gathered", "alignedat", "cases", "split", "array")
                    while content:
                        tail = content[-1]
                        m = re.match(r"^\s*\\end\{([a-zA-Z*]+)\}\s*\}*\s*(?:\\right[.)\]]\s*)?$", tail)
                        if m and m.group(1) in CENTERED:
                            content.pop()
                            continue
                        if re.match(r"^\s*\\right[.)\]]\s*$", tail):
                            content.pop()
                            continue
                        break
                    last = content[-1].rstrip() if content else ""
                    # 证明收尾的 Halmos 符号（§4 证明段）：\quad\square 结尾先剥掉再判
                    last_chk = re.sub(r"\s*\\quad\\square\s*$", "", last)
                    # §8.8(a)：式末必须以半角 . , ; 收束（\right. 的句点是语法符号，不算）
                    if not (last_chk and last_chk[-1] in ".,;" and not last_chk.endswith("\\right.")):
                        add("公式末缺标点", path, n, last, last[-40:])
                    # 半角体例：式末不得再用 \text{。}/\text{，}
                    if re.search(r"\\text\{[。，；]\}\s*$", last):
                        add("式末用全角标点", path, n, last, last[-40:])
                for x in disp_body:
                    bare = re.sub(r"\\text\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", "", x)
                    if re.search(r"[，。；：、？！（）]", bare):
                        add("公式内中文标点", path, disp_start, x, x.strip()[:50])
                disp_body = []
            else:
                disp_body.append(line)
            continue

        p = probe_of(line)

        # ---- 表格行 ----
        s = line.strip()
        if s.startswith("|") and not re.match(r"^\|[\s:\-|]+\|$", s):
            for cell in [c.strip() for c in s.strip("|").split("|")]:
                if cell.endswith(("。", "；", "，")):
                    add("表格单元格末标点", path, n, line, cell[:30])

        # ---- 1 引号体例 ----
        if re.search(r"[「」『』]", p):
            add("直角引号", path, n, line)
        for m in re.finditer(r'"[^"\n]*"', p):
            if re.search("[%s]" % HAN, m.group(0)):
                add("半角引号包中文", path, n, line, m.group(0))

        for ch in p:
            if ch == "“":
                quote_depth += 1
            elif ch == "”":
                quote_depth -= 1
                if quote_depth < 0:
                    add("引号方向反了", path, n, line)
                    quote_depth = 0

        # 引号前多余空格：去掉行首 Markdown 标记后再判
        p2 = re.sub(r"^\s*(#{1,6}|[-*+]|\d+\.|>|:)\s+", "", p, count=1)
        for m in re.finditer(r"(?:[%s。，；：、）】》]|\*\*)[ \t]+“" % HAN, p2):
            add("引号前多余空格", path, n, line, m.group(0))

        # ---- 2 标点连用 ----
        if re.search(r"[。，；：、！？]{2,}", p):
            add("重复标点", path, n, line)
        if re.search(r"[。，；：、][ \t]*[。，；]", p):
            add("标点连用", path, n, line)

        # ---- 3 半角/全角混用、空格 ----
        for m in re.finditer(r"[%s][,;:?!]|[,;:?!][%s]" % (HAN, HAN), p):
            add("中文邻接半角标点", path, n, line, m.group(0))
        for m in re.finditer(r"[%s][ \t]+[%s]|[%s][ \t]+[%s]" % (HAN, CJK, CJK, HAN), p):
            add("汉字与标点间空格", path, n, line, m.group(0))
        if re.search(r"：[ \t]+[%s]" % HAN, p):
            add("冒号后空格", path, n, line)

        # ---- 4 省略号、全角字符、序号 ----
        if "..." in p:
            add("ASCII 省略号", path, n, line)
        if re.search(r"(?<!…)…(?!…)", p):
            add("单字符省略号", path, n, line)
        if re.search(r"[０-９Ａ-Ｚａ-ｚ]", p):
            add("全角数字字母", path, n, line)
        if re.search(r"(?<![A-Za-z0-9_$\u0001])\([0-9]{1,2}\)", p) and not re.match(r"^\s*[-*+]\s", line):
            add("行文序号用半角括号", path, n, line)

        # ---- 5 破折号、范围号 ----
        if re.search(r"[：，][ \t]*——|——[ \t]*[：，]", p):
            add("标点与破折号连用", path, n, line)
        if re.search(r"第[ \t]*\d+[ \t]*[-~][ \t]*\d+[ \t]*[章节]", p):
            add("范围号用 - 或 ~", path, n, line)

    if raw.count("（") != raw.count("）"):
        add("全角括号不配对", path, 0, "", "（ %d / ） %d" % (raw.count("（"), raw.count("）")))
    if quote_depth:
        add("引号未配对", path, 0, "", "差 %d 个" % quote_depth)

    # ---- 6 题注 / 表题 ----
    for m in re.finditer(r"!\[([^\]]*)\]\(", raw):
        cap = m.group(1).rstrip()
        if cap.endswith(("：", ":", "。", ".")):
            add("题注末尾带标点", path, raw[:m.start()].count("\n") + 1, cap, cap[:40])
    for m in re.finditer(r"^[ \t]*:(?!:)[ \t]*(.+?)[ \t]*(?:\{#tbl-[^}]*\})?[ \t]*$", raw, re.M):
        if m.group(1).rstrip().endswith(("：", ":", "。", ".", "，", ",")):
            add("表题末尾带标点", path, raw[:m.start()].count("\n") + 1, m.group(1))

for rule, path, lineno, detail, line in hits:
    if VERBOSE:
        print("%-16s %s:%d | %s | %s" % (rule, path, lineno, detail, line))
    else:
        print("%-16s %s:%d | %s" % (rule, path, lineno, detail))

if hits:
    print("\n合计 %d 处违规（加 -v 看上下文）" % len(hits))
    sys.exit(1)
print("PUNCT OK: 0 处违规")
