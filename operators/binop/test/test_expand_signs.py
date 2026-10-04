"""Sign and coefficient hygiene for glcntrct / sclrprdct expand (NH₃-style panels)."""

from __future__ import annotations

import pytest
from sympy import Rational

from Sygal.Box import Box
from Sygal.GExpr import GExpr
from Sygal.initial import A1, B1, B2, B3, B4, B5, B6, a1, a2, a3, b1, b2
from Sygal.operators.binop.test.expand_helpers import (
    coeff_to_complex,
    count_sclrprdct_nodes,
    expand_panel_pipeline,
    iter_gadd_box_terms,
    miss_min_coeff,
    subset_sum_coeff,
)


def _panel(left, wedge, amp):
    return Box.__new__(Box, left < wedge, Rational(str(float(amp))))


@pytest.mark.parametrize(
    "wedge, sym_names, n_terms, expect_subset_sum",
    [
        (B1 ^ B2, ("B1", "B2"), 2, False),
        (B1 ^ B2 ^ B3, ("B1", "B2", "B3"), 3, True),
        (B1 ^ B2 ^ B3 ^ B4, ("B1", "B2", "B3", "B4"), 4, False),
    ],
)
def test_glcntrct_expand_drop_one_term_count(wedge, sym_names, n_terms, expect_subset_sum):
    """``glcntrct`` split: n grade-1 down-args → n drop-one remainder terms."""
    amp = 0.31
    expanded = expand_panel_pipeline(_panel(A1, wedge, amp))
    terms = iter_gadd_box_terms(expanded)
    assert len(terms) == n_terms
    assert count_sclrprdct_nodes(expanded) == 0


@pytest.mark.parametrize(
    "wedge, sym_names, expect_subset_sum",
    [
        (B1 ^ B2, ("B1", "B2"), False),
        (B1 ^ B2 ^ B3, ("B1", "B2", "B3"), True),
        (B1 ^ B2 ^ B3 ^ B4, ("B1", "B2", "B3", "B4"), False),
    ],
)
def test_expand_coefficients_miss_min_recovers_input(wedge, sym_names, expect_subset_sum):
    """Minimum missing-atom term coeff equals panel ``Box.coeff``."""
    amp = -0.47
    expanded = expand_panel_pipeline(_panel(A1, wedge, amp))
    got, n_used = miss_min_coeff(expanded, sym_names)
    assert n_used == len(sym_names)
    assert coeff_to_complex(got) == pytest.approx(amp, abs=1e-9)


@pytest.mark.parametrize(
    "wedge, sym_names, expect_zero_sum",
    [
        (B1 ^ B2, ("B1", "B2"), True),
        (B1 ^ B2 ^ B3 ^ B4, ("B1", "B2", "B3", "B4"), True),
    ],
)
def test_even_term_count_subset_sum_cancels(wedge, sym_names, expect_zero_sum):
    """Even number of ± paired drop-one terms → subset-sum zero."""
    amp = 0.19
    expanded = expand_panel_pipeline(_panel(A1, wedge, amp))
    total, _ = subset_sum_coeff(expanded, sym_names)
    assert abs(total) < 1e-12


def test_odd_three_blade_subset_sum_equals_input():
    """Odd n=3: signed sum of drop-one terms equals panel coeff (NH₃ n_exc=3 pattern)."""
    amp = Rational(2, 7)
    sym = ("B1", "B2", "B3")
    expanded = expand_panel_pipeline(_panel(A1, B1 ^ B2 ^ B3, amp))
    total, n_used = subset_sum_coeff(expanded, sym)
    assert n_used == 3
    assert coeff_to_complex(total) == pytest.approx(float(amp), abs=1e-9)


def test_gextp_anticommutativity_opposite_coeffs():
    """``a1^a2`` and ``a2^a1``: same blade, opposite sign (``test_gextp.test_0``)."""
    assert (a1 ^ a2).mv == (a2 ^ a1).mv
    assert (a1 ^ a2).coeff + (a2 ^ a1).coeff == 0


def test_panel_coeff_propagation_not_fci_oracle():
    """Expand tracks ``Box.coeff``; wrong input → wrong miss_min readout."""
    sym = ("B1", "B2")
    wedge = B1 ^ B2
    for amp in (0.25, -0.5, 1.0):
        expanded = expand_panel_pipeline(_panel(A1, wedge, amp))
        got, _ = miss_min_coeff(expanded, sym)
        assert coeff_to_complex(got) == pytest.approx(amp, abs=1e-9)


def test_xor_nested_contractions_parity_str_regression():
    """Nested contraction XOR must not crash parity / gextp canonicalization.

    Uses lowercase (13-D) atoms: over the uppercase 4-D span this grade-6 wedge
    is identically zero, so it could not exercise the non-zero path.
    """
    from Sygal.initial import b3
    from Sygal.operators.assop.gextp import gextp
    from Sygal.strategies.iters import canon_iter

    expr = (
        (b3 ^ (a1 < (b1 ^ b2 ^ a2)))
        ^ (a1 < (b2 ^ b3))
        ^ (b2 < (b1 ^ b3))
        ^ (b2 < (a2 ^ b3))
    )
    out = canon_iter(gextp)(expr)
    assert out != GExpr.Znl
