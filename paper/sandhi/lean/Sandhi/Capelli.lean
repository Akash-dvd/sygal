import Sandhi.Basic
import Sandhi.Expansion
import Sandhi.Grade
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

/-!
# Capelli / seam pairing \(A \mid S\)

For equal-length lists,
\[
\operatorname{capelli}(A,S)=\det[(a_i\cdot s_j)],\qquad
\operatorname{seamPairing}(A,S)=(-1)^{r(r-1)/2}\operatorname{capelli}(A,S).
\]

Main result (`contractBlade_ofList_eq_seamPairing`): for every grade \(r\),
iterated left contraction of the seam by the contractor is the scalar
`seamPairing`. The proof is Laplace expansion along the last contractor row
against the grade-1 expansion (3.1).
-/

open LinearMap (BilinForm)
open Matrix Finset

namespace Sandhi

variable {R : Type*} [CommRing R]
variable {M : Type*} [AddCommGroup M] [Module R M]

/-- Gram matrix \((a_i \cdot s_j)\) of size `n`. -/
def gramMatrix (B : BilinForm R M) (n : ℕ) (as ss : List M) :
    Matrix (Fin n) (Fin n) R :=
  .of fun i j => B (as.getD i 0) (ss.getD j 0)

def capelliN (B : BilinForm R M) (n : ℕ) (as ss : List M) : R :=
  (gramMatrix B n as ss).det

def capelli (B : BilinForm R M) (as ss : List M) : R :=
  if as.length = ss.length then capelliN B as.length as ss else 0

def capelliSign (r : ℕ) : R := (-1 : R) ^ (r * (r - 1) / 2)

def seamPairing (B : BilinForm R M) (as ss : List M) : R :=
  capelliSign (R := R) as.length * capelli B as ss

theorem capelliSign_succ (n : ℕ) :
    capelliSign (R := R) (n + 1) = (-1) ^ n * capelliSign (R := R) n := by
  have h := Nat.choose_succ_succ' n 1
  rw [Nat.choose_one_right, show (1 : ℕ) + 1 = 2 from rfl, Nat.choose_two_right,
    Nat.choose_two_right] at h
  unfold capelliSign
  rw [h, pow_add]

@[simp] theorem capelli_nil (B : BilinForm R M) :
    capelli B ([] : List M) [] = 1 := by
  simp [capelli, capelliN, det_fin_zero]

@[simp] theorem seamPairing_nil (B : BilinForm R M) :
    seamPairing B ([] : List M) [] = 1 := by
  simp [seamPairing, capelliSign]

@[simp] theorem capelli_singleton (B : BilinForm R M) (a s : M) :
    capelli B [a] [s] = B a s := by
  simp [capelli, capelliN, gramMatrix]

@[simp] theorem seamPairing_singleton (B : BilinForm R M) (a s : M) :
    seamPairing B [a] [s] = B a s := by
  simp [seamPairing, capelliSign]

theorem capelli_length_ne (B : BilinForm R M) (as ss : List M)
    (h : as.length ≠ ss.length) : capelli B as ss = 0 := by
  simp [capelli, h]

@[simp] theorem seamPairing_length_ne (B : BilinForm R M) (as ss : List M)
    (h : as.length ≠ ss.length) : seamPairing B as ss = 0 := by
  simp [seamPairing, capelli_length_ne B as ss h]

theorem getD_eraseIdx_succAbove (ss : List M) {n : ℕ} (j : Fin (n + 1))
    (k : Fin n) :
    (ss.eraseIdx j).getD k 0 = ss.getD (j.succAbove k) 0 := by
  simp only [List.getD_eq_getElem?_getD, List.getElem?_eraseIdx]
  by_cases h : (k : ℕ) < j
  · rw [Fin.succAbove_of_castSucc_lt _ _ (by simpa [Fin.lt_def] using h)]
    simp [h]
  · rw [Fin.succAbove_of_le_castSucc _ _ (by simpa [Fin.le_def] using h)]
    simp [h]

/-- Laplace expansion of the Gram determinant along the last contractor row. -/
theorem capelliN_append_singleton (B : BilinForm R M) (as : List M) (a : M)
    (ss : List M) :
    capelliN B (as.length + 1) (as ++ [a]) ss =
      ∑ j : Fin (as.length + 1),
        (-1 : R) ^ (as.length + (j : ℕ)) * B a (ss.getD j 0) *
          capelliN B as.length as (ss.eraseIdx j) := by
  unfold capelliN
  rw [det_succ_row _ (Fin.last as.length)]
  refine sum_congr rfl fun j _ => ?_
  have hsub :
      (gramMatrix B (as.length + 1) (as ++ [a]) ss).submatrix
          (Fin.last as.length).succAbove j.succAbove =
        gramMatrix B as.length as (ss.eraseIdx j) := by
    ext i k
    simp only [gramMatrix, submatrix_apply, of_apply, Fin.succAbove_last,
      Fin.val_castSucc, getD_eraseIdx_succAbove]
    congr 1
    simp [List.getD_eq_getElem?_getD]
  rw [hsub]
  simp [gramMatrix]

/--
Capelli extraction for every grade: contracting the seam blade `S` by an
equal-grade contractor `A` gives the scalar `A ∣ S`.
-/
theorem contractBlade_ofList_eq_seamPairing (B : BilinForm R M) (as : List M) :
    ∀ ss : List M, as.length = ss.length →
      contractBlade B as (ofList ss) =
        algebraMap R (ExteriorAlgebra R M) (seamPairing B as ss) := by
  induction as using List.reverseRecOn with
  | nil =>
      intro ss h
      cases ss with
      | nil => simp [Algebra.algebraMap_eq_smul_one]
      | cons => cases h
  | append_singleton as a ih =>
      intro ss h
      have hss : ss.length = as.length + 1 := by simpa using h.symm
      rw [contractBlade_append, LinearMap.comp_apply, contractBlade_singleton,
        contractVec_ofList_eq_expandSum, expandSum, map_sum]
      have hpair :
          seamPairing B (as ++ [a]) ss =
            ∑ i ∈ range ss.length,
              capelliSign (R := R) (as.length + 1) *
                ((-1 : R) ^ (as.length + i) * B a (ss.getD i 0) *
                  capelliN B as.length as (ss.eraseIdx i)) := by
        simp only [seamPairing, capelli, h, if_true]
        rw [hss, capelliN_append_singleton, mul_sum]
        exact Fin.sum_univ_eq_sum_range
          (fun i => capelliSign (R := R) (as.length + 1) *
            ((-1 : R) ^ (as.length + i) * B a (ss.getD i 0) *
              capelliN B as.length as (ss.eraseIdx i))) _
      rw [hpair, map_sum]
      refine sum_congr rfl fun i hi => ?_
      have hi' : i < ss.length := mem_range.1 hi
      have hlen : as.length = (ss.eraseIdx i).length := by
        rw [List.length_eraseIdx_of_lt hi']; omega
      rw [map_smul, eraseFactor, ih _ hlen, Algebra.smul_def, ← map_mul]
      congr 1
      simp only [seamPairing, capelli, hlen, if_true, expandCoeff, expandSign,
        capelliSign_succ, pow_add]
      rw [← hlen]
      have hsq : ((-1 : R) ^ as.length) * (-1) ^ as.length = 1 := by
        rw [← mul_pow]; simp
      linear_combination
        (-((-1 : R) ^ i * B a (ss.getD i 0) * capelliSign (R := R) as.length *
          capelliN B as.length as (ss.eraseIdx i))) * hsq

theorem contractBlade_ofList_eq_seamPairing_of_length_le_one
    (B : BilinForm R M) (as ss : List M)
    (hlen : as.length = ss.length) (_hle : as.length ≤ 1) :
    contractBlade B as (ofList ss) =
      algebraMap R (ExteriorAlgebra R M) (seamPairing B as ss) :=
  contractBlade_ofList_eq_seamPairing B as ss hlen

end Sandhi
