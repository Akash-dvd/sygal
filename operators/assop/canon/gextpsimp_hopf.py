"""Option C backend: Hopf-coproduct based sandhi scaffold.

This module is intentionally separate from `gextpsimp.py` so Option C can be
iterated independently. It is usable now via backend selection, but remains
experimental compared to Option B.
"""

from Sygal.Box import Box


class hopf_concat:
  @staticmethod
  def sandhi(expr: Box):
    """Experimental Option C entrypoint.

    Current behavior:
    - Uses Option B as a correctness fallback.

    Planned behavior:
    - Implement explicit coproduct-based vichcheda and refactor-by-pattern
      sandhi reconstruction.
    """
    # Keep Option C safe while the explicit coproduct engine is developed.
    from Sygal.operators.assop.canon.gextpcanon import concat as canon_concat
    return canon_concat.sandhi(expr)

