/-!
# Fixed-schedule stitching: the induction skeleton

This module formalizes the control-flow part of the nested sandhi argument
without yet choosing a representation for exterior-algebra blades.  The
algebraic work belongs in a later module; this file makes the closure
obligation and the induction theorem explicit.
-/

namespace Sandhi

universe u v

inductive Gate
  | descend
  | balanced
  | vanish
  deriving DecidableEq, Repr

structure Spec (State : Type u) (Result : Type v) where
  gate : State → Gate
  down : State → State
  balanced : State → Result
  zero : Result
  direct : State → Result
  balanced_sound :
    ∀ {s : State}, gate s = Gate.balanced → balanced s = direct s
  vanish_sound :
    ∀ {s : State}, gate s = Gate.vanish → zero = direct s
  descend_sound :
    ∀ {s : State}, gate s = Gate.descend → direct (down s) = direct s

def reduce {State : Type u} {Result : Type v} (spec : Spec State Result) :
    Nat → State → Result
  | 0, s => spec.balanced s
  | n + 1, s =>
      match spec.gate s with
      | Gate.descend => reduce spec n (spec.down s)
      | Gate.balanced => spec.balanced s
      | Gate.vanish => spec.zero

/- The validity predicate is the sole-seam closure invariant for the
   fixed-schedule recursion.  A descend node must produce a valid node of
   strictly smaller height. -/
inductive Valid {State : Type u} {Result : Type v} (spec : Spec State Result) :
    Nat → State → Prop
  | terminal {s : State} :
      spec.gate s = Gate.balanced →
      Valid spec 0 s
  | balanced {n : Nat} {s : State} :
      spec.gate s = Gate.balanced →
      Valid spec (n + 1) s
  | vanish {n : Nat} {s : State} :
      spec.gate s = Gate.vanish →
      Valid spec (n + 1) s
  | descend {n : Nat} {s : State} :
      spec.gate s = Gate.descend →
      Valid spec n (spec.down s) →
      Valid spec (n + 1) s

theorem reduce_sound {State : Type u} {Result : Type v}
    (spec : Spec State Result) :
    ∀ {n : Nat} {s : State}, Valid spec n s → reduce spec n s = spec.direct s
  | 0, s, Valid.terminal h => by
      simpa [reduce, h] using spec.balanced_sound h
  | n + 1, s, Valid.balanced h => by
      simpa [reduce, h] using spec.balanced_sound h
  | n + 1, s, Valid.vanish h => by
      simpa [reduce, h] using spec.vanish_sound h
  | n + 1, s, Valid.descend h valid => by
      rw [show reduce spec (n + 1) s = reduce spec n (spec.down s) by
        simp [reduce, h]]
      rw [reduce_sound spec valid]
      exact spec.descend_sound h

end Sandhi
