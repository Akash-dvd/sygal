"""Binop tests: unit metric patch for numeric expand coefficients."""

from __future__ import annotations

import pytest

from Sygal.operators.binop.test.metric_fixtures import (
    apply_unit_metric_patch,
    restore_metric_patch,
)


@pytest.fixture(autouse=True)
def _unit_metric_for_expand_tests():
    apply_unit_metric_patch()
    yield
    restore_metric_patch()
