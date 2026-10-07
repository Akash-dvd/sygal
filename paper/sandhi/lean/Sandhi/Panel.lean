import Sandhi.Basic
import Sandhi.Grade
import Sandhi.SeamR
import Sandhi.Capelli
import Sandhi.Induction
import Sandhi.Stitching
import Mathlib.Tactic

/-!
# Concrete panel state, grade gate, and stitching soundness

A state carries a contractor `A`, outer wings `U`, `V`, the exposed seam `S`,
the shared factors `H` not yet exposed, and a parity counter:
\[
\text{left} = U \wedge H^{\mathrm{rev}} \wedge S,\qquad
\text{right} = S \wedge H \wedge V,\qquad
\text{direct} = (-1)^{\text{parity}}
  (A\lrcorner\text{left})\wedge(A\lrcorner\text{right}).
\]

| \(t\) vs \(r\) | gate | action |
|----------------|------|--------|
| \(t < r\) | `descend` | expose the next shared factor; record its reordering sign |
| \(t = r\) | `balanced` | Capelli scalar \(A\mid S\) times the stitched panel |
| \(t > r\) | `vanish` | zero |

All three branches are proved sound for every grade (`panelSpec`), and
`panelStitch_sound` shows the fixed schedule terminates after
\(r - t + 1\) steps with the direct left-contraction value whenever enough
shared factors exist (\(r \le t + |H|\)).
-/

open LinearMap (BilinForm)

namespace Sandhi

variable {R : Type*} [CommRing R]
variable {M : Type*} [AddCommGroup M] [Module R M]

structure PanelState (M : Type*) where
  contractor : List M
  left : List M
  hidden : List M
  seam : List M
  right : List M
  parity : ℕ
  deriving Repr

namespace PanelState

variable {M : Type*}

def r (s : PanelState M) : ℕ := s.contractor.length
def t (s : PanelState M) : ℕ := s.seam.length

def gate (s : PanelState M) : Gate :=
  if s.t < s.r then Gate.descend
  else if s.t = s.r then Gate.balanced
  else Gate.vanish

theorem t_eq_r_of_balanced (s : PanelState M) (h : s.gate = Gate.balanced) :
    s.t = s.r := by
  by_cases h₁ : s.t < s.r
  · simp [gate, h₁] at h
  · by_cases h₂ : s.t = s.r
    · exact h₂
    · simp [gate, h₁, h₂] at h

theorem r_lt_t_of_vanish (s : PanelState M) (h : s.gate = Gate.vanish) :
    s.r < s.t := by
  by_cases h₁ : s.t < s.r
  · simp [gate, h₁] at h
  · by_cases h₂ : s.t = s.r
    · simp [gate, h₂] at h
    · omega

/-- Left wing `U ∧ H^rev` (everything before the seam). -/
def wingL (s : PanelState M) : List M := s.left ++ s.hidden.reverse

/-- Right wing `H ∧ V` (everything after the seam). -/
def wingR (s : PanelState M) : List M := s.hidden ++ s.right

/-- Expose the next shared factor as the new leading seam factor. -/
def down (s : PanelState M) : PanelState M :=
  match s.hidden with
  | [] => s
  | x :: h =>
      { s with hidden := h, seam := x :: s.seam,
               parity := s.parity + s.seam.length }

theorem down_of_hidden_cons (s : PanelState M) {x : M} {h : List M}
    (hh : s.hidden = x :: h) :
    s.down = { s with hidden := h, seam := x :: s.seam,
                      parity := s.parity + s.seam.length } := by
  unfold down; rw [hh]

end PanelState

namespace PanelState

def direct (B : BilinForm R M) (s : PanelState M) : ExteriorAlgebra R M :=
  expandSign (R := R) s.parity •
    (contractBlade B s.contractor (panelLeftR s.wingL s.seam) *
      contractBlade B s.contractor (panelRightR s.seam s.wingR))

def balanced (B : BilinForm R M) (s : PanelState M) : ExteriorAlgebra R M :=
  expandSign (R := R) s.parity •
    (seamPairing B s.contractor s.seam •
      contractBlade B s.contractor (panelStitchR s.wingL s.seam s.wingR))

end PanelState

variable (B : BilinForm R M)

theorem panel_balanced_sound (s : PanelState M)
    (hgate : s.gate = Gate.balanced) :
    PanelState.balanced (R := R) B s = PanelState.direct (R := R) B s := by
  have hlen : s.contractor.length = s.seam.length :=
    (PanelState.t_eq_r_of_balanced s hgate).symm
  rw [PanelState.balanced, PanelState.direct,
    soleSeam_gradeR B s.contractor s.wingL s.seam s.wingR hlen]

theorem panel_vanish_sound (s : PanelState M) (hgate : s.gate = Gate.vanish) :
    (0 : ExteriorAlgebra R M) = PanelState.direct (R := R) B s := by
  rw [PanelState.direct,
    soleSeam_vanish B s.contractor s.wingL s.seam s.wingR
      (PanelState.r_lt_t_of_vanish s hgate), smul_zero]

/-- Exposing a shared factor preserves the direct value (sign is recorded). -/
theorem panel_down_sound (s : PanelState M) :
    PanelState.direct (R := R) B s.down = PanelState.direct (R := R) B s := by
  cases hh : s.hidden with
  | nil => unfold PanelState.down; rw [hh]
  | cons x h =>
      rw [PanelState.down_of_hidden_cons s hh]
      simp only [PanelState.direct, PanelState.wingL, PanelState.wingR, hh]
      have hL :
          panelLeftR (R := R) (s.left ++ h.reverse) (x :: s.seam) =
            panelLeftR (s.left ++ (x :: h).reverse) s.seam := by
        simp only [panelLeftR, List.reverse_cons, ofList_append, ofList_cons,
          ofList_nil, mul_one, mul_assoc]
      have hR :
          panelRightR (R := R) s.seam ((x :: h) ++ s.right) =
            expandSign (R := R) s.seam.length •
              panelRightR (x :: s.seam) (h ++ s.right) := by
        simp only [panelRightR, List.cons_append, ofList_cons]
        rw [← mul_assoc, ofList_mul_ι, smul_mul_assoc]
      rw [hL, hR, map_smul, mul_smul_comm, smul_smul, expandSign_add]

noncomputable def panelSpec : Spec (PanelState M) (ExteriorAlgebra R M) where
  gate := PanelState.gate
  down := PanelState.down
  balanced := PanelState.balanced (R := R) B
  zero := 0
  direct := PanelState.direct (R := R) B
  balanced_sound := fun hs => panel_balanced_sound B _ hs
  vanish_sound := fun hs => panel_vanish_sound B _ hs
  descend_sound := fun _ => panel_down_sound B _

/--
With at least `r - t` shared factors left to expose, the fixed schedule is
valid for `r - t + 1` steps.
-/
theorem panel_valid (d : ℕ) :
    ∀ s : PanelState M, s.r - s.t = d → s.r ≤ s.t + s.hidden.length →
      Valid (panelSpec (R := R) B) (d + 1) s := by
  induction d with
  | zero =>
      intro s hd _
      by_cases heq : s.t = s.r
      · exact Valid.balanced (by simp [panelSpec, PanelState.gate, heq])
      · have hgt : ¬ s.t < s.r := by omega
        exact Valid.vanish (by simp [panelSpec, PanelState.gate, hgt, heq])
  | succ d ih =>
      intro s hd hle
      have hlt : s.t < s.r := by omega
      cases hh : s.hidden with
      | nil => rw [hh] at hle; simp at hle; omega
      | cons x h =>
          refine Valid.descend (by simp [panelSpec, PanelState.gate, hlt]) ?_
          have hdown := PanelState.down_of_hidden_cons s hh
          change Valid (panelSpec (R := R) B) (d + 1) s.down
          rw [hdown]
          apply ih
          · simp only [PanelState.r, PanelState.t, List.length_cons] at hd ⊢
            omega
          · simp only [PanelState.r, PanelState.t, List.length_cons, hh] at hle ⊢
            omega

noncomputable def panelStitchReduce (n : ℕ) (s : PanelState M) :
    ExteriorAlgebra R M :=
  stitch (panelSpec (R := R) B) n s

theorem panelStitchReduce_sound (n : ℕ) (s : PanelState M)
    (hv : Valid (panelSpec (R := R) B) n s) :
    panelStitchReduce (R := R) B n s = PanelState.direct (R := R) B s :=
  stitch_sound (panelSpec (R := R) B) hv

/--
**Fixed-schedule stitching correctness (flat panels).** Grade-gated
stitching for `r - t + 1` steps equals the direct left-contraction value.
-/
theorem panelStitch_sound (s : PanelState M)
    (hle : s.r ≤ s.t + s.hidden.length) :
    panelStitchReduce (R := R) B (s.r - s.t + 1) s =
      PanelState.direct (R := R) B s :=
  panelStitchReduce_sound B _ s (panel_valid B _ s rfl hle)

end Sandhi
