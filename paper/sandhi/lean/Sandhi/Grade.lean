import Sandhi.Basic
import Mathlib.Tactic

/-!
# Homogeneous spans and seam-error spans

* `homSpan k`: span of decomposable blades of grade `k`.
* `subSpan l k`: span of `ofList m` with `m` an ordered sublist of `l`, `|m| = k`.
* `seamErr ss j`: span of `ofList n * ofList m` with `m <+ ss`, `|m| > j`;
  every such element dies when wedged with `ofList ss` on the right.

Main tools for the grade-\(r\) sole-seam proof:

* graded Leibniz rule for homogeneous left factors;
* `contractBlade_mul_of_annihilated`: a blade contraction passes through a
  homogeneous factor that every contractor vector annihilates;
* `contractBlade_ofList_mul_seam_sub_mem`: contracting `U ∧ S` equals the
  pure-seam term up to `seamErr`.
-/

open CliffordAlgebra
open LinearMap (BilinForm)

namespace Sandhi

variable {R : Type*} [CommRing R]
variable {M : Type*} [AddCommGroup M] [Module R M]

theorem ofList_append (xs ys : List M) :
    ofList (R := R) (xs ++ ys) = ofList xs * ofList ys := by
  simp [ofList, List.prod_append]

theorem contractBlade_append (B : BilinForm R M) (as bs : List M) :
    contractBlade B (as ++ bs) = contractBlade B as ∘ₗ contractBlade B bs := by
  induction as with
  | nil => simp
  | cons a as ih => simp [ih, LinearMap.comp_assoc]

theorem expandSign_add (m n : ℕ) :
    expandSign (R := R) (m + n) = expandSign m * expandSign n := by
  simp [expandSign, pow_add]

theorem expandSign_mul_self (n : ℕ) :
    expandSign (R := R) n * expandSign n = 1 := by
  simp [expandSign, ← mul_pow]

theorem ι_mul_ι_anticomm (a b : M) :
    ExteriorAlgebra.ι R a * ExteriorAlgebra.ι R b =
      -(ExteriorAlgebra.ι R b * ExteriorAlgebra.ι R a) :=
  CliffordAlgebra.ι_mul_ι_comm_of_isOrtho (Q := (0 : QuadraticForm R M))
    (QuadraticMap.IsOrtho.all (N := R) a b)

/-- Moving a vector across a blade of grade `|l|`. -/
theorem ofList_mul_ι (l : List M) (x : M) :
    ofList (R := R) l * ExteriorAlgebra.ι R x =
      expandSign (R := R) l.length • (ExteriorAlgebra.ι R x * ofList l) := by
  induction l with
  | nil => simp [expandSign]
  | cons a l ih =>
      rw [ofList_cons, mul_assoc, ih, mul_smul_comm, ← mul_assoc,
        ι_mul_ι_anticomm, List.length_cons, expandSign_succ, neg_mul,
        smul_neg, neg_smul, mul_assoc]

/-! ### Spans -/

/-- Span of decomposable blades of grade `k`. -/
def homSpan (k : ℕ) : Submodule R (ExteriorAlgebra R M) :=
  Submodule.span R {x | ∃ m : List M, m.length = k ∧ ofList m = x}

/-- Span of sub-blades of `l` of grade `k` (factors kept in order). -/
def subSpan (l : List M) (k : ℕ) : Submodule R (ExteriorAlgebra R M) :=
  Submodule.span R {x | ∃ m : List M, m.Sublist l ∧ m.length = k ∧ ofList m = x}

/-- Products whose right factor is a sub-blade of `ss` of grade `> j`. -/
def seamErr (ss : List M) (j : ℕ) : Submodule R (ExteriorAlgebra R M) :=
  Submodule.span R
    {x | ∃ n m : List M, m.Sublist ss ∧ j < m.length ∧ ofList n * ofList m = x}

theorem ofList_mem_homSpan (m : List M) :
    ofList (R := R) m ∈ homSpan (R := R) (M := M) m.length :=
  Submodule.subset_span ⟨m, rfl, rfl⟩

theorem ofList_mem_subSpan {m l : List M} (h : m.Sublist l) :
    ofList (R := R) m ∈ subSpan (R := R) l m.length :=
  Submodule.subset_span ⟨m, h, rfl, rfl⟩

theorem subSpan_mono {l l' : List M} (h : l.Sublist l') (k : ℕ) :
    subSpan (R := R) l k ≤ subSpan l' k :=
  Submodule.span_mono fun _ ⟨m, hm, hk, hx⟩ => ⟨m, hm.trans h, hk, hx⟩

theorem subSpan_le_homSpan (l : List M) (k : ℕ) :
    subSpan (R := R) l k ≤ homSpan k :=
  Submodule.span_mono fun _ ⟨m, _, hk, hx⟩ => ⟨m, hk, hx⟩

theorem seamErr_mono {ss : List M} {i j : ℕ} (h : i ≤ j) :
    seamErr (R := R) ss j ≤ seamErr ss i :=
  Submodule.span_mono fun _ ⟨n, m, hm, hj, hx⟩ => ⟨n, m, hm, by omega, hx⟩

theorem ι_mul_mem_subSpan {l : List M} {k : ℕ} (a : M)
    {z : ExteriorAlgebra R M} (hz : z ∈ subSpan (R := R) l k) :
    ExteriorAlgebra.ι R a * z ∈ subSpan (R := R) (a :: l) (k + 1) := by
  induction hz using Submodule.span_induction with
  | mem x hx =>
      obtain ⟨m, hm, rfl, rfl⟩ := hx
      rw [← ofList_cons]
      exact Submodule.subset_span ⟨a :: m, List.cons_sublist_cons.2 hm, rfl, rfl⟩
  | zero => simp
  | add x y _ _ hx hy => rw [mul_add]; exact add_mem hx hy
  | smul c x _ hx => rw [mul_smul_comm]; exact Submodule.smul_mem _ c hx

/-! ### Contraction lowers grade inside sub-blade spans -/

theorem contractVec_ofList_mem_subSpan (B : BilinForm R M) (u : M) (l : List M) :
    contractVec B u (ofList (R := R) l) ∈ subSpan (R := R) l (l.length - 1) := by
  induction l with
  | nil => simp
  | cons a l ih =>
      rw [ofList_cons, contractVec_ι_mul]
      refine sub_mem (Submodule.smul_mem _ _ ?_) ?_
      · simpa using ofList_mem_subSpan (R := R) (List.sublist_cons_self a l)
      · cases l with
        | nil => simp
        | cons b l =>
            simpa using ι_mul_mem_subSpan (R := R) a ih

theorem contractVec_mem_subSpan (B : BilinForm R M) (u : M) {l : List M} {k : ℕ}
    {z : ExteriorAlgebra R M} (hz : z ∈ subSpan (R := R) l k) :
    contractVec B u z ∈ subSpan (R := R) l (k - 1) := by
  induction hz using Submodule.span_induction with
  | mem x hx =>
      obtain ⟨m, hm, rfl, rfl⟩ := hx
      exact subSpan_mono hm _ (contractVec_ofList_mem_subSpan B u m)
  | zero => simp
  | add x y _ _ hx hy => rw [map_add]; exact add_mem hx hy
  | smul c x _ hx => rw [map_smul]; exact Submodule.smul_mem _ c hx

theorem contractBlade_mem_subSpan (B : BilinForm R M) (as : List M) {l : List M}
    {k : ℕ} {z : ExteriorAlgebra R M} (hz : z ∈ subSpan (R := R) l k) :
    contractBlade B as z ∈ subSpan (R := R) l (k - as.length) := by
  induction as with
  | nil => simpa using hz
  | cons a as ih =>
      have := contractVec_mem_subSpan B a ih
      simpa [Nat.sub_sub] using this

theorem contractBlade_ofList_mem_subSpan (B : BilinForm R M) (as l : List M) :
    contractBlade B as (ofList (R := R) l) ∈
      subSpan (R := R) l (l.length - as.length) :=
  contractBlade_mem_subSpan B as (ofList_mem_subSpan (List.Sublist.refl l))

/-! ### Vanishing against the seam -/

theorem ι_mul_mul_ofList_of_mem {x : M} {ss : List M} (hx : x ∈ ss)
    (y : ExteriorAlgebra R M) :
    ExteriorAlgebra.ι R x * y * ofList ss = 0 := by
  obtain ⟨s, t, rfl⟩ := List.append_of_mem hx
  rw [ofList_append, ofList_cons]
  calc
    ExteriorAlgebra.ι R x * y * (ofList s * (ExteriorAlgebra.ι R x * ofList t))
        = (ExteriorAlgebra.ι R x * (y * ofList s) * ExteriorAlgebra.ι R x) *
            ofList t := by simp only [mul_assoc]
    _ = 0 := by rw [ι_mul_mul_ι, zero_mul]

theorem ofList_mul_ofList_of_sublist {m ss : List M} (hm : m.Sublist ss)
    (hne : m ≠ []) : ofList (R := R) m * ofList ss = 0 := by
  obtain ⟨x, m', rfl⟩ := List.exists_cons_of_ne_nil hne
  rw [ofList_cons]
  exact ι_mul_mul_ofList_of_mem (hm.subset (List.mem_cons_self ..)) _

theorem mul_ofList_eq_zero_of_mem_subSpan {ss : List M} {k : ℕ} (hk : 1 ≤ k)
    {z : ExteriorAlgebra R M} (hz : z ∈ subSpan (R := R) ss k) :
    z * ofList ss = 0 := by
  induction hz using Submodule.span_induction with
  | mem x hx =>
      obtain ⟨m, hm, rfl, rfl⟩ := hx
      exact ofList_mul_ofList_of_sublist hm (List.ne_nil_of_length_pos hk)
  | zero => simp
  | add x y _ _ hx hy => rw [add_mul, hx, hy, add_zero]
  | smul c x _ hx => rw [smul_mul_assoc, hx, smul_zero]

theorem mul_ofList_eq_zero_of_mem_seamErr {ss : List M} {j : ℕ}
    {z : ExteriorAlgebra R M} (hz : z ∈ seamErr (R := R) ss j) :
    z * ofList ss = 0 := by
  induction hz using Submodule.span_induction with
  | mem x hx =>
      obtain ⟨n, m, hm, hj, rfl⟩ := hx
      rw [mul_assoc, ofList_mul_ofList_of_sublist hm (List.ne_nil_of_length_pos
        (by omega)), mul_zero]
  | zero => simp
  | add x y _ _ hx hy => rw [add_mul, hx, hy, add_zero]
  | smul c x _ hx => rw [smul_mul_assoc, hx, smul_zero]

theorem mul_mem_seamErr {ss : List M} {i k j : ℕ} (hjk : j < k)
    {z w : ExteriorAlgebra R M} (hz : z ∈ homSpan (R := R) (M := M) i)
    (hw : w ∈ subSpan (R := R) ss k) :
    z * w ∈ seamErr (R := R) ss j := by
  induction hz using Submodule.span_induction with
  | mem x hx =>
      obtain ⟨n, -, rfl⟩ := hx
      induction hw using Submodule.span_induction with
      | mem y hy =>
          obtain ⟨m, hm, hmk, rfl⟩ := hy
          exact Submodule.subset_span ⟨n, m, hm, by omega, rfl⟩
      | zero => simp
      | add y y' _ _ h h' => rw [mul_add]; exact add_mem h h'
      | smul c y _ h => rw [mul_smul_comm]; exact Submodule.smul_mem _ c h
  | zero => simp
  | add x x' _ _ h h' => rw [add_mul]; exact add_mem h h'
  | smul c x _ h => rw [smul_mul_assoc]; exact Submodule.smul_mem _ c h

/-! ### Graded Leibniz on homogeneous spans -/

theorem contractVec_mul_of_mem_homSpan (B : BilinForm R M) (u : M) {k : ℕ}
    {z : ExteriorAlgebra R M} (hz : z ∈ homSpan (R := R) (M := M) k)
    (y : ExteriorAlgebra R M) :
    contractVec B u (z * y) =
      contractVec B u z * y + expandSign (R := R) k • (z * contractVec B u y) := by
  induction hz using Submodule.span_induction with
  | mem x hx =>
      obtain ⟨m, rfl, rfl⟩ := hx
      exact contractVec_ofList_mul B u m y
  | zero => simp
  | add x x' _ _ hx hx' =>
      rw [add_mul, map_add, hx, hx', map_add, add_mul, add_mul, smul_add]
      abel
  | smul c x _ hx =>
      rw [smul_mul_assoc, map_smul, hx, map_smul, smul_mul_assoc, smul_mul_assoc,
        smul_add, smul_comm c (expandSign k)]

theorem contractVec_mem_seamErr (B : BilinForm R M) (u : M) {ss : List M} {j : ℕ}
    (hj : 1 ≤ j) {z : ExteriorAlgebra R M} (hz : z ∈ seamErr (R := R) ss j) :
    contractVec B u z ∈ seamErr (R := R) ss (j - 1) := by
  induction hz using Submodule.span_induction with
  | mem x hx =>
      obtain ⟨n, m, hm, hjm, rfl⟩ := hx
      rw [contractVec_ofList_mul]
      refine add_mem ?_ (Submodule.smul_mem _ _ ?_)
      · exact mul_mem_seamErr (i := n.length - 1) (k := m.length) (by omega)
          (subSpan_le_homSpan _ _ (contractVec_ofList_mem_subSpan B u n))
          (ofList_mem_subSpan hm)
      · exact mul_mem_seamErr (i := n.length) (k := m.length - 1) (by omega)
          (ofList_mem_homSpan n)
          (subSpan_mono hm _ (contractVec_ofList_mem_subSpan B u m))
  | zero => simp
  | add x y _ _ hx hy => rw [map_add]; exact add_mem hx hy
  | smul c x _ hx => rw [map_smul]; exact Submodule.smul_mem _ c hx

/-! ### Self-annihilation and passing a blade through a factor -/

/-- Each contractor vector annihilates the contraction it took part in. -/
theorem contractVec_contractBlade_of_mem (B : BilinForm R M) {a : M} {as : List M}
    (ha : a ∈ as) (x : ExteriorAlgebra R M) :
    contractVec B a (contractBlade B as x) = 0 := by
  induction as with
  | nil => cases ha
  | cons b bs ih =>
      simp only [contractBlade_cons, LinearMap.comp_apply]
      rcases List.mem_cons.1 ha with rfl | hb
      · exact contractLeft_contractLeft (B a) _
      · change contractLeft (B a) (contractLeft (B b) _) = 0
        rw [contractLeft_comm]
        change -(contractVec B b (contractVec B a (contractBlade B bs x))) = 0
        rw [ih hb, map_zero, neg_zero]

/--
If every contractor vector kills the homogeneous factor `z`, the blade
contraction passes through `z` with the Koszul sign `(-1)^{k r}`.
-/
theorem contractBlade_mul_of_annihilated (B : BilinForm R M) (as : List M) {k : ℕ}
    {z : ExteriorAlgebra R M} (hz : z ∈ homSpan (R := R) (M := M) k)
    (hann : ∀ a ∈ as, contractVec B a z = 0) (y : ExteriorAlgebra R M) :
    contractBlade B as (z * y) =
      expandSign (R := R) (k * as.length) • (z * contractBlade B as y) := by
  induction as with
  | nil => simp [expandSign]
  | cons a as ih =>
      have ih' := ih fun b hb => hann b (List.mem_cons_of_mem a hb)
      simp only [contractBlade_cons, LinearMap.comp_apply, List.length_cons]
      rw [ih', map_smul, contractVec_mul_of_mem_homSpan B a hz,
        hann a (List.mem_cons_self ..), zero_mul, zero_add, smul_smul,
        Nat.mul_succ, expandSign_add]

/-! ### Contracting `U ∧ S` up to seam error -/

theorem contractBlade_ofList_mul_seam_sub_mem (B : BilinForm R M) (us ss : List M) :
    ∀ as : List M, as.length ≤ ss.length →
      contractBlade B as (ofList (R := R) us * ofList ss) -
          expandSign (R := R) (us.length * as.length) •
            (ofList us * contractBlade B as (ofList ss)) ∈
        seamErr (R := R) ss (ss.length - as.length)
  | [], _ => by simp
  | a :: as, h => by
      have h' : as.length < ss.length := by simpa using h
      obtain ⟨e, he, hsplit⟩ :
          ∃ e ∈ seamErr (R := R) ss (ss.length - as.length),
            contractBlade B as (ofList (R := R) us * ofList ss) =
              expandSign (R := R) (us.length * as.length) •
                (ofList us * contractBlade B as (ofList ss)) + e :=
        ⟨_, contractBlade_ofList_mul_seam_sub_mem B us ss as h'.le, by abel⟩
      set σ := expandSign (R := R) (us.length * as.length)
      have key :
          contractBlade B (a :: as) (ofList (R := R) us * ofList ss) -
              expandSign (R := R) (us.length * (a :: as).length) •
                (ofList us * contractBlade B (a :: as) (ofList ss)) =
            σ • (contractVec B a (ofList us) * contractBlade B as (ofList ss)) +
              contractVec B a e := by
        simp only [contractBlade_cons, LinearMap.comp_apply, List.length_cons]
        rw [hsplit, map_add, map_smul, contractVec_ofList_mul, Nat.mul_succ,
          expandSign_add, mul_smul, smul_add]
        abel
      rw [key, List.length_cons, ← Nat.sub_sub]
      refine add_mem (Submodule.smul_mem _ _ ?_) ?_
      · exact mul_mem_seamErr (i := us.length - 1) (k := ss.length - as.length)
          (by omega)
          (subSpan_le_homSpan _ _ (contractVec_ofList_mem_subSpan B a us))
          (contractBlade_ofList_mem_subSpan B as ss)
      · exact contractVec_mem_seamErr B a (by omega) he

/--
Right-wedging with the seam kills every term that contracted into `U`:
\((A\lrcorner(U\wedge S))\wedge S = (-1)^{pr}\,U\wedge(A\lrcorner S)\wedge S\).
-/
theorem contractBlade_ofList_mul_seam_mul_seam (B : BilinForm R M)
    (as us ss : List M) (hle : as.length ≤ ss.length) :
    contractBlade B as (ofList (R := R) us * ofList ss) * ofList ss =
      expandSign (R := R) (us.length * as.length) •
        (ofList us * contractBlade B as (ofList ss) * ofList ss) := by
  have h := mul_ofList_eq_zero_of_mem_seamErr
    (contractBlade_ofList_mul_seam_sub_mem B us ss as hle)
  rw [sub_mul, sub_eq_zero, smul_mul_assoc] at h
  exact h

end Sandhi
