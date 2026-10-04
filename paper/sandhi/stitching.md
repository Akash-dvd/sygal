# The Stitching Algorithm

*Draft exposition for §Algorithm. All examples verified by direct expansion.*

---

## 1. The picture

Two contraction panels share a common blade — the **seam**. The seam is a
physical joint: to stitch the panels together, the seam must face the join
from both sides.

```
        panel B                  panel C
   ┌──────────┬─────┐      ┌─────┬──────────┐
   │    b     │  S  │      │  S  │    c     │
   └──────────┴─────┘      └─────┴──────────┘
                  seam    seam
                     ↘    ↙
              ┌──────────┬─────┬──────────┐
              │    b     │  S  │    c     │
              └──────────┴─────┴──────────┘
                   stitched, seam counted once
```

Three steps:

1. **Align.** Reorder each panel's down blade so the seam is adjacent to the
   join — rightmost in the left panel, leftmost in the right panel. Each
   reordering costs a parity sign.
2. **Check the joint.** The seam must be grade-matched to the accumulated
   contractor. If it is, the pairing extracts as a scalar. If the seam is too
   small, descend one level; if too large, the expression is zero.
3. **Stitch.** Concatenate `b ∧ S ∧ c`, counting the seam once, and multiply
   by the extracted scalar and the accumulated parity.

Nothing else happens. The same three steps run at every nesting level and at
every seam grade.

---

## 2. Notation

| Symbol | Meaning |
|---|---|
| `∧` | exterior product |
| `⌟` | left contraction |
| `(A \| S)` | scalar pairing of grade-matched blades |
| `A` | accumulated contractor, grade `r` |
| `S` | seam blade, grade `t` |
| `b`, `c` | unique (non-seam) factors, grades `p`, `q` |

Throughout, `p_ij := a_i · a_j`.

---

## 3. Why alignment is not cosmetic

The seam has an orientation. Writing `B = b ∧ S` versus `B = S ∧ b` differs
by `(-1)^{pt}`, and that sign lands in the final answer. Alignment is the step
that fixes the convention so the parity can be computed once and carried.

**Convention.** Left panel presents the seam last; right panel presents it
first:

```
B = ε_B · (b ∧ S)        C = ε_C · (S ∧ c)        ε ∈ {+1, −1}
```

`ε_B`, `ε_C` are the parities of the reorderings that put the blades in these
forms.

---

## 4. Worked examples

### 4.1 Already aligned (the base case)

```
a₁ ⌟ (a₂ ∧ a₃)   ∧   a₁ ⌟ (a₃ ∧ a₄)
```

Seam `a₃`. Left panel: seam already rightmost, `ε_B = +1`, `b = a₂`.
Right panel: seam already leftmost, `ε_C = +1`, `c = a₄`.

Stitch:

```
(a₁ · a₃) · a₁ ⌟ (a₂ ∧ a₃ ∧ a₄)
```

**Verification.** Expanding each contraction,

```
LHS = [p₁₂a₃ − p₁₃a₂] ∧ [p₁₃a₄ − p₁₄a₃]
    = p₁₂p₁₃(a₃∧a₄) − p₁₃²(a₂∧a₄) + p₁₃p₁₄(a₂∧a₃)
    = p₁₃ · [ p₁₂(a₃∧a₄) − p₁₃(a₂∧a₄) + p₁₄(a₂∧a₃) ]
```

and the bracket is exactly `a₁ ⌟ (a₂ ∧ a₃ ∧ a₄)`. ✓

Note the seam pairing `p₁₃` factors out cleanly — this is the mechanism the
whole algorithm generalizes.

### 4.2 Misaligned — the parity is real

```
a₁ ⌟ (a₂ ∧ a₃)   ∧   a₁ ⌟ (a₂ ∧ a₄)
```

Seam `a₂`. It is **leftmost** in the left panel, so it must be moved:

```
a₂ ∧ a₃ = −(a₃ ∧ a₂)        ⟹  ε_B = −1,  b = a₃
a₂ ∧ a₄  already aligned     ⟹  ε_C = +1,  c = a₄
```

Stitch:

```
−(a₁ · a₂) · a₁ ⌟ (a₃ ∧ a₂ ∧ a₄)
```

**Verification.**

```
LHS = [p₁₂a₃ − p₁₃a₂] ∧ [p₁₂a₄ − p₁₄a₂]
    = p₁₂ · [ p₁₂(a₃∧a₄) − p₁₄(a₃∧a₂) − p₁₃(a₂∧a₄) ]

RHS = −p₁₂ · a₁ ⌟ (a₃ ∧ a₂ ∧ a₄)
    = −p₁₂ · [ p₁₃(a₂∧a₄) − p₁₂(a₃∧a₄) + p₁₄(a₃∧a₂) ]
```

Equal. ✓ Had the parity been dropped, the result would carry the wrong sign
throughout — this is the most common failure mode of a naive matcher.

### 4.3 Degenerate seam — the sanity check

Let `A = a₁ ∧ a₂` (grade 2), `S` a grade-2 blade, and take `b` empty:

```
(A ⌟ S) ∧ (A ⌟ (S ∧ c))
```

Here `A ⌟ S = (A | S)` is already scalar, so the left side is literally
`(A | S) · A ⌟ (S ∧ c)` — which is what the rule returns with `b` empty.
The identity is trivially satisfied, confirming the convention has no stray
sign at the boundary. ✓

### 4.4 Shared factor outside the seam — vanishing

```
a₁ ⌟ (a₂ ∧ a₃)   ∧   a₁ ⌟ (a₃ ∧ a₂)
```

Seam `a₃`, but `b = a₂` and `c = a₂` are not disjoint. The stitched blade
`a₂ ∧ a₃ ∧ a₂ = 0`, so the right side vanishes.

The left side vanishes too: the second panel is the negative of the first, and
`X ∧ X = 0` for `X` of odd grade... more precisely, the two contractions are
proportional, so their wedge is zero. ✓

**This is why disjointness appears as a hypothesis.** It is not needed for the
equality — both sides vanish — but it is needed for `S` to be *the* seam
rather than one of several.

### 4.5 Grade-matched seam of higher grade

```
A = d₁ ∧ d₂        (r = 2)
S = s₁ ∧ s₂        (t = 2)
B = b ∧ s₁ ∧ s₂    C = s₁ ∧ s₂ ∧ c
```

Stitch:

```
(A | S) · A ⌟ (b ∧ s₁ ∧ s₂ ∧ c),    where (A | S) = det [ dᵢ · sⱼ ]
```

The pairing is the 2×2 Gram determinant. This is the point where the
coefficient stops being a single inner product and becomes a minor — and it
is the same rule, not a new one.

### 4.6 Nested — three levels

```
T₁ = d₁ ⌟ ( a₁∧a₂ ∧ ( d₂ ⌟ ( b₁∧b₂ ∧ ( d₃ ⌟ (c₁∧c₂∧c₃) ) ) ) )
T₂ = d₁ ⌟ ( a₃∧a₄ ∧ ( d₂ ⌟ ( b₃∧b₄ ∧ ( d₃ ⌟ (c₁∧c₂∧c₃∧c₄) ) ) ) )
```

Processed outside-in. At each level the contractor and the seam both grow:

| Level | Accumulated contractor | Accumulated seam | Matched? |
|---|---|---|---|
| 1 | `d₁` | — | no, descend |
| 2 | `d₁∧d₂` | — | no, descend |
| 3 | `d₁∧d₂∧d₃` | `c₁∧c₂∧c₃` | **yes**, grade 3 = 3 |

Result:

```
(d₁∧d₂∧d₃ | c₁∧c₂∧c₃)
  × d₁ ⌟ ( a₁∧a₂∧a₃∧a₄ ∧ ( d₂ ⌟ ( b₁∧b₂∧b₃∧b₄
                          ∧ ( d₃ ⌟ (c₁∧c₂∧c₃∧c₄) ) ) ) )
```

The scalar cannot be determined before descending, because neither the
contractor nor the seam is complete until the innermost level is reached.
This is why a flat pattern matcher fails and recursion is essential.

---

## 5. The grade condition, stated correctly

Let `r = grade(A)`, `t = grade(S)`, `p = grade(b)`, `q = grade(c)`.

```
LHS grade  =  (p + t − r) + (t + q − r)  =  p + q + 2t − 2r
RHS grade  =  (p + t + q − r)
Difference =  t − r
```

A **scalar** coefficient is therefore possible exactly when `t = r`.

| Condition | Meaning | Action |
|---|---|---|
| `t < r` | seam not yet complete | descend one level, accumulate |
| `t = r` | seam matches contractor | extract scalar, stitch |
| `t > r` | seam over-contracted | zero |

The deficit `x` used in the implementation is a restatement of `t − r`; it
need not be computed as an independent quantity. **The gate is: does the
aligned seam match the accumulated contractor's grade?**

---

## 6. The algorithm

```
stitch(expression):
    while some pair of panels shares a seam:
        (P, Q) ← the pair
        align P so its seam is rightmost      → parity ε_P
        align Q so its seam is leftmost       → parity ε_Q
        A ← accumulated contractor
        S ← aligned seam

        if grade(S) > grade(A):
            return 0
        if grade(S) < grade(A):
            descend into the merged down expression and recurse
        else:
            κ ← (A | S) · ε_P · ε_Q
            replace P ∧ Q  by  κ · (A ⌟ (b ∧ S ∧ c))
    return expression
```

One rule. It does not branch on seam grade, on nesting depth, or on whether
the down arguments are atoms or further contractions — those only change
*what* is aligned, never *how*.

---

## 7. What the algorithm is not

- It is not a pattern substitution. The coefficient at any level depends on
  structure discovered below it (§4.6).
- It is not grade-specific. §4.1 (`t = 1`) and §4.5 (`t = 2`) are the same
  rule.
- It does not require the down arguments to be flat. A nested contraction is
  aligned exactly as an atom is.

---

## 8. Open point

Every example above is a single application, or a chain of applications along
one lineage. That the rule remains correct under *arbitrary* nested schedules
— that the merged expression stays in the sole-seam class at every stage — is
verified computationally to depth six but not yet proved. See the conjecture
in §The Recursion.