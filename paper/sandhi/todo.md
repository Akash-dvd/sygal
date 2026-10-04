# Formal Proof Checklist

The local grade-\(r\) identity has been proved mathematically. This file
separates the proof details that still need to be written explicitly in the
paper from the global claims currently supported only by symbolic experiments.

The current draft now includes a conditional induction theorem for nested
recursion. It assumes an explicit sole-seam closure invariant; the remaining
formal task is to derive that invariant from the concrete panel syntax rather
than treating it as an assumption.

## Local identity: write the complete proof

- [ ] State the contraction-order convention precisely for
  \(A=a_1\wedge\cdots\wedge a_r\).
- [ ] Expand \(A\mathbin{\lrcorner}X\) as a signed sum over \(r\)-element
  subsets of the ordered factors of \(X\).
- [ ] Prove that the coefficient of the seam block is the determinant
  \(A\mid S=\det[(a_i\cdot s_j)]\), including the contraction-order sign.
- [ ] Show explicitly how terms with repeated residual factors vanish.
- [ ] Show that the surviving terms are exactly the Laplace/Cauchy--Binet
  expansion of
  \(A\mathbin{\lrcorner}(b\wedge S\wedge c)\).
- [ ] Track \(\epsilon_B\epsilon_C\) through the orientation changes.

## Grade gate

- [ ] Derive \(x=t-r\) from the grades of the two panels and their merged
  panel.
- [ ] Prove the \(t=r\) case produces a scalar coefficient.
- [ ] Under the sole-seam invariant, prove that \(t>r\) leaves repeated
  residual seam factors and therefore gives zero.
- [ ] Explain why \(t<r\) requires descent rather than scalar extraction.

## Nested recursion: remaining global proof

- [ ] Define the sole-seam invariant for a nested contraction tree.
- [ ] Prove that one valid merge preserves decomposability and the
  sole-seam invariant of the merged expression.
- [x] Draft an induction on nesting depth under an explicit sole-seam
  invariant.
- [ ] Prove from the concrete panel syntax that the sole-seam invariant is
  preserved at every merge.
- [ ] Prove by induction on nesting depth, without assuming the closure clause,
  that contractor and seam grades accumulate together.
- [ ] Prove that every recursive cross term containing a repeated residual
  seam factor vanishes.
- [ ] Prove that the grade gate agrees with direct left-contraction expansion
  at every recursive level.
- [ ] If schedule independence is claimed, prove that different valid merge
  orders produce the same result.

## Capelli coefficient

- [ ] Prove that the determinant pairing and the Capelli contraction use the
  same ordering convention.
- [ ] Isolate the parity contribution from seam alignment from the determinant
  sign.

## Applications

- [ ] Write the explicit CGA contraction skeleton for Monge's theorem and
  verify the three-step count.
- [ ] Write the explicit cyclic-quadrilateral reduction for Ptolemy's theorem
  and verify the two-step count.
- [ ] Expand the midpoint construction for the nine-point tangent and verify
  the three-step count against Li's equations (4.14)--(4.20).
- [ ] Check that the three application outputs use the same orientation and
  scale conventions as the cited CGA sources.

## Evidence and claim wording

- [ ] Keep manual symbolic checks separate from mathematical proof.
- [ ] Identify `test2.py` as a manual grade-three, three-panel sanity check;
  it compares expanded expressions rather than asserting a theorem.
- [ ] Record the tested nesting depths and grades for the computational
  evidence.
- [ ] Do not state a global normal-form or confluence theorem until the
  nested-recursion proof is complete.
