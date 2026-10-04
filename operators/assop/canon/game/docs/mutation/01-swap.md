# Mutation 1 — Swap

Swap exchanges two factors inside one exterior-product germ. Because the wedge
is alternating, the germ keeps its structure but its coefficient changes sign.

## Vector-only domain

Every atomic symbol such as `a₁`, `a₂` or `b₁` is a grade-1 vector. The game
does not treat a general versor, rotor, spinor or mixed-grade multivector as one
atomic factor. Higher-grade blades are constructed only by wedging vectors.

## Symbolic examples

For two vectors:

```text
a₁ ∧ a₂  →  −(a₂ ∧ a₁)
```

Inside a longer blade:

```text
a₁ ∧ a₂ ∧ a₃  →  −(a₁ ∧ a₃ ∧ a₂)
```

Exchanging the first and third factors is one transposition, so it also changes
the sign:

```text
a₁ ∧ a₂ ∧ a₃  →  −(a₃ ∧ a₂ ∧ a₁)
```

Moving one factor through two positions uses two adjacent swaps and therefore
does not change the final sign:

```text
a₁ ∧ a₂ ∧ a₃
  → −a₂ ∧ a₁ ∧ a₃
  → +a₂ ∧ a₃ ∧ a₁
```

For homogeneous blocks `Aᵣ` and `Bₛ` of grades `r` and `s`:

```text
Aᵣ ∧ Bₛ = (−1)^(r·s) Bₛ ∧ Aᵣ
```

A repeated factor annihilates the germ:

```text
a₁ ∧ a₂ ∧ a₁ = 0
```

## Game operation

1. Select two factor slots in the same wedge blade.
2. Exchange the selected factors.
3. Multiply the germ's stored coefficient by `−1`.
4. If the swap creates a repeated factor, replace the germ with zero.

The sign belongs to the germ and must survive later shape changes, Viccheda and
Sandhi operations.

## Boundary

This mutation swaps factors **inside one wedge**. Exchanging arbitrary branches
of a contraction tree is not automatically a wedge transposition and must be
validated by the algebra engine.
