"""Wide sandhi tests: multivector, coefficient (overlap), sign, idempotence."""

from __future__ import annotations

import pytest
from sympy import S

from Sygal.GExpr import GExpr
from .sandhi_helpers import (
    assert_box_equal,
    assert_coeff_equal_or_opposite,
    assert_coeff_zero_diff,
    assert_mv_equal,
    assert_sandhi_merge,
    box_coeff,
    box_mv,
    chain_panels,
    is_idempotent,
    is_merged_panel,
    is_sandhi_zero,
    panel,
    sandhi_canon,
)
from Sygal.operators.binop.glcntrct import glcntrct


def _atoms():
    from Sygal.initial import (
        A1,
        A2,
        B1,
        B2,
        B3,
        B4,
        B5,
        B6,
        C1,
        C2,
        C3,
        D1,
        D2,
        a1,
        a2,
        a3,
        a4,
        b1,
        b2,
        b3,
    )

    return locals()


@pytest.mark.parametrize(
    "case_id",
    ["A1-B2", "A1-B3", "a1-a3", "a1-b2", "A2-B3", "B1-B2"],
)
def test_sandhi_merge_mv_coeff_and_normal_form(case_id):
    a = _atoms()
    cases = {
        "A1-B2": (a["A1"], a["B2"], (a["B1"], a["B2"]), (a["B2"], a["B3"]), (a["B1"], a["B2"], a["B3"])),
        "A1-B3": (a["A1"], a["B3"], (a["B2"], a["B3"]), (a["B3"], a["B4"]), (a["B2"], a["B3"], a["B4"])),
        "a1-a3": (a["a1"], a["a3"], (a["a2"], a["a3"]), (a["a3"], a["a4"]), (a["a2"], a["a3"], a["a4"])),
        "a1-b2": (a["a1"], a["b2"], (a["b1"], a["b2"]), (a["b2"], a["b3"]), (a["b1"], a["b2"], a["b3"])),
        "A2-B3": (a["A2"], a["B3"], (a["B2"], a["B3"]), (a["B3"], a["B4"]), (a["B2"], a["B3"], a["B4"])),
        "B1-B2": (a["B1"], a["B2"], (a["B1"], a["B2"]), (a["B2"], a["B3"]), (a["B1"], a["B2"], a["B3"])),
    }
    up, seam, left, right, merged = cases[case_id]
    la, lb = left
    lc, ld = right
    inp = panel(up, la, lb) ^ panel(up, lc, ld)
    assert_sandhi_merge(inp, up, seam, *merged)


@pytest.mark.parametrize("case_id", ["A1-B2", "a1-a3"])
def test_sandhi_swap_panel_order_opposite_coeff_same_mv(case_id):
    a = _atoms()
    cases = {
        "A1-B2": (a["A1"], (a["B1"], a["B2"]), (a["B2"], a["B3"])),
        "a1-a3": (a["a1"], (a["a2"], a["a3"]), (a["a3"], a["a4"])),
    }
    up, left, right = cases[case_id]
    la, lb = left
    lc, ld = right
    y1 = sandhi_canon(panel(up, la, lb) ^ panel(up, lc, ld))
    y2 = sandhi_canon(panel(up, lc, ld) ^ panel(up, la, lb))
    assert_mv_equal(y1, y2)
    assert_coeff_zero_diff(y1, y2 * S.NegativeOne)


def test_gmul_two_proj_sandhi_identity():
    a = _atoms()
    inp = panel(a["a1"], a["a2"], a["a3"]) ^ panel(a["a1"], a["a3"], a["a4"])
    assert_sandhi_merge(inp, a["a1"], a["a3"], a["a2"], a["a3"], a["a4"])


@pytest.mark.parametrize("n_panels", [2, 3])
def test_sandhi_chain_merge_idempotent_and_single_panel(n_panels):
    a = _atoms()
    blades = [a["B1"], a["B2"], a["B3"], a["B4"], a["B5"], a["B6"]]
    expr = chain_panels(a["A1"], blades[: n_panels + 1])
    out = sandhi_canon(expr)
    assert out != GExpr.Znl
    assert is_idempotent(expr)
    assert is_merged_panel(out)


@pytest.mark.parametrize("n_panels", [2])
def test_sandhi_chain_overlap_via_iterative_merge(n_panels):
    a = _atoms()
    blades = [a["B1"], a["B2"], a["B3"], a["B4"], a["B5"], a["B6"]]
    expr = chain_panels(a["A1"], blades[: n_panels + 1])
    got = sandhi_canon(expr)
    ref = panel(a["A1"], blades[0], blades[1])
    for i in range(1, n_panels):
        ref = sandhi_canon(ref ^ panel(a["A1"], blades[i], blades[i + 1]))
    assert_box_equal(got, ref)


@pytest.mark.parametrize(
    "case_id",
    ["A1-B", "a1-a", "nested-B3"],
)
def test_sandhi_idempotent(case_id):
    a = _atoms()
    factories = {
        "A1-B": lambda: panel(a["A1"], a["B1"], a["B2"]) ^ panel(a["A1"], a["B2"], a["B3"]),
        "a1-a": lambda: panel(a["a1"], a["a2"], a["a3"]) ^ panel(a["a1"], a["a3"], a["a4"]),
        "nested-B3": lambda: (
            (a["B3"] ^ panel(a["A1"], a["B1"], a["B2"], a["A2"]))
            ^ panel(a["A1"], a["B2"], a["B3"])
            ^ panel(a["B2"], a["B1"], a["B3"])
            ^ panel(a["B2"], a["A2"], a["B3"])
        ),
    }
    assert is_idempotent(factories[case_id]())


def test_sandhi_nested_stress_not_zero():
    """Lowercase atoms: the uppercase span is 4-D, where this grade-6 wedge is zero."""
    a = _atoms()
    expr = (
        (a["b3"] ^ panel(a["a1"], a["b1"], a["b2"], a["a2"]))
        ^ panel(a["a1"], a["b2"], a["b3"])
        ^ panel(a["b2"], a["b1"], a["b3"])
        ^ panel(a["b2"], a["a2"], a["b3"])
    )
    out = sandhi_canon(expr)
    assert out != GExpr.Znl
    assert is_idempotent(expr)


def test_wedge_anticommutativity_mv_and_coeff():
    a = _atoms()
    p12 = a["a1"] ^ a["a2"]
    p21 = a["a2"] ^ a["a1"]
    assert p12.mv == p21.mv
    assert p12.coeff + p21.coeff == 0


def test_sandhi_merge_single_contraction_mv():
    a = _atoms()
    out = sandhi_canon(panel(a["A1"], a["B1"], a["B2"]) ^ panel(a["A1"], a["B2"], a["B3"]))
    assert is_merged_panel(out)
    assert type(box_mv(out)) == glcntrct


def test_sandhi_output_is_box_with_nontrivial_mv():
    a = _atoms()
    out = sandhi_canon(panel(a["A1"], a["B1"], a["B2"]) ^ panel(a["A1"], a["B2"], a["B3"]))
    assert box_mv(out) != GExpr.nl
    assert box_coeff(out) != S.Zero


def test_sandhi_forward_reverse_three_panel_chain():
    """Chain-adjacent 2-blade panels: reverse wedge order flips coeff, same mv."""
    a = _atoms()
    terms = [
        panel(a["A1"], a["B1"], a["B2"]),
        panel(a["A1"], a["B2"], a["B3"]),
        panel(a["A1"], a["B3"], a["B4"]),
    ]
    yf = sandhi_canon(terms[0] ^ terms[1] ^ terms[2])
    yr = sandhi_canon(terms[2] ^ terms[1] ^ terms[0])
    assert_mv_equal(yf, yr)
    assert_coeff_zero_diff(yf, yr * S.NegativeOne)


@pytest.mark.parametrize("perm_index", list(range(6)))
def test_sandhi_three_panel_permutation_idempotent(perm_index):
    from itertools import permutations

    a = _atoms()
    terms = [
        panel(a["A1"], a["B1"], a["B2"]),
        panel(a["A1"], a["B2"], a["B3"]),
        panel(a["A1"], a["B3"], a["B4"]),
    ]
    perm = list(permutations(terms))[perm_index]
    out = sandhi_canon(perm[0] ^ perm[1] ^ perm[2])
    assert sandhi_canon(out) == out


def test_sandhi_complex_three_panels_overflow_zero():
    """Zero because three grade-2 panels overflow the 4-D ``I41`` ceiling.

    The same shape over lowercase (13-D) atoms merges to a non-zero normal form
    with a squared overlap scalar; see ``test_sandhi_complex`` in ``test_gextp``.
    """
    a = _atoms()
    inp = (
        panel(a["A1"] ^ a["A2"], a["B1"], a["B2"], a["C1"], a["C2"])
        ^ panel(a["A1"] ^ a["A2"], a["B1"], a["B2"], a["D1"], a["D2"])
        ^ panel(a["A1"] ^ a["A2"], a["B1"], a["B2"], a["B3"], a["C3"])
    )
    assert is_sandhi_zero(sandhi_canon(inp))


def test_sandhi_two_blade_up_shared_pair():
    """2-blade up: overlap at ``B1^B2`` (linear, not squared in Option B)."""
    from Sygal.operators.assop.gextp import gextp

    a = _atoms()
    t1 = (a["A1"] ^ a["A2"]) < (a["B1"] ^ a["B2"] ^ a["C1"])
    t2 = (a["A1"] ^ a["A2"]) < (a["B1"] ^ a["B2"] ^ a["C2"])
    got = sandhi_canon(t1 ^ t2)
    up = a["A1"] ^ a["A2"]
    want = (up | (a["B1"] ^ a["B2"])) * (up < gextp(a["B1"], a["B2"], a["C1"], a["C2"]))
    assert_mv_equal(got, want)
    assert_coeff_equal_or_opposite(got, want)


def test_sandhi_option_b_matches_canon_iter():
    from Sygal.operators.assop.canon.gextpsimp import gextpsimp_with_backend
    from Sygal.operators.assop.gextp import gextp as gextp_cls

    a = _atoms()
    gextpsimp_with_backend("option_b")
    inp = panel(a["A1"], a["B1"], a["B2"]) ^ panel(a["A1"], a["B2"], a["B3"])
    assert_box_equal(gextp_cls.gsimplify(inp), sandhi_canon(inp))


@pytest.mark.parametrize("case_id", ["B23", "B34", "a234"])
def test_sandhi_many_seams_param(case_id):
    a = _atoms()
    cases = {
        "B23": ((a["B1"], a["B2"]), (a["B2"], a["B3"]), a["B2"], (a["B1"], a["B2"], a["B3"])),
        "B34": ((a["B2"], a["B3"]), (a["B3"], a["B4"]), a["B3"], (a["B2"], a["B3"], a["B4"])),
        "a234": ((a["a2"], a["a3"]), (a["a3"], a["a4"]), a["a3"], (a["a2"], a["a3"], a["a4"])),
    }
    left, right, seam, merged = cases[case_id]
    la, lb = left
    lc, ld = right
    assert_sandhi_merge(panel(a["A1"], la, lb) ^ panel(a["A1"], lc, ld), a["A1"], seam, *merged)


def test_sandhi_coeff_is_nontrivial():
    a = _atoms()
    out = sandhi_canon(panel(a["A1"], a["B1"], a["B2"]) ^ panel(a["A1"], a["B2"], a["B3"]))
    assert box_coeff(out) != S.Zero


def test_sandhi_zero_panel_xor_is_zero():
    a = _atoms()
    z = sandhi_canon(panel(a["A1"], a["B1"], a["B2"]) ^ panel(a["A1"], a["B1"], a["B2"]))
    assert is_sandhi_zero(z)


def test_sandhi_merged_down_is_wedge():
    from Sygal.operators.assop.gextp import gextp

    a = _atoms()
    out = sandhi_canon(panel(a["A1"], a["B1"], a["B2"]) ^ panel(a["A1"], a["B2"], a["B3"]))
    down = box_mv(out).down
    assert type(down) == gextp
    assert len(down.args) == 3


def test_sandhi_quad_panel_chain_not_znl():
    a = _atoms()
    expr = chain_panels(a["A1"], [a["B1"], a["B2"], a["B3"], a["B4"], a["B5"]])
    out = sandhi_canon(expr)
    assert out != GExpr.Znl
    assert is_idempotent(expr)


def test_sandhi_double_merge_overlap_squared():
    a = _atoms()
    inp = panel(a["A1"], a["B1"], a["B2"]) ^ panel(a["A1"], a["B2"], a["B3"])
    once = sandhi_canon(inp)
    assert_sandhi_merge(inp, a["A1"], a["B2"], a["B1"], a["B2"], a["B3"])
    twice_inp = once ^ panel(a["A1"], a["B3"], a["B4"])
    assert is_idempotent(twice_inp)
