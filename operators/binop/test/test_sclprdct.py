"""``sclrprdct`` expand with unit metric patch (see ``conftest.py``)."""

from __future__ import annotations

from sympy import Rational, S

from Sygal.Box import Box
from Sygal.GExpr import GExpr
from Sygal.initial import A1, B1, B2, B3
from Sygal.operators.assop.gextp import gextp
from Sygal.operators.binop.sclrprdct import sclrprdct
from Sygal.operators.binop.test.expand_helpers import (
    count_sclrprdct_nodes,
    expand_panel_pipeline,
)


def test_sclrprdct_gexpand1_chains_through_glcntrct():
    """``gexpand1`` on multi-blade inner product feeds ``glcntrct`` pipeline."""
    wedge = B1 ^ B2 ^ B3
    panel = Box.__new__(Box, A1 < wedge, Rational(1, 3))
    expanded = expand_panel_pipeline(panel)
    assert count_sclrprdct_nodes(expanded) == 0
    assert expanded != GExpr.Znl


def test_sclrprdct_gexpand1_produces_gadd_of_blades():
    """``gexpand1`` on panel expand yields blade sum (inners folded via ``glcntrct``)."""
    from Sygal.operators.binop.test.expand_helpers import (
        expand_panel_pipeline,
        iter_gadd_box_terms,
    )

    wedge = B1 ^ B2
    panel = Box.__new__(Box, A1 < wedge, Rational(1, 5))
    expanded = expand_panel_pipeline(panel)
    assert len(iter_gadd_box_terms(expanded)) == 2
