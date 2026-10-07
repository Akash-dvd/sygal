# Lean sources for sandhi / viccheda formalization

Status survey of what already exists in Mathlib and the community, versus
what this project still needs. Companion to [`README.md`](README.md) and
[`../todo.md`](../todo.md).

**Location decision:** keep this Lake project under
`Sygal/paper/sandhi/lean/` (colocated with the paper in the language repo).
Do **not** start a separate Clifford library repo first. Depend on Mathlib;
fork or PR only if a reusable lemma belongs upstream.

---

## 1. What this folder already contains

### Phase 1 (done)

| File | Role | Maturity |
|------|------|----------|
| `lakefile.toml` / `lean-toolchain` | Lean **v4.33.1** + Mathlib `v4.33.1` | wired |
| `Sandhi/Basic.lean` | `contractVec` / `contractBlade` / `ofList` + graded Leibniz | **done** |
| `Sandhi/Expansion.lean` | Grade-1 Σ-expansion (3.1): `expandRec` = `expandSum` | **done** |
| `Sandhi/Seam.lean` | Grade-1 sole-seam identity (aligned panels) | **done** |
| `Sandhi/Induction.lean` | Abstract `Spec` + gate/`reduce` | control-flow only |
| `Sandhi/Stitching.lean` | `stitch` / `stitch_sound` | depends on Induction |

### Phase 2 (done for flat panels)

| File / obligation | Status |
|-------------------|--------|
| `Sandhi/Grade.lean` | homogeneous / sub-blade / seam-error spans; annihilation lemmas | **done** |
| `Sandhi/Capelli.lean` | `seamPairing`; extraction \(A\lrcorner S = A\mid S\) for all \(r\) | **done** |
| `Sandhi/SeamR.lean` | `soleSeam_gradeR` (all \(r\)); `soleSeam_vanish` (\(t>r\)) | **done** |
| `Sandhi/Panel.lean` | `panelSpec` (all gates sound); `panelStitch_sound` | **done** |
| Closed Σ-form (3.1) for \(r>1\) | not needed by the proof; open |
| `Sandhi/Nested.lean` | nested sole-seam `nested_soleSeam'` (any depth, shuffle sign); `nested_vanish`; `Sygal/test1.py` as a corollary | **done** |
| Front-end: parsing a general tree into `Level` lists, seam detection | open |
| Schedule / confluence | deferred |

**Phase 2 summary:** the local grade-\(r\) identity, the vanish branch, Capelli
extraction, fixed-schedule stitching over flat panels, and the nested
sole-seam identity of any depth are proved with no `sorry`. What remains is
the syntactic front-end (recognizing the shape in an arbitrary expression)
and confluence.

---

## 2. Mathlib (primary dependency)

Mathlib already formalizes the algebraic substrate we need for the *local*
sandhi identity. Use it; do not reimplement Clifford from scratch.

### 2.1 Clifford algebra (basis-free)

| Item | Path / docs |
|------|-------------|
| Definition + universal property | [`Mathlib.LinearAlgebra.CliffordAlgebra.Basic`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/CliffordAlgebra/Basic.html) |
| Left/right contraction by duals | [`Mathlib.LinearAlgebra.CliffordAlgebra.Contraction`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/CliffordAlgebra/Contraction.html) |
| Module iso to exterior (char ≠ 2) | `CliffordAlgebra.equivExterior` |

Especially useful for sandhi:

- `CliffordAlgebra.contractLeft` / `contractRight` (notation `d ⌋ x`, `x ⌊ d`)
- Recurrence: `contractLeft_ι_mul`, commutativity `contractLeft_comm`, nilpotency `contractLeft_contractLeft`
- `changeForm` / `equivExterior` to move between Clifford and exterior when needed

**Caveat:** Mathlib contracts by a **dual** `Module.Dual R M`. The paper’s
vector–blade left contraction \(A \lrcorner X\) needs the metric/musical
isomorphism (or work entirely in exterior with an explicit bilinear form).
That glue layer is **ours to write**, not Mathlib’s gap in the Clifford core.

### 2.1.1 Left-contraction expansion algo — what Mathlib has vs paper (3.1)

The paper’s **closed-form sum** (draft §3 / `todo.md`) is:

\[
A\lrcorner X
=\sum_{\lvert I\rvert=r}\Delta_A(I;X)\,X_{\widehat I},
\qquad
\Delta_A(I;X)=\operatorname{sgn}(I)\det[(a_\alpha\cdot x_{i_\beta})].
\]

That is the Capelli / minor expansion over \(r\)-subsets of factors of \(X\).

| Piece | In Mathlib? | Notes |
|-------|-------------|--------|
| Vector recurrence (derivation rule) | **Yes** | `contractLeft_ι_mul`: \(d\lfloor(\iota a\cdot b)=d(a)\cdot b-\iota a\cdot(d\lfloor b)\) |
| Linearity in \(+\) / scalars | **Yes** | `contractLeft` is bilinear |
| Iterate \(r\) vector contractions | **Derive** | Compose the recurrence; no named blade API |
| Closed sum \(\sum_{\lvert I\rvert=r}\) with \(\Delta_A\) | **No** | Paper formula (3.1) — **we prove** |
| Capelli pairing \(A\mid S=\det[(a_i\cdot s_j)]\) as coeff of seam block | **No** | Needs our sign convention |
| Nested partition sum over \(I_1\mathbin{\dot\cup}\cdots\) | **No** | Graded Leibniz / panel expansion — ours |
| Laplace–Cauchy–Binet identification of surviving terms | **Partial** | Determinant / compound-matrix tools exist; wiring to \(\Delta_A\) is ours |

**Bottom line:** Mathlib gives the **recursive algorithm** (one vector at a time).
It does **not** ship the paper’s **Σ-over-index-sets expansion** or Capelli
coefficients. Unrolling the recurrence *is* how one proves (3.1); that proof
is still on our checklist (`todo.md`: “Expand \(A\lrcorner X\) as a signed
sum…”).

### 2.2 Exterior algebra

| Item | Notes |
|------|--------|
| `ExteriorAlgebra R M` | Present in Mathlib |
| Wedge / grading | Available; API thinner than some GA texts |
| Dedicated “interior product of blades” | **Not** a rich high-level API; often obtained via Clifford + `equivExterior` or by defining contraction ourselves |

### 2.3 Dual pairing (not GA contraction)

[`Mathlib.LinearAlgebra.Contraction`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Contraction.html)
is the dual–module pairing \(M^* \otimes M \to R\). Do **not** confuse it
with geometric left contraction; it is still useful when wiring duals to
vectors via a bilinear form.

### 2.4 Related Mathlib pieces we will touch

- `QuadraticForm`, bilinear forms / associated forms  
- Alternating maps / determinants (for Capelli / seam pairing \(A\mid S\))  
- Multilinear algebra lemmas for Laplace / Cauchy–Binet style expansions  

---

## 3. Community Geometric Algebra work

| Project | What it is | Relevance to sandhi |
|---------|------------|---------------------|
| **[utensil/lean-ga](https://github.com/utensil/lean-ga)** | Partial GA on top of Mathlib Clifford; versors; experimental **CGA** | Inspiration / optional dep for conformal applications later |
| **Eric Wieser’s Mathlib Clifford** (from *Formalizing Geometric Algebra in Lean*, AACA) | The Mathlib Clifford we depend on | **Already upstream** |
| Older Lean 3 / other provers’ GA ports | Historical | Prefer Mathlib4 API |

**Verdict:** lean-ga is useful later for **CGA applications** (Monge, Ptolemy
skeletons in `todo.md`). For the core sandhi identity, **Mathlib Clifford +
exterior is enough**. Do not block on finishing lean-ga’s CGA layer.

---

## 4. Gap analysis: paper obligations vs libraries

From [`../todo.md`](../todo.md):

| Obligation | In Mathlib / community? | We must build |
|------------|-------------------------|---------------|
| Exterior / Clifford product, ι | Yes | Thin notation wrappers |
| Left contraction by vectors/blades matching paper convention | Partially (dual contraction) | Metric ♭/♯ + blade contraction; sign/order convention |
| Local grade‑\(r\) sole-seam identity | No | **Main theorem** |
| Determinant / Capelli seam pairing | Determinant tools exist | Align ordering with paper |
| Grade gate \(t \lessgtr r\) | No | Define on our panel type |
| Nested panels + sole-seam invariant | Control-flow only (`Induction.lean`) | Concrete `State` = panels; prove invariant preservation |
| Schedule / confluence | No | Separate theorem; defer |
| CGA encoding of apps | lean-ga partial CGA | After core sandhi |

---

## 5. Recommended build plan (on top of Mathlib)

1. ~~**Wire Mathlib** into `lakefile.toml` / `lake-manifest.json`.~~
2. ~~**`Sandhi/Basic.lean`:** `ExteriorAlgebra` + `BilinForm` contraction; paper order.~~
3. ~~**Grade‑1 local identity** + grade‑1 Σ-expansion.~~
4. ~~**Capelli pairing** + sole-seam for \(r\le 1\); instantiate `Spec`.~~
5. ~~**Grade‑\(r\)** Capelli extract + sole-seam; vanish for \(t>r\).~~
6. **Real nesting:** contraction-tree grammar; sole-seam closure by height.
7. **Applications / CGA:** later; lean-ga optional — not a prerequisite.

---

## 6. Repo layout (confirmed)

```text
Sygal/                          ← language repo (Akash-dvd/sygal)
  paper/sandhi/
    draft.tex | draft.md | todo.md
    lean/                     ← THIS project (correct place)
      SOURCES.md              ← this file
      README.md
      Sandhi/...
```

| Alternative | When to use |
|-------------|-------------|
| Separate `sandhi-lean` repo | Only if Lean CI / collaborators outgrow the paper folder |
| New “full Clifford lib” repo | **Avoid** — Mathlib + optional lean-ga already cover the base |

Local monorepo may also have `paper/sandhi/` as a working copy; **canonical
tracked tree for Lean is under `Sygal/paper/sandhi/lean/`.**

---

## 7. Community / docs links

- Mathlib Clifford Basic: https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/CliffordAlgebra/Basic.html  
- Mathlib Clifford Contraction: https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/CliffordAlgebra/Contraction.html  
- lean-ga: https://github.com/utensil/lean-ga  
- Paper: Wieser et al., *Formalizing Geometric Algebra in Lean* (AACA)  
- Lean Zulip `#maths` / Mathlib maintainers for upstream contributions  

---

## 8. One-line summary

**Mathlib already gives Clifford + dual contraction + exterior iso; the community
has partial GA/CGA extras. Our work is the sandhi-specific layer: metric-aware
blade contraction, sole-seam identity, Capelli pairing, and nesting — not a
new Clifford library.**
