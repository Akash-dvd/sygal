"""Tests for ``Sygal.utils.util.parity`` (permutation sign on grade-1 blades)."""

from __future__ import annotations

from sympy import S

from Sygal.initial import a1, a2, a3, a4, b1, b2
from Sygal.utils.util import parity


def test_parity_identity_is_plus_one():
    args = [a1, a2, a3]
    assert parity(args, args) == S.One


def test_parity_swap_two_grade1_atoms_is_minus_one():
    args = [a1, a2]
    swapped = [a2, a1]
    assert parity(args, swapped) == S.NegativeOne


def test_parity_double_swap_restores_plus_one():
    args = [a1, a2, b1, b2]
    once = [a2, a1, b1, b2]
    twice = [a2, a1, b2, b1]
    assert parity(args, once) == S.NegativeOne
    assert parity(args, twice) == S.One


def test_parity_matches_gextp_coeff_sign():
    """Outer product reorder flips sign via parity in ``gextp.__new__``."""
    assert (a1 ^ a2).coeff + (a2 ^ a1).coeff == 0
    assert (a1 ^ a2 ^ a3).coeff == -(a3 ^ a2 ^ a1).coeff or (
        (a1 ^ a2 ^ a3).mv == (a3 ^ a2 ^ a1).mv
    )
