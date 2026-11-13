#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""div 配对体检：检查 chapters/*.qmd 与 index.qmd 中 ::: 围栏 div 的开合配对。

规则：
- `::: {#id}` / `::: {.class}` 等带内容的行是"打开"；
- 只有冒号的行（`::: ` 或 `::::`）是"关闭"；
- 冒号可多于三个（`::::`），按普通栈式配对即可（pandoc 语义允许嵌套）；
- 文件结束仍留在栈中的 div 记为"未关闭"；无栈可弹的关闭记为"多余关闭"。

用法：python tools/check_div.py [-v]
"""
import argparse
import glob
import io
import os
import re
import sys

FENCE_RE = re.compile(r"^(:{3,})[ \t]*(.*)$")


def check_file(path, verbose):
    bad = 0
    stack = []
    with io.open(path, encoding="utf-8", newline="") as fh:
        for i, line in enumerate(fh, 1):
            m = FENCE_RE.match(line.rstrip("\n"))
            if not m:
                continue
            rest = m.group(2).strip()
            if rest == "":  # 关闭
                if stack:
                    stack.pop()
                else:
                    print(f"多余关闭:::      {rel(path)}:{i}")
                    bad += 1
            else:  # 打开
                stack.append((i, rest))
    for i, rest in stack:
        print(f"div 未关闭        {rel(path)}:{i}  {rest[:50]}")
        bad += 1
    if verbose:
        print(f"[ok] {rel(path)} div 配对正常" if bad == 0 else f"[!!] {rel(path)} {bad} 处")
    return bad


def rel(path):
    return path.replace(os.sep, "/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    targets = sorted(glob.glob(os.path.join(root, "chapters", "*.qmd")))
    targets += [os.path.join(root, "index.qmd")]

    total = sum(check_file(p, args.verbose) for p in targets)
    print(f"div 配对问题合计 {total} 处。")
    sys.exit(0 if total == 0 else 1)


if __name__ == "__main__":
    main()
