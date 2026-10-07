# Sandhi formalization

Lean 4 / Mathlib proof that **sandhi stitching is a theorem**: when two
contraction expressions share a seam, their wedge product collapses to a single
expression times a scalar pairing, with an exact sign. No `sorry`; the main
results depend only on the standard axioms (`propext`, `Classical.choice`,
`Quot.sound`).

See [`SOURCES.md`](SOURCES.md) for the Mathlib inventory and gap analysis.

## Scope

The proof answers one question: *given* a seam across two expressions, is
stitching them valid? Yes — for every grade and every nesting depth.

**Out of scope here:** *finding* the seam in an arbitrary expression
(pattern matching, reordering factors into position, orientation). That is a
search problem handled by the Python canonicalizer
(`operators/assop/canon/`), not a mathematical claim.

## Main theorem — nested stitching

A nest is a list of levels $(D_i, U_i, V_i)$: contractor $D_i$, left wing
$U_i$, right wing $V_i$. Write

$$
\Phi_U(X) = D_1\lrcorner\bigl(U_1\wedge D_2\lrcorner(U_2\wedge\cdots D_k\lrcorner X)\bigr),
\qquad A = D_1 D_2\cdots D_k,
$$

and similarly $\Phi_V$ (wings $V_i$) and $\Phi_{UV}$ (wings $U_i\wedge V_i$).
Let $S$ be the shared seam blade.

| Case | Statement | Lean |
|------|-----------|------|
| $\lvert A\rvert = \lvert S\rvert$ | $\Phi_U(U_x\wedge S)\wedge\Phi_V(S\wedge W) = \varepsilon\,(A\mid S)\,\Phi_{UV}(U_x\wedge S\wedge W)$ | `nested_soleSeam'` |
| $\lvert A\rvert < \lvert S\rvert$ | $\Phi_U(U_x\wedge S)\wedge\Phi_V(S\wedge W) = 0$ | `nested_vanish` |

- **Sign:** $\varepsilon = (-1)^{\sum_i \lvert V_i\rvert\,(\lvert U_x\rvert + \sum_{j>i}\lvert U_j\rvert)}$,
  the shuffle parity of moving each $V_i$ past the deeper left wings.
- **Pairing:** $(A\mid S) = (-1)^{\binom r2}\det[a_i\cdot s_j]$ (Capelli),
  `contractBlade_ofList_eq_seamPairing`.
- Depth $k = 1$ is the flat sole-seam identity `soleSeam_gradeR` /
  `soleSeam_vanish`.
- The three-level identity checked symbolically by Sygal in
  [`../tests/test1.py`](../tests/test1.py) is proved as an `example` at the end
  of `Sandhi/Nested.lean` (sign $+1$). The flat and two-panel checks
  [`test2.py`](../tests/test2.py) and [`test3.py`](../tests/test3.py) are
  instances of the same theorems.

Conventions: `ExteriorAlgebra R M` over a commutative ring, an arbitrary
bilinear form `B`, left contraction `contractVec B u = contractLeft (B u)`, and
$(u\wedge A)\lrcorner X = u\lrcorner(A\lrcorner X)$.

## Proof idea

Flat case, with $Z = A\lrcorner(U\wedge S)$:

1. Every contractor $a_i$ annihilates $Z$, so
   $Z\wedge(A\lrcorner Y) = \pm A\lrcorner(Z\wedge Y)$.
2. $Z\wedge S = \pm U\wedge(A\lrcorner S)\wedge S$: a term that spends a
   contractor on $U$ keeps a factor of $S$, which dies against $S$.
3. $A\lrcorner S = (A\mid S)$ when $\lvert A\rvert=\lvert S\rvert$ (Laplace on
   the last row); $(A\lrcorner S)\wedge S = 0$ when $\lvert A\rvert<\lvert S\rvert$.

Nested case: induction on depth, carrying an extra contractor $E$ outside
the right nest. Each step pulls the outer $D$ out of both sides, pushes
$E\,D$ past $V_1$ (error terms vanish by the deficient case), and recurses.
The base is $S\wedge(E\lrcorner(S\wedge Y)) = S\wedge(E\lrcorner S)\wedge Y$.
No sum over index sets is needed.

## Modules

| Module | Contents |
|--------|----------|
| `Sandhi.Basic` | `contractVec`, `contractBlade`, `ofList`, graded Leibniz |
| `Sandhi.Expansion` | Grade-1 Σ-expansion (3.1) |
| `Sandhi.Seam` | Grade-1 sole-seam |
| `Sandhi.Grade` | Homogeneous / seam-error spans, self-annihilation |
| `Sandhi.Capelli` | Gram determinant, `seamPairing`, extraction for all $r$ |
| `Sandhi.SeamR` | Flat stitching for all $r$: `soleSeam_gradeR`, `soleSeam_vanish` |
| `Sandhi.Nested` | Nested stitching, any depth: `nested_soleSeam'`, `nested_vanish` |
| `Sandhi.Panel` | Flat panel state machine, grade gate, `panelStitch_sound` |
| `Sandhi.Induction`, `Sandhi.Stitching` | Abstract gate / reduce soundness |

## Build

```bash
lake exe cache get   # once
lake build
```

Toolchain: Lean **v4.33.1**, Mathlib **v4.33.1**.

## Not formalized

- Seam detection and putting an arbitrary expression tree into level form
  (search / pattern matching; see Scope).
- The hidden-seam regime $\lvert A\rvert > \lvert S\rvert$ inside a nest
  (up/down vichcheda). `Sandhi.Panel` models only a flat version.
- The closed Σ-form (3.1) for $r > 1$ — the proof does not need it.
- Schedule independence (confluence).
