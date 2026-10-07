import Sandhi.Nested

/-!
# Up vichcheda (unequal contractors)

When two panels have contractors `K ∧ P` and `K`, the implementation peels
`P` into the first panel's down blade,

\[
(K\wedge P)\lrcorner X = K\lrcorner(P\lrcorner X),
\]

(`contractBlade_append`) and stitches on the seam \(S = P\lrcorner X\) when
it occurs as a factor of the other panel. Every non-scalar result of that
path is the vanishing

\[
(K\lrcorner S)\wedge K\lrcorner(w_1\wedge S\wedge w_2) = 0
\qquad (\operatorname{grade} S > |K|),
\]

proved here as `upVichcheda_vanish` (seam on the right panel) and
`upVichcheda_vanish_right` (seam on the left panel).

The statement is false for a general homogeneous \(S\); it uses that
\(P\lrcorner X\) is again a blade when \(X\) is a wedge of vectors
(`contractBlade_ofList_blade`, over a field).
-/

open LinearMap (BilinForm)

namespace Sandhi

section CommRing

variable {R : Type*} [CommRing R]
variable {M : Type*} [AddCommGroup M] [Module R M]

theorem contractVec_ofList_of_forall_eq_zero (B : BilinForm R M) (u : M) :
    ∀ l : List M, (∀ y ∈ l, B u y = 0) → contractVec B u (ofList (R := R) l) = 0
  | [], _ => by simp [ofList_nil]
  | y :: l, h => by
      rw [ofList_cons, contractVec_ι_mul, h y (List.mem_cons_self ..), zero_smul, zero_sub,
        contractVec_ofList_of_forall_eq_zero B u l
          (fun z hz => h z (List.mem_cons_of_mem _ hz)), mul_zero, neg_zero]

/-- Adding multiples of `x` to the other factors does not change `x ∧ ⋯`. -/
theorem ι_mul_ofList_map_add_smul (x : M) (c : M → R) :
    ∀ l : List M,
      ExteriorAlgebra.ι R x * ofList (R := R) (l.map fun y => y + c y • x) =
        ExteriorAlgebra.ι R x * ofList l
  | [] => rfl
  | a :: l => by
      have hx : ExteriorAlgebra.ι R x * ExteriorAlgebra.ι R (a + c a • x) =
          ExteriorAlgebra.ι R x * ExteriorAlgebra.ι R a := by
        rw [map_add, map_smul, mul_add, mul_smul_comm, ExteriorAlgebra.ι_sq_zero, smul_zero,
          add_zero]
      rw [List.map_cons, ofList_cons, ofList_cons, ← mul_assoc, hx, ← mul_assoc,
        ι_mul_ι_anticomm x a, neg_mul, neg_mul, mul_assoc, mul_assoc,
        ι_mul_ofList_map_add_smul x c l]

theorem ofList_append_cons (l₁ l₂ : List M) (x : M) :
    ofList (R := R) (l₁ ++ x :: l₂) =
      expandSign (R := R) l₁.length • (ExteriorAlgebra.ι R x * ofList (l₁ ++ l₂)) := by
  rw [ofList_append, ofList_cons, ← mul_assoc, ofList_mul_ι, smul_mul_assoc, mul_assoc,
    ← ofList_append]

/-- A sub-blade of `ss` of positive grade, times anything, dies against `ss`. -/
theorem mul_mul_ofList_eq_zero_of_mem_subSpan {ss : List M} {k : ℕ} (hk : 1 ≤ k)
    {z : ExteriorAlgebra R M} (hz : z ∈ subSpan (R := R) ss k) (w : ExteriorAlgebra R M) :
    z * w * ofList ss = 0 := by
  induction hz using Submodule.span_induction with
  | mem x hx =>
      obtain ⟨m, hm, hlen, rfl⟩ := hx
      obtain ⟨y, m', rfl⟩ := List.exists_cons_of_ne_nil
        (List.ne_nil_of_length_pos (l := m) (by omega))
      rw [ofList_cons, mul_assoc (ExteriorAlgebra.ι R y)]
      exact ι_mul_mul_ofList_of_mem (hm.subset (List.mem_cons_self ..)) _
  | zero => simp
  | add x y _ _ hx hy => rw [add_mul, add_mul, hx, hy, add_zero]
  | smul a x _ hx => rw [smul_mul_assoc, smul_mul_assoc, hx, smul_zero]

/--
**Vanish with arbitrary wings:** for \(|K| < |S|\),
\((K\lrcorner S)\wedge K\lrcorner(w_1\wedge S\wedge w_2) = 0\).
-/
theorem soleSeam_vanish_wings (B : BilinForm R M) (as ss : List M)
    (w₁ w₂ : ExteriorAlgebra R M) (hlt : as.length < ss.length) :
    contractBlade B as (ofList (R := R) ss) * contractBlade B as (w₁ * ofList ss * w₂) = 0 := by
  have hzs := contractBlade_ofList_mem_subSpan (R := R) B as ss
  have h := contractBlade_mul_of_annihilated B as (subSpan_le_homSpan _ _ hzs)
    (fun a ha => contractVec_contractBlade_of_mem B ha _) (w₁ * ofList ss * w₂)
  have hzero : contractBlade B as (ofList (R := R) ss) * (w₁ * ofList ss * w₂) = 0 := by
    rw [← mul_assoc, ← mul_assoc,
      mul_mul_ofList_eq_zero_of_mem_subSpan (by omega) hzs, zero_mul]
  rw [hzero, map_zero] at h
  have h2 := congrArg
    (fun t => expandSign (R := R) ((ss.length - as.length) * as.length) • t) h
  simp only [smul_zero, smul_smul, expandSign_mul_self, one_smul] at h2
  exact h2.symm

/-- The same with the seam panel on the right; the wings are homogeneous. -/
theorem soleSeam_vanish_wings_right (B : BilinForm R M) (as ss : List M) {i₁ i₂ : ℕ}
    {w₁ w₂ : ExteriorAlgebra R M} (h₁ : w₁ ∈ homSpan (R := R) (M := M) i₁)
    (h₂ : w₂ ∈ homSpan (R := R) (M := M) i₂) (hlt : as.length < ss.length) :
    contractBlade B as (w₁ * ofList (R := R) ss * w₂) * contractBlade B as (ofList ss) = 0 := by
  have hz := contractBlade_mem_homSpan B as (ofList_mem_homSpan (R := R) ss)
  have hy := contractBlade_mem_homSpan B as
    (mul_mem_homSpan (mul_mem_homSpan h₁ (ofList_mem_homSpan (R := R) ss)) h₂)
  rw [homSpan_mul_comm hz hy, soleSeam_vanish_wings B as ss w₁ w₂ hlt, smul_zero]

end CommRing

section Field

variable {R : Type*} [Field R]
variable {M : Type*} [AddCommGroup M] [Module R M]

/-- Over a field, contracting a blade by a vector gives a scalar times a blade. -/
theorem contractVec_ofList_blade (B : BilinForm R M) (u : M) (xs : List M) :
    ∃ (c : R) (ys : List M), ys.length = xs.length - 1 ∧
      contractVec B u (ofList (R := R) xs) = c • ofList ys := by
  by_cases h : ∀ y ∈ xs, B u y = 0
  · exact ⟨0, xs.tail, by simp, by rw [contractVec_ofList_of_forall_eq_zero B u xs h, zero_smul]⟩
  · push Not at h
    obtain ⟨x, hx, hux⟩ := h
    obtain ⟨l₁, l₂, rfl⟩ := List.append_of_mem hx
    let c : M → R := fun y => -(B u y / B u x)
    have hg : ∀ y ∈ (l₁ ++ l₂).map (fun y => y + c y • x), B u y = 0 := by
      intro y hy
      obtain ⟨z, -, rfl⟩ := List.mem_map.1 hy
      simp only [c, map_add, map_smul, smul_eq_mul]
      field_simp
      ring
    refine ⟨expandSign (R := R) l₁.length * B u x, (l₁ ++ l₂).map (fun y => y + c y • x),
      by simp, ?_⟩
    rw [ofList_append_cons, map_smul, ← ι_mul_ofList_map_add_smul x c, contractVec_ι_mul,
      contractVec_ofList_of_forall_eq_zero B u _ hg, mul_zero, sub_zero, smul_smul]

/-- Over a field, contracting a blade by a blade gives a scalar times a blade. -/
theorem contractBlade_ofList_blade (B : BilinForm R M) :
    ∀ (P xs : List M), ∃ (c : R) (ys : List M), ys.length = xs.length - P.length ∧
      contractBlade B P (ofList (R := R) xs) = c • ofList ys
  | [], xs => ⟨1, xs, by simp, by simp⟩
  | p :: P, xs => by
      obtain ⟨c, ys, hl, h⟩ := contractBlade_ofList_blade B P xs
      obtain ⟨c', zs, hl', h'⟩ := contractVec_ofList_blade B p ys
      refine ⟨c * c', zs, by simp only [hl', hl, List.length_cons]; omega, ?_⟩
      rw [contractBlade_cons, LinearMap.comp_apply, h, map_smul, h', smul_smul]

/--
**Up vichcheda, vanish branch.** With contractors `K ++ P` and `K`, peel `P`
into the first panel; if the peeled seam \(S = P\lrcorner X\) occurs in the
second panel and \(\operatorname{grade} S > |K|\), the product is zero.
-/
theorem upVichcheda_vanish (B : BilinForm R M) (K P xs : List M)
    (w₁ w₂ : ExteriorAlgebra R M) (h : K.length + P.length < xs.length) :
    contractBlade B (K ++ P) (ofList (R := R) xs) *
        contractBlade B K (w₁ * contractBlade B P (ofList xs) * w₂) = 0 := by
  obtain ⟨c, ys, hl, hP⟩ := contractBlade_ofList_blade B P xs
  rw [contractBlade_append, LinearMap.comp_apply, hP]
  simp only [map_smul, mul_smul_comm, smul_mul_assoc]
  rw [soleSeam_vanish_wings B K ys w₁ w₂ (by omega), smul_zero, smul_zero]

/-- **Up vichcheda, vanish branch**, seam panel on the other side. -/
theorem upVichcheda_vanish_right (B : BilinForm R M) (K P xs : List M) {i₁ i₂ : ℕ}
    {w₁ w₂ : ExteriorAlgebra R M} (h₁ : w₁ ∈ homSpan (R := R) (M := M) i₁)
    (h₂ : w₂ ∈ homSpan (R := R) (M := M) i₂) (h : K.length + P.length < xs.length) :
    contractBlade B K (w₁ * contractBlade B P (ofList (R := R) xs) * w₂) *
        contractBlade B (K ++ P) (ofList xs) = 0 := by
  obtain ⟨c, ys, hl, hP⟩ := contractBlade_ofList_blade B P xs
  rw [contractBlade_append, LinearMap.comp_apply, hP]
  simp only [map_smul, mul_smul_comm, smul_mul_assoc]
  rw [soleSeam_vanish_wings_right B K ys h₁ h₂ (by omega), smul_zero, smul_zero]

end Field

end Sandhi
