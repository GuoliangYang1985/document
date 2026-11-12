#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""定理类环境体检（《书籍规范》§4）。

用法：
    python tools/check_theorem_env.py        # 只报告违规项
    python tools/check_theorem_env.py -v     # 附带命中上下文

退出码：0 = 全部合规；1 = 有违规（提示项不影响退出码）。

检查项（违规／提示两级）：
    1. 环境标题含类名（“公理／命题／定理／引理／推论／定义”）——渲染后会重复；
       专名（“Stone 定理”）除外；
    2. 环境内出现解释性语词（“这正是”“也就是说”“由此可见”…）——属说明，应出块；
       公理／定义内为违规；命题／定理／引理／推论内为提示（可能是推导连接词，须人工判断）；
    3. 环境内出现 @sec- 章级引用——同上分级；
    4. 环境末段缺句末标点（末行非公式行时须以 。： 收尾）；
    5. （提示）公理／定义出现两段及以上正文——多半夹带了说明。

不可机器判定的项（陈述是否掺入动机、说明是否复述陈述、必要的记号约定与
评论的界线）须人工复核。
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
KIND = {"cnj": "公理", "prp": "命题", "thm": "定理", "lem": "引理", "cor": "推论", "def": "定义"}
STRICT = ("cnj", "def")

# 解释性语词：出现在环境内即认为混入了说明
EXPLAIN = re.compile(r"这正是|也就是说|换句话说|由此可见|这说明|这解释了|不牵涉|不妨|直观地|读者")
# 标题里不应出现的类名；前面带拉丁字母的专名（Stone 定理）不算
CLASSNAME = re.compile(r"(?<![A-Za-z])(公理|命题|定理|引理|推论|定义)")
PROPER = re.compile(r"[A-Za-z][A-Za-z\s]*\s(公理|命题|定理|引理|推论|定义)")

hits = []


def add(rule, path, lineno, detail=""):
    hits.append(
        (rule, os.path.relpath(path, ROOT).replace("\\", "/"), lineno, detail)
    )


def body_blocks(body):
    """把环境正文按空行切段；公式块整体算一段。"""
    blocks, cur, in_disp = [], [], False
    for line in body:
        if line.strip().startswith("$$"):
            in_disp = not in_disp
            cur.append(line)
            if not in_disp:
                blocks.append(cur)
                cur = []
            continue
        if in_disp:
            cur.append(line)
        elif line.strip():
            cur.append(line)
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    return blocks


def is_formula_block(block):
    return block and block[0].strip().startswith("$$")


for path in FILES:
    raw = io.open(path, encoding="utf-8", newline="").read()
    lines = raw.split("\n")
    n = 0
    while n < len(lines):
        m = re.match(r"^(:::+)\s*\{#(cnj|prp|thm|lem|cor|def)-([A-Za-z0-9-]+)\}", lines[n])
        if not m:
            n += 1
            continue
        fence, kind, label = m.group(1), m.group(2), m.group(3)
        start = n + 1
        j = start
        while j < len(lines) and lines[j].rstrip() != fence:
            j += 1
        body = lines[start:j]

        # 1. 标题
        for k, line in enumerate(body):
            if line.startswith("#"):
                title = line.lstrip("#").strip()
                if CLASSNAME.search(title) and not PROPER.search(title):
                    add("标题含类名", path, start + k + 1, "%s（%s）" % (title, KIND[kind]))
                break

        # 2/3. 解释词与章级引用（公理／定义为违规，其余为提示）
        for k, line in enumerate(body):
            if line.startswith("#") or line.strip().startswith("$$"):
                continue
            mm = EXPLAIN.search(line)
            if mm:
                tag = "" if kind in STRICT else "提示："
                add(tag + "环境内解释词「%s」" % mm.group(0), path, start + k + 1, "%s-%s" % (kind, label))
            if "@sec-" in line:
                tag = "" if kind in STRICT else "提示："
                add(tag + "环境内章级引用", path, start + k + 1, "%s-%s" % (kind, label))

        # 4. 末段标点
        blocks = body_blocks(body)
        if blocks:
            last = [l for l in blocks[-1] if l.strip()]
            tail = last[-1].strip() if last else ""
            if tail and not is_formula_block(blocks[-1]):
                if not re.search(r"[。：！？]|\\end\{[a-zA-Z*]+\}[,;.]?$|\$\$.*[,;.]$", tail):
                    if not tail.endswith("$$") and not re.search(r"[,;.]\s*$", tail):
                        add("末段缺句末标点", path, start + len(body), "%s-%s：…%s" % (kind, label, tail[-24:]))

        # 5. 公理／定义多段
        if kind in ("cnj", "def"):
            paras = [b for b in blocks if not b[0].startswith("#")]
            if len(paras) >= 2:
                add("提示：公理／定义多段", path, start + 1, "%s-%s（%d 段）" % (kind, label, len(paras)))

        n = j + 1

if not hits:
    print("定理类环境：全部合规。")
    sys.exit(0)

hard = [h for h in hits if not h[0].startswith("提示")]
soft = [h for h in hits if h[0].startswith("提示")]
for title, group in (("违规", hard), ("提示", soft)):
    if not group:
        continue
    print("== %s（%d）==" % (title, len(group)))
    for rule, path, lineno, detail in group:
        print("  %s:%s  %s%s" % (path, lineno, rule, ("  " + detail) if detail else ""))
sys.exit(1 if hard else 0)
