import Sandhi.Induction

/-!
# Fixed-schedule stitching

The executable part of the first formalization is intentionally generic:
`Spec` supplies the algebra-specific gate, descent operation, and local
soundness lemmas.  The theorem below is the Lean analogue of fixed-schedule
stitching correctness.
-/

namespace Sandhi

universe u v

def stitch {State : Type u} {Result : Type v}
    (spec : Spec State Result) : Nat → State → Result :=
  reduce spec

theorem stitch_sound {State : Type u} {Result : Type v}
    (spec : Spec State Result) :
    ∀ {n : Nat} {s : State}, Valid spec n s → stitch spec n s = spec.direct s :=
  reduce_sound spec

end Sandhi
