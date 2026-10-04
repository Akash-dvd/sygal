# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.strategies import exhaust, do_one
from Sygal.imports.utils import parity, is_uniGraded
from typing import NamedTuple, Optional, List
from Sygal.imports.typing_helpers import Tuple
from Sygal.imports.sympy_basic import S
from sympy.utilities.iterables import subsets

from Sygal.operators.assop.gextp import gextp
from Sygal.operators.assop.canon.gextpcapelli import CapelliOptionB

new = gextp.__new__


class UpVichchedaResult(NamedTuple):
  """Successful UP vichcheda: shared contracting blade and peeled downs."""
  shared_up: GExpr
  acc_blade: GExpr
  dn1: GExpr
  dn2: GExpr


class DownVichchedaResult(NamedTuple):
  """DOWN vichcheda: merged down args, parity signs, seam for overlap coeff."""
  merged_down_args: List
  sign_left: object
  sign_right: object
  seam_blade: GExpr


class SandhiCanon:
  """Recursive sandhi / vichcheda on wedges of glcntrct panels (gextp mv).

  Pipeline per pairwise merge:
    align_up_blades  →  vichcheda_split_down  →  grade_balance  →  emit merge

  Canonical-form invariant:
    every merged down blade is constructed through ``gextp`` in its oriented
    canonical order, and the parity needed to reach that order is stored in
    its coefficient exactly once.  Later stitching may use the canonical
    factors structurally without applying that parity again.
  """

  # --- Public entry ---------------------------------------------------------

  @staticmethod
  def sandhi(expr: Box, blade1: GExpr = lambda: GExpr.Onl) -> Box:
    """One pass of sandhi on a single gextp Box (one pairwise merge if possible).

    What we are trying to achieve (GA)
    --------------------------------
    Input is a **wedge of contraction panels**, e.g.

        (A < (B1 ^ B2))  ^  (A < (B2 ^ B3))  ^  ...

    Goal: **fuse** two panels that share the same contracting up-blade A and a
    common down factor B2 (the seam), into one panel

        A < (B1 ^ B2 ^ B3)

    possibly times a scalar κ from overlap (Capelli) when the grade gate allows.

    This function performs **at most one** such fusion per call. The outer driver
    `exhaust(do_one(sandhi, ...))` repeats until no more merges apply.

    `blade1` (often 1 at the top level) is the **accumulated contracting blade**
    along nested recursion: inside deeper calls it becomes `acc_blade` after
    each shared up is wedged in (blade1 ^ shared_up ^ ...).

    Example call shape
    ------------------
        sandhi( Box( coeff * gextp( A<(B1^B2), A<(B2^B3), ... ) ), blade1=1 )
    """
    if callable(blade1):
      blade1 = blade1()

    # Only graded Boxes whose mv is a wedge of terms are in scope.
    if type(expr) == Box and is_uniGraded(expr) and is_uniGraded(blade1):
      bx = expr
      if type(bx.mv) == gextp:
        return SandhiCanon.try_merge_first_pair(bx, blade1)
    return expr

  @staticmethod
  def try_merge_first_pair(bx: Box, acc_blade_path: GExpr) -> Box:
    """Pick one pair of contraction slots in bx.mv and try to sandhi-merge them.

    What we are trying to achieve (GA)
    --------------------------------
    bx.mv is a gextp wedge; some slots are glcntrct with gextp down, e.g.

        gextp(  A<(B1^B2),  A<(B2^B3),  other_terms...  )

    We enumerate **unordered pairs** of such slots (i, j), call
    try_merge_two_contractions on that pair, and stop at the **first** pair that
    succeeds. That design matches "one rewrite step per sandhi() invocation."

    Example (indices 0 and 1 merge)
    -------------------------------
        BEFORE:  gextp( A<(B1^B2), A<(B2^B3) )
        AFTER:   gextp( A<(B1^B2^B3) ) * coeff   (+ parity from slot reorder)

    If no pair can merge (ups do not align, grade gate says incompatible, etc.),
    return bx unchanged. If merge yields zero, return Znl for the whole Box.

    `acc_blade_path` is forwarded into the pair merge (starts as 1 at top level).
    """
    from Sygal.operators.binop.glcntrct import glcntrct

    # Slots that look like  (up) < (down wedge)  — the sandhi fragment.
    mergeable = [
      i for i, x in enumerate(bx.mv.args)
      if type(x) == glcntrct and type(x.down) == gextp
    ]
    for i, j in subsets(mergeable, 2):
      ok, merged = SandhiCanon.try_merge_two_contractions(
        bx.mv.args[i], bx.mv.args[j], acc_blade_path
      )
      if ok:
        if merged == GExpr.Znl:
          return merged
        # Replace the two wedge slots by one merged glcntrct; keep Box.coeff.
        return SandhiCanon.replace_merged_pair_in_box(bx, merged, i, j) * bx.coeff
    return bx

  @staticmethod
  def try_merge_two_contractions(
    term1, term2, acc_blade_path: GExpr
  ) -> Tuple[bool, Box]:
    """One sandhi attempt on two glcntrct terms."""
    up_align = SandhiCanon.align_up_blades_vichcheda(
      term1.up, term2.up, term1.down, term2.down, acc_blade_path
    )
    if up_align is None:
      return (False, GExpr.Znl)

    shared_up, acc_blade, dn1, dn2 = up_align
    dn11, dn21, box_coeff = SandhiCanon.unwrap_down_multivectors(dn1, dn2)
    down_split = SandhiCanon.vichcheda_split_down(dn11, dn21)
    if down_split is None:
      return (False, GExpr.Znl)

    # The gextp constructor canonicalizes the oriented factors and carries
    # vichcheda parity in merged_down's coefficient exactly once.
    merged_down = gextp(*down_split.merged_down_args) * box_coeff * down_split.sign_left * down_split.sign_right
    grade_x = SandhiCanon.grade_balance_deficit(dn11, dn21, merged_down, acc_blade)

    return SandhiCanon.emit_merge_by_grade(
      grade_x,
      shared_up=shared_up,
      acc_blade=acc_blade,
      merged_down=merged_down,
      seam_blade=down_split.seam_blade,
      # The vichcheda parity is already embedded in merged_down.
      vichcheda_sign=S(1),
    )

  # --- UP vichcheda ---------------------------------------------------------

  @staticmethod
  def align_up_blades_vichcheda(
    up1: GExpr, up2: GExpr, dn1: GExpr, dn2: GExpr, acc_blade_path: GExpr
  ) -> Optional[UpVichchedaResult]:
    """Match shared UP blade; peel non-common wedge into the larger UP's down."""
    if up1 == up2:
      shared = up1
      return UpVichchedaResult(shared, acc_blade_path ^ shared, dn1, dn2)

    if up1.is_atom and type(up2) == gextp:
      return SandhiCanon._align_atom_into_gextp_up(up1, up2, dn1, dn2, acc_blade_path, peel_into_dn1=False)

    if type(up1) == gextp and up2.is_atom:
      return SandhiCanon._align_atom_into_gextp_up(up2, up1, dn1, dn2, acc_blade_path, peel_into_dn1=True)

    if type(up1) == gextp and type(up2) == gextp:
      up1_in_up2 = all(ele in up2.args for ele in up1.args)
      up2_in_up1 = all(ele in up1.args for ele in up2.args)
      if up1_in_up2 and up2_in_up1:
        raise ValueError("Should have been caught earlier")
      if up1_in_up2:
        return SandhiCanon._align_gextp_subset_up(up1, up2, dn1, dn2, acc_blade_path, peel_from_dn2=True)
      if up2_in_up1:
        return SandhiCanon._align_gextp_subset_up(up2, up1, dn2, dn1, acc_blade_path, peel_from_dn2=False)

    return None

  @staticmethod
  def _peel_atom_from_up_into_down(atom: GExpr, up_gextp: gextp, down: GExpr) -> GExpr:
    """UP vichcheda peel: shared atom leaves UP wedge, enters DOWN as gextp(rest)<down>."""
    rest = [ele for ele in up_gextp.args if ele != atom]
    reorder = [atom, *rest]
    sign = parity(up_gextp.args, reorder)
    return (gextp(*rest) < down) * sign

  @staticmethod
  def _align_atom_into_gextp_up(
    atom: GExpr,
    up_gextp: gextp,
    dn1: GExpr,
    dn2: GExpr,
    acc_blade_path: GExpr,
    peel_into_dn1: bool,
  ) -> Optional[UpVichchedaResult]:
    if atom not in up_gextp.args:
      return None
    shared = atom
    acc = acc_blade_path ^ shared
    target_dn = dn1 if peel_into_dn1 else dn2
    peeled = SandhiCanon._peel_atom_from_up_into_down(atom, up_gextp, target_dn)
    if peel_into_dn1:
      return UpVichchedaResult(shared, acc, peeled, dn2)
    return UpVichchedaResult(shared, acc, dn1, peeled)

  @staticmethod
  def _align_gextp_subset_up(
    shared_up_gextp: gextp,
    larger_up_gextp: gextp,
    dn_small_side: GExpr,
    dn_large_side: GExpr,
    acc_blade_path: GExpr,
    peel_from_dn2: bool,
  ) -> UpVichchedaResult:
    shared = shared_up_gextp
    acc = acc_blade_path ^ shared
    peel_args = [ele for ele in larger_up_gextp.args if ele not in shared_up_gextp.args]
    reorder = list(shared_up_gextp.args) + peel_args
    sign = parity(larger_up_gextp.args, reorder)
    peeled_dn = (gextp(*peel_args) < dn_large_side) * sign
    if peel_from_dn2:
      return UpVichchedaResult(shared, acc, dn_small_side, peeled_dn)
    return UpVichchedaResult(shared, acc, peeled_dn, dn_small_side)

  # --- DOWN vichcheda -------------------------------------------------------

  @staticmethod
  def unwrap_down_multivectors(dn1: GExpr, dn2: GExpr):
    """Split Box wrappers on downs into (mv1, mv2, scalar_factor)."""
    dmvs = []
    cf = S(1)
    if type(dn1) == Box:
      dmvs.append(dn1.mv)
      cf *= dn1.coeff
    else:
      dmvs.append(dn1)
    if type(dn2) == Box:
      dmvs.append(dn2.mv)
      cf *= dn2.coeff
    else:
      dmvs.append(dn2)
    return dmvs[0], dmvs[1], cf

  @staticmethod
  def _parity_for_reordered_gextp(original_args, reordered_args):
    return parity(original_args, reordered_args)

  @staticmethod
  def vichcheda_split_down(
    dn11: GExpr, dn21: GExpr
  ) -> Optional[DownVichchedaResult]:
    """Split two down multivectors along common wedge factors (seam)."""
    if type(dn11) == gextp and type(dn21) == gextp:
      intersect = [ele for ele in dn11.args if ele in dn21.args]
      if not intersect:
        return None
      unique2 = [ele for ele in dn21.args if ele not in intersect]
      order1 = [ele for ele in dn11.args if ele not in intersect] + intersect
      order2 = intersect + unique2
      sign1 = SandhiCanon._parity_for_reordered_gextp(dn11.args, order1)
      sign2 = SandhiCanon._parity_for_reordered_gextp(dn21.args, order2)
      merged = order1 + unique2
      seam = gextp(*intersect)
      return DownVichchedaResult(merged, sign1, sign2, seam)

    if type(dn11) == gextp:
      return SandhiCanon._vichcheda_split_down_one_gextp(dn11, dn21, gextp_on_left=True)

    if type(dn21) == gextp:
      return SandhiCanon._vichcheda_split_down_one_gextp(dn21, dn11, gextp_on_left=False)

    raise NotImplementedError

  @staticmethod
  def _vichcheda_split_down_one_gextp(
    dn_gextp: gextp, dn_other: GExpr, gextp_on_left: bool
  ) -> DownVichchedaResult:
    if dn_other in dn_gextp.args:
      order = [ele for ele in dn_gextp.args if ele != dn_other] + [dn_other]
      sign_gextp = SandhiCanon._parity_for_reordered_gextp(dn_gextp.args, order)
      sign_other = S(1)
      merged = list(dn_gextp.args)
      seam = dn_other
      if gextp_on_left:
        return DownVichchedaResult(merged, sign_gextp, sign_other, seam)
      return DownVichchedaResult(merged, sign_other, sign_gextp, seam)

    return None

  # --- Grade gate + emit ----------------------------------------------------

  @staticmethod
  def grade_balance_deficit(dn11, dn21, merged_down, acc_blade) -> int:
    """x = grd(dn11)+grd(dn21) - grd(merged_down) - grd(acc_blade); see binary_op comment."""
    grd_sum = next(iter(dn11.grade)) + next(iter(dn21.grade))
    return grd_sum - next(iter(merged_down.grade)) - next(iter(acc_blade.grade))

  @staticmethod
  def emit_merge_by_grade(
    grade_x: int,
    *,
    shared_up: GExpr,
    acc_blade: GExpr,
    merged_down: GExpr,
    seam_blade: GExpr,
    vichcheda_sign: object,
  ) -> Tuple[bool, Box]:
    """x<0: recurse inner sandhi; x==0: overlap coeff; x>0: zero."""
    inner = SandhiCanon.sandhi(merged_down, acc_blade)

    if grade_x < 0:
      if inner == merged_down:
        return (False, GExpr.Znl)
      return (True, shared_up < inner)

    if grade_x == 0:
      overlap = SandhiCanon.overlap_coefficient_at_seam(
        acc_blade, seam_blade, vichcheda_sign
      )
      return (True, (shared_up < inner) * overlap)

    return (True, GExpr.Znl)

  @staticmethod
  def overlap_coefficient_at_seam(
    acc_blade: GExpr, seam_blade: GExpr, local_sign=S(1)
  ):
    """Scalar κ from Capelli Option B (x==0 only); local_sign from down parity."""
    return CapelliOptionB.overlap_scalar_at_seam(acc_blade, seam_blade, local_sign)

  @staticmethod
  def replace_merged_pair_in_box(oexpr: Box, merged: Box, i: int, j: int) -> Box:
    """Replace two wedge slots by one merged contraction; parity on slot order."""
    kept = [ele for idx, ele in enumerate(oexpr.mv.args) if idx not in (i, j)]
    before_merge = kept + [oexpr.mv.args[i], oexpr.mv.args[j]]
    sign = parity(oexpr.mv.args, before_merge)
    return gextp(*kept, merged) * sign

  # --- Backward-compatible aliases (old names) ------------------------------

  iter = try_merge_first_pair
  binary_op = try_merge_two_contractions
  remake = replace_merged_pair_in_box
  _down_to_mv_and_coeff = unwrap_down_multivectors

  @staticmethod
  def _split_common_unique(dn11, dn21):
    """Deprecated name; returns legacy 4-tuple for any external callers."""
    r = SandhiCanon.vichcheda_split_down(dn11, dn21)
    return r.merged_down_args, r.sign_left, r.sign_right, r.seam_blade

  _scalar_part = overlap_coefficient_at_seam


# Public API alias used by gextpsimp / gextp registration
concat = SandhiCanon


def inv_gextp(expr):
  from Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion

  if type(expr) == Box:
    bx = expr
    if type(bx.mv) == gextp:
      for i, arg in enumerate(bx.mv.args):
        if type(arg) == inversion:
          up = arg.up
          down = arg.down
          if (up in bx.mv.args) or (down in bx.mv.args):
            lst = list(bx.mv.args)
            t = arg.gexpand()
            t1 = t.gexpand()
            lst[i] = t1
            t2 = gextp(*t1)
            t3 = t2.gdistribute()
            return t3
      return expr
    return expr
  return expr


def proj_gextp(expr):
  from Sygal.operators.binop.outermorphic.projection import projection

  if type(expr) == Box:
    bx = expr
    if type(bx.mv) == gextp:
      for arg in bx.mv.args:
        if type(arg) == projection and (arg.down in bx.mv.args):
          return GExpr.Znl
      return expr
    return expr
  return expr


def rej_gextp(expr):
  from Sygal.operators.binop.outermorphic.rejection import rejection

  if type(expr) == Box:
    bx = expr
    if type(bx.mv) == gextp:
      for i, arg in enumerate(bx.mv.args):
        if type(arg) == rejection and (arg.down in bx.mv.args):
          lst = list(bx.mv.args)
          lst[i] = (arg.up ^ arg.down)
          return gextp(*lst)
      return expr
    return expr
  return expr


def gextpcanon():
  gextp.gcanonicalization = exhaust(do_one(SandhiCanon.sandhi, inv_gextp, proj_gextp, rej_gextp))
