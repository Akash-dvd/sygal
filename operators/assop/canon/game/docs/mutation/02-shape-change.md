# Mutation 2 — Shape Change

Shape change alters the tree representation of a left contraction without
changing its algebraic value. It lets a germ become flatter or deeper so that
another mutation can match its structure.

## Vector-only domain

All named atoms and all individual contraction pins are grade-1 vectors.
A flattened left blade such as `a₁∧a₂` is therefore a blade built from vectors;
deepening exposes those same vectors as separate contraction levels. General
versors are outside the game grammar.

## Symbolic examples

For a two-vector left blade:

```text
(a₁ ∧ a₂) ⌋ (b₁ ∧ b₂ ∧ b₃)
  ↔
a₁ ⌋ (a₂ ⌋ (b₁ ∧ b₂ ∧ b₃))
```

For a three-vector left blade:

```text
(a₁ ∧ a₂ ∧ a₃) ⌋ B
  ↔
a₁ ⌋ (a₂ ⌋ (a₃ ⌋ B))
```

The rightmost factor of the flat left blade acts first:

```text
(a₁ ∧ a₂) ⌋ B
                 a₂ acts first
  = a₁ ⌋ (a₂ ⌋ B)
```

Shape change can act on a selected subtree rather than the whole germ:

```text
d ⌋ (L ∧ ((a₁ ∧ a₂) ⌋ B) ∧ R)

  ↔

d ⌋ (L ∧ (a₁ ⌋ (a₂ ⌋ B)) ∧ R)
```

## Two directions

### Deepen

```text
(a₁ ∧ a₂) ⌋ B
  → a₁ ⌋ (a₂ ⌋ B)
```

This exposes individual contraction levels.

### Flatten

```text
a₁ ⌋ (a₂ ⌋ B)
  → (a₁ ∧ a₂) ⌋ B
```

This is the direction implemented by Sygal's `glcntrct` canonicalization rule
`lcntrctconcat_rl`.

## Game operation

1. Select a contraction subtree.
2. Choose **deepen** or **flatten**.
3. Replace only that subtree.
4. Preserve its coefficient and sign.
5. Recompute grades and possible Sandhi matches.

Shape change does not itself earn or borrow a scalar. It is a structural
equivalence, not a Sandhi merge or a Viccheda split.

## Boundary

The rewrite assumes Sygal's left-contraction convention and valid homogeneous
grades. The engine must reject a requested reshape when the selected expression
does not match the contraction-tree pattern.
