# -*- coding: utf-8 -*-
"""从各章「术语说明」表抽取词条，用已渲染 PDF 的页码生成索引页。

用法：python tools/build_index.py   （须在 quarto render 成功后运行）
生成的 chapters/term-index.qmd 会被下一次 render 收进去；页码可能随版式
变动一行，版式改动后重跑一次即可收敛。
"""
import io, os, re, glob, unicodedata
from pypdf import PdfReader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "_book", "理论测量的边界.pdf")

# ---- 0. 章号：按 _quarto.yml 的章节顺序编号，前置件与附录取名不计号
FRONT = {"index.qmd", "reading-guide.qmd", "notation.qmd", "term-index.qmd",
         "references.qmd", "acc-source.qmd", "sector-metrics.qmd"}


def chapter_map():
    """返回 {文件名: 章序号}，只含正文各章。"""
    yml = io.open(os.path.join(ROOT, "_quarto.yml"), encoding="utf-8").read()
    m = re.search(r"\n\s*chapters:\s*\n((?:\s*-\s*\S+\n)+)", yml)
    if not m:
        return {}
    files = re.findall(r"-\s*(\S+)", m.group(1))
    out, n = {}, 0
    for f in files:
        base = os.path.basename(f)
        if base in FRONT:
            continue
        n += 1
        out[base] = n
    return out


CHAP = chapter_map()


def chap_label(src):
    """把源文件名换成「第 N 章」，不把构建产物印到纸上。"""
    if not src:
        return "—"
    n = CHAP.get(src)
    return u"第 %d 章" % n if n else "—"

# ---- 1. 词表：从各章「术语说明」抓取，并补充关键专名
terms = {}
for f in sorted(glob.glob(os.path.join(ROOT, "chapters", "*.qmd"))):
    txt = io.open(f, encoding="utf-8").read()
    src = os.path.basename(f)
    blocks = re.split(r"\n## 术语说明", txt)[1:]
    for b in blocks:
        # 术语说明块遇到下一个二级标题就结束（避免吞进「结论」表）
        b = re.split(r"\n## ", b)[0]
        for line in b.split("\n"):
            if line.startswith("|") and "---" not in line:
                cells = [c.strip() for c in line.strip("|").split("|")]
                if len(cells) >= 2 and cells[0] and len(cells[0]) <= 24:
                    name = cells[0].strip("`*_ ")
                    terms.setdefault(name, src)

# 纯数学符号条目不进索引（已在「符号与约定」附录登记）
terms = {k: v for k, v in terms.items() if not re.fullmatch(r"\$[^$]*\$", k)}

extra = ["Bargmann 群", "Bargmann 代数", "Carroll 结构", "Newton–Cartan 几何",
         "Inönü–Wigner 收缩", "群收缩", "恒速群", "恒速场", "中央扩张", "中央荷",
         "质量超选择", "李代数收缩", "射线表示", "读数", "配对", "同时面",
         "非相对论极限", "相态参数", "对称双生子", "校验线", "事件视界", "变换因子",
         "Schwarzschild", "标架", "Weyl 张量", "共形平坦", "拖曳", "单射", "暗物质", "扇区度规", "响应系数"]
for e in extra:
    terms.setdefault(e, "")

# ---- 2. 页码：用印刷页码（正文 arabic），不是 PDF 页序
reader = PdfReader(PDF)
try:
    labels = list(reader.page_labels)
except Exception:  # pragma: no cover
    labels = [str(i + 1) for i in range(len(reader.pages))]
raw = []
for i, pg in enumerate(reader.pages):
    lab = labels[i] if i < len(labels) else str(i + 1)
    if not lab.isdigit():  # 只收录正文（arabic 页码）
        continue
    txt = (pg.extract_text() or "").replace("\n", " ")
    raw.append((lab, txt))

# 索引自身占若干页，其后是参考文献；这一段不能参与检索，
# 否则每个词条都会命中索引页（旧版只排除了首页，其余索引页仍会中招）。
# 注意不能用「关键词索引」作锚——目录页里也有这四个字；用索引首页
# 独有的导语句作锚。
IDX_MARK = u"本索引列出全书主要术语"
idx_start = next((k for k, (_, t) in enumerate(raw) if IDX_MARK in t), None)
idx_end = None
if idx_start is not None:
    idx_end = next((k for k in range(idx_start + 1, len(raw)) if u"参考文献" in raw[k][1]),
                   len(raw))
skip = set(lab for lab, _ in raw[idx_start:idx_end]) if idx_start is not None else set()

pages = []
for lab, txt in raw:
    if lab in skip:
        continue
    # 排除目录、图目录、表目录：它们有密集的点引导线，正文不会出现。
    # 全书改用连续阿拉伯数字页码后，这些前置页的页码也是数字，会被上面
    # isdigit() 那一关放行，故在此按点引导线的密度剔除。
    if len(re.findall(r"\.\s\.\s\.", txt)) >= 3:
        continue
    pages.append((lab, txt))

GREEK = {"\\gamma": "γ", "\\nabla": "∇", "\\partial": "∂", "\\infty": "∞",
         "\\mathrm{d}": "d", "\\Box": "□", "\\hbar": "ℏ"}


def norm(s):
    """把 Union 数学字体回落为普通字符，便于与 PDF 抽取文本比对。"""
    for k, v in GREEK.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[\s　]+", "", s)
    return s.replace("–", "-").replace("—", "-")


def plain(s):
    """把含 LaTeX 的词条转成可用于文本检索的纯文本。"""
    s = re.sub(r"\$[^$]*\$", lambda m: re.sub(r"\\[a-zA-Z]+|[{}^_\\]", "", m.group(0)), s)
    s = re.sub(r"[│|]", "", s)
    s = re.sub(r"\\[a-zA-Z]+", "", s)
    s = s.replace("$", "").replace("{", "").replace("}", "")
    s = s.replace("^", "").replace("_", "")
    return (re.split(r"[（(\[]", s)[0].strip() or s.strip())

hit = {}
for name in terms:
    probes = [name]
    # PDF 文本可能把希腊字母/上下标拆开，用主词再试一次
    core = plain(name)
    if core and core != name:
        probes.append(core)
    lead = re.split(r"[（(\$]", name)[0].strip()
    if len(lead) >= 2:
        probes.append(lead)
    for probe in probes:
        n = norm(probe)
        if len(n) < 2:
            continue
        found = [pg for pg, t in pages if n in norm(t)]
        if found:
            hit[name] = sorted(set(found), key=lambda x: int(x))
            break
    else:
        hit[name] = []

miss = [k for k, v in hit.items() if not v]
rows = []
for name in sorted(terms):
    pages_ = hit.get(name, [])
    rows.append((name, terms[name], pages_))

out = [u"# 关键词索引 {.unnumbered #sec-term-index}",
       u"",
       u"本索引列出全书主要术语及其在正文中出现的页。",
       u"",
       u"```{=latex}",
       u"\\begingroup",
       u"\\renewcommand{\\arraystretch}{1.3}",
       u"```",
       u"",
       u"| 词条 | 首见 | 页码 |",
       u"|---|---|---|"]
for name, src, pages_ in rows:
    if not pages_:
        pg_list = "（见相应章节）"
    else:
        pg_list = "、".join(pages_)
    out.append(u"| %s | %s | %s |" % (name, chap_label(src), pg_list))

# 表格结束：恢复行距。索引表每条只占一行，条目间留白由局部
# \arraystretch 给出；\addlinespace 无法直接写进 Markdown 单元格。
out += [u"", u"```{=latex}", u"\\endgroup", u"```"]

p = os.path.join(ROOT, "chapters", "term-index.qmd")
io.open(p, "w", encoding="utf-8", newline="\n").write(u"\n".join(out) + u"\n")
print("terms:", len(rows), "missing:", len(miss))
print("missing list:", miss)
