# The Boundary of Theoretical Measurement (Version 1.0)

A book manuscript on **measurement, symmetry, and the structure of physical theories**. The whole book turns on a single axis: the invariant-speed group $G_K$, in which the invariant speed is written as a parameter $K$. The Lorentz transformation ($K=c$), the Galilean transformation ($K=\infty$), and the Carrollian limit ($K=0$) then appear as three values of one and the same family of structures. The manuscript asks, value by value, which conclusions depend on $K$ and which do not.

- **Author**: Guoliang Yang (Jinan, Shandong)
- **Version**: 1.0
- **Typesetting**: Quarto book + XeLaTeX (`ctexbook`), A4, Chinese text
- **Output**: `_book/理论测量的边界.pdf`

---

## 1. What the book is about

The book pursues one question throughout: **does a given physical conclusion come from the object under study, or from the coordinates and pairing rules we use to describe it?**

To separate the two, "measurement" is split into layers that can be checked independently:

| Layer | Content | Depends on the frame? |
|-------|---------|----------------------|
| Events and clock readings | the number a given clock shows at a given event | no |
| Pairing (simultaneity) rule | whose event is compared with whose | **yes** |
| Transformation formulas and coordinate quantities | coordinate time, projected time | yes |

The book's stance: **list the conclusions of each layer separately, each with its own premises, and never present a difference at the pairing layer as a difference at the object layer.** The twin analyses of Chapter 13 give the fullest demonstration of this method.

---

## 2. Chapter structure

| Part | Ch. | Title | Role |
|------|-----|-------|------|
| Preface | — | Preface | Problem, method, roadmap |
| **Main line** | 1 | The symmetric-twins experiment | A formula-free opening: mirror symmetry ⟹ equal readings; Lorentz pairing gives another number; the two sit at different layers |
| | 2 | Deriving the Galilean and Lorentz transformations | One derivation; the split sits in the third axiom |
| | 3 | The constant-speed group | The parametrised family $G_K$, structure constant $1/K^2$ |
| | 4 | The constant-speed field group | Promoting $K$ from a constant to a field |
| | 5 | Dynamics of the constant-speed field group | The conformal ansatz and its hard limits |
| | 6 | The complete geometry of the constant-speed field | Adding shift and spatial metric: the full 10 degrees of freedom |
| | 7 | Algebraic generation of the quantum phase | Lie-algebra contraction, projective representations, mass as a central charge |
| **Field-theory cases** | 8 | Maxwell's equations | The standard case in the $K=c$ branch |
| | 9 | Galilean-covariant field equations | Its counterpart in the $K=\infty$ branch |
| | 10 | Propagation and two-source fields under the Galilean postulate | Pure mathematical consequences of axioms A1 + A2 |
| | 11 | Symmetric tensor fields on flat spacetime | Equivalence and breakdown of the $(\eta,h)$ and $g$ bookkeepings |
| **Extensions** | 12 | The clock-coupling framework | Rate functions, moduli space, uplift to the operator level |
| | 13 | The symmetric twins revisited | Three inputs side by side; the criterion separating covariance from the clock-reading scale; the Earth-version twins under both sets of axioms |
| | 14 | The symmetric twins in non-inertial coordinates | Both viewpoints, the condition for the coordinate map to be injective, and the calibration-line cut: the two inertial segments contribute exactly $0$ to the difference of readings |
| **Appendix** | — | Notation and conventions | Symbol registry, curvature convention, house style |
| | — | References | — |

---

## 3. Features

1. **Comparable numbers.** The same question ("how much does B's clock advance while A's advances by one second?") is answered three times — using symmetry only, the Lorentz transformation only, and the Galilean transformation only — and the three answers are placed side by side (Chapter 13, Table 13.1).
2. **Symbolic computation kept in step with the text.** Every closed-form result (Ricci and Weyl components, central extensions, twin ratios) is produced term by term with sympy in `chapters/images/*.py`; the script output matches the text one-for-one. Changing a formula means changing its script.
3. **Two branches side by side, without adjudication.** Chapter 13 places the Earth-version twins in both the $K=c$ and the $K=\infty$ branch, gives the axioms and results of each, and leaves the choice open.
4. **Conclusions stated as checkable criteria.** Every statement in the twins chapters is given as a mathematical criterion — a piecewise cut along calibration lines, the choice of a pairing rule, the condition for the coordinate map to be injective — with no claim reaching beyond what the derivation yields. Chapter 1 deliberately carries no formulas: it sets out the two threads and the difference in their level.

---

## 4. Building

### Requirements

- [Quarto](https://quarto.org) (≥ 1.4)
- A TeX distribution (TinyTeX or TeX Live) providing `xelatex` and the `ctex` bundle
- Python 3.13 (figures only) with `sympy`, `matplotlib`, `numpy`

### Commands

```bash
# Build the PDF (output to _book/)
quarto render --to pdf

# Build the HTML version
quarto render --to html
```

### Figures

Figure scripts live in `chapters/images/`; each script writes a PNG of the same name:

```bash
cd chapters/images
python twins-earth-two-branches.py      # writes twins-earth-two-branches.png
```

Every script begins with a sympy verification block and prints the key identities to stdout (for example `gamma(K) = 1/sqrt(1 - v**2/K**2)`, `K -> oo : 1`).

### Layout

```
_quarto.yml            book configuration (chapter order, theorem labels, formats)
preamble.tex           LaTeX preamble (book name, layout, headers and footers)
before-body.tex        custom title page (with version number)
chapters/*.qmd         the chapters
chapters/images/*.py   figure scripts (each with symbolic verification)
chapters/references.bib  bibliography
_deliver/              standalone single-chapter versions
```

---

## 5. House style

- Theorem-like environments are numbered per chapter: axiom, definition, proposition, theorem, lemma, corollary.
- Equations are numbered consecutively per chapter; cross-references are hyperlinks, never hand-written numbers.
- No end-of-proof symbol is used.
- Symbol clashes and multiple meanings are registered in the "Notation and conventions" chapter (in particular the roles of $K$, $h$, and $c$).

---

## 6. Version history

| Version | Notes |
|---------|-------|
| 1.0 | First release: 14 chapters plus the notation appendix; Chapter 1 rewritten as a formula-free opening; conclusions in the twins chapters stated as mathematical criteria; "Covariance and clock-reading interpretation" added to Chapter 13, the calibration-line cut and the injectivity condition added to Chapter 14; quotation marks unified throughout; version number added to the title page |

---

## 7. Statement

The mathematics is the author's; the verification scripts ship with the book and are independently reproducible. AI assistance was used during writing (text organisation, verification scripts, figure code, and cross-reference checking). The author takes responsibility for all results and derivations.
