# Sandhi formalization

This directory contains the Lean formalization of the sandhi identities.

## Verification order

1. Establish the exterior-algebra operations and contraction convention.
2. Prove the grade-one sole-seam identity.
3. Generalize the proof to a grade-\(r\) seam and its determinant pairing.
4. Define nested contraction panels and prove fixed-schedule stitching soundness
   by induction on nesting height.
5. Treat schedule independence as a separate confluence theorem.

The paper currently states the nested result conditionally on a sole-seam
closure invariant. The Lean development must either prove that invariant for
the concrete panel syntax or retain the theorem as an explicitly conditional
result.