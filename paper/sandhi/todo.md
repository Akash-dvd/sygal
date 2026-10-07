# Formal Proof Checklist

Items marked **Lean** are machine-checked in `lean/` (names in parentheses);
see `lean/README.md` and Section 8 of the draft. Paper-only proofs and open
items are listed separately. Finding seams in an arbitrary expression is an
implementation (search) concern and is deliberately not on this list.

## Local identity

- [x] Contraction-order convention for \(A=a_1\wedge\cdots\wedge a_r\):
  \((u\wedge A)\lrcorner X=u\lrcorner(A\lrcorner X)\). **Lean** (`contractBlade`)
- [x] Coefficient of the seam block is
  \(A\mid S=(-1)^{\binom r2}\det[(a_i\cdot s_j)]\), including the
  contraction-order sign. **Lean** (`contractBlade_ofList_eq_seamPairing`)
- [x] Grade-\(r\) sole-seam identity for arbitrary wings.
  **Lean** (`soleSeam_gradeR`)
- [x] Terms with repeated residual factors vanish. **Lean** (`Sandhi.Grade`
  kill lemmas)
- [x] Orientation factors \(\epsilon_B\epsilon_C\): the theorem is stated on
  oriented panels, so they multiply both sides.
- [ ] Signed sum (3.1) over \(r\)-element subsets for \(r>1\). Paper proof;
  Lean has \(r=1\) (`contractVec_ofList_eq_expandSum`) and does not need
  \(r>1\).

## Grade gate

- [x] Grade difference of the two sides is \(t-r\) (paper, Section 3).
- [x] \(t=r\) gives a scalar coefficient. **Lean** (`soleSeam_gradeR`)
- [x] \(t>r\) gives zero. **Lean** (`soleSeam_vanish`, `nested_vanish`)
- [x] \(t<r\) requires descent: in a nest the contractor accumulates level by
  level until it matches the seam. **Lean** (`nested_soleSeam'`, innermost
  seam)

## Nested recursion

- [x] Closed-form nested identity of any depth with the exact shuffle sign.
  **Lean** (`nested_soleSeam'`, `nestSign_eq`)
- [x] Contractor and seam grades accumulate together (the theorem's
  hypothesis \(\lvert A_{\mathrm{acc}}\rvert=\lvert S\rvert\)). **Lean**
- [x] Recursive cross terms with a repeated residual seam factor vanish.
  **Lean** (`nest_stitch` error terms)
- [ ] Sole-seam invariant for general nested trees, and its preservation
  under one merge (visibility, sibling separation, one-stitch closure).
  Paper proof only.
- [ ] Seam factors distributed across several levels (beyond the
  innermost-seam closed form). Paper proof only.
- [ ] Schedule independence (confluence). Open; do not claim.

## Capelli coefficient

- [x] Determinant pairing and Capelli contraction use the same ordering
  convention. **Lean** (`seamPairing`)
- [x] Seam-alignment parity is separate from the determinant sign: the
  nested sign \(\sigma\) is a shuffle parity, the determinant carries
  \((-1)^{\binom r2}\).

## Applications

- [ ] Write the explicit CGA contraction skeleton for Monge's theorem and
  verify the three-step count.
- [ ] Write the explicit cyclic-quadrilateral reduction for Ptolemy's theorem
  and verify the two-step count.
- [ ] Expand the midpoint construction for the nine-point tangent and verify
  the three-step count against Li's equations (4.14)--(4.20).
- [ ] Check that the three application outputs use the same orientation and
  scale conventions as the cited CGA sources.

## Implementation vs. theorem

- [ ] Confirm Sygal's `|` pairing equals `seamPairing` (sign included) for
  \(r\ge 2\).
- [x] Keep symbolic checks separate from proof: `tests/test1.py`–`test3.py`
  are regression checks of the implementation; `test1` is also proved as a
  Lean `example`.
- [ ] Record the tested nesting depths and grades for the computational
  evidence.
