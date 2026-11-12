# -*- coding: utf-8 -*-
"""把 qmd 正文里写死的「第 N 章」换成动态交叉引用「@sec-xxx 章」。

章号在结构改动后会平移，写死的数字会跟着过期；换成 @sec- 引用后由
Quarto 在渲染时填入实际章号（language.crossref-ch-prefix 已设为「第」）。

用法：python tools/dynref_chapters.py [--check]
      --check 只报告将要替换的处数，不写文件。
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 章号 -> 章级标签（顺序与 _quarto.yml 的 chapters 列表一致）
MAP = {
    1: "sec-transform-derivation",
    2: "sec-invariant-speed-group",
    3: "sec-invariant-speed-field-group",
    4: "sec-invariant-speed-dynamics",
    5: "sec-invariant-speed-geometry",
    6: "sec-quantum-phase",
    7: "sec-maxwell-equations",
    8: "sec-galilean-electrodynamics",
    9: "sec-two-source-field",
    10: "sec-flat-space-gravity",
    11: "sec-clock-coupling",
    12: "sec-twins-comparison",
    13: "sec-twins-noninertial",
    14: "sec-asymmetric-twins",
    15: "sec-layers",
}

# 「第 N 章」里的 N 超出上表即视为未登记，跳过并报告
# 「第 4—6、11 章」：范围之后还跟若干个章号，需在范围规则之前处理
MIXED = re.compile(r"第\s*(\d+)\s*([—–]|-)\s*(\d+)\s*((?:\s*[、,]\s*\d+)+)\s*章")
RANGE = re.compile(r"第\s*(\d+)\s*([—–]|-)\s*(\d+)\s*章")
LIST = re.compile(r"第\s*(\d+(?:\s*[、,]\s*\d+)+)\s*章")
ONE = re.compile(r"第\s*(\d+)\s*章")

# 需要放空格的分隔符（中文标点/@ 前紧邻汉字时 pandoc 解析不稳）
PRE_SPACE = re.compile(r"[^\s\|\(（\[「『，。；：、,.;:]$")


def ref(n):
    return "@" + MAP[n] + " 章"


def join_parts(nums, seps):
    """按原始分隔符拼回引用串。nums 为数字列表，seps 为它们之间的分隔符。"""
    out = [ref(nums[0])]
    for i, s in enumerate(seps):
        out.append(s.strip())
        out.append(ref(nums[i + 1]))
    return "".join(out)


def convert(text):
    total = 0
    unknown = []

    def need_space(pos):
        if pos <= 0:
            return False
        return bool(PRE_SPACE.match(text[pos - 1]))

    def repl_mixed(m):
        nonlocal total
        a, dash, b = int(m.group(1)), m.group(2), int(m.group(3))
        tail = [int(x) for x in re.split(r"\s*[、,]\s*", m.group(4).strip()) if x]
        nums = [a, b] + tail
        if any(n not in MAP for n in nums):
            unknown.append(m.group(0))
            return m.group(0)
        total += 1
        seps = re.findall(r"([、,])", m.group(4))
        s = ref(a) + dash + ref(b)
        for i, n in enumerate(tail):
            s += seps[i] + ref(n)
        return (" " if need_space(m.start()) else "") + s

    text = MIXED.sub(repl_mixed, text)

    def repl_range(m):
        nonlocal total
        a, dash, b = int(m.group(1)), m.group(2), int(m.group(3))
        if a not in MAP or b not in MAP:
            unknown.append(m.group(0))
            return m.group(0)
        total += 1
        s = ref(a) + dash + ref(b)
        return (" " if need_space(m.start()) else "") + s

    text = RANGE.sub(repl_range, text)

    def repl_list(m):
        nonlocal total
        nums = [int(x) for x in re.split(r"\s*[、,]\s*", m.group(1))]
        if any(n not in MAP for n in nums):
            unknown.append(m.group(0))
            return m.group(0)
        total += 1
        seps = re.findall(r"\s*([、,])\s*", m.group(1))
        s = join_parts(nums, seps)
        return (" " if need_space(m.start()) else "") + s

    text = LIST.sub(repl_list, text)

    def repl_one(m):
        nonlocal total
        n = int(m.group(1))
        if n not in MAP:
            unknown.append(m.group(0))
            return m.group(0)
        total += 1
        return (" " if need_space(m.start()) else "") + ref(n)

    text = ONE.sub(repl_one, text)
    return text, total, unknown


def main():
    check = "--check" in sys.argv
    files = [os.path.join(ROOT, "index.qmd")]
    files += sorted(
        os.path.join(ROOT, "chapters", f)
        for f in os.listdir(os.path.join(ROOT, "chapters"))
        if f.endswith(".qmd")
    )
    grand = 0
    for f in files:
        src = io.open(f, encoding="utf-8").read()
        if "章" not in src:
            continue
        new, n, unk = convert(src)
        if n:
            grand += n
            print("%-46s %d 处" % (os.path.basename(f), n))
            if unk:
                print("    未登记（跳过）:", unk)
            if not check and new != src:
                io.open(f, "w", encoding="utf-8", newline="\n").write(new)
    print("合计 %d 处" % grand)


if __name__ == "__main__":
    main()
