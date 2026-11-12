"""证明段体例检查（规范 §4 证明段条款）。

检查项：
    1. 证明头部格式：只允许 `**证明**`、`**证明（…）**`、`**证明要点**`；
       `**证明.**` 一类带句点的头部判违规；
    2. 禁用结束记号：`证毕`、`\\blacksquare`、`∎`；
    3. 每个证明段区域内必须出现至少一个 `\\square`（Halmos 符号）；
       区域 = 从证明段起到下一个证明段或 1—3 级标题为止；
    4. 孤立 □：出现在任何证明段区域之外的 `\\square` 判提示。

用法：python tools/check_proof.py
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = sorted(glob.glob(os.path.join(ROOT, "chapters", "*.qmd")))

RX_START = re.compile(r"^\*\*证明[^*]*\*\*")
RX_HEAD_OK = re.compile(r"^\*\*证明(?:（[^*]*）)?\*\*|^\*\*证明要点\*\*")
RX_HEADING = re.compile(r"^#{1,3}\s")
hits = []


def add(rule, path, lineno, detail):
    hits.append((rule, os.path.relpath(path, ROOT), lineno, detail))


def main():
    n_proof = 0
    for fp in FILES:
        lines = io.open(fp, encoding="utf-8").read().split("\n")
        i = 0
        while i < len(lines):
            l = lines[i]
            if RX_START.match(l) and not RX_HEAD_OK.match(l):
                add("头部带句点或格式非法", fp, i + 1, l.strip()[:50])
            if RX_START.match(l):
                n_proof += 1
                # 区域：到下一个证明段或 1—3 级标题
                j = i + 1
                while j < len(lines):
                    if RX_START.match(lines[j]) or RX_HEADING.match(lines[j]):
                        break
                    j += 1
                region = "\n".join(lines[i:j])
                if "\\square" not in region:
                    add("证明段无 Halmos 符号", fp, i + 1, lines[i].strip()[:50])
                # 区域外的 \square 由全程扫描兜底
                i = j
                continue
            if re.search(r"证毕|\\blacksquare|∎", l):
                add("禁用结束记号", fp, i + 1, l.strip()[:50])
            i += 1

    # 4. 孤立 □：不在任何证明段区域内
    for fp in FILES:
        lines = io.open(fp, encoding="utf-8").read().split("\n")
        in_proof = False
        for k, l in enumerate(lines):
            if RX_START.match(l):
                in_proof = True
            elif RX_HEADING.match(l) and not l.startswith("####"):
                in_proof = False
            if "\\square" in l and not in_proof:
                add("提示：□ 出现在证明段区域之外", fp, k + 1, l.strip()[:50])

    for rule, path, lineno, detail in hits:
        print("%-28s %s:%d | %s" % (rule, path, lineno, detail))
    print("\n证明段 %d 个，问题 %d 处。" % (n_proof, len(hits)))
    sys.exit(1 if any("提示" not in h[0] for h in hits) else 0)


if __name__ == "__main__":
    main()
