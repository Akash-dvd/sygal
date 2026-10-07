import Sandhi.Basic
import Sandhi.Seam
import Sandhi.Capelli
import Sandhi.Grade
import Mathlib.Tactic

/-!
# Grade-\(r\) sole-seam (Phase 2)

Aligned panels with a decomposable seam list `ss` of grade \(r\):

\[
A = U \wedge S,\qquad B = S \wedge V,\qquad
A \sqcup B = U \wedge S \wedge V,
\]

and contractor `as` with `|as| = |ss| = r`.

\[
(A_{\mathrm{ctr}}\lrcorner A)\wedge(A_{\mathrm{ctr}}\lrcorner B)
=(A_{\mathrm{ctr}}\mid S)\,(A_{\mathrm{ctr}}\lrcorner(A\sqcup B)).
\]

Fully proved for \(r \le 1\). The general-\(r\) statement is given in terms of
`seamPairing` and reduces to Capelli extraction + the grade-1 identity.
-/

open LinearMap (BilinForm)

namespace Sandhi

variable {R : Type*} [CommRing R]
variable {M : Type*} [AddCommGroup M] [Module R M]

/-- Left panel `U ∧ S`. -/
def panelLeftR (us ss : List M) : ExteriorAlgebra R M :=
  ofList us * ofList ss

/-- Right panel `S ∧ V`. -/
def panelRightR (ss vs : List M) : ExteriorAlgebra R M :=
  ofList ss * ofList vs

/-- Stitched blade `U ∧ S ∧ V`. -/
def panelStitchR (us ss vs : List M) : ExteriorAlgebra R M :=
  ofList us * ofList ss * ofList vs

@[simp] theorem panelLeftR_singleton (us : List M) (s : M) :
    panelLeftR (R := R) us [s] = panelLeft us s := by
  simp [panelLeftR, panelLeft, ofList_cons, ofList_nil, mul_one]

@[simp] theorem panelRightR_singleton (s : M) (vs : List M) :
    panelRightR (R := R) [s] vs = panelRight s vs := by
  simp [panelRightR, panelRight, ofList_cons, ofList_nil]

@[simp] theorem panelStitchR_singleton (us : List M) (s : M) (vs : List M) :
    panelStitchR (R := R) us [s] vs = panelStitch us s vs := by
  simp [panelStitchR, panelStitch, ofList_cons, ofList_nil, mul_one]

/-- Grade-0 sole-seam (empty contractor and seam). -/
theorem soleSeam_grade0 (B : BilinForm R M) (us vs : List M) :
    contractBlade B ([] : List M) (panelLeftR us []) *
        contractBlade B ([] : List M) (panelRightR [] vs) =
      seamPairing B ([] : List M) [] •
        contractBlade B ([] : List M) (panelStitchR us [] vs) := by
  simp [panelLeftR, panelRightR, panelStitchR, ofList_nil, one_mul, mul_one,
    seamPairing_nil, one_smul]

/-- Grade-1 sole-seam recovered from Phase 1. -/
theorem soleSeam_grade1_lists (B : BilinForm R M) (a s : M)
    (us vs : List M) :
    contractBlade B [a] (panelLeftR us [s]) *
        contractBlade B [a] (panelRightR [s] vs) =
      seamPairing B [a] [s] •
        contractBlade B [a] (panelStitchR us [s] vs) := by
  simpa [seamPairing_singleton] using soleSeam_grade1 B a s us vs

/--
Moving the second panel's contraction outside:
\((A\lrcorner(U\wedge S))\wedge(A\lrcorner Y)
 = (-1)^{kr}\,A\lrcorner\bigl((A\lrcorner(U\wedge S))\wedge Y\bigr)\),
where \(k = |U| + |S| - r\).
-/
theorem contractBlade_panel_mul (B : BilinForm R M) (as us ss : List M)
    (y : ExteriorAlgebra R M) :
    contractBlade B as (panelLeftR us ss) * contractBlade B as y =
      expandSign (R := R) (((us ++ ss).length - as.length) * as.length) •
        contractBlade B as (contractBlade B as (panelLeftR us ss) * y) := by
  have hz :
      contractBlade B as (panelLeftR (R := R) us ss) ∈
        homSpan (R := R) (M := M) ((us ++ ss).length - as.length) := by
    rw [panelLeftR, ← ofList_append]
    exact subSpan_le_homSpan _ _ (contractBlade_ofList_mem_subSpan B as _)
  rw [contractBlade_mul_of_annihilated B as hz
      (fun a ha => contractVec_contractBlade_of_mem B ha _) y,
    smul_smul, expandSign_mul_self, one_smul]

/--
**Grade-\(r\) sole-seam identity** (paper §3), aligned panels, any grade:
\[
(A\lrcorner(U\wedge S))\wedge(A\lrcorner(S\wedge V))
 =(A\mid S)\,A\lrcorner(U\wedge S\wedge V).
\]
-/
theorem soleSeam_gradeR (B : BilinForm R M) (as us ss vs : List M)
    (hlen : as.length = ss.length) :
    contractBlade B as (panelLeftR us ss) *
        contractBlade B as (panelRightR ss vs) =
      seamPairing B as ss •
        contractBlade B as (panelStitchR us ss vs) := by
  set σ := expandSign (R := R) (us.length * as.length)
  have hk : (us ++ ss).length - as.length = us.length := by simp [hlen]
  have hseam :
      contractBlade B as (panelLeftR (R := R) us ss) * ofList ss =
        σ • (seamPairing B as ss • panelLeftR (R := R) us ss) := by
    rw [panelLeftR, contractBlade_ofList_mul_seam_mul_seam B as us ss hlen.le,
      contractBlade_ofList_eq_seamPairing B as ss hlen, mul_assoc,
      ← Algebra.smul_def, mul_smul_comm]
  rw [contractBlade_panel_mul, hk, panelRightR, ← mul_assoc, hseam,
    smul_mul_assoc, smul_mul_assoc, map_smul, map_smul, smul_smul, smul_smul,
    expandSign_mul_self, one_mul, panelLeftR, panelStitchR]

/--
**Vanish branch of the grade gate:** if the seam is longer than the
contractor (\(t > r\)), the two contracted panels wedge to zero.
-/
theorem soleSeam_vanish (B : BilinForm R M) (as us ss vs : List M)
    (hlt : as.length < ss.length) :
    contractBlade B as (panelLeftR us ss) *
        contractBlade B as (panelRightR ss vs) = 0 := by
  have hseam :
      contractBlade B as (panelLeftR (R := R) us ss) * ofList ss = 0 := by
    rw [panelLeftR, contractBlade_ofList_mul_seam_mul_seam B as us ss hlt.le,
      mul_assoc, mul_ofList_eq_zero_of_mem_subSpan (k := ss.length - as.length)
        (by omega) (contractBlade_ofList_mem_subSpan B as ss),
      mul_zero, smul_zero]
  rw [contractBlade_panel_mul, panelRightR, ← mul_assoc, hseam, zero_mul,
    map_zero, smul_zero]

theorem soleSeam_gradeR_of_length_le_one (B : BilinForm R M)
    (as us ss vs : List M) (hlen : as.length = ss.length)
    (_hle : as.length ≤ 1) :
    contractBlade B as (panelLeftR us ss) *
        contractBlade B as (panelRightR ss vs) =
      seamPairing B as ss •
        contractBlade B as (panelStitchR us ss vs) :=
  soleSeam_gradeR B as us ss vs hlen

end Sandhi
