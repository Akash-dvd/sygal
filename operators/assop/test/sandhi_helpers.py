"""Helpers for sandhi / gextp canonicalization tests (mv, coeff, normal form)."""

from __future__ import annotations

from typing import Callable, Iterable, Union

from sympy import S, expand

from Sygal.Box import Box
from Sygal.GExpr import GExpr
from Sygal.operators.assop.gextp import gextp
from Sygal.operators.binop.glcntrct import glcntrct
from Sygal.strategies.iters import canon_iter

SandhiExpr = Union[Box, GExpr]

_canon: Callable[[SandhiExpr], Box] | None = None


def sandhi_canon(expr: SandhiExpr) -> Box:
    """Fixed-point ``canon_iter(gextp)`` (Option B sandhi backend)."""
    global _canon
    if _canon is None:
        _canon = canon_iter(gextp)
    out = _canon(expr)
    if type(out) is not Box:
        out = Box.__new__(Box, out, S.One)
    return out


def box_mv(expr: SandhiExpr) -> GExpr:
    if type(expr) == Box:
        return expr.mv
    return expr


def box_coeff(expr: SandhiExpr):
    if type(expr) == Box:
        return expr.coeff
    return S.One


def assert_box_equal(a: SandhiExpr, b: SandhiExpr) -> None:
    """Structural equality: hash match or matching mv + coeff."""
    if a == b:
        return
    assert_mv_equal(a, b)
    assert_coeff_zero_diff(a, b)


def assert_mv_equal(a: SandhiExpr, b: SandhiExpr) -> None:
    assert box_mv(a) == box_mv(b)


def assert_coeff_zero_diff(a: SandhiExpr, b: SandhiExpr) -> None:
    da = box_coeff(a)
    db = box_coeff(b)
    try:
        assert expand(da - db) == 0
    except Exception:
        assert da == db


def assert_coeff_equal_or_opposite(a: SandhiExpr, b: SandhiExpr) -> None:
    """Coefficients match up to overall sign (sandhi wedge order)."""
    try:
        assert_coeff_zero_diff(a, b)
    except AssertionError:
        neg_b = Box.__new__(Box, box_mv(b), S.NegativeOne * box_coeff(b))
        assert_coeff_zero_diff(a, neg_b)


def wedge_glcntrct_count(expr: SandhiExpr) -> int:
    """``glcntrct`` slots inside a top-level ``gextp`` wedge."""
    mv = box_mv(expr)
    if type(mv) == glcntrct:
        return 1
    if type(mv) != gextp:
        return 0
    return sum(1 for a in mv.args if type(a) == glcntrct)


def is_merged_panel(expr: SandhiExpr) -> bool:
    """After sandhi, a single contraction panel (not a multi-panel wedge)."""
    return type(box_mv(expr)) == glcntrct


def is_idempotent(expr: SandhiExpr) -> bool:
    once = sandhi_canon(expr)
    return sandhi_canon(once) == once


def panel(up, *blade_atoms) -> Box:
    """``up < (b1 ^ b2 ^ ...)``."""
    wedge = blade_atoms[0]
    for b in blade_atoms[1:]:
        wedge = wedge ^ b
    return up < wedge


def overlap_times_merged(up, seam_atom, *down_atoms) -> Box:
    """Tutorial NF: ``(up | seam) * (up < down wedge)`` (canonical ``gextp`` order)."""
    return (up | seam_atom) * (up < gextp(*down_atoms))


def is_sandhi_zero(expr: SandhiExpr) -> bool:
    """True for ``GExpr.Znl`` or scalar zero Box."""
    if expr == GExpr.Znl:
        return True
    return type(expr) == Box and box_mv(expr) == GExpr.nl


def assert_sandhi_merge(
    inp: SandhiExpr,
    up,
    seam_atom,
    *merged_blades,
) -> Box:
    """Canon(inp) matches overlap * merged panel (mv + coeff)."""
    got = sandhi_canon(inp)
    want = (up | seam_atom) * (up < gextp(*merged_blades))
    if got != want:
        assert_mv_equal(got, want)
        assert_coeff_equal_or_opposite(got, want)
    assert_mv_equal(got, panel(up, *merged_blades))
    return got


def chain_panels(up, blade_sequence: Iterable) -> Box:
    """Wedge of chain panels ``up < (b_i ^ b_{i+1})`` along consecutive blades."""
    blades = list(blade_sequence)
    expr = panel(up, blades[0], blades[1])
    for i in range(1, len(blades) - 1):
        expr = expr ^ panel(up, blades[i], blades[i + 1])
    return expr
