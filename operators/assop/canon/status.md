# Sandhi / Vichcheda — implementation status

Workstream: `Sygal/operators/assop/canon`  
Scope: **algebraic canonical transformation only** (normal form + coefficients). Game, diagram IR, and board product are **out of scope** here (see `DG.md`, `diagram.md`).

---

## What “complete” means (for this file)

**Complete** = on a **defined input fragment**, the pipeline reaches the **intended canonical form** with **correct scalar coefficients** (signs + overlap factors), using **recursive** sandhi/vichcheda and **iteration to fixed point**.

It does **not** mean:

- full Brini 2015 paper stack (bitableaux, straightening, all of `U(gl(n))`),
- proved global confluence on all `GExpr`,
- drawable diagram semantics or commercial game readiness.

---

## Module map (where the code lives)

| Module | Role | Sandhi-related? |
|--------|------|-----------------|
| **`gextpcanon.py`** | Sandhi/vichcheda engine: `concat.sandhi`, `binary_op`, `_split_common_unique`, grade gate, `iter` | **Yes — core** |
| **`gextpcapelli.py`** | Option B: `CapelliOptionB.coefficient(acc, common, local_sign)` | **Yes — coefficients only** |
| **`gextpsimp.py`** | Default backend; registers `gextp.gsimplify` / canon wiring | **Yes — entry** |
| **`gextpsimp_hopf.py`** | Option C scaffold (Hopf); falls back to Option B | Partial |
| **`Sygal/utils/util.py`** | `parity()` → `sign1`, `sign2` | **Yes — signs** |
| **`test_gextp.py`** | Acceptance tests for NF + coeffs | **Yes — spec** |
| **`gaddcanon.py`** | `pass` stub | **No** — `gadd` canon not implemented |

Sandhi is **not** in `gaddcanon.py`. The pair for algebra is **`gextpcanon.py` + `gextpcapelli.py`**.

---

## How canonicalization runs

```text
canon_iter(gextp)
  →  exhaust(do_one(sandhi, inv_gextp, proj_gextp, rej_gextp))   # gextpcanon.gextpcanon()
```

| Mechanism | Behavior |
|-----------|----------|
| **`concat.sandhi`** | One successful **pairwise** merge per call (`iter` over contraction pairs in a wedge). |
| **`exhaust`** | Repeats until no change → **fixed point** on the expression. |
| **`binary_op`** | Up/down vichcheda; **`x < 0`** → recurse `sandhi` on inner down first; **`x == 0`** → merge + `CapelliOptionB.coefficient`. |
| **`blade2`** | `blade1 ^ blade12` — accumulated contracting path for nested overlap scalars. |
| **Signs** | `sign1`, `sign2` from `parity`; `coeff = CapelliOptionB(..., sign1*sign2)`. |

This is **recursive decomposition + rewrite to fixed point**, not a single closed-form pass and not enumeration of all binary merge trees in one step.

---

## Input fragment (operational contract)

The engine is built and tested roughly for:

- `gextp` products of **`glcntrct`** with **`gextp` down** (plus up-matching cases in `binary_op`),
- **uni-graded** `Box` wrappers,
- sandhi-compatible shared up/down blades.

Known code limits:

- `_split_common_unique`: **TODO** — `gatom` support for **grade > 1**
- `iter`: first successful pair in `subsets` order, not parallel exploration of all merge orders
- **`gadd`** canonicalization: not wired (`gaddcanon` stub)

**“Complete” is fair within this fragment and `test_gextp`; too strong for all of Sygal without more tests/proofs.**

---

## What is completed

### 1. Canonical engine (`gextpcanon.py`)

- Recursive sandhi/vichcheda (`binary_op`, nested `sandhi(dbx_U, blade2)`).
- Up-side vichcheda (shared atom / subset wedge on `up`).
- Down-side vichcheda (`_split_common_unique`).
- Grade gate `x < 0 | == 0 | > 0` with recurse-first coefficient policy on `x == 0`.
- `_down_to_mv_and_coeff`, `remake` + `parity` on outer wedge reorder.

### 2. Option-B coefficients (`gextpcapelli.py`)

- **C1** — virtual operator layer (`VirtualOp`, super-bracket, adjoint).
- **C2** — devirtualization (`_iterated_adjoint`, `_capelli_map`, `devirtualize_scalar`).
- **C3** — canonical path uses `CapelliOptionB.coefficient` only (via `_scalar_part` in `gextpcanon`).

### 3. Wiring and backends

- **`gextpsimp.py`** — Option B default.
- **`gextpsimp_hopf.py`** — Option C module exists; runtime still delegates to canonical sandhi.

### 4. Tests (`test_gextp.py`)

- `test_cases_sandhi` — basic merge identities.
- `test_cases_gmul_2proj` — overlap scalars e.g. `(a1|a3) * (...)`.
- `test_cases_sandhi_complex` — deep nested D1/D2/D3-style merge, including the
  squared overlap scalar. Passes over 13-D atoms.
- **C4** — idempotence, order-invariance, deep stress batch.

**Choose the atom space deliberately.** Uppercase atoms (`A1`, `B1`, …) span the
4-dimensional `I41`; lowercase atoms (`a1`, `b1`, …) span the 13-dimensional `I13`.
A wedge whose total grade exceeds the span is identically zero, so multi-panel
tests written over uppercase atoms are vacuous. Deep sandhi cases belong in `I13`.

### 5. Documentation

- `extsimp.md` — Hopf mapping (§3); physics/tableau parallels (§7–8).
- `tutorial.md` — examples and sign sketches.
- `diagram.md` — schematic sandhi/vichcheda + **§2a nested signs** (not a formal proof).

---

## Completeness assessment (algebra only)

| Claim | Status |
|-------|--------|
| Core sandhi/vichcheda implementation exists | **Yes** — `gextpcanon.py` |
| Recursive nested merge + inner sandhi first (`x < 0`) | **Yes** |
| Coefficients via Option B × local sign | **Yes** — `gextpcapelli.py` |
| Fixed-point canonicalization (`exhaust`) | **Yes** — for `gextp` rule set |
| Intended NF on tested inputs | **Yes** — `test_gextp` |
| **Exhaustive** over all merge orders in one step | **No** — one pair per `sandhi` call; order fixed by `iter` |
| Order-invariant NF on tested inputs | **Yes** — canonical `gextp` sorting makes all 24 permutations of a non-degenerate 4-panel chain agree (with the wedge sign required by antisymmetry) |
| **Proved** unique / confluent NF for all expressions | **No** — deterministic sorted scan is not a confluence proof; alternate successful pair schedules have not been enumerated |
| **Brini-exact** coefficients in all cases | **Partial** — tested cases; not a full proof |
| Full Sygal (all grades, `gadd`, all ops) | **No** |
| Diagram IR / game | **Not started** (by design here) |

**Summary:** Past prototype for **algebraic transformation on the tested fragment**. Not a certificate of completeness for arbitrary GA input.

---

## What is still pending (algebra)

1. **Fragment spec** — write explicit grammar of inputs sandhi must handle (extend `diagram.md` or this file).
2. **Confluence hardening** — parameterize the pair scheduler, then compare every
   successful merge schedule (or randomized schedules) from the same sorted input.
   Permuting source panels alone does not test this because `gextp` sorts before sandhi.
3. **Grade > 1 down atoms** — implement `_split_common_unique` TODO for `gatom`.
4. **Coefficient cross-checks** — `CapelliOptionB` vs direct `(acc_blade | common) * local_sign` on hard cases.
5. **Parity / virtual-algebra cleanup** — reduce ad-hoc parity-only paths (`status` item from earlier passes).
6. **Option C runtime** — explicit Hopf/coproduct path aligned with `extsimp.md` (optional; Option B is production path).
7. **`gaddcanon`** — separate track; not required for `gextp` sandhi completeness.

Paper-level Brini stack (bitableaux, full straightening) remains **research**, not blocking “NF + coeff on fragment.”

---

## Confidence (algebraic)

| Area | Level |
|------|--------|
| Structural sandhi/vichcheda on tested shapes | **High** |
| Nested recursion + grade gate | **High** (code + complex tests) |
| Option-B coefficients on tested shapes | **High** (tests); **medium** as universal proof |
| Global confluence / unique NF | **Medium** — order-invariant on every non-degenerate case tested; unproved in general |
| Full GA / all grades | **Low** (known TODOs) |

---

## Checkpoints

- [x] **C1** — Virtual operator execution layer (`gextpcapelli.py`)
- [x] **C2** — Adjoint-action devirtualization core
- [x] **C3** — Canonical coefficient path through C2 / `CapelliOptionB`
- [x] **C4** — Deep stress, idempotence, order-invariance tests
- [ ] **C5** — Independent Option C runtime (optional)
- [ ] **C6** — Fragment grammar doc + confluence property suite
- [ ] **C7** — Grade > 1 / `gatom` in `_split_common_unique`

---

## Conceptual parallels (physics, math, Young tableaux)

This section records **structural** relationships — not claims that chemistry codes call `sandhi` by name. Detail: [`extsimp.md`](extsimp.md) §7–8; differential forms: [`differential_form.md`](differential_form.md); frptConf stack: [`../../../cirFramework/frptConf/overview.md`](../../../cirFramework/frptConf/overview.md).

### Grade gate and “allowed combination”

`emit_merge_by_grade` in `gextpcanon.py` (`grade_x < 0 | == 0 | > 0`):

| `x` | Engine | Analogue |
|-----|--------|----------|
| **&lt; 0** | Recurse `sandhi` on inner down before coeff | Unresolved inner bond / nested subdiagram |
| **== 0** | Merge + `CapelliOptionB.coefficient` | Balanced grades — **allowed** channel; overlap scalar |
| **&gt; 0** | `GExpr.Znl` | **Forbidden** — no merge (like illegal quantum numbers / tableau term) |

### Exterior wedge and tests

- Dependent or duplicate directions → zero via antisymmetry (`test_0` in `test_gextp.py`).
- Simple merge: `test_sandhi` — shared `A1`, seam `B2`.
- Overlap scalar: `test_gmul_2Proj` — `(a1|a3) * (a1 < (a2^a3^a4))`.

### Young tableaux — relation to Capelli and sandhi

| Layer | Status in repo |
|-------|----------------|
| **Young / semistandard tableaux, straightening, bitableaux** | Brini 2015 / representation theory — **not** implemented as explicit structures |
| **Capelli epimorphism (Option B)** | **Implemented** — `gextpcapelli.py` |
| **Sandhi–vichcheda normal form** | **Implemented** on tested `gextp` fragment — `gextpcanon.py` |

**Similarity (precise):** both solve “many raw antisymmetric / noncommutative products → **one standard piece** + **sign/scalar**, or **zero**.”

- **Tableau side:** discrete labels in boxes; **straightening**; illegal filling → 0.
- **Sandhi side:** split **common seam** vs unique blades (**vichcheda**); **sandhi** merge; `parity` signs; scalar at `x==0`.

Sandhi is **not** a Young tableau. The link is **Capelli/Brini**: tableaux index operators classically; Sygal uses **virtual-variable Capelli** (Option B) on the rewrite path instead of a bitableau API.

**Pending (tableau track):** C6 fragment grammar; optional future **bitableaux + straightening** prover layer — does not block current NF + coeff tests.

### QC / many-body (hypothesis)

[`QC/docs/framework/Quantum chemistry .md`](../../../QC/docs/framework/Quantum%20chemistry%20.md) frames sandhi as preserving **shared admissibility genealogy** in fermionic expressions vs flat determinant blow-up. **Representational** claim; requires benchmarks — not part of `test_gextp` acceptance.

---

## Related files

| File | Purpose |
|------|---------|
| `gextpcanon.py` | Sandhi engine |
| `gextpcapelli.py` | Coefficients |
| `test_gextp.py` | Tests = operational definition of “correct” |
| `extsimp.md` | Hopf reading; §7–8 physics / Young tableaux vs sandhi |
| `differential_form.md` | Sandhi vs differential forms / \(d\), \(\iota\), scope |
| `diagram.md` | Schematic diagrams + sign flow §2a |
| `DG.md`, `DG1.md`, `DG2.md` | Product / math context (not blocking algebra) |

Update this file when fragment, tests, or coefficient path changes materially.
