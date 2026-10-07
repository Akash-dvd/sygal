import Mathlib.LinearAlgebra.ExteriorAlgebra.Basic
import Mathlib.LinearAlgebra.CliffordAlgebra.Contraction
import Mathlib.LinearAlgebra.BilinearForm.Basic
import Mathlib.Tactic

/-!
# Exterior left contraction (paper convention)

Multivectors are `ExteriorAlgebra R M` (definitionally `CliffordAlgebra 0`).
The metric is a bilinear form `B`; vector left contraction is Mathlib's
`CliffordAlgebra.contractLeft` applied to the dual `B u`.

Blade contraction iterates vectors in paper order:
`A = a₁ ∧ ⋯ ∧ aᵣ` acts as `a₁ ⌟ (a₂ ⌟ (⋯ ⌟ ·))`.
-/

open CliffordAlgebra
open LinearMap (BilinForm)

namespace Sandhi

variable {R : Type*} [CommRing R]
variable {M : Type*} [AddCommGroup M] [Module R M]

private abbrev Q0 : QuadraticForm R M := 0

/-- Left contraction by a vector via the metric `B`. -/
def contractVec (B : BilinForm R M) (u : M) :
    ExteriorAlgebra R M →ₗ[R] ExteriorAlgebra R M :=
  contractLeft (B u)

@[simp]
theorem contractVec_one (B : BilinForm R M) (u : M) :
    contractVec B u (1 : ExteriorAlgebra R M) = 0 :=
  contractLeft_one Q0 (B u)

@[simp]
theorem contractVec_ι (B : BilinForm R M) (u v : M) :
    contractVec B u (ExteriorAlgebra.ι R v) =
      algebraMap R (ExteriorAlgebra R M) (B u v) :=
  contractLeft_ι Q0 (B u) v

theorem contractVec_ι_mul (B : BilinForm R M) (u a : M)
    (b : ExteriorAlgebra R M) :
    contractVec B u (ExteriorAlgebra.ι R a * b) =
      B u a • b - ExteriorAlgebra.ι R a * contractVec B u b :=
  contractLeft_ι_mul (B u) a b

/-- In the exterior algebra, \(v \wedge x \wedge v = 0\). -/
theorem ι_mul_mul_ι (v : M) (x : ExteriorAlgebra R M) :
    ExteriorAlgebra.ι R v * x * ExteriorAlgebra.ι R v = 0 := by
  change ι Q0 v * x * ι Q0 v = 0
  induction x using CliffordAlgebra.left_induction with
  | algebraMap r =>
      -- ιv * algebraMap r * ιv = algebraMap r * (ιv * ιv) = 0
      rw [← Algebra.commutes, mul_assoc, ι_sq_scalar, zero_apply, map_zero, mul_zero]
  | add x y hx hy =>
      simp [mul_add, add_mul, hx, hy]
  | ι_mul x m hx =>
      -- ι_mul binders are (x : CliffordAlgebra, m : M); Q0 ⇒ all pairs orthogonal
      have hortho : Q0.IsOrtho v m := QuadraticMap.IsOrtho.all (N := R) v m
      have hanticomm : ι Q0 v * ι Q0 m = -(ι Q0 m * ι Q0 v) :=
        ι_mul_ι_comm_of_isOrtho hortho
      calc
        ι Q0 v * (ι Q0 m * x) * ι Q0 v
            = (ι Q0 v * ι Q0 m) * (x * ι Q0 v) := by simp [mul_assoc]
        _ = (-(ι Q0 m * ι Q0 v)) * (x * ι Q0 v) := by rw [hanticomm]
        _ = -(ι Q0 m * (ι Q0 v * x * ι Q0 v)) := by
              simp [mul_assoc, neg_mul]
        _ = 0 := by simp [hx]

/-- Decomposable blade from an ordered list of vectors (exterior product). -/
def ofList (xs : List M) : ExteriorAlgebra R M :=
  (xs.map (fun x => (ExteriorAlgebra.ι R x : ExteriorAlgebra R M))).prod

@[simp]
theorem ofList_nil : ofList (R := R) (M := M) [] = 1 :=
  rfl

@[simp]
theorem ofList_cons (x : M) (xs : List M) :
    ofList (x :: xs) = ExteriorAlgebra.ι R x * ofList xs :=
  rfl

/-- Iterated left contraction by an ordered contractor blade. -/
def contractBlade (B : BilinForm R M) :
    List M → ExteriorAlgebra R M →ₗ[R] ExteriorAlgebra R M
  | [] => LinearMap.id
  | a :: as => contractVec B a ∘ₗ contractBlade B as

@[simp]
theorem contractBlade_nil (B : BilinForm R M) :
    contractBlade B ([] : List M) = LinearMap.id :=
  rfl

@[simp]
theorem contractBlade_cons (B : BilinForm R M) (a : M) (as : List M) :
    contractBlade B (a :: as) = contractVec B a ∘ₗ contractBlade B as :=
  rfl

@[simp]
theorem contractBlade_singleton (B : BilinForm R M) (a : M)
    (x : ExteriorAlgebra R M) :
    contractBlade B [a] x = contractVec B a x := by
  simp [contractBlade]

/-- Sign of index `i` in the grade-1 expansion (paper: `(-1)^i`). -/
def expandSign (i : ℕ) : R := (-1 : R) ^ i

@[simp]
theorem expandSign_zero : expandSign (R := R) 0 = 1 := by
  simp [expandSign]

@[simp]
theorem expandSign_succ (i : ℕ) :
    expandSign (R := R) (i + 1) = -expandSign (R := R) i := by
  simp [expandSign, pow_succ]

theorem expandSign_cons_length (n : ℕ) :
    expandSign (R := R) (n + 1) = -expandSign (R := R) n :=
  expandSign_succ n

/--
Graded Leibniz rule when the left factor is a decomposable list of length `p`:
`u ⌟ (U ∧ y) = (u ⌟ U) ∧ y + (-1)^p U ∧ (u ⌟ y)`.
-/
theorem contractVec_ofList_mul (B : BilinForm R M) (u : M) (us : List M)
    (y : ExteriorAlgebra R M) :
    contractVec B u (ofList us * y) =
      contractVec B u (ofList us) * y +
        expandSign (R := R) us.length • (ofList us * contractVec B u y) := by
  induction us with
  | nil =>
      simp [expandSign, contractVec_one]
  | cons v vs ih =>
      have h1 : (B u v) • (ofList vs * y) = (B u v • ofList vs) * y :=
        (smul_mul_assoc (B u v) (ofList vs) y).symm
      have h2 :
          ExteriorAlgebra.ι R v * (contractVec B u (ofList vs) * y) =
            ExteriorAlgebra.ι R v * contractVec B u (ofList vs) * y := by
        rw [mul_assoc]
      have h3 :
          ExteriorAlgebra.ι R v *
              (expandSign (R := R) vs.length •
                (ofList vs * contractVec B u y)) =
            expandSign (R := R) vs.length •
              (ExteriorAlgebra.ι R v * ofList vs * contractVec B u y) := by
        rw [mul_smul_comm, mul_assoc]
      rw [ofList_cons, mul_assoc, contractVec_ι_mul, ih, contractVec_ι_mul,
        mul_add, sub_add_eq_sub_sub, sub_mul, List.length_cons,
        expandSign_cons_length, h1, h2, h3]
      -- LHS: A - B - (σ • Z); RHS: A - B + (-σ) • Z
      rw [neg_smul, ← sub_eq_add_neg]

end Sandhi
