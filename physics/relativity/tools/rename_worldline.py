# -*- coding: utf-8 -*-
"""
把"世界线积分的值"从时钟语言改回数学本名。

新名：世界线长度（简称"线长"），符号沿用 (M4) 已有的 s：
  \Delta\tau_X -> \Delta s_X   （该段的线长增量）
  \tau_X       -> s_X
  \tau_1/\sigma_1 -> s_1/s_2   （两次切割的参数）
  裸 \tau       -> s
  例外：\tau' 在 twins-noninertial 里是 A 视角的时间坐标参数，不换算；
        裸 \sigma 是"以 M 为心的校验线族"的参数名，保留。
  asymmetric-twins 中 L（返程段线长）保留。

用法：
  python tools/rename_worldline.py --check   # 干跑：报告各处将替换的数目与剩余
  python tools/rename_worldline.py           # 执行
"""
import io
import os
import re
import sys
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = "--check" in sys.argv

# ---------------------------------------------------------------- 符号（按文件限定）
SYM = collections.OrderedDict([
    # 先处理带 \Delta 的、再处理带下标的、最后裸 \tau
    (r"\\Delta\\tau_(\w)",     r"\\Delta s_\1"),
    (r"\\Delta\\tau_(\{\w+\})", r"\\Delta s_\1"),
    (r"\\Delta\\tau",          r"\\Delta s"),
    (r"\\sigma_1",             r"s_2"),
    (r"\\tau_(\w)",            r"s_\1"),
    (r"\\tau_(\{\w+\})",       r"s_\1"),
    (r"\\tau(?!')",            r"s"),
])
SYM_FILES = ["chapters/twins-comparison.qmd",
             "chapters/twins-noninertial.qmd",
             "chapters/asymmetric-twins.qmd"]

# ---------------------------------------------------------------- 中文（长词优先）
CN = collections.OrderedDict([
    ("读数定义",   "线长定义"),
    ("读数尺度",   "线元"),
    ("等固有读数轨迹", "等长轨迹"),
    ("等读数双曲线", "等长双曲线"),
    ("等读数点",   "等长点"),
    ("等读数线",   "等长线"),
    ("等读数",     "等长"),
    ("读数之差",   "长度之差"),
    ("读数差",     "长度之差"),
    ("总读数",     "总长度"),
    ("整段读数",   "整段长度"),
    ("累积读数",   "累积长度"),
    ("读数预估",   "线长估计"),
    ("读数",       "线长"),
])

# ---------------------------------------------------------------- 仅在符号表/术语表等处的定点改写
SPOT = [
    # (文件, 原文片段, 新片段)
    ("chapters/notation.qmd",
     "| $\\tau$ | 随身钟的读数（沿世界线累积） |",
     "| $s$、$\\Delta s$ | 世界线长度（简称线长）；沿世界线对线元积分所得的量 |"),
    ("chapters/notation.qmd",
     "| $\\int\\mathrm{d}s$ | 沿世界线的累积读数 |",
     "| $\\int\\mathrm{d}s$ | 世界线长度 |"),
    ("chapters/notation.qmd",
     "## 读数、几何与曲率 {#sec-notation-geometry}",
     "## 线长、几何与曲率 {#sec-notation-geometry}"),
]


def apply_sym(text):
    n = 0
    for pat, rep in SYM.items():
        text, k = re.subn(pat, rep, text)
        n += k
    return text, n


def apply_cn(text):
    counts = collections.OrderedDict()
    for old, new in CN.items():
        k = text.count(old)
        if k:
            counts[f"{old} -> {new}"] = k
            text = text.replace(old, new)
    return text, counts


def main():
    total_sym = 0
    for rel in SYM_FILES:
        p = os.path.join(ROOT, rel)
        s = io.open(p, encoding="utf-8").read()
        s2, nsym = apply_sym(s)
        s3, ccn = apply_cn(s2)
        print(f"### {rel}   符号 {nsym} 处")
        for k, v in ccn.items():
            if v:
                print(f"      {v:4d}  {k}")
        total_sym += nsym
        rest = [x for x in re.findall(r".{0,26}\\\\tau.{0,16}", s3)]
        print("      残留 \\tau:", len(rest))
        for x in collections.Counter(rest).most_common(6):
            print("        ", x[1], x[0].replace("\n", " "))
        if not CHECK:
            io.open(p, "w", encoding="utf-8").write(s3)
    print("符号替换总数:", total_sym)

    for rel, old, new in SPOT:
        p = os.path.join(ROOT, rel)
        s = io.open(p, encoding="utf-8").read()
        if old in s:
            print(f"[SPOT] {rel}: {s.count(old)} 处 -> {new[:30]}...")
            if not CHECK:
                io.open(p, "w", encoding="utf-8").write(s.replace(old, new))
        else:
            print(f"[SPOT 未命中] {rel}: {old[:40]}")


if __name__ == "__main__":
    main()
