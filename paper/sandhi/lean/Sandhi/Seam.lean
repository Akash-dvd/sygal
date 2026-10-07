import Sandhi.Basic
import Mathlib.Tactic

/-!
# Grade-1 sole-seam identity

Paper §2 (sole-shared-seam), with orientation signs taken to be `+1`
by working in aligned form:

\[
A = U \wedge s,\qquad B = s \wedge V,\qquad
A \sqcup B = U \wedge s \wedge V.
\]

\[
(a \lrcorner A) \wedge (a \lrcorner B)
 = (a\cdot s)\,(a \lrcorner (A \sqcup B)).
\]

Here `U = ofList us` and `V = ofList vs` are decomposable.
-/

open LinearMap (BilinForm)

namespace Sandhi

variable {R : Type*} [CommRing R]
variable {M : Type*} [AddCommGroup M] [Module R M]

/-- Aligned left panel `U ∧ s`. -/
def panelLeft (us : List M) (s : M) : ExteriorAlgebra R M :=
  ofList us * ExteriorAlgebra.ι R s

/-- Aligned right panel `s ∧ V`. -/
def panelRight (s : M) (vs : List M) : ExteriorAlgebra R M :=
  ExteriorAlgebra.ι R s * ofList vs

/-- Stitched blade `U ∧ s ∧ V`. -/
def panelStitch (us : List M) (s : M) (vs : List M) : ExteriorAlgebra R M :=
  ofList us * ExteriorAlgebra.ι R s * ofList vs

/-- Special case `U = 1`. -/
theorem soleSeam_grade1_nil (B : BilinForm R M) (a s : M) (vs : List M) :
    contractVec B a (panelLeft [] s) * contractVec B a (panelRight s vs) =
      B a s • contractVec B a (panelStitch [] s vs) := by
  simp only [panelLeft, panelRight, panelStitch, ofList_nil, one_mul]
  rw [contractVec_ι, contractVec_ι_mul]
  simp [Algebra.algebraMap_eq_smul_one, smul_sub]

/--
Grade-1 sole-shared-seam identity (paper §2), aligned orientations.
-/
theorem soleSeam_grade1 (B : BilinForm R M) (a s : M)
    (us vs : List M) :
    contractVec B a (panelLeft us s) * contractVec B a (panelRight s vs) =
      B a s • contractVec B a (panelStitch us s vs) := by
  -- Notation for the proof
  set U := ofList (R := R) (M := M) us
  set V := ofList (R := R) (M := M) vs
  set σ := expandSign (R := R) us.length
  set cU := contractVec B a U
  set cV := contractVec B a V
  set ιs := (ExteriorAlgebra.ι R s : ExteriorAlgebra R M)
  set α := B a s
  -- Panel expansions
  have hL : contractVec B a (panelLeft us s) = cU * ιs + σ • (U * (α • 1)) := by
    simp only [panelLeft, U, σ, cU, ιs, α]
    simpa [contractVec_ι, Algebra.algebraMap_eq_smul_one] using
      contractVec_ofList_mul B a us (ExteriorAlgebra.ι R s)
  have hR : contractVec B a (panelRight s vs) = α • V - ιs * cV := by
    simp only [panelRight, V, ιs, α, cV]
    exact contractVec_ι_mul B a s (ofList vs)
  have hS :
      contractVec B a (panelStitch us s vs) =
        cU * (ιs * V) + σ • (U * (α • V - ιs * cV)) := by
    simp only [panelStitch, U, V, σ, cU, ιs, α, cV, mul_assoc]
    have := contractVec_ofList_mul B a us (ExteriorAlgebra.ι R s * ofList vs)
    simpa [contractVec_ι_mul, contractVec_ι, Algebra.algebraMap_eq_smul_one,
      mul_assoc] using this
  -- s ∧ s = 0 kills the cross term (cU * ιs) * (ιs * cV)
  have kill : (cU * ιs) * (ιs * cV) = 0 := by
    rw [mul_assoc cU, ← mul_assoc ιs ιs, ExteriorAlgebra.ι_sq_zero, zero_mul, mul_zero]
  rw [hL, hR, hS]
  simp only [add_mul, mul_sub, smul_mul_assoc, mul_smul_comm, smul_sub, smul_smul,
    mul_assoc, kill, zero_add, one_mul]
  -- Expand both sides' α-distributions
  conv_lhs => rw [smul_add]
  conv_rhs => rw [smul_add, smul_sub]
  simp only [smul_smul, mul_left_comm, mul_comm]
  abel

end Sandhi
