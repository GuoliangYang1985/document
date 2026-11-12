# -*- coding: utf-8 -*-
"""
把第 12 章（twins-comparison）从 blanket 改名回滚到"读数/τ"。

原因：上一版 tools/rename_worldline.py 做了一个错误的假设——
把"读数"一律当作"世界线积分值"的同义词。第 12 章不是这样：
它整章是三组输入（S 对称 / L 洛伦兹 / G 伽利略）的对照，算的全是
"钟的读数"这一个量，从不把它定义成任何积分。所以第 12 章里的
"读数"不是被改名对象，必须原样保留。

第 13、14 章以 (M4)（沿曲线对线元积分）为输入，讲的是 ∫ds 这个
几何量本身，那里保留新名"线长 / s"是对的。

本脚本只处理 twins-comparison.qmd。
"""
import io
import os
import re
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "chapters", "twins-comparison.qmd")
CHECK = "--check" in [a for a in __import__("sys").argv]


# ------------------------------------------------------------------ 符号回滚
# 顺序很重要：先长后短；且不要碰 $\mathrm{d}s$ 之类本就属于几何层的写法
SYM = collections.OrderedDict([
    (r"\\Delta s_\{(\w+)\}",      r"\\Delta\\tau_{\1}"),
    (r"\\Delta s_(\w)",           r"\\Delta\\tau_\1"),
    (r"\\Delta s",                r"\\Delta\\tau"),
    (r"s_\{(\w+)\}",              r"\\tau_{\1}"),
    (r"s_(\w)",                   r"\\tau_\1"),
    (r"\$(s)\$",                  r"$\\tau$"),
    (r"([^\w\\{])s([^\w_^])",     r"\1\\tau\2"),
])

# ------------------------------------------------------------------ 中文回滚
CN = collections.OrderedDict([
    ("线长定义",        "读数定义"),
    ("等长轨迹",        "等固有读数轨迹"),
    ("等长双曲线",      "等读数双曲线"),
    ("等长点",          "等读数点"),
    ("等长线",          "等读数线"),
    ("等长",            "等读数"),
    ("长度之差",        "读数之差"),
    ("总长度",          "总读数"),
    ("整段长度",        "整段读数"),
    ("累积长度",        "累积读数"),
    ("线长估计",        "读数预估"),
    ("线长诠释",        "读数诠释"),
    ("线长层",          "读数层"),
    ("线长增量",        "读数增量"),
    ("线长积分",        "读数积分"),
    ("线长",            "读数"),
])

# 个别行长 Sword 有"线元"本义（第 5 章引入的 Mathfrak 记号），用定点表处理
SPOT = [
    # (原文片段, 回滚后)
    ("欧氏圆 $t^{2}+x^{2}=s^{2}$ 不是任何钟的读数轨迹",
     "欧氏圆 $t^{2}+x^{2}=\\tau^{2}$ 不是任何钟的读数轨迹"),
]


def main():
    s = io.open(TARGET, encoding="utf-8").read()
    orig = s

    nsym = 0
    for pat, rep in SYM.items():
        s, k = re.subn(pat, rep, s)
        nsym += k

    ccn = collections.OrderedDict()
    for old, new in CN.items():
        k = s.count(old)
        if k:
            ccn[f"{old} -> {new}"] = k
            s = s.replace(old, new)

    for old, new in SPOT:
        if old in s:
            ccn[f"[SPOT] {old[:24]}..."] = s.count(old)
            s = s.replace(old, new)

    print("符号回滚:", nsym, "处")
    for k, v in ccn.items():
        print(f"   {v:4d}  {k}")

    left = collections.Counter(re.findall(r".{0,18}线长.{0,12}", s))
    print("残留 线长:", sum(left.values()))
    for k, v in left.most_common(15):
        print("    ", v, k.replace("\n", " "))
    print("回滚后 读数:", s.count("读数"), "| \\tau:", s.count("\\tau"),
          "| 独立 s:", len(re.findall(r"[^\w\\{]s[^\w_^]", s)))

    if not CHECK:
        io.open(TARGET, "w", encoding="utf-8").write(s)
        print("已写回:", TARGET)
    else:
        print("（干跑，未写入）")


if __name__ == "__main__":
    main()
