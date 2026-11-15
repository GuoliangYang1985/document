# -*- coding: utf-8 -*-
"""从书末「术语总表」(chapters/glossary.qmd) 抽取词条，用已渲染 PDF 的页码生成索引页。

用法：python tools/build_index.py   （须在 quarto render 成功后运行）
生成的 chapters/term-index.qmd 会被下一次 render 收进去；页码可能随版式
变动一行，版式改动后重跑一次即可收敛。

词条的唯一来源是 glossary.qmd 的表格首列（规范 §6.6：章末不设术语表）。
含 " / " 的复合词条（如 "Ricci 张量 / Ricci 标量"）在正文中总是拆开
出现，检索时按 " / " 拆成子词分别查找，页码取并集。
"""
import io, os, re, glob, sys, unicodedata
from pypdf import PdfReader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "_book", "理论测量的边界.pdf")

# ---- 0. 章号：按 _quarto.yml 的章节顺序编号，前置件与附录取名不计号
FRONT = {"index.qmd", "reading-guide.qmd", "notation.qmd", "glossary.qmd",
         "term-index.qmd", "references.qmd", "acc-source.qmd", "sector-metrics.qmd"}


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

# ---- 1. 词表：从书末「术语总表」抓取首列，并补充关键专名
# sec 标签 -> 所在文件（解析总表第三列的 @sec- 引用，取最早正文章作“首见”）
SEC_OWNER = {}
for f in sorted(glob.glob(os.path.join(ROOT, "chapters", "*.qmd"))) + [os.path.join(ROOT, "index.qmd")]:
    txt = io.open(f, encoding="utf-8").read()
    base = os.path.basename(f)
    for lab in re.findall(r"\{#(sec-[A-Za-z0-9_-]+)", txt):
        SEC_OWNER.setdefault(lab, base)

GLOSSARY = os.path.join(ROOT, "chapters", "glossary.qmd")
terms = {}
if os.path.exists(GLOSSARY):
    txt = io.open(GLOSSARY, encoding="utf-8").read()
    for line in txt.split("\n"):
        if not line.startswith("|") or "---" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3 or cells[0] in ("", "术语") or not cells[0]:
            continue
        name = cells[0].strip("`*_ ")
        if len(name) > 24:
            continue
        # 首见：第三列中最早出现的正文章
        src = ""
        owners = [SEC_OWNER[m] for m in re.findall(r"@?(sec-[A-Za-z0-9_-]+)", cells[2])
                  if m in SEC_OWNER]
        nums = [CHAP.get(o) for o in owners if CHAP.get(o)]
        if nums:
            first = min(nums)
            src = next(o for o in owners if CHAP.get(o) == first)
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
if not os.path.exists(PDF):
    sys.exit(u"未找到 %s；请先在项目根目录运行 quarto render 成功后再运行本脚本。" % PDF)
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

# 索引自身与其前的「术语总表」各占若干页，其后是参考文献；这两段不能参与
# 检索，否则每个词条都会命中索引/总表页。注意不能用「关键词索引」作锚——
# 目录页里也有这四个字；用各首页独有的导语句作锚。
GLOSS_MARK = u"全书术语按三层安置"
IDX_MARK = u"本索引列出全书主要术语"
gloss_start = next((k for k, (_, t) in enumerate(raw) if GLOSS_MARK in t), None)
idx_start = next((k for k, (_, t) in enumerate(raw) if IDX_MARK in t), None)
idx_end = None
if idx_start is not None:
    idx_end = next((k for k in range(idx_start + 1, len(raw)) if u"参考文献" in raw[k][1]),
                   len(raw))
lo = gloss_start if gloss_start is not None else idx_start
skip = set(lab for lab, _ in raw[lo:idx_end]) if lo is not None and idx_end is not None else set()

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


def probe_pages(probe):
    """单个探测词的命中页码（升序列表，可能为空）。"""
    n = norm(probe)
    if len(n) < 2:
        return []
    found = set(pg for pg, t in pages if n in norm(t))
    return sorted(found, key=lambda x: int(x))


def hit_of(name):
    """词条的命中页。复合词条（含 " / "）在正文中总是拆开出现，
    故按 " / " 拆成子词分别检索、页码取并集；拆开皆未命中时退回整名。"""
    parts = [p.strip() for p in name.split(u" / ") if p.strip()]
    if len(parts) > 1:
        got = set()
        for part in parts:
            got |= set(hit_of(part))
        if got:
            return sorted(got, key=lambda x: int(x))
    probes = [name]
    # PDF 文本可能把希腊字母/上下标拆开，用主词再试一次
    core = plain(name)
    if core and core != name:
        probes.append(core)
    lead = re.split(r"[（(\$]", name)[0].strip()
    if len(lead) >= 2 and lead not in probes:
        probes.append(lead)
    for probe in probes:
        found = probe_pages(probe)
        if found:
            return found
    return []


hit = {name: hit_of(name) for name in terms}

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
