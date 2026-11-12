"""证明段结束位置探测：列出每个 **证明** 段的候选结束行，供人工核对。

规则：
- 证明从 `**证明**` 段起；
- 向后逐段走，遇以下新段即停：标题 / ::: 围栏 / 代码围栏 / 表格行 /
  引用块 / 任何以 ** 开头的新标签段 / 列表行；
- 结束行 = 停止前最后一个非空行。
用法：python tools/check_proof.py [--report]
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = sorted(glob.glob(os.path.join(ROOT, "chapters", "*.qmd")))

RX_START = re.compile(r"^\*\*证明[^*]*\*\*")
RX_BADHEAD = re.compile(r"^\*\*证明((（[^*]*）)?)[^*]*\*\*")


def is_stop(line):
    s = line.lstrip()
    return bool(
        re.match(r"^#{1,6}\s", s)
        or s.startswith(":::")
        or s.startswith("```")
        or s.startswith("|")
        or s.startswith(">")
        or s.startswith("**")
        or re.match(r"^(-|\*|\d+[.、)])\s", s)
    )


def main():
    rows = []
    for fp in FILES:
        lines = io.open(fp, encoding="utf-8").read().split("\n")
        i = 0
        while i < len(lines):
            if RX_START.match(lines[i]):
                start = i
                # 向后找结束行
                j = i + 1
                end = i
                while j < len(lines):
                    if is_stop(lines[j]):
                        break
                    if lines[j].strip():
                        end = j
                    j += 1
                rows.append((fp, start, end, lines[end].rstrip()))
                i = j
            else:
                i += 1
    for fp, s, e, tail in rows:
        rel = os.path.relpath(fp, ROOT)
        mark = "HAS" if re.search(r"\\square|\\blacksquare|证毕|∎", tail) else "   "
        print("%-36s %4d -> %4d  %s  ...%s" % (rel, s + 1, e + 1, mark, tail[-52:]))
    print("\n共 %d 个证明段" % len(rows))


if __name__ == "__main__":
    main()
