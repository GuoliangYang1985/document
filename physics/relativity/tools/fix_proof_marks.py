"""统一证明段：头部去句点 + 证明末加 Halmos 符号 □（\\square）。

- 文本收尾：句末标点后接 `$\\quad\\square$`
- 显示公式收尾：公式末行标点后接 ` \\quad\\square`（块内）
- 代码块/表格收尾：`$\\square$` 单独成段置于其后
- `**证明.**` / `**证明（…）.**` → 去句点
- 既有 `$\\blacksquare$` → `$\\quad\\square$`

用法：--dry 预览；--apply 落盘。幂等。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv

TEXT = [
    ("chapters/clock-coupling.qmd", 45, 65),
    ("chapters/clock-coupling.qmd", 402, 410),
    ("chapters/clock-coupling.qmd", 494, 508),
    ("chapters/clock-coupling.qmd", 550, 563),
    ("chapters/flat-space-gravity.qmd", 143, 173),
    ("chapters/flat-space-gravity.qmd", 253, 270),
    ("chapters/flat-space-gravity.qmd", 306, 487),
    ("chapters/flat-space-gravity.qmd", 561, 608),
    ("chapters/flat-space-gravity.qmd", 654, 685),
    ("chapters/flat-space-gravity.qmd", 707, 738),
    ("chapters/flat-space-gravity.qmd", 785, 812),
    ("chapters/flat-space-gravity.qmd", 849, 849),
    ("chapters/flat-space-gravity.qmd", 863, 863),
    ("chapters/galilean-electrodynamics.qmd", 91, 91),
    ("chapters/galilean-electrodynamics.qmd", 151, 151),
    ("chapters/galilean-electrodynamics.qmd", 228, 244),
    ("chapters/galilean-electrodynamics.qmd", 258, 265),
    ("chapters/galilean-electrodynamics.qmd", 283, 283),
    ("chapters/invariant-speed-field.qmd", 71, 77),
    ("chapters/invariant-speed-geometry.qmd", 36, 50),
    ("chapters/quantum-phase.qmd", 227, 227),
    ("chapters/quantum-phase.qmd", 292, 338),
    ("chapters/quantum-phase.qmd", 465, 474),
    ("chapters/twins-comparison.qmd", 133, 161),
    ("chapters/twins-comparison.qmd", 194, 211),
    ("chapters/twins-comparison.qmd", 360, 362),
    ("chapters/twins-comparison.qmd", 469, 485),
    ("chapters/twins-noninertial.qmd", 43, 43),
    ("chapters/twins-noninertial.qmd", 52, 54),
    ("chapters/twins-noninertial.qmd", 84, 84),
    ("chapters/twins-noninertial.qmd", 86, 86),
    ("chapters/twins-noninertial.qmd", 141, 141),
    ("chapters/twins-noninertial.qmd", 264, 266),
    ("chapters/twins-noninertial.qmd", 284, 291),
    ("chapters/two-source-field.qmd", 218, 288),
    ("chapters/two-source-field.qmd", 714, 732),
]
DISP = [
    ("chapters/clock-coupling.qmd", 260, 275),
    ("chapters/galilean-electrodynamics.qmd", 127, 132),
    ("chapters/two-source-field.qmd", 150, 192),
]
INSERT = [
    ("chapters/quantum-phase.qmd", 68, "```\n\n### 不变量的个数", "```\n\n$\\square$\n\n### 不变量的个数"),
    ("chapters/quantum-phase.qmd", 421, "| **不可以**（超选择） |\n\n### 位置–动量对易关系的导出",
     "| **不可以**（超选择） |\n\n$\\square$\n\n### 位置–动量对易关系的导出"),
]
QED = "$\\quad\\square$"
OK_TAIL = "。．.，,；;：:！？）》」'”"


def main():
    counts = {"text": 0, "disp": 0, "insert": 0, "sq": 0, "head": 0}
    cache = {}

    def load(fp):
        if fp not in cache:
            cache[fp] = io.open(os.path.join(ROOT, fp), encoding="utf-8").read().split("\n")
        return cache[fp]

    for fp, s, e in TEXT:
        lines = load(fp)
        assert re.match(r"^\*\*证明", lines[s - 1]), (fp, s, lines[s - 1][:40])
        tail = lines[e - 1].rstrip()
        if QED in tail:
            counts["text"] += 1
            continue
        assert tail and tail[-1] in OK_TAIL, (fp, e, tail[-30:])
        assert "\\square" not in tail, (fp, e, tail[-30:])
        lines[e - 1] = tail + QED
        counts["text"] += 1
        print("text  %-38s %4d  ...%s%s" % (fp.split("/")[-1], e, tail[-34:], QED))

    for fp, s, e in DISP:
        lines = load(fp)
        assert re.match(r"^\*\*证明", lines[s - 1]), (fp, s, lines[s - 1][:40])
        tail = lines[e - 1].rstrip()
        if tail.endswith("\\square"):
            counts["disp"] += 1
            continue
        assert tail[-1] in ".。，,；;，", (fp, e, tail[-30:])
        lines[e - 1] = tail + " \\quad\\square"
        counts["disp"] += 1
        print("disp  %-38s %4d  ...%s \\quad\\square" % (fp.split("/")[-1], e, tail[-34:]))

    for fp, s, old, new in INSERT:
        t = "\n".join(load(fp))
        c = t.count(old)
        assert c == 1, (fp, s, old[:30], c)
        if new in t:
            counts["insert"] += 1
            continue
        if APPLY:
            cache[fp] = t.replace(old, new).split("\n")
        counts["insert"] += 1
        print("insert %-38s @%d  %s" % (fp.split("/")[-1], s, old[:28].replace("\n", "|")))

    for fp in ("chapters/acc-source.qmd",):
        lines = load(fp)
        for i, l in enumerate(lines):
            if "$\\blacksquare$" in l:
                assert "。$\\blacksquare$" in l, (fp, i + 1)
                lines[i] = l.replace("。$\\blacksquare$", "。" + QED)
                counts["sq"] += 1
                print("sq    %-38s %4d" % (fp.split("/")[-1], i + 1))

    RX = re.compile(r"\*\*证明((?:（[^*]*）)?)\.\*\*")
    for fp in sorted(cache):
        lines = cache[fp]
        for i, l in enumerate(lines):
            if RX.search(l):
                counts["head"] += len(RX.findall(l))
                lines[i] = RX.sub(r"**证明\1**", l)
                print("head  %-38s %4d  %s" % (fp.split("/")[-1], i + 1, lines[i][:44]))

    print("\nplan:", counts, "TOTAL", sum(counts.values()))
    if not APPLY:
        print("(dry run; --apply to write)")
        return
    for fp, lines in cache.items():
        p = os.path.join(ROOT, fp)
        data = "\n".join(lines)
        io.open(p, "w", encoding="utf-8", newline="\n").write(data)
    print("written:", ", ".join(sorted(cache)))


if __name__ == "__main__":
    main()
