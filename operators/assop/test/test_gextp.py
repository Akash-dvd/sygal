# Required for tests
import sys
import os
from itertools import permutations

import pytest

# Add /app to path for imports
if '/app' not in sys.path:
    sys.path.insert(0, '/app')

from Sygal.initial import *

"""
1)  Check anti-commutivity
2)  Check sorting ,hash order independent
3)  Check concatenation mv
4)  Check concatenation correct coefficient
5)  Check pseudoscalar 
6)  Check local pseudoscalar 
7)  Check simplification for inv,pro,rej
8)  Check for concatenated <,> -> ^ 
9)  Check for grade zero symplification \
    a>(b^c)^a -> a<(b^c^a)
10) Check for local pseudoscalar concat symp \
    a>(c^d)^b<(e^f) -> a^b<(c^d^e^f) when a|e,f = b|c,d = 0 
11) Check for proj^proj^proj ... simplification
12) Check for rej^rej^rej ... simplification
13) Check unmixed grade ordering a1^(a2*a3)^a4
TODO
1) ((a1^a2..a_r)<((b1..br)^(c1..cm)))^((a1..a_r)<((b1..br)^(d1..dn))) ==
(a1^a2..a_r)<((b1..br)^(c1..cm)^(d1..dn))
Will be done after implementing dot product and multiplication.
"""

# Test cases for anti-commutativity
test_cases_anticommu = [
  # Anti-commutativity: (a1^a2) and (a2^a1) have same multivector but opposite coefficients
  # This is a property test, not a transformation
  ((a1^a2).mv, (a2^a1).mv),
]

def test_0():
  """Test anti-commutativity of outer product."""
  # Check that multivectors are equal and coefficients sum to zero
  assert (a1^a2).mv == (a2^a1).mv
  assert ((a1^a2).coeff + (a2^a1).coeff) == 0




def _sandhi_cases_simple():
  """Built lazily so ``Sygal.initial`` atoms exist (see ``Sygal/conftest.py``)."""
  return [
    ((A1 < (B1 ^ B2)) ^ (A1 < (B2 ^ B3)), A1 < (B1 ^ B2 ^ B3)),
  ]


def test_sandhi():
  """Sandhi merge: overlap at seam times merged contraction (tutorial §2.1)."""
  from .sandhi_helpers import assert_sandhi_merge, panel
  from Sygal.initial import A1, B1, B2, B3

  inp = panel(A1, B1, B2) ^ panel(A1, B2, B3)
  assert_sandhi_merge(inp, A1, B2, B1, B2, B3)


def _gmul_2proj_cases():
  return [
    ((a1 < (a2 ^ a3)) ^ (a1 < (a3 ^ a4)), (a1 | a3) * (a1 < (a2 ^ a3 ^ a4))),
  ]


def test_gmul_2Proj():
  """``(a1<(a2^a3))^(a1<(a3^a4))`` → ``(a1|a3)*(a1<(a2^a3^a4))``."""
  from .sandhi_helpers import assert_sandhi_merge, panel
  from Sygal.initial import a1, a2, a3, a4

  inp = panel(a1, a2, a3) ^ panel(a1, a3, a4)
  assert_sandhi_merge(inp, a1, a3, a2, a3, a4)


def test_sandhi_canonical_form_tracks_wedge_sign():
  """Canonical wedge ordering preserves orientation in the coefficient."""
  from .sandhi_helpers import assert_coeff_zero_diff, box_mv, panel, sandhi_canon
  from Sygal.initial import a1, a2, a3, a4
  from Sygal.operators.assop.gextp import gextp

  oriented = gextp(a3, a2, a4)
  canonical = gextp(a2, a3, a4)
  assert oriented.mv == canonical.mv
  assert oriented.coeff == -canonical.coeff

  got = sandhi_canon(panel(a1, a2, a3) ^ panel(a1, a2, a4))
  want = (a1 | a2) * (a1 < gextp(a2, a3, a4))
  assert_coeff_zero_diff(got, want)
  assert box_mv(got).down.args == (a2.mv, a3.mv, a4.mv)


def test_sandhi_rejects_empty_down_seam():
  """Panels with no shared down factor are not a merge candidate."""
  from .sandhi_helpers import panel
  from Sygal.initial import a1, a2, a3, a4, b1
  from Sygal.operators.assop.canon.gextpcanon import SandhiCanon

  expr = panel(a1, a2, a3) ^ panel(a1, a4, b1)
  assert SandhiCanon.sandhi(expr) == expr


def test_sandhi_hidden_nested_overlap_matches_direct_expansion():
  """A buried residual overlap still agrees with full direct expansion."""
  from .sandhi_helpers import panel, sandhi_canon
  from Sygal.GExpr import GExpr
  from Sygal.initial import a1, a2, a3, a4, b1, b2
  from Sygal.operators.binop.glcntrct import glcntrct
  from Sygal.operators.binop.sclrprdct import sclrprdct
  from Sygal.strategies.iters import expand_iter

  left_down = a2 ^ a3 ^ (a4 < (b1 ^ b2))
  right_down = a3 ^ b1
  expr = panel(a1, left_down) ^ panel(a1, right_down)

  def expand_all_contractions(value):
    expanded = expand_iter(glcntrct)(value)
    expanded = GExpr.gdistribute(expanded)
    expanded = sclrprdct.gexpand1(expanded)
    return GExpr.gdistribute(expanded)

  stitched = sandhi_canon(expr)
  assert expand_all_contractions(stitched) == expand_all_contractions(expr)


def test_sandhi_outer_matcher_keeps_nested_factors_opaque():
  """Outer seam matching sees the nested panel, not its buried factors."""
  from Sygal.initial import a2, a3, a4, b1, b2
  from Sygal.operators.assop.canon.gextpcanon import SandhiCanon

  nested = a4 < (b1 ^ b2)
  left_down = a2 ^ a3 ^ nested
  right_down = a3 ^ b1
  split = SandhiCanon.vichcheda_split_down(left_down.mv, right_down.mv)

  assert b1.mv not in left_down.mv.args
  assert split is not None
  assert split.seam_blade == a3


def test_sandhi_three_panel_forced_critical_pair_converges():
  """Forcing either first stitch yields the same canonical result."""
  from .sandhi_helpers import assert_box_equal, panel, sandhi_canon
  from Sygal.GExpr import GExpr
  from Sygal.initial import A1, B1, B2, B3, B4
  from Sygal.operators.assop.canon.gextpcanon import SandhiCanon
  from Sygal.operators.assop.gextp import gextp

  p1 = panel(A1, B1, B2)
  p2 = panel(A1, B2, B3)
  p3 = panel(A1, B3, B4)

  ok_left, merged_left = SandhiCanon.try_merge_two_contractions(
    p1.mv, p2.mv, GExpr.Onl
  )
  ok_right, merged_right = SandhiCanon.try_merge_two_contractions(
    p2.mv, p3.mv, GExpr.Onl
  )
  assert ok_left and ok_right
  assert merged_left.mv != merged_right.mv

  # Apply the second stitch after explicitly selecting the first one.
  left_first = sandhi_canon(merged_left ^ p3)
  right_first = sandhi_canon(merged_right ^ p1)
  expected = (A1 | B2) * (A1 | B3) * (A1 < gextp(B1, B2, B3, B4))

  assert_box_equal(left_first, right_first)
  assert_box_equal(left_first, expected)


@pytest.mark.skip(reason="rx/oo placeholders are None in Sygal.initial (legacy test)")
def test_3():
  """Canonicalization with rx and oo — requires frame reciprocal atoms."""
  transformation = canon_iter(gextp)
  cases = [
    (
      (rx < (a1 ^ a2)) ^ (rx < (a2 ^ a3)) ^ (rx < (a3 ^ b1)) ^ oo,
      (rx < (b1 ^ a1 ^ a2 ^ a3)) ^ oo,
    ),
  ]
  assert all(transformation(x) == y for x, y in cases)


def _sandhi_complex_cases():
  """Lowercase atoms: the uppercase ones live in 4-D ``I41``, where a wedge of
  three grade-2 panels overflows the pseudoscalar ceiling and is identically zero."""
  return [
    (
      (
        ((a1 ^ a2) < (b1 ^ b2 ^ c1 ^ c2))
        ^ ((a1 ^ a2) < (b1 ^ b2 ^ d1 ^ d2))
        ^ ((a1 ^ a2) < (b1 ^ b2 ^ b3 ^ c3))
      ),
      (((a1 ^ a2) | (b1 ^ b2)) ** 2) * ((a1 ^ a2) < (b1 ^ b2 ^ c1 ^ c2 ^ d1 ^ d2 ^ b3 ^ c3)),
    ),
  ]


def test_sandhi_complex():
  """Complex sandhi/projection identity (2-blade core, coeff squared)."""
  transformation = canon_iter(gextp)
  assert all(transformation(x) == y for x, y in _sandhi_complex_cases())


def _deep_stress_expr():
  return (
    (b3 ^ (a1 < (b1 ^ b2 ^ a2)))
    ^ (a1 < (b2 ^ b3))
    ^ (b2 < (b1 ^ b3))
    ^ (b2 < (a2 ^ b3))
  )


def test_sandhi_idempotence_complex():
  """Idempotence on nested contraction XOR."""
  transformation = canon_iter(gextp)
  expr = _deep_stress_expr()
  assert transformation(transformation(expr)) == transformation(expr)


def test_sandhi_order_invariance_simple():
  """Reorder four chained contractions; same canonical form."""
  transformation = canon_iter(gextp)
  terms = [
    a1 < (b1 ^ b2 ^ c1),
    a1 < (b2 ^ b3 ^ c2),
    a1 < (b3 ^ b4 ^ c3),
    a1 < (b4 ^ c4 ^ d1),
  ]
  refs = [transformation(p[0] ^ p[1] ^ p[2] ^ p[3]) for p in permutations(terms)]
  assert refs[0] != GExpr.Znl
  assert all(r == refs[0] for r in refs[1:])


def test_sandhi_wedge_overflowing_dimension_is_zero():
  """Uppercase atoms span 4-D ``I41``; a grade-8 wedge of panels is zero, not a unit."""
  transformation = canon_iter(gextp)
  terms = [
    A1 < (B1 ^ B2 ^ C1),
    A1 < (B2 ^ B3 ^ C2),
    A1 < (B3 ^ B4 ^ C3),
    A1 < (B1 ^ B4 ^ C4),
  ]
  assert transformation(terms[0] ^ terms[1] ^ terms[2] ^ terms[3]) == GExpr.Znl


def test_sandhi_deep_stress_batch():
  """Deep stress batch: reaches a non-zero idempotent fixed point."""
  transformation = canon_iter(gextp)
  out = transformation(_deep_stress_expr())
  assert transformation(out) == out
  assert out != GExpr.Znl


def test_zero():
  pass

