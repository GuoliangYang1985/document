#!/usr/bin/env python3
"""check_xref.py — 交叉引用体检（规范 §6.6/§13 第 10 项）

检查三类问题：
  1. 引用了但全书未定义的标签（@sec-/@eq-/@tbl-/@prp-/@lem-/@thm-/@cor-/@def-/@cnj-/@fig-）；
     渲染时表现为 "Unable to resolve crossref @xxx"。
  2. 跨文件重复定义的标签（Quarto 会静默取其一或报警告）。
  3. 引用指向 .unnumbered 章（书末附录）内的 sec 标签 —— Quarto 不给不编号的章
     注册 section crossref，即使标签存在也无法解析。此类引用必须改为文字引用。

用法：python tools/check_xref.py [--dry 不适用，本检查只读]
退出码：0 = 无问题，1 = 有问题。
"""
import re
import sys
import glob
import collections
import os

REF_KINDS = ("sec", "eq", "tbl", "prp", "lem", "thm", "cor", "def", "cnj", "fig")
REF_RX = re.compile(
    r"@(" + "|".join(REF_KINDS) + r")-[A-Za-z0-9_-]+")
LABEL_RX = re.compile(r"\{#([A-zA-Z][A-zA-Z0-9_-]*)")
UNNUMBERED_RX = re.compile(r"^#\s+.*\.unnumbered", re.M)

FENCE_RX = re.compile(r"```")

def load_files():
    files = sorted(glob.glob("chapters/*.qmd")) + ["index.qmd"]
    out = {}
    for f in files:
        if not os.path.exists(f):
            continue
        raw = open(f, encoding="utf-8", newline="").read()
        out[f] = raw
    return out

def strip_code_fences(raw):
    """围栏代码块内的 @ 不是引用（如脚本示例）。"""
    parts = FENCE_RX.split(raw)
    return "".join(parts[::2])

def main():
    files = load_files()
    if not files:
        print("未找到章节文件")
        return 1

    labels_in = collections.defaultdict(list)   # 标签 -> [文件]
    unnumbered_secs = set()                    # unnumbered 章内的全部 sec 标签
    problems = 0

    for f, raw in files.items():
        for lab in LABEL_RX.findall(raw):
            labels_in[lab].append(f)
        if UNNUMBERED_RX.search(raw):
            # 该文件是不编号的章（书末附录），其内所有 sec- 标签不可 crossref
            for lab in LABEL_RX.findall(raw):
                if lab.startswith("sec-"):
                    unnumbered_secs.add(lab)

    # 1) 未定义引用
    for f, raw in files.items():
        text = strip_code_fences(raw)
        for m in REF_RX.finditer(text):
            ref = m.group(0)[1:]
            if ref not in labels_in:
                line = text[:m.start()].count("\n") + 1
                print(f"未定义引用 {m.group(0)}  {f}:{line}")
                problems += 1
            elif ref in unnumbered_secs and ref.startswith("sec-"):
                line = text[:m.start()].count("\n") + 1
                print(f"引用不编号章的标签 {m.group(0)}  {f}:{line}"
                      f"（.unnumbered 章不注册 crossref，须改为文字引用）")
                problems += 1

    # 2) 跨文件重复标签
    for lab, fs in sorted(labels_in.items()):
        if len(fs) > 1:
            print(f"重复标签 {lab}  定义于: {', '.join(fs)}")
            problems += 1

    print(f"交叉引用问题合计 {problems} 处。")
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
