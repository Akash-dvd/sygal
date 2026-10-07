import Sandhi.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic

/-!
# Grade-1 left-contraction expansion

Paper formula (3.1) for `r = 1`:

\[
a \lrcorner X
 = \sum_i (-1)^i\, (a\cdot x_i)\, X_{\widehat i}
\]

when `X = x₀ ∧ ⋯ ∧ xₙ₋₁` is encoded as `ofList xs`.

We first match the recursive algorithm (`expandRec`), then show it equals
the closed Finset sum (`expandSum`).
-/

open LinearMap (BilinForm)
open Finset

namespace Sandhi

variable {R : Type*} [CommRing R]
variable {M : Type*} [AddCommGroup M] [Module R M]

/-- Omit the `i`-th factor from a decomposable blade. -/
def eraseFactor (xs : List M) (i : ℕ) : ExteriorAlgebra R M :=
  ofList (xs.eraseIdx i)

/-- Grade-1 Capelli coefficient `(-1)^i (a · xᵢ)`. -/
def expandCoeff (B : BilinForm R M) (a : M) (xs : List M) (i : ℕ) : R :=
  expandSign (R := R) i * B a (xs.getD i 0)

/-- Recursive expansion mirroring `contractVec_ι_mul`. -/
def expandRec (B : BilinForm R M) (a : M) : List M → ExteriorAlgebra R M
  | [] => 0
  | x :: xs =>
      B a x • ofList xs - ExteriorAlgebra.ι R x * expandRec B a xs

/-- Closed grade-1 expansion sum over factor indices. -/
def expandSum (B : BilinForm R M) (a : M) (xs : List M) : ExteriorAlgebra R M :=
  ∑ i ∈ range xs.length, expandCoeff B a xs i • eraseFactor xs i

/-- The recursive expansion is exactly vector left contraction. -/
theorem contractVec_ofList_eq_expandRec (B : BilinForm R M) (a : M)
    (xs : List M) :
    contractVec B a (ofList xs) = expandRec B a xs := by
  induction xs with
  | nil =>
      simp [expandRec, contractVec_one]
  | cons x xs ih =>
      simp [ofList_cons, contractVec_ι_mul, expandRec, ih]

@[simp]
theorem eraseFactor_zero_cons (x : M) (xs : List M) :
    eraseFactor (R := R) (x :: xs) 0 = ofList xs := by
  simp [eraseFactor]

@[simp]
theorem eraseFactor_succ_cons (x : M) (xs : List M) (i : ℕ) :
    eraseFactor (R := R) (x :: xs) (i + 1) =
      ExteriorAlgebra.ι R x * eraseFactor (R := R) xs i := by
  simp [eraseFactor, ofList_cons]

@[simp]
theorem expandCoeff_zero_cons (B : BilinForm R M) (a x : M) (xs : List M) :
    expandCoeff B a (x :: xs) 0 = B a x := by
  simp [expandCoeff, expandSign]

theorem expandCoeff_succ_cons (B : BilinForm R M) (a x : M) (xs : List M)
    (i : ℕ) :
    expandCoeff B a (x :: xs) (i + 1) = -expandCoeff B a xs i := by
  simp [expandCoeff, expandSign_succ, neg_mul]

/-- Recursive form equals the closed Σ-expansion. -/
theorem expandRec_eq_expandSum (B : BilinForm R M) (a : M) (xs : List M) :
    expandRec B a xs = expandSum B a xs := by
  induction xs with
  | nil =>
      simp [expandRec, expandSum]
  | cons x xs ih =>
      simp only [expandRec, expandSum, List.length_cons, sum_range_succ',
        expandCoeff_zero_cons, eraseFactor_zero_cons, ih]
      -- Ba•xs - ι * ∑_xs = Ba•xs + ∑_i (-cᵢ)•(ι * eᵢ)
      have h :
          (∑ i ∈ range xs.length,
              expandCoeff B a (x :: xs) (i + 1) •
                eraseFactor (R := R) (x :: xs) (i + 1)) =
            -(ExteriorAlgebra.ι R x *
              ∑ i ∈ range xs.length,
                expandCoeff B a xs i • eraseFactor (R := R) xs i) := by
        calc
          (∑ i ∈ range xs.length,
              expandCoeff B a (x :: xs) (i + 1) •
                eraseFactor (R := R) (x :: xs) (i + 1))
              = ∑ i ∈ range xs.length,
                  -(expandCoeff B a xs i •
                    (ExteriorAlgebra.ι R x *
                      eraseFactor (R := R) xs i)) := by
                  refine sum_congr rfl fun i _ => ?_
                  rw [expandCoeff_succ_cons, eraseFactor_succ_cons, neg_smul]
          _ = ∑ i ∈ range xs.length,
                -(ExteriorAlgebra.ι R x *
                  (expandCoeff B a xs i • eraseFactor (R := R) xs i)) := by
                refine sum_congr rfl fun i _ => ?_
                rw [← mul_smul_comm (expandCoeff B a xs i)
                  (ExteriorAlgebra.ι R x)]
          _ = -(∑ i ∈ range xs.length,
                  ExteriorAlgebra.ι R x *
                    (expandCoeff B a xs i • eraseFactor (R := R) xs i)) := by
                rw [sum_neg_distrib]
          _ = -(ExteriorAlgebra.ι R x *
                ∑ i ∈ range xs.length,
                  expandCoeff B a xs i • eraseFactor (R := R) xs i) := by
                rw [Finset.mul_sum]
      rw [h]
      abel

/-- Grade-1 case of paper expansion (3.1). -/
theorem contractVec_ofList_eq_expandSum (B : BilinForm R M) (a : M)
    (xs : List M) :
    contractVec B a (ofList xs) = expandSum B a xs := by
  rw [contractVec_ofList_eq_expandRec, expandRec_eq_expandSum]

end Sandhi
