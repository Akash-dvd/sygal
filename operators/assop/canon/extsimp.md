# Sandhi-Vichcheda: Example, Hopf Mapping, and Implementation

## 1) Example first

Input expression:

```text
(D1 < (A1 ^ A2 ^ (D2 < (B1 ^ B2 ^ (D3 < (C1 ^ C2 ^ C3))))))
 ^
(D1 < (A3 ^ A4 ^ (D2 < (B3 ^ B4 ^ (D3 < (C1 ^ C2 ^ C3 ^ C4))))))
```

Target canonical output:

```text
((D1 ^ D2 ^ D3) | (C1 ^ C2 ^ C3))
*
(D1 < (A1 ^ A2 ^ A3 ^ A4 ^ (D2 < (B1 ^ B2 ^ B3 ^ B4 ^ (D3 < (C1 ^ C2 ^ C3 ^ C4))))))
```

Interpretation:
- merged contraction structure (multivector part),
- scalar overlap factor (coefficient part).

---

## 2) Sandhi and vichcheda from the same example

### Sandhi (combine)

```text
(A < (B_common ^ U1)) ^ (A < (B_common ^ U2))
  -> coeff * (A < (B_common ^ U1 ^ U2))
```

### Vichcheda (separate)

At each level:
1. split down blades into `common` and `unique`,
2. keep split-order sign,
3. recurse into nested common contractions,
4. return merged expression + scalar factor.

In the example recursion:
- D1-level common contains D2 contraction,
- D2-level common contains D3 contraction,
- D3-level common is `(C1 ^ C2 ^ C3)`.

---

## 3) Exact Hopf algebra mapping

Let `Lambda(V)` be the exterior Hopf algebra.

### 3.1 Vichcheda = coproduct split

```text
Delta(v1 ^ ... ^ vk) = sum_{S subset [k]} sign(S, S^c) * v_S tensor v_{S^c}
```

This is the algebraic version of splitting into common/unique with shuffle signs.

### 3.2 Contraction from coproduct

```text
A < B = (A* tensor id)(Delta(B))
```

So each contraction step is already coproduct-based splitting + pairing.

### 3.3 Sandhi = refactor after split

- vichcheda side: product-like form expands to sum over split terms,
- sandhi side: compatible terms are recognized and refactored to canonical contraction form.

### 3.4 Operational mapping table

- `common/unique split` -> coproduct components,
- `local sign` -> shuffle sign from coproduct ordering,
- `scalar overlap` -> pairing of accumulated blade with common component,
- `recursive merge` -> repeated coproduct/contract/collect across depth.

---

## 4) How this is implemented in current code

### 4.1 Option B (default path)

Main files:
- `gextpcanon.py` (canonical sandhi engine),
- `gextpcapelli.py` (Option-B helper layer),
- `gextpsimp.py` (backend selector; default is Option B).

Execution flow in current Option B:
1. `gextpcanon.concat.binary_op` finds mergeable contraction pair.
2. Up-part normalization and accumulation of recursion blade (`blade2`).
3. Down-part split via `_split_common_unique`.
4. Recursive merge on merged down expression.
5. Coefficient computed through `CapelliOptionB.coefficient(acc_blade, common_part, local_sign)`.
6. Rebuild merged contraction term.

Option-B helper objects currently in code:
- `VirtualSymbol`,
- `BalancedMonomial`,
- `CapelliOptionB.build_balanced_monomial(...)`,
- `CapelliOptionB.devirtualize_scalar(...)`,
- `CapelliOptionB.coefficient(...)`.

### 4.1.1 Where C1/C2/C3/C4 are implemented

**C1: Virtual operator execution layer**
- File: `gextpcapelli.py`
- Core symbols:
  - `VirtualOp`
  - `VirtualMonomial`
  - `VirtualExpr`
- Core logic:
  - `_super_bracket(...)` (graded commutator)
  - `_ad(...)` (adjoint as graded derivation)

**C2: Adjoint-action devirtualization core**
- File: `gextpcapelli.py`
- Core logic:
  - `_iterated_adjoint(...)`
  - `_devirtualize_virtual_expr(...)`
  - `devirtualize_scalar(...)`

**C3: Canonical coefficient path routed through C2**
- Callsite wiring:
  - `gextpcanon.py` -> `concat._scalar_part(...)` -> `CapelliOptionB.coefficient(...)`
- C2 map stage:
  - `gextpcapelli.py` -> `_capelli_map(...)` used inside `devirtualize_scalar(...)`
- Effect:
  - canonical coefficient flow now goes through Option-B virtual/devirtualization path.

**C4: Deep stress + confluence-oriented tests**
- File: `test_gextp.py`
- Added tests:
  - `test_sandhi_order_invariance_complex` (permutation/order invariance)
  - `test_sandhi_deep_stress_batch` (deep nested stability batch)
  - plus expanded complex/idempotence checks:
    - `test_sandhi_complex`
    - `test_sandhi_idempotence_complex`

### 4.2 Option C (separate file)

File:
- `gextpsimp_hopf.py`

Current state:
- separate Option-C entry exists,
- currently safe-falls back to canonical sandhi,
- explicit coproduct expansion engine is not yet enabled as standalone runtime path.

---

## 5) How the paper implements it (Brini 2015)

Paper: [https://arxiv.org/pdf/1501.03639](https://arxiv.org/pdf/1501.03639)

Core implementation pattern in the paper:
1. introduce graded virtual variables,
2. build balanced monomials (`creation` then `annihilation`),
3. perform calculations in virtual algebra,
4. apply Capelli epimorphism (devirtualization) to return to proper algebra,
5. signs come from supercommutation structure.

Direct correspondence to Sygal terms:
- sandhi/vichcheda recursion <-> balanced monomial split/collect behavior,
- accumulated blade <-> virtual chain across recursion depth,
- coefficient <-> devirtualized scalar from virtual representation.

---

## 6) Minimal usage pseudocode

```python
def sandhi_option_b(expr, acc_blade=1):
    for each mergeable pair:
        up_common, dn1, dn2 = split_up(expr1, expr2)
        acc2 = acc_blade ^ up_common

        dn1_mv, dn2_mv, scalar_cf = unwrap_box(dn1, dn2)
        merged_dn, sign_local, common_dn = split_common_unique(dn1_mv, dn2_mv)

        deep = sandhi_option_b(merged_dn * scalar_cf * sign_local, acc2)
        coeff = capelli_option_b.coefficient(acc2, common_dn, sign_local)

        return (up_common < deep) * coeff
```

---

## 7) Physical and mathematical analogues

Sandhi–vichcheda is the **Sygal normal form** for wedges of left contractions. It is **not** marketed under this name in standard physics courses, but the **structure** recurs.

### 7.1 Antisymmetry and the wedge

Exterior algebra: \(v \wedge w = 0\) if \(v,w\) are dependent. In Sygal, `test_gextp.test_0`: `(a1^a2)` and `(a2^a1)` share the same multivector part but **opposite** coefficients — the wedge is antisymmetric.

**Physics:** fermionic wavefunctions — repeating the same orbital in an antisymmetric product gives **zero** (Pauli exclusion). Same mechanism as “redundant direction kills the term.”

### 7.2 Seam, merge, and overlap scalar

```text
(A < (B1 ^ B2)) ^ (A < (B2 ^ B3))  →  coeff · (A < (B1 ^ B2 ^ B3))
```

With explicit overlap (`test_gmul_2Proj`):

```text
(a1 < (a2 ^ a3)) ^ (a1 < (a3 ^ a4))  →  (a1 | a3) * (a1 < (a2 ^ a3 ^ a4))
```

| Sandhi piece | Math / physics analogue |
|--------------|-------------------------|
| Shared **up** blade `A` | Same contractor / filter |
| **Vichcheda** seam `B2`, `a3` | Shared index, orbital, or tensor bond |
| **Sandhi** merged down | Reduced determinant / merged tensor leg |
| **Scalar** `(a1\|a3)` | Slater–Condon **overlap**; tensor trace factor |
| **`exhaust` fixed point** | Keep rewriting until no further compatible merge |

### 7.3 Grade gate `x` (allowed vs forbidden)

In `gextpcanon`, after down vichcheda:

```text
x = grd(dn11) + grd(dn21) - grd(merged_down) - grd(acc_blade)
```

| Branch | Behavior | Interpretation |
|--------|----------|----------------|
| **x &lt; 0** | `sandhi` on inner down first; **no** Capelli at this level | Nested structure not ready — contract inner bonds first |
| **x == 0** | `sandhi` + `CapelliOptionB.coefficient` | **Balanced** — merge allowed; release overlap scalar |
| **x &gt; 0** | Zero | **Forbidden** merge — no admissible combined form |

This is the operational form of “only certain grade / representation labels can close.” It parallels **selection rules** and tensor **contraction rank** matching, not spatial coordinates.

### 7.4 Deep recursion

The §1 nested `D1,D2,D3` example is the same **pattern** as:

- nested tensor-network contractions,
- coupled-cluster style nested excitations on antisymmetric manifolds,
- repeated coproduct split + collect (§3) before outer pairing.

**Caveat:** proving cheaper QC than Slater determinants is a **separate benchmark** (see project QC docs). This file documents **algebraic** equivalence targets on `test_gextp`, not industrial chemistry codes.

---

## 8) Young tableaux, bitableaux, and sandhi — discrete vs symbolic arrangement

### 8.1 Two kinds of “arrangement”

**Young tableau (discrete combinatorics)**

- Place labels \(1,2,\ldots\) in boxes of a fixed **diagram** (partition).
- **Global rules:** e.g. semistandard increasing along rows/columns; size bounds.
- **Many** fillings possible; **straightening** picks a **standard** representative (or shows equivalence up to sign).
- **Illegal** pattern → term is **zero** in \(U(\mathfrak{gl}(n))\) calculations.

**Sandhi–vichcheda (symbolic GA)**

- **Panels:** `(up < down)` factors in a `gextp` wedge — e.g. two expressions sharing `A` and seam `B2`.
- **Global rules:** antisymmetry on `^`, shared up blade, `_split_common_unique`, grade gate `x`.
- **Vichcheda:** label each side as **common** (seam) + **unique** tails; `parity` on reordering.
- **Sandhi:** one merged contraction; at `x==0`, **Capelli** scalar (not box labels — **overlap** along the seam).
- **Illegal:** `x>0` or dependent wedge → **zero**.

Sandhi does **not** store a grid of integers. The discrete part is **which atoms occupy common vs unique slots** and **wedge order** — the same *type* of problem as ordering entries in a tableau row, but objects are **blades** (`GAtom`s), not \(1..n\) in boxes.

### 8.2 Where Capelli / Brini sits between them

```text
  Young tableaux / Capelli bitableaux
       index which polarizations survive; straightening laws
              ‖
  Brini 2015 (virtual variables, balanced monomials, devirtualization)
       Option B: CapelliOptionB.coefficient — implemented in gextpcapelli.py
              ‖
  Sandhi–vichcheda (gextpcanon.py)
       operational split/merge on contractions; coeff only at x == 0
```

Brini’s paper also lists **straightening for Capelli bitableaux** and the **Koszul** map Sym\([\mathfrak{gl}(n)]\) → \(U(\mathfrak{gl}(n))\). Those are **paper-level** in this repo — see `status.md`, `q1.md` — not an explicit tableau data structure in code.

### 8.3 Comparison table

| Question | Young / bitableau | Sandhi–vichcheda |
|----------|-------------------|------------------|
| What is combined? | Two monomials → standard filling | Two panels → one `up < down` |
| What is the extra number? | Sign from column permutation | `parity` × Capelli scalar |
| Many possibilities? | Many fillings; straighten | Many wedge orders; `exhaust` + tests |
| When zero? | Illegal tableau | `x>0`, antisymmetric collapse |
| Implemented here? | **No** (research backlog) | **Yes** on `gextp` fragment |

### 8.4 Honest bottom line

- **Related:** same mathematical family (antisymmetric GA, \(\mathfrak{gl}(n)\) representation theory, Capelli).
- **Not the same object:** tableaux are **index bookkeeping**; sandhi is a **rewrite calculus** on `GExpr`.
- **Implemented path:** sandhi + Option B — not Young tableaux API.
- **Possible future work:** prove fragment equivalence to straightening on a class of inputs, or add bitableaux-driven rules (checkpoint C6+ in `status.md`).

**One sentence:** sandhi arranges **shared seam + merged wedge** under grade and antisymmetry rules; Young tableaux arrange **index order in a diagram** under straightening rules; **Brini–Capelli** is the formula for the scalar when both arrangements lock on the same core.

---

## Related

- `diagram.md` — flowcharts and nested walkthrough
- `status.md` — implementation completeness + § conceptual parallels
- `tutorial.md` — sign arithmetic examples
- `q1.md` — Brini paper components vs what is coded
- [`cirFramework/frptConf/overview.md`](../../../cirFramework/frptConf/overview.md) — frptConf stack + condensed § on analogues and tableaux
- [`differential_form.md`](differential_form.md) — sandhi vs exterior calculus / de Rham (what is in vs out of scope)
