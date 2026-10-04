"""Unit inner-product patch for expand sign tests (⟨u|v⟩ = 1 on grade-1 blades)."""

from __future__ import annotations

from typing import Optional

from sympy import Rational, S

from Sygal.Box import Box
from Sygal.GExpr import GExpr
from Sygal.imports.utils import is_vecBlade
from Sygal.operators.assop.gadd import gadd
from Sygal.operators.binop.glcntrct import glcntrct
from Sygal.operators.binop.sclrprdct import sclrprdct

_ORIGINALS: dict = {}


def _scalar_box(val) -> Box:
    if val is None:
        return Box.Znl
    return Box.__new__(Box, GExpr.Onl, Rational(val) if val != 1 else S.One)


def apply_unit_metric_patch() -> None:
    """Force grade-1 blade contractions to scalar 1 so expand coeffs are numeric."""
    from Sygal.operators.binop.expand import glcntrctexpand as glex
    from Sygal.operators.binop.expand import sclrprdctexpand as slex
    from Sygal.imports.sympy_basic import Mul, subsets
    from Sygal.operators.assop.gextp import gextp as gxp
    from Sygal.operators.binop.expand.glcntrctexpand import parity

    if "_glcntrct_expand" not in _ORIGINALS:
        _ORIGINALS["_glcntrct_expand"] = glex.glcntrct_expand

    def _glcntrct_expand(expr):
        if type(expr) != Box:
            return _ORIGINALS["_glcntrct_expand"](expr)
        BX = GExpr.gdistribute(expr)
        cf = BX.coeff
        if type(BX.mv) != glcntrct:
            return BX
        up = BX.mv.up
        down = BX.mv.down
        if not (is_vecBlade(up) and is_vecBlade(down)):
            return BX
        up_args = [up] if up.grade == {1} else up.args
        down_args = [down] if down.grade == {1} else down.args
        lst = []
        for Bset in subsets(down_args, len(up_args)):
            diffdown = [ele for ele in down_args if ele not in Bset]
            cpydiffdown = list(Bset) + diffdown
            signdown = parity(down_args, cpydiffdown)
            if diffdown:
                mv = gxp(*diffdown)
                lst.append(mv * Mul(signdown, S.One, cf))
            else:
                lst.append(GExpr.nl * Mul(signdown, S.One, cf))
        return gadd(*lst) if len(lst) > 1 else lst[0]

    glex.glcntrct_expand = _glcntrct_expand
    glex.glcntrctexpand()

    if "_sclprdct_expand" not in _ORIGINALS:
        _ORIGINALS["_sclprdct_expand"] = slex.sclprdct_expand

    def _scl_expand(expr):
        if type(expr) == sclrprdct:
            sc = expr
            if is_vecBlade(sc.up) and is_vecBlade(sc.down):
                return _scalar_box(S.One)
        if isinstance(expr, Box) and type(expr.mv) == sclrprdct:
            sc = expr.mv
            if is_vecBlade(sc.up) and is_vecBlade(sc.down):
                return GExpr.gdistribute(_scalar_box(S.One) * expr.coeff)
        return _ORIGINALS["_sclprdct_expand"](expr)

    slex.sclprdct_expand = _scl_expand
    slex.sclrprdctexpand()


def restore_metric_patch() -> None:
    from Sygal.operators.binop.expand import glcntrctexpand as glex
    from Sygal.operators.binop.expand import sclrprdctexpand as slex

    if "_glcntrct_expand" in _ORIGINALS:
        glex.glcntrct_expand = _ORIGINALS["_glcntrct_expand"]
        glex.glcntrctexpand()
    if "_sclprdct_expand" in _ORIGINALS:
        slex.sclprdct_expand = _ORIGINALS["_sclprdct_expand"]
        slex.sclrprdctexpand()
