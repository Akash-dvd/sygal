"""Ensure ``Sygal.initial`` is loaded before assop tests collect parametrized atoms."""

import pytest

from Sygal.initial import *  # noqa: F401, F403


@pytest.fixture(autouse=True)
def _reset_sandhi_canon_cache():
    """Avoid stale ``canon_iter`` closures across tests that re-register gextp canon."""
    from . import sandhi_helpers as sandhi_h

    sandhi_h._canon = None
    from Sygal.operators.assop.canon.gextpcanon import gextpcanon

    gextpcanon()
    yield
    sandhi_h._canon = None
