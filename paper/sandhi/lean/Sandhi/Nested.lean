import Sandhi.Grade
import Sandhi.Capelli
import Mathlib.Tactic

/-!
# Nested sole-seam identity

A *level* is a triple `(D, U, V)`: contractor `D`, left wedge factors `U`,
right wedge factors `V`. For levels `ℓ₁ … ℓ_k`,
\[
\Phi_U(X) = D_1\lrcorner\bigl(U_1\wedge D_2\lrcorner(U_2\wedge\cdots
  D_k\lrcorner(U_k\wedge X))\bigr),
\]
and similarly `Φ_V` (with `V_i`) and the merged nest `Φ_{UV}` (with
`U_i ∧ V_i`). The accumulated contractor is `A = D₁ ++ ⋯ ++ D_k`.

Main results (`nested_soleSeam`, `nested_vanish`): for a seam `S`,
\[
\Phi_U(U_x\wedge S)\wedge\Phi_V(S\wedge W)
 =\pm\,(A\mid S)\;\Phi_{UV}(U_x\wedge S\wedge W)\quad(|A|=|S|),
\]
and the left side is `0` when `|A| < |S|`. The sign is `nestSign`.

Proof: induction on depth with an extra contractor `E` outside the right
nest (`nest_stitch`). The outer contractor annihilates its own panel and is
pulled out; the right copy joins `E` and is pushed inside past `V₁`, where
terms that spend a contractor on `V₁` vanish by the deficient case.
-/

open CliffordAlgebra
open LinearMap (BilinForm)

namespace Sandhi

variable {R : Type*} [CommRing R]
variable {M : Type*} [AddCommGroup M] [Module R M]

/-! ### Graded commutation and homogeneous spans -/

theorem ofList_mul_ofList_comm (m n : List M) :
    ofList (R := R) m * ofList n =
      expandSign (R := R) (m.length * n.length) • (ofList n * ofList m) := by
  induction n with
  | nil => simp [expandSign]
  | cons x n ih =>
      calc
        ofList (R := R) m * ofList (x :: n)
            = (ofList m * ExteriorAlgebra.ι R x) * ofList n := by
              rw [ofList_cons, mul_assoc]
        _ = expandSign (R := R) m.length •
              (ExteriorAlgebra.ι R x * (ofList m * ofList n)) := by
              rw [ofList_mul_ι, smul_mul_assoc, mul_assoc]
        _ = expandSign (R := R) (m.length * (x :: n).length) •
              (ofList (x :: n) * ofList m) := by
              rw [ih, mul_smul_comm, smul_smul, ← expandSign_add, ofList_cons,
                ← mul_assoc, List.length_cons,
                show m.length + m.length * n.length = m.length * (n.length + 1) by ring]

theorem mul_mem_homSpan {i j : ℕ} {z w : ExteriorAlgebra R M}
    (hz : z ∈ homSpan (R := R) (M := M) i) (hw : w ∈ homSpan (R := R) (M := M) j) :
    z * w ∈ homSpan (R := R) (M := M) (i + j) := by
  induction hz using Submodule.span_induction with
  | mem x hx =>
      obtain ⟨m, rfl, rfl⟩ := hx
      induction hw using Submodule.span_induction with
      | mem y hy =>
          obtain ⟨n, rfl, rfl⟩ := hy
          rw [← ofList_append]
          simpa using ofList_mem_homSpan (R := R) (m ++ n)
      | zero => simp
      | add y y' _ _ h h' => rw [mul_add]; exact add_mem h h'
      | smul c y _ h => rw [mul_smul_comm]; exact Submodule.smul_mem _ c h
  | zero => simp
  | add x x' _ _ h h' => rw [add_mul]; exact add_mem h h'
  | smul c x _ h => rw [smul_mul_assoc]; exact Submodule.smul_mem _ c h

theorem homSpan_mul_comm {i j : ℕ} {z w : ExteriorAlgebra R M}
    (hz : z ∈ homSpan (R := R) (M := M) i) (hw : w ∈ homSpan (R := R) (M := M) j) :
    w * z = expandSign (R := R) (j * i) • (z * w) := by
  induction hz using Submodule.span_induction with
  | mem x hx =>
      obtain ⟨m, rfl, rfl⟩ := hx
      induction hw using Submodule.span_induction with
      | mem y hy =>
          obtain ⟨n, rfl, rfl⟩ := hy
          exact ofList_mul_ofList_comm n m
      | zero => simp
      | add y y' _ _ h h' => rw [add_mul, h, h', mul_add, smul_add]
      | smul c y _ h => rw [smul_mul_assoc, h, mul_smul_comm, smul_comm]
  | zero => simp
  | add x x' _ _ h h' => rw [mul_add, h, h', add_mul, smul_add]
  | smul c x _ h => rw [mul_smul_comm, h, smul_mul_assoc, smul_comm]

theorem contractVec_mem_homSpan (B : BilinForm R M) (u : M) {k : ℕ}
    {z : ExteriorAlgebra R M} (hz : z ∈ homSpan (R := R) (M := M) k) :
    contractVec B u z ∈ homSpan (R := R) (M := M) (k - 1) := by
  induction hz using Submodule.span_induction with
  | mem x hx =>
      obtain ⟨m, rfl, rfl⟩ := hx
      exact subSpan_le_homSpan _ _ (contractVec_ofList_mem_subSpan B u m)
  | zero => simp
  | add x y _ _ hx hy => rw [map_add]; exact add_mem hx hy
  | smul c x _ hx => rw [map_smul]; exact Submodule.smul_mem _ c hx

theorem contractBlade_mem_homSpan (B : BilinForm R M) (D : List M) {k : ℕ}
    {z : ExteriorAlgebra R M} (hz : z ∈ homSpan (R := R) (M := M) k) :
    contractBlade B D z ∈ homSpan (R := R) (M := M) (k - D.length) := by
  induction D with
  | nil => simpa using hz
  | cons a D ih => simpa [Nat.sub_sub] using contractVec_mem_homSpan B a ih

/-! ### Contraction calculus -/

/-- A blade contraction passes a factor that all its vectors kill. -/
theorem contractBlade_mul_of_killed (B : BilinForm R M) (D : List M) {k : ℕ}
    {P Q : ExteriorAlgebra R M} (hP : P ∈ homSpan (R := R) (M := M) k)
    (hQ : ∀ d ∈ D, contractVec B d Q = 0) :
    contractBlade B D (P * Q) = contractBlade B D P * Q := by
  induction D with
  | nil => simp
  | cons d D ih =>
      simp only [contractBlade_cons, LinearMap.comp_apply]
      rw [ih fun e he => hQ e (List.mem_cons_of_mem d he),
        contractVec_mul_of_mem_homSpan B d (contractBlade_mem_homSpan B D hP),
        hQ d (List.mem_cons_self ..), mul_zero, smul_zero, add_zero]

theorem contractVec_contractBlade_comm (B : BilinForm R M) (d : M) (D : List M)
    (x : ExteriorAlgebra R M) :
    contractVec B d (contractBlade B D x) =
      expandSign (R := R) D.length • contractBlade B D (contractVec B d x) := by
  induction D with
  | nil => simp [expandSign]
  | cons a D ih =>
      simp only [contractBlade_cons, LinearMap.comp_apply, List.length_cons]
      change contractLeft (B d) (contractLeft (B a) _) = _
      rw [contractLeft_comm]
      change -(contractVec B a (contractVec B d (contractBlade B D x))) = _
      rw [ih, map_smul, expandSign_succ, neg_smul]

theorem contractBlade_contractBlade_comm (B : BilinForm R M) (E D : List M)
    (x : ExteriorAlgebra R M) :
    contractBlade B E (contractBlade B D x) =
      expandSign (R := R) (E.length * D.length) •
        contractBlade B D (contractBlade B E x) := by
  induction E with
  | nil => simp [expandSign]
  | cons c E ih =>
      simp only [contractBlade_cons, LinearMap.comp_apply, List.length_cons]
      rw [ih, map_smul, contractVec_contractBlade_comm, smul_smul, ← expandSign_add,
        show (E.length + 1) * D.length = E.length * D.length + D.length by ring]

/-! ### Pushing a contractor past a left wedge factor -/

/-- Terms where fewer than `j` contractors reach `Y`. -/
def pushErr (B : BilinForm R M) (Y : ExteriorAlgebra R M) (j : ℕ) :
    Submodule R (ExteriorAlgebra R M) :=
  Submodule.span R
    {x | ∃ (i : ℕ) (z : ExteriorAlgebra R M) (C : List M),
      z ∈ homSpan (R := R) (M := M) i ∧ C.length < j ∧ z * contractBlade B C Y = x}

theorem contractVec_mem_pushErr (B : BilinForm R M) (c : M) {Y : ExteriorAlgebra R M}
    {j : ℕ} {x : ExteriorAlgebra R M} (hx : x ∈ pushErr B Y j) :
    contractVec B c x ∈ pushErr B Y (j + 1) := by
  induction hx using Submodule.span_induction with
  | mem y hy =>
      obtain ⟨i, z, C, hz, hC, rfl⟩ := hy
      rw [contractVec_mul_of_mem_homSpan B c hz]
      refine add_mem (Submodule.subset_span ⟨i - 1, _, C, contractVec_mem_homSpan B c hz,
        by omega, rfl⟩) (Submodule.smul_mem _ _ (Submodule.subset_span ⟨i, z, c :: C, hz,
        by simp; omega, rfl⟩))
  | zero => simp
  | add x y _ _ hx hy => rw [map_add]; exact add_mem hx hy
  | smul a x _ hx => rw [map_smul]; exact Submodule.smul_mem _ a hx

theorem contractBlade_ofList_mul_push_sub_mem (B : BilinForm R M) (V : List M)
    (Y : ExteriorAlgebra R M) :
    ∀ C : List M,
      contractBlade B C (ofList (R := R) V * Y) -
          expandSign (R := R) (V.length * C.length) • (ofList V * contractBlade B C Y) ∈
        pushErr B Y C.length
  | [] => by simp [expandSign]
  | c :: C => by
      obtain ⟨e, he, hsplit⟩ :
          ∃ e ∈ pushErr B Y C.length,
            contractBlade B C (ofList (R := R) V * Y) =
              expandSign (R := R) (V.length * C.length) •
                (ofList V * contractBlade B C Y) + e :=
        ⟨_, contractBlade_ofList_mul_push_sub_mem B V Y C, by abel⟩
      have key :
          contractBlade B (c :: C) (ofList (R := R) V * Y) -
              expandSign (R := R) (V.length * (c :: C).length) •
                (ofList V * contractBlade B (c :: C) Y) =
            expandSign (R := R) (V.length * C.length) •
                (contractVec B c (ofList V) * contractBlade B C Y) +
              contractVec B c e := by
        simp only [contractBlade_cons, LinearMap.comp_apply, List.length_cons]
        rw [hsplit, map_add, map_smul, contractVec_ofList_mul, Nat.mul_succ,
          expandSign_add, mul_smul, smul_add]
        abel
      rw [key, List.length_cons]
      refine add_mem (Submodule.smul_mem _ _ (Submodule.subset_span
        ⟨V.length - 1, _, C, contractVec_mem_homSpan B c (ofList_mem_homSpan V),
          by omega, rfl⟩)) (contractVec_mem_pushErr B c he)

/-! ### The seam on the left -/

/-- Terms `w * z` with `w` a sub-blade of `ss` of grade `> j`. -/
def seamErrL (ss : List M) (j : ℕ) : Submodule R (ExteriorAlgebra R M) :=
  Submodule.span R
    {x | ∃ (i : ℕ) (w z : ExteriorAlgebra R M),
      j < i ∧ w ∈ subSpan (R := R) ss i ∧ w * z = x}

theorem contractVec_mem_seamErrL (B : BilinForm R M) (c : M) {ss : List M} {j : ℕ}
    (hj : 1 ≤ j) {x : ExteriorAlgebra R M} (hx : x ∈ seamErrL (R := R) ss j) :
    contractVec B c x ∈ seamErrL (R := R) ss (j - 1) := by
  induction hx using Submodule.span_induction with
  | mem y hy =>
      obtain ⟨i, w, z, hji, hw, rfl⟩ := hy
      rw [contractVec_mul_of_mem_homSpan B c (subSpan_le_homSpan _ _ hw)]
      refine add_mem (Submodule.subset_span ⟨i - 1, _, z, by omega,
        contractVec_mem_subSpan B c hw, rfl⟩) (Submodule.smul_mem _ _
        (Submodule.subset_span ⟨i, w, _, by omega, hw, rfl⟩))
  | zero => simp
  | add x y _ _ hx hy => rw [map_add]; exact add_mem hx hy
  | smul a x _ hx => rw [map_smul]; exact Submodule.smul_mem _ a hx

theorem ofList_mul_eq_zero_of_mem_subSpan {ss : List M} {k : ℕ} (hk : 1 ≤ k)
    {w : ExteriorAlgebra R M} (hw : w ∈ subSpan (R := R) ss k) :
    ofList ss * w = 0 := by
  induction hw using Submodule.span_induction with
  | mem x hx =>
      obtain ⟨m, hm, rfl, rfl⟩ := hx
      rw [ofList_mul_ofList_comm, ofList_mul_ofList_of_sublist hm
        (List.ne_nil_of_length_pos hk), smul_zero]
  | zero => simp
  | add x y _ _ hx hy => rw [mul_add, hx, hy, add_zero]
  | smul a x _ hx => rw [mul_smul_comm, hx, smul_zero]

theorem ofList_mul_eq_zero_of_mem_seamErrL {ss : List M} {j : ℕ}
    {x : ExteriorAlgebra R M} (hx : x ∈ seamErrL (R := R) ss j) :
    ofList ss * x = 0 := by
  induction hx using Submodule.span_induction with
  | mem y hy =>
      obtain ⟨i, w, z, hji, hw, rfl⟩ := hy
      rw [← mul_assoc, ofList_mul_eq_zero_of_mem_subSpan (by omega) hw, zero_mul]
  | zero => simp
  | add x y _ _ hx hy => rw [mul_add, hx, hy, add_zero]
  | smul a x _ hx => rw [mul_smul_comm, hx, smul_zero]

theorem contractBlade_seam_mul_sub_mem (B : BilinForm R M) (ss : List M)
    (Y : ExteriorAlgebra R M) :
    ∀ E : List M, E.length ≤ ss.length →
      contractBlade B E (ofList (R := R) ss * Y) - contractBlade B E (ofList ss) * Y ∈
        seamErrL (R := R) ss (ss.length - E.length)
  | [], _ => by simp
  | c :: E, h => by
      have h' : E.length < ss.length := by simpa using h
      obtain ⟨e, he, hsplit⟩ :
          ∃ e ∈ seamErrL (R := R) ss (ss.length - E.length),
            contractBlade B E (ofList (R := R) ss * Y) =
              contractBlade B E (ofList ss) * Y + e :=
        ⟨_, contractBlade_seam_mul_sub_mem B ss Y E h'.le, by abel⟩
      have hw := contractBlade_ofList_mem_subSpan (R := R) B E ss
      have key :
          contractBlade B (c :: E) (ofList (R := R) ss * Y) -
              contractBlade B (c :: E) (ofList ss) * Y =
            expandSign (R := R) (ss.length - E.length) •
                (contractBlade B E (ofList ss) * contractVec B c Y) +
              contractVec B c e := by
        simp only [contractBlade_cons, LinearMap.comp_apply]
        rw [hsplit, map_add, contractVec_mul_of_mem_homSpan B c (subSpan_le_homSpan _ _ hw)]
        abel
      rw [key, List.length_cons, ← Nat.sub_sub]
      exact add_mem (Submodule.smul_mem _ _ (Submodule.subset_span
        ⟨_, _, _, by omega, hw, rfl⟩)) (contractVec_mem_seamErrL B c (by omega) he)

/-- \(S\wedge(E\lrcorner(S\wedge Y)) = S\wedge(E\lrcorner S)\wedge Y\) for \(|E|\le|S|\). -/
theorem ofList_mul_contractBlade_seam_mul (B : BilinForm R M) (ss E : List M)
    (Y : ExteriorAlgebra R M) (h : E.length ≤ ss.length) :
    ofList ss * contractBlade B E (ofList (R := R) ss * Y) =
      ofList ss * contractBlade B E (ofList ss) * Y := by
  have := ofList_mul_eq_zero_of_mem_seamErrL (contractBlade_seam_mul_sub_mem B ss Y E h)
  rw [mul_sub, sub_eq_zero] at this
  rw [this, mul_assoc]

/-! ### Nests -/

/-- A nesting level: contractor, left wedge factors, right wedge factors. -/
abbrev Level (M : Type*) := List M × List M × List M

/-- Accumulated contractor `D₁ ++ ⋯ ++ D_k`. -/
def accum : List (Level M) → List M
  | [] => []
  | (D, _, _) :: ls => D ++ accum ls

/-- Left nest `D₁⌟(U₁ ∧ D₂⌟(U₂ ∧ ⋯ x))`. -/
def nestL (B : BilinForm R M) : List (Level M) → ExteriorAlgebra R M → ExteriorAlgebra R M
  | [], x => x
  | (D, U, _) :: ls, x => contractBlade B D (ofList U * nestL B ls x)

/-- Right nest `D₁⌟(V₁ ∧ D₂⌟(V₂ ∧ ⋯ x))`. -/
def nestR (B : BilinForm R M) : List (Level M) → ExteriorAlgebra R M → ExteriorAlgebra R M
  | [], x => x
  | (D, _, V) :: ls, x => contractBlade B D (ofList V * nestR B ls x)

/-- Merged nest `D₁⌟(U₁ ∧ V₁ ∧ D₂⌟(U₂ ∧ V₂ ∧ ⋯ x))`. -/
def nestM (B : BilinForm R M) : List (Level M) → ExteriorAlgebra R M → ExteriorAlgebra R M
  | [], x => x
  | (D, U, V) :: ls, x => contractBlade B D (ofList (U ++ V) * nestM B ls x)

/-- Grade of `nestL ls x` when `x` has grade `k`. -/
def nestGrade : List (Level M) → ℕ → ℕ
  | [], k => k
  | (D, U, _) :: ls, k => (U.length + nestGrade ls k) - D.length

/-- Orientation sign; `e` = length of the extra outer contractor. -/
def nestSign : List (Level M) → ℕ → ℕ → R
  | [], _, _ => 1
  | (D, _, V) :: ls, e, g =>
      expandSign (R := R) (V.length * (e + D.length)) *
        expandSign (R := R) (nestGrade ls g * V.length) * nestSign ls (e + D.length) g

theorem nestL_mem_homSpan (B : BilinForm R M) {k : ℕ} {x : ExteriorAlgebra R M}
    (hx : x ∈ homSpan (R := R) (M := M) k) :
    ∀ ls : List (Level M), nestL B ls x ∈ homSpan (R := R) (M := M) (nestGrade ls k)
  | [] => hx
  | (D, U, _) :: ls =>
      contractBlade_mem_homSpan B D
        (mul_mem_homSpan (ofList_mem_homSpan U) (nestL_mem_homSpan B hx ls))

theorem nestM_smul (B : BilinForm R M) (c : R) (x : ExteriorAlgebra R M) :
    ∀ ls : List (Level M), nestM B ls (c • x) = c • nestM B ls x
  | [] => rfl
  | (D, U, V) :: ls => by
      simp only [nestM]
      rw [nestM_smul B c x ls, mul_smul_comm, map_smul]

theorem nestM_zero (B : BilinForm R M) :
    ∀ ls : List (Level M), nestM B ls (0 : ExteriorAlgebra R M) = 0
  | [] => rfl
  | (D, U, V) :: ls => by simp only [nestM]; rw [nestM_zero B ls, mul_zero, map_zero]

/-- Innermost merged argument, with the total contractor `C` acting on a seam copy. -/
def core (B : BilinForm R M) (Ux S W C : List M) : ExteriorAlgebra R M :=
  ofList Ux * ofList S * contractBlade B C (ofList S) * ofList W

theorem core_eq_zero_of_lt (B : BilinForm R M) (Ux S W C : List M)
    (h : C.length < S.length) : core (R := R) B Ux S W C = 0 := by
  rw [core, mul_assoc (ofList Ux), ofList_mul_eq_zero_of_mem_subSpan (k := S.length - C.length)
    (by omega) (contractBlade_ofList_mem_subSpan B C S), mul_zero, zero_mul]

theorem core_eq (B : BilinForm R M) (Ux S W C : List M) (h : C.length = S.length) :
    core (R := R) B Ux S W C =
      seamPairing B C S • (ofList Ux * ofList S * ofList W) := by
  rw [core, contractBlade_ofList_eq_seamPairing B C S h, ← Algebra.commutes,
    ← Algebra.smul_def, smul_mul_assoc]

/-! ### Main induction -/

/--
Stitching with an extra contractor `E` outside the right nest. When
`|E| + |A| = |S|` the core is the scalar `(E ++ A) ∣ S`; when it is smaller,
the core vanishes.
-/
theorem nest_stitch (B : BilinForm R M) (Ux S W : List M) :
    ∀ (ls : List (Level M)) (E : List M),
      E.length + (accum ls).length ≤ S.length →
      nestL B ls (ofList (R := R) Ux * ofList S) *
          contractBlade B E (nestR B ls (ofList S * ofList W)) =
        nestSign (R := R) ls E.length (Ux.length + S.length) •
          nestM B ls (core B Ux S W (E ++ accum ls))
  | [], E, h => by
      simp only [nestL, nestR, nestM, accum, nestSign, List.append_nil, one_smul, core]
      rw [mul_assoc, ofList_mul_contractBlade_seam_mul B S E _ (by simpa [accum] using h),
        ← mul_assoc, ← mul_assoc]
  | (D, U, V) :: ls, E, h => by
      have hacc : accum ((D, U, V) :: ls) = D ++ accum ls := rfl
      rw [hacc] at h ⊢
      have hlen : (E ++ D).length + (accum ls).length ≤ S.length := by
        simp only [List.length_append] at h ⊢; omega
      set L' := nestL B ls (ofList (R := R) Ux * ofList S) with hL'def
      set R' := nestR B ls (ofList (R := R) S * ofList W) with hR'def
      set g := nestGrade ls (Ux.length + S.length)
      have hL' : L' ∈ homSpan (R := R) (M := M) g := by
        refine nestL_mem_homSpan B ?_ ls
        rw [← ofList_append]
        simpa using ofList_mem_homSpan (R := R) (Ux ++ S)
      have hP : ofList U * L' ∈ homSpan (R := R) (M := M) (U.length + g) :=
        mul_mem_homSpan (ofList_mem_homSpan U) hL'
      -- pull the outer contractor out of both panels
      have hpull :
          nestL B ((D, U, V) :: ls) (ofList (R := R) Ux * ofList S) *
              contractBlade B E (nestR B ((D, U, V) :: ls) (ofList S * ofList W)) =
            contractBlade B D
              (ofList U * L' * contractBlade B (E ++ D) (ofList V * R')) := by
        simp only [nestL, nestR]
        rw [← hL'def, ← hR'def, contractBlade_append, LinearMap.comp_apply,
          contractBlade_contractBlade_comm B E D, mul_smul_comm, mul_smul_comm, map_smul,
          contractBlade_mul_of_killed B D hP
            (fun d hd => contractVec_contractBlade_of_mem B hd _)]
      -- terms that spend a contractor on V vanish
      have hvan : ∀ C : List M, C.length < (E ++ D).length →
          L' * contractBlade B C R' = 0 := by
        intro C hC
        rw [nest_stitch B Ux S W ls C (by omega), core_eq_zero_of_lt B Ux S W _
          (by simp only [List.length_append] at hC hlen ⊢; omega), nestM_zero, smul_zero]
      have herr : ∀ x ∈ pushErr B R' (E ++ D).length, L' * x = 0 := by
        intro x hx
        induction hx using Submodule.span_induction with
        | mem y hy =>
            obtain ⟨i, z, C, hz, hC, rfl⟩ := hy
            rw [← mul_assoc, homSpan_mul_comm hz hL', smul_mul_assoc, mul_assoc, hvan C hC,
              mul_zero, smul_zero]
        | zero => simp
        | add x y _ _ hx hy => rw [mul_add, hx, hy, add_zero]
        | smul a x _ hx => rw [mul_smul_comm, hx, smul_zero]
      obtain ⟨e, he, hsplit⟩ :
          ∃ e ∈ pushErr B R' (E ++ D).length,
            contractBlade B (E ++ D) (ofList (R := R) V * R') =
              expandSign (R := R) (V.length * (E ++ D).length) •
                (ofList V * contractBlade B (E ++ D) R') + e :=
        ⟨_, contractBlade_ofList_mul_push_sub_mem B V R' (E ++ D), by abel⟩
      have hinner :
          L' * contractBlade B (E ++ D) (ofList (R := R) V * R') =
            (expandSign (R := R) (V.length * (E ++ D).length) *
                expandSign (R := R) (g * V.length) *
                nestSign (R := R) ls (E ++ D).length (Ux.length + S.length)) •
              (ofList V * nestM B ls (core B Ux S W (E ++ D ++ accum ls))) := by
        rw [hsplit, mul_add, herr e he, add_zero, mul_smul_comm, ← mul_assoc,
          homSpan_mul_comm (ofList_mem_homSpan V) hL', smul_mul_assoc, mul_assoc,
          nest_stitch B Ux S W ls (E ++ D) hlen, mul_smul_comm, smul_smul, smul_smul,
          mul_assoc]
      rw [hpull, mul_assoc, hinner, mul_smul_comm, ← mul_assoc, ← ofList_append, map_smul,
        List.append_assoc]
      simp only [nestM, nestSign, List.length_append]
      rfl

/-! ### Main theorems -/

/--
**Nested sole-seam identity.** With accumulated contractor `A = accum ls` of
the same grade as the seam `S`,
\[
\Phi_U(U_x\wedge S)\wedge\Phi_V(S\wedge W)
 = \operatorname{sign}\cdot(A\mid S)\cdot\Phi_{UV}(U_x\wedge S\wedge W).
\]
-/
theorem nested_soleSeam (B : BilinForm R M) (Ux S W : List M) (ls : List (Level M))
    (h : (accum ls).length = S.length) :
    nestL B ls (ofList (R := R) Ux * ofList S) * nestR B ls (ofList S * ofList W) =
      (nestSign (R := R) ls 0 (Ux.length + S.length) * seamPairing B (accum ls) S) •
        nestM B ls (ofList Ux * ofList S * ofList W) := by
  have := nest_stitch B Ux S W ls [] (by simp [h])
  rw [contractBlade_nil, LinearMap.id_apply] at this
  rw [this, List.nil_append, core_eq B Ux S W _ h, nestM_smul, smul_smul]
  rfl

/-! ### Closed form of the sign -/

def sumU : List (Level M) → ℕ
  | [] => 0
  | (_, U, _) :: ls => U.length + sumU ls

/-- Shuffle parity of interleaving `U₁⋯U_k U_x` with `V₁⋯V_k` into
`U₁V₁⋯U_kV_k U_x`: each `V_i` crosses every deeper `U_j` and `U_x`. -/
def shuffleExp (ux : ℕ) : List (Level M) → ℕ
  | [] => 0
  | (_, _, V) :: ls => V.length * (ux + sumU ls) + shuffleExp ux ls

omit [AddCommGroup M] in
theorem nestGrade_eq :
    ∀ (ls : List (Level M)) (k : ℕ), (accum ls).length ≤ k →
      nestGrade ls k = k + sumU ls - (accum ls).length
  | [], k, _ => by simp [nestGrade, sumU, accum]
  | (D, U, V) :: ls, k, h => by
      have h' : (accum ls).length + D.length ≤ k := by
        simp only [accum, List.length_append] at h; omega
      simp only [nestGrade, sumU, accum, List.length_append]
      rw [nestGrade_eq ls k (by omega)]
      omega

theorem expandSign_add_two_mul (a b : ℕ) :
    expandSign (R := R) (a + 2 * b) = expandSign (R := R) a := by
  simp [expandSign, pow_add, pow_mul]

omit [AddCommGroup M] [Module R M] in
theorem nestSign_eq (ux t : ℕ) :
    ∀ (ls : List (Level M)) (e : ℕ), e + (accum ls).length = t →
      nestSign (R := R) ls e (ux + t) = expandSign (R := R) (shuffleExp ux ls)
  | [], _, _ => by simp [nestSign, shuffleExp, expandSign]
  | (D, U, V) :: ls, e, h => by
      have h' : (e + D.length) + (accum ls).length = t := by
        simp only [accum, List.length_append] at h; omega
      have hg : nestGrade ls (ux + t) = ux + sumU ls + (e + D.length) := by
        rw [nestGrade_eq ls _ (by omega)]; omega
      simp only [nestSign, shuffleExp]
      rw [nestSign_eq ux t ls _ h', hg, ← expandSign_add, ← expandSign_add,
        show V.length * (e + D.length) + (ux + sumU ls + (e + D.length)) * V.length +
            shuffleExp ux ls =
          (V.length * (ux + sumU ls) + shuffleExp ux ls) + 2 * (V.length * (e + D.length))
          by ring, expandSign_add_two_mul]

/--
**Nested sole-seam identity, closed-form sign.** The sign is the shuffle
parity \((-1)^{\sum_i |V_i|(|U_x| + \sum_{j>i}|U_j|)}\).
-/
theorem nested_soleSeam' (B : BilinForm R M) (Ux S W : List M) (ls : List (Level M))
    (h : (accum ls).length = S.length) :
    nestL B ls (ofList (R := R) Ux * ofList S) * nestR B ls (ofList S * ofList W) =
      (expandSign (R := R) (shuffleExp Ux.length ls) * seamPairing B (accum ls) S) •
        nestM B ls (ofList Ux * ofList S * ofList W) := by
  rw [nested_soleSeam B Ux S W ls h, nestSign_eq Ux.length S.length ls 0 (by simp [h])]

/-- `Sygal/test1.py`: three-level nest whose seam `c₁c₂c₃` sits at the bottom. -/
example (B : BilinForm R M) (d1 d2 d3 a1 a2 a3 a4 b1 b2 b3 b4 c1 c2 c3 c4 : M) :
    contractVec B d1 (ofList (R := R) [a1, a2] * contractVec B d2 (ofList [b1, b2] *
        contractVec B d3 (ofList [c1, c2, c3]))) *
      contractVec B d1 (ofList [a3, a4] * contractVec B d2 (ofList [b3, b4] *
        contractVec B d3 (ofList [c1, c2, c3, c4]))) =
    seamPairing B [d1, d2, d3] [c1, c2, c3] •
      contractVec B d1 (ofList [a1, a2, a3, a4] * contractVec B d2 (ofList [b1, b2, b3, b4] *
        contractVec B d3 (ofList [c1, c2, c3, c4]))) := by
  have := nested_soleSeam' (R := R) B [] [c1, c2, c3] [c4]
    [([d1], [a1, a2], [a3, a4]), ([d2], [b1, b2], [b3, b4]), ([d3], [], [])] rfl
  simp only [nestL, nestR, nestM, accum, shuffleExp, sumU, List.length_nil,
    List.length_cons, ofList_nil, one_mul, List.nil_append, List.cons_append,
    contractBlade_singleton] at this
  rw [← ofList_append] at this
  simpa [expandSign, show ((-1 : R) ^ 4) = 1 by norm_num] using this

/-- **Nested vanish branch.** If the seam outgrows the accumulated contractor,
the two nested panels wedge to zero. -/
theorem nested_vanish (B : BilinForm R M) (Ux S W : List M) (ls : List (Level M))
    (h : (accum ls).length < S.length) :
    nestL B ls (ofList (R := R) Ux * ofList S) * nestR B ls (ofList S * ofList W) = 0 := by
  have := nest_stitch B Ux S W ls [] (by simp; omega)
  rw [contractBlade_nil, LinearMap.id_apply] at this
  rw [this, List.nil_append, core_eq_zero_of_lt B Ux S W _ h, nestM_zero, smul_zero]

end Sandhi
