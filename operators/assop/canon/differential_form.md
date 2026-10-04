# Sandhi–vichcheda and differential forms (exterior calculus)

How the sandhi engine relates to **differential forms** and **exterior calculus**: what is the same algebraically, what Sygal implements today, and what would be needed for full de Rham-style work.

**Related:** [`extsimp.md`](extsimp.md) (Hopf on \(\Lambda(V)\), §7–8), [`status.md`](status.md) (fragment contract), [`diagram.md`](diagram.md), [`test_gextp.py`](../test/test_gextp.py), [`gextpcanon.py`](gextpcanon.py).

---

## Short answer

- **Yes** — at the level of **exterior algebra**, sandhi–vichcheda is the same kind of structure as wedge + interior product on forms: antisymmetric products, shared factors split (**vichcheda**), compatible panels merged (**sandhi**), overlap scalar when grades balance.
- **Not the full calculus** — the production sandhi path does **not** include exterior derivative \(d\), \(d^2=0\), Cartan formula, charts, pullback, or integration as rewrite rules.
- **In Sygal today** — sandhi runs on **`gextp` wedges of `glcntrct`** (left contraction `<` on tested fragments). Encode \(k\)-forms as grade-\(k\) blades and \(\iota_v \omega\) as `v < omega` when that matches the fragment.

---

## Same core as exterior calculus

[`extsimp.md`](extsimp.md) §3 places vichcheda on the **exterior Hopf algebra** \(\Lambda(V)\):

| Sygal | Exterior / forms language |
|-------|---------------------------|
| `^` (`gextp`) | Wedge \(\omega \wedge \eta\) — antisymmetric product |
| `<` (`glcntrct`) | Left contraction; for a vector \(v\) and form \(\omega\), same **role** as interior product \(\iota_v \omega\) |
| `\|` (`sclrprdct`) | Metric pairing when a Clifford / inner-product metric is available |
| Dependent or repeated factor in wedge | \( \mathrm{d}x \wedge \mathrm{d}x = 0\) — linear dependence kills the term |
| `parity` on reorder | Sign from permuting form factors |

**Vichcheda** splits a down-wedge into **common** (seam) + **unique** tails — the coproduct picture \(\Delta(\alpha \wedge \beta)\) with shuffle signs.

**Sandhi** collects compatible contraction panels into one `up < merged_down` plus scalars at grade gate **`x == 0`**.

So any expression that is **only** a wedge of interior/contraction factors on form-degree multivectors lives in the same algebra sandhi normalizes.

### Example (tests)

Antisymmetry (`test_gextp.test_0`):

```text
(a1^a2)  and  (a2^a1)  — same mv, opposite coeff  →  wedge annihilates symmetric part
```

Simple merge (`test_sandhi`):

```text
(A < (B1 ^ B2)) ^ (A < (B2 ^ B3))  →  A < (B1 ^ B2 ^ B3)
```

Read as: \(\iota_A(\beta_1 \wedge \beta_2) \wedge \iota_A(\beta_2 \wedge \beta_3)\) with shared vector \(A\) and shared form factor \(\beta_2\).

Overlap scalar (`test_gmul_2Proj`):

```text
(a1 < (a2 ^ a3)) ^ (a1 < (a3 ^ a4))  →  (a1 | a3) * (a1 < (a2 ^ a3 ^ a4))
```

Read as: \(\langle a_1, a_3 \rangle \cdot \iota_{a_1}(a_2 \wedge a_3 \wedge a_4)\) when `|` is the metric pairing on 1-blades.

---

## What differential forms add (beyond current sandhi)

| Idea | Role in exterior calculus | In sandhi / Sygal today |
|------|---------------------------|-------------------------|
| \(\Omega^k\) — \(k\)-forms | Sections of \(\Lambda^k T^*M\) | Grade-\(k\) blades / atoms (encoding choice) |
| Wedge \(\wedge\) | Graded product | **`gextp`** — **yes** |
| Interior \(\iota_v\) | Contraction of forms | **`glcntrct`** `<` — **yes** on tested fragment |
| Exterior derivative \(d\) | Raises degree, \(d^2=0\) | **Not** in `canon_iter(gextp)` sandhi loop |
| Cartan \( \mathcal{L}_v = d\iota_v + \iota_v d \) | Lie derivative | **Not** wired as sandhi rules |
| Coordinate \(\mathrm{d}x^i\), pullback, integration | de Rham / analysis on \(M\) | **Not** — GA/CGA **atoms**, not chart API |
| Hodge \(\star\), codifferential | Metric geometry | Partial via other canon rules (inv/proj/rej in `exhaust`), not unified with sandhi |

Sandhi is **algebraic** exterior calculus on a **fixed fragment** ([`status.md`](status.md)), not automatic for every symbolic \(\omega \in \Omega^k(M)\) with \(d\omega\) in the same pipeline.

---

## Grade gate `x` (forms viewpoint)

After down vichcheda, `gextpcanon` uses:

```text
x = grd(dn11) + grd(dn21) - grd(merged_down) - grd(acc_blade)
```

| Branch | Engine | Forms / analysis reading |
|--------|--------|---------------------------|
| **x < 0** | Recurse `sandhi` on inner down; no Capelli at this level | Nested interior factors not ready — simplify inner \(\iota\) / \(\wedge\) first |
| **x == 0** | Merge + `CapelliOptionB.coefficient` | Grades balance — one interior of a merged wedge; overlap scalar |
| **x > 0** | `GExpr.Znl` (zero) | No admissible combined form — like an illegal degree mismatch |

This is **not** a spatial coordinate; it is **grade / degree bookkeeping**, analogous to only closing contractions when form degrees add correctly.

---

## Stack picture

```text
  Differential forms on a manifold M
       Ω^k  —  wedge of covector / form factors
       d    —  coboundary (raises k)     ←  not sandhi’s main operator
       ι_v   —  interior product        ↔  Sygal `<` on vector-like 1-blades
              ↓
  Exterior algebra Λ(V)  —  Hopf Δ ↔ vichcheda, collect ↔ sandhi  (extsimp §3)
              ↓
  Sandhi–vichcheda (gextpcanon)  —  NF for  (v1 < ω1) ^ (v2 < ω2) ^ …
              ↓
  frptConf / CGA  —  same Clifford/exterior ops for geometric constructions
```

Deep nesting (e.g. `D1 < (... (D3 < (C1^C2^C3)) ...)`) is **nested interior products** on a form built from smaller forms — the same pattern as chained `<` in GA proofs.

---

## Using sandhi on forms in practice

1. Represent **\(k\)-forms** as grade-\(k\) `GExpr` blades (or sums via `gadd` when wired).
2. Write **\(\iota_v \omega\)** as **`v < omega`** (left contraction).
3. Build **products of several such terms** as a top-level **`gextp`** wedge.
4. Run **`canon_iter(gextp)`** — sandhi + inv/proj/rej until fixed point ([`gextpsimp.py`](../../gextpsimp.py), Option B).

**Limits today** ([`status.md`](status.md)):

- `_split_common_unique`: **TODO** for **`gatom` grade > 1** on down seams.
- Sandhi: one successful pair per `sandhi` call; merge order from `iter`, not all trees at once.
- **`gadd`** canonicalization: stub — general sums of forms not on the sandhi track.
- No built-in **`d`** rewrite (Leibniz \(d(\alpha\wedge\beta)\), \(d^2=0\)).

---

## Implemented vs possible (honest)

| Claim | Status |
|-------|--------|
| Wedge antisymmetry / dependence → zero | **Exact** — exterior algebra; `test_0` |
| Merge + seam on contraction wedges | **Implemented** on `gextp` / `glcntrct` fragment — `test_gextp`, `test_sandhi_wide` |
| Overlap scalar at balanced seam | **Implemented** — `CapelliOptionB` at `x == 0` |
| Full de Rham with \(d\), integration, charts | **Not** in sandhi pipeline — separate future rules / types |
| Equivalence to every handwritten form proof | **Not certified** — operational tests, not all `GExpr` |

---

## Relation to other docs

| Topic | Where |
|-------|--------|
| Hopf ↔ split/merge | [`extsimp.md`](extsimp.md) §3 |
| Physics / fermion analogues | [`extsimp.md`](extsimp.md) §7, [`status.md`](status.md) § conceptual parallels |
| Young tableaux vs sandhi | [`extsimp.md`](extsimp.md) §8 |
| frptConf stack | [`../../../cirFramework/frptConf/overview.md`](../../../cirFramework/frptConf/overview.md) |
| Brini / Capelli coefficients | [`gextpcapelli.py`](gextpcapelli.py), [`extsimp.md`](extsimp.md) §5 |

---

## Possible extensions (research, not implemented)

1. **`d` as operator** — rewrite rules: \(d^2=0\), Leibniz on wedges, interaction with \(\iota\) (Cartan).
2. **Explicit form basis** — atoms `dx_i`, chart change, pullback functorially.
3. **Widen vichcheda** — grade > 1 common seams on down (`status` C7).
4. **`gadd` + sandhi** — distribute sandhi over sums of forms.
5. **Prove fragment** — interior-product identities on \(\Omega^\bullet\) equivalent to `test_gextp` shapes.

Until then, treat sandhi as **powerful normal form for wedges of contractions in \(\Lambda(V)\)** — the same algebraic substrate as differential forms, with **interior + wedge** implemented and **exterior derivative + analysis** still outside the default canon loop.
