# Mutation 3 — Viccheda

Viccheda dissects a selected section of a germ into overlapping child panels.
The overlap is deliberately present in both children so that a later Sandhi can
recognize their shared seam.

Viccheda must also record the scalar that Sandhi would produce when the children
are recombined. The children alone are generally **not** literally equal to the
original expression.

## Vector-only domain

Every atomic pin and every factor appearing in a cut section is a grade-1
vector. A multi-vector seam such as `B∧C` is an explicitly ordered blade made
from vectors, never an opaque general versor.

## Symbolic example — one-vector seam

Start with:

```text
T = d ⌋ (A ∧ B ∧ C)
```

Cut at `B`:

```text
left  = d ⌋ (A ∧ B)
right = d ⌋ (B ∧ C)
```

Their later Sandhi relation is:

```text
left ∧ right = (d | B) · T
```

Therefore Viccheda stores:

```text
children: [left, right]
borrowed scalar: (d | B)
```

Equivalently, if `(d | B)` is invertible:

```text
T = ((d ⌋ (A ∧ B)) ∧ (d ⌋ (B ∧ C))) / (d | B)
```

The game should normally keep a scalar-debt token instead of introducing an
unsafe symbolic division.

## Symbolic example — longer chain

Select the section `B ∧ C` of:

```text
T = d ⌋ (A ∧ B ∧ C ∧ D)
```

A cut may produce:

```text
left  = d ⌋ (A ∧ B ∧ C)
right = d ⌋ (B ∧ C ∧ D)
```

The shared section is:

```text
S = B ∧ C
```

The split state carries an overlap scalar associated with contracting the pin
against `S`. For a multi-vector seam this can be a determinant/Capelli factor,
not merely a single inner product.

Schematic accounting:

```text
left ∧ right = overlap(d, S) · T
```

The exact `overlap(d, S)` and any sign must come from `SandhiCanon`.

## Nested example

```text
T = d₁ ⌋ (A ∧ (d₂ ⌋ (B ∧ C ∧ D)) ∧ E)
```

Selecting only the inner section gives:

```text
inner-left  = d₂ ⌋ (B ∧ C)
inner-right = d₂ ⌋ (C ∧ D)
borrowed scalar = (d₂ | C)
```

The outer shell `d₁ ⌋ (A ∧ □ ∧ E)` is retained around the resulting children.

## Game operation

1. Select a contiguous section and a cut seam.
2. Validate that both child panels are legal.
3. Duplicate the seam into both children.
4. Preserve the parent sign and surrounding tree context.
5. Attach a borrowed-scalar token containing:
   - overlap expression,
   - sign/parity,
   - source seam,
   - source parent ID.
6. Do not allow the token to disappear except through a validated Sandhi,
   cancellation or explicit scalar payment.

## Boundary

The existing browser game's midpoint split is only a teaching approximation.
Exact arbitrary-section Viccheda requires engine-generated children and overlap
accounting. It must not assert `parent = left ∧ right` while omitting the
borrowed scalar.
