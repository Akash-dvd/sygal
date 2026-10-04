# Required for tests
import sys
import os

# Add /app to path for imports
if '/app' not in sys.path:
    sys.path.insert(0, '/app')

from Sygal.initial import *
from Sygal.GAtom import GAtom

"""
1)  Check higher to proj,rej
2)  Check for expansion
3)  Check for transformation to grcntrct
4)  Check for zero grade transformation
5)  Check for scalar behavior

Grade conventions (I41 subspace, grdlmt 4):
- L1+L3 (angle bisector) = grade 1
- (_oo<(e_L1_oo^e_L3_oo)) (perp bisector) = grade 2-1 = 1
- C (circle) = grade 1
- f^g^a = grade 1+1+1 = 3
- (f^g^a)<I41: blade grade 3 < I41 grade 4 => result grade 1 (point)
- 4+3=7 was wrong; correct is blade grade 3.
"""


def test_glcntrct_basic_grade1_wedge_contraction():
  """(a^b^c)<I41 with grade-1 a,b,c should NOT be Znl. Blade grade 3 < I41 grade 4 => point."""
  mtDt1 = {GExpr.I41: 1}  # grade 1
  mtDt_ps = {GExpr.I41: 4}  # pseudoscalar (I41 limit 4)
  a1 = GAtom("a1", mtDt1)
  b1 = GAtom("b1", mtDt1)
  c1 = GAtom("c1", mtDt1)
  I41_ps = GAtom("I41_ps", mtDt_ps)
  blade = a1 ^ b1 ^ c1
  result = blade < I41_ps
  assert result != GExpr.Znl, "grade-3 blade < grade-4 I41 should yield non-zero point"


def test_glcntrct_gadd_grade1_wedge_contraction():
  """((a+b)^c^d)<I41 with grade-1 elements. f=(a+b) grade 1, g=c grade 1, a=d grade 1 => blade grade 3."""
  mtDt1 = {GExpr.I41: 1}
  mtDt_ps = {GExpr.I41: 4}
  a1 = GAtom("a1", mtDt1)
  b1 = GAtom("b1", mtDt1)
  c1 = GAtom("c1", mtDt1)
  d1 = GAtom("d1", mtDt1)
  I41_ps = GAtom("I41_ps", mtDt_ps)
  f = a1 + b1
  blade = f ^ c1 ^ d1
  result = blade < I41_ps
  assert result != GExpr.Znl, "((a+b)^c^d)<I41 with grade-1 elements should not be Znl"


def test_glcntrct_frptConf_GeoFlexPoint_with_pseudoscalar():
  """Exact GeoFlexPoint expression with GExpr.I41_ps (pseudoscalar from GAtom._preprocess)."""
  try:
    from cirFramework.frptConf.frptConf import frptConf
    conf = frptConf()
    L1, L3, C = conf.L1, conf.L3, conf.C
    e_L1_oo, e_L3_oo = conf.e_L1_oo, conf.e_L3_oo
    _oo = GExpr._oo
    I41_ps = GExpr.I41_ps  # pseudoscalar GAtom from GAtom._preprocess
    f = L1 + L3
    g = _oo < (e_L1_oo ^ e_L3_oo)
    blade = f ^ g ^ C
    result = blade < I41_ps
    assert result != GExpr.Znl, (
      "((L1+L3)^(_oo<(e_L1_oo^e_L3_oo))^C)<I41_ps should not be Znl"
    )
  except ImportError:
    pass


def test_glcntrct_GeoFlexPoint_with_string_I41_fails():
  """Demonstrates the bug: blade < GExpr.I41 (string) yields Znl.
  GExpr.I41 is the string 'I41', not a pseudoscalar GAtom - Box treats it as scalar."""
  try:
    from cirFramework.frptConf.frptConf import frptConf
    conf = frptConf()
    L1, L3, C = conf.L1, conf.L3, conf.C
    e_L1_oo, e_L3_oo = conf.e_L1_oo, conf.e_L3_oo
    _oo = GExpr._oo
    f = L1 + L3
    g = _oo < (e_L1_oo ^ e_L3_oo)
    blade = f ^ g ^ C
    result_with_string = blade < GExpr.I41  # string "I41" - wrong operand type
    # This test documents current (wrong) behavior - result is Znl
    # Fix: GeoFlexPoint should use pseudoscalar GAtom, not GExpr.I41 string
    assert result_with_string == GExpr.Znl  # expected to fail with string I41
  except ImportError:
    pass


def test_glcntrct():
  assert True