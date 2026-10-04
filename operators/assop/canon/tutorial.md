# Sandhi and vichcheda: tutorial (with `test_gextp.py` examples)

This note walks from **small, checked examples** in `Sygal/operators/assop/test/test_gextp.py` up to one nested layer. The engine lives in `gextpcanon.concat` (see also `extsimp.md` for Hopf wording).

Notation: `<` is **left contraction**; `^` is the **exterior (wedge) product**; `*` is ordinary **scalar** product; `|` is the **scalar / pairing** used when projections appear in the normal form.

---

## 1. Signs: `+` / `−` before sandhi

**Antisymmetry of the wedge (one swap flips sign).**  
`test_0` fixes the convention: `(a1^a2)` and `(a2^a1)` share the same multivector part, but the **coefficients are opposite**, so they sum to zero.

```text
(a1^a2).mv == (a2^a1).mv
(a1^a2).coeff + (a2^a1).coeff == 0
```

So whenever arguments of a blade are **reordered**, the implementation tracks a **sign** (here a `±1` factor on the `Box` coefficient). In the sandhi path, reorderings during **vichcheda** use the same idea via `parity(old_args, new_args)` in `_split_common_unique` (`gextpcanon.py`): each regrouping of factors contributes a **local sign** `sign1`, `sign2`; these feed the Option-B coefficient path together with the **common blade** used at that level.

**Rule of thumb:** `±` never comes from nowhere—it is either **swap count** in the wedge or **parity of merging** two orders into one canonical order.

---

## 2. Many small examples (single level)

These are **exactly** the shapes exercised in the tests (input `→` canonical output after `canon_iter(gextp)`).

### 2.0 Simplest case: only two 1-blades (two terms in one wedge)

Before any contraction sandhi, the wedge of **two** vectors is controlled by **alternation**: there are only two orderings, and they are not independent.

**Expansion formula (two-term alternating identity).**  
For 1-blades `u`, `v`:

```text
u^v  =  − (v^u)
```

Equivalently, the **sum of the two orderings** is zero:

```text
u^v  +  v^u  =  0
```

That is the “expansion” in the sense of **antisymmetrization**: the 2-blade is fixed by one order, and the reverse order is the **same** multivector with the **opposite** scalar coefficient.

**Proof by expansion (one swap).**  
Start from `u^v`. To obtain `v^u`, **swap** the two factors (one adjacent transposition in a 2-vector). In an exterior algebra, each swap of two **distinct** 1-blades introduces a factor `−1`. Hence `v^u = −(u^v)`, which is the first display. Adding `v^u` to both sides gives `u^v + v^u = 0`.

**Check in tests (`test_0`).** The same relation is what `test_gextp.test_0` encodes: `(a1^a2).mv == (a2^a1).mv` and `(a1^a2).coeff + (a2^a1).coeff == 0`, i.e. the two wedge orders are one 2-blade with coefficients `+c` and `−c`.

---

### 2.1 Minimal sandhi (shared 1-blades only)

**Left contraction on a 2-blade (expansion formula).**  
For 1-blades `a`, `b1`, `b2`, the left contraction obeys the usual “first hit” expansion (same sign convention as a graded derivation on the wedge):

```text
a < (b1^b2)  =  (a|b1)*b2  −  (a|b2)*b1
```

Here `|` is the scalar inner product, `*` multiplies a scalar into a 1-blade.

**Left contraction on a 3-blade (one step longer).**

```text
a < (b1^b2^b3)  =  (a|b1)*b2^b3  −  (a|b2)*b1^b3  +  (a|b3)*b1^b2
```

---

**Complete expansion proof of the sandhi identity.**  
Set `a = A1` and write

```text
L1 = A1 < (B1^B2) = (A1|B1)*B2 − (A1|B2)*B1
L2 = A1 < (B2^B3) = (A1|B2)*B3 − (A1|B3)*B2
```

Expand the wedge **distributively** (bilinearity of `^` over addition, and scalars pull out):

```text
L1 ^ L2
  =  (A1|B1)(A1|B2) * B2^B3
     −  (A1|B1)(A1|B3) * B2^B2
     −  (A1|B2)² * B1^B3
     +  (A1|B2)(A1|B3) * B1^B2
```

The term with `B2^B2` is **zero** (repeated factor in an exterior product). So

```text
L1 ^ L2
  =  (A1|B1)(A1|B2) * B2^B3
     −  (A1|B2)² * B1^B3
     +  (A1|B2)(A1|B3) * B1^B2
```

Now expand `(A1|B2) * (A1 < (B1^B2^B3))` using the 3-blade formula above:

```text
(A1|B2) * (A1 < (B1^B2^B3))
  =  (A1|B2) * [ (A1|B1)*B2^B3 − (A1|B2)*B1^B3 + (A1|B3)*B1^B2 ]
  =  (A1|B1)(A1|B2) * B2^B3 − (A1|B2)² * B1^B3 + (A1|B2)(A1|B3) * B1^B2
```

This is **identical** to `L1 ^ L2`. Hence, by pure expansion,

```text
(A1 < (B1^B2)) ^ (A1 < (B2^B3))  =  (A1|B2) * (A1 < (B1^B2^B3))
```

The **shared middle** blade `B2` is exactly what produces the overall scalar factor `(A1|B2)`—the same “overlap” phenomenon as in `test_gmul_2Proj`:

```text
(a1 < (a2^a3)) ^ (a1 < (a3^a4))  →  (a1|a3) * (a1 < (a2^a3^a4))
```

**Automated check (`test_sandhi`).** The test stores the normal form as a **single** contraction:

```text
(A1 < (B1^B2)) ^ (A1 < (B2^B3))  →  A1 < (B1^B2^B3)
```

Algebraically the content is the product `(A1|B2) * (A1 < (B1^B2^B3))`; depending on how `Box` coefficients and normal forms are printed, the scalar `(A1|B2)` may sit on the `Box` or be folded with other data—the **structural** sandhi step is still “one contraction over `B1^B2^B3`” with the **overlap scalar** from the common `B2`.

### 2.2 Same pattern with more bookkeeping

Further single-level identities from `test_cases_sandhi` (verbatim from `test_gextp.py`):

```text
(B3^(A1<(B1^B2^A2)))^(A1<(B2^B3))^(B2<(B1^B3))^(B2<(A2^B3))
  →  (B3^(A1<(B1^B2^B3^A2)))^(B2<(A2^B1^B3))

(A2^(A1<(((B1<(A1^A2))^B2^B3)))^(A1<(((B1<(A1^A2))^A2)))
  →  A2^(A1<(((B1<(A1^A2))^A2^B2^B3)))

(A2^(A1<(((B1<(A1^A2^A3))^B2)))^(A1<(((B1<(A1^A2))^B3)))
  →  A2^(A1<(((B1<(A1^A2^A3))^B2^B3)))
```

These differ only in **how much** is already nested under `<`; the **first** sandhi steps still act at the level of **matching upper blades** and **shared / unique** splits on plain `gextp` down blades.

### 2.3 When a **scalar** appears: “gmul → projection” (still one conceptual level)

From `test_cases_gmul_2proj` / `test_gmul_2Proj`:

```text
(a1 < (a2^a3)) ^ (a1 < (a3^a4))  →  (a1|a3) * (a1 < (a2^a3^a4))
```

Here the overlap is the **middle** 1-blade `a3`. The normal form pulls out **`(a1|a3)`** as an explicit scalar factor and leaves a single contraction over `a2^a3^a4`. The `±` bookkeeping is folded into that scalar and into `CapelliOptionB.coefficient` for this backend—not left as a raw wedge sign on the same term.

Another single-level shape with a **2-blade** upper and projection brackets:

```text
((A1^A2) < (B1^B2^C1^C2)) ^ ((A1^A2) < (B1^B2^D1^D2)) ^ ((A1^A2) < (D1^D2^B4^C4))
  →  (((A1^A2)|(B1^B2)) * ((A1^A2)|(D1^D2))) * ((A1^A2) < (B1^B2^C1^C2^D1^D2^B4^C4))
```

So: **expansion** in the user-facing sense means “wedge of several mergeable contractions **expands** (rewrites) to **one** long contraction, times **scalar** factors built from overlaps (`|`) and coefficients.”

---

## 3. Single level: what “expansion” means (proof sketch)

Fix one merge of two factors `(A < X) ^ (A < Y)` where `X` and `Y` are **pure wedge products** of 1-blades (same `A`, and compatible geometry so sandhi applies).

**Step A — vichcheda (split).**  
Write `X = U1 ^ C` and `Y = C ^ U2` after reordering, where `C` is the **greatest common wedge** of `X` and `Y` (in the tests, often a single shared `B2` or `a3`). Reordering `X` and `Y` into `(unique part) ^ (common part)` costs signs `sign1`, `sign2` from `parity`.

**Step B — sandhi (merge).**  
The algorithm builds one down blade whose atomic factors are **`U1`, factors of `C`, `U2`** in the order prescribed by the merge (see `_split_common_unique` and the following rebuild). Intuitively:

```text
(A < (U1^C)) ^ (A < (C^U2))  ⇒  coeff * (A < (U1^C^U2))
```

with `coeff` absorbing `sign1`, `sign2`, metric pairings (e.g. `(a1|a3)`), and higher Option-B data.

**Step C — why this is a “proof by expansion” at one level.**  
You are not summing a huge coproduct sum by hand; you are showing that the **closed normal form** is obtained by:

1. **Expanding** the two sides into a common/unique decomposition (vichcheda),
2. **Collecting** into one contraction (sandhi),
3. **Reading off** the scalar factor (possibly `1` or a product of `|` terms).

The test suite **proves** the identities for those expressions by running `canon_iter(gextp)` and comparing to the expected right-hand side—so for those inputs, the expansion is **exactly** the displayed rewrite, including sign and scalar placement.

**Minimal arithmetic of `±` for the first sandhi line.**  
Take `X = B1^B2` and `Y = B2^B3`. Intersection is `{B2}`; unique parts are `{B1}` and `{B3}`. On the first side, the target order “unique then common” is already `[B1, B2]`, so `sign1 = parity([B1,B2],[B1,B2]) = +1`. On the second side, `[B2,B3]` is already “common then unique”, so `sign2 = parity([B2,B3],[B2,B3]) = +1`. No extra `−` is introduced at this level; the merged down blade is `B1^B2^B3` as in `A1<(B1^B2^B3)`. (Other examples need nontrivial swaps or scalar pairings—then `±` shows up in `parity` or in factors like `(a1|a3)`.)

---

## 4. One level deeper (nested shared core)

When the shared “middle” is not only 1-blades but **repeated contraction depth** (`D1`, `D2`, `D3`, …), the same vichcheda/sandhi story repeats **inside** the down side. From `test_cases_gmul_2proj` (lines 85–86) / `test_cases_sandhi_complex`:

```text
((D1<(A1^A2^(D2<(B1^B2^(D3<(C1^C2^C3))))))^(D1<(A3^A4^(D2<(B3^B4^(D3<(C1^C2^C3^C4)))))))
  →
((D1^D2^D3)|(C1^C2^C3))*(D1<(A1^A2^A3^A4^(D2<(B1^B2^B3^B4^(D3<(C1^C2^C3^C4))))))
```

Outer merge lines up `D1`; inner merges line up `D2`, `D3`, and the shared `C`-blade; the **scalar** block `((D1^D2^D3)|(C1^C2^C3))` is the packaged “overlap” at that depth. **Idempotence** and **order-invariance** checks for similar shapes are in `test_sandhi_idempotence_complex`, `test_sandhi_order_invariance_complex`, and `test_sandhi_deep_stress_batch`.

---

## 5. Pointers

| Topic | Location |
|--------|----------|
| Examples and assertions | `Sygal/operators/assop/test/test_gextp.py` |
| Split/merge implementation | `gextpcanon.py` → `concat`, `_split_common_unique` |
| Coefficient / virtual layer | `gextpcapelli.py` |
| Hopf / coproduct picture | `extsimp.md` |
