"""Exterior-product simplification backends.

This module now supports two strategies:

- option_b (default): virtual-variable / Capelli-style implementation via
  `gextpcanon.concat.sandhi`. This path preserves coefficients correctly.
- option_c: Hopf-coproduct scaffold in a separate module for future use.

Why this change:
The previous `concat.sandhi` worked directly on `gextp` nodes and ignored
`Box.coeff`, so it could merge multivectors but lose/corrupt scalar factors.
The new default runs on full `Box` expressions where coefficient tracking is
available.
"""

from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.typing_helpers import Callable
from Sygal.imports.strategies import exhaust, do_one

from Sygal.operators.assop.gextp import gextp
from Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion
from Sygal.operators.binop.outermorphic.projection import projection
from Sygal.operators.binop.outermorphic.rejection import rejection


# Backend id used by `gextpsimp()` unless caller overrides.
DEFAULT_SANDHI_BACKEND = "option_b"


def _sandhi_option_b(expr: Box):
  """Option B (default): delegate to Capelli-style canonical sandhi.

  This uses the Box-aware implementation in `gextpcanon`, which can propagate
  nested signs/coefficients and is the default recommended path for Sygal.
  Internally, `gextpcanon` now computes this-level coefficients via the
  explicit Option-B helper layer (`gextpcapelli`).
  """
  from Sygal.operators.assop.canon.gextpcanon import concat as canon_concat
  return canon_concat.sandhi(expr)


def _sandhi_option_c(expr: Box):
  """Option C: Hopf-coproduct backend entrypoint.

  Implemented in a separate module so it can evolve independently. It is kept
  optional and non-default for now.
  """
  from Sygal.operators.assop.canon.gextpsimp_hopf import hopf_concat
  return hopf_concat.sandhi(expr)


def _resolve_sandhi_backend(name: str) -> Callable:
  if name == "option_b":
    return _sandhi_option_b
  if name == "option_c":
    return _sandhi_option_c
  raise ValueError(
    f"Unknown sandhi backend '{name}'. Expected 'option_b' or 'option_c'."
  )


def inv_gextp(expr):

  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gextp:

      for i,arg in enumerate(BX.mv.args):
        if(type(arg)==inversion):
          up = arg.up
          down = arg.down
          if(up in BX.mv.args) or (down in BX.mv.args):
            lst = list(BX.mv.args)
            # INV -> Gmul
            # sub*obj*sub/(sub<sub)
            t = arg.gexpand()
            # Gmul -> Gadd
            t1 = t.gexpand()
            # distribute over sum
            lst[i] = t1
            t2 = gextp(*t1)
            t3 = t2.gdistribute()
            return t3
      else :
        return expr
    else :
      return expr 
  else :
    return expr

# sign issues
def proj_gextp(expr):
  # DproU^D -> 0
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gextp:

      for i,arg in enumerate(BX.mv.args):
        if(type(arg)==projection):
          up = arg.up
          down = arg.down
          if (down in BX.mv.args):
            return GExpr.Znl
          # (up in BX.mv.args): doesn't make much sense
      else :
        return expr
    else :
      return expr 
  else :
    return expr

# sign issues
def rej_gextp(expr):
  # DrejU^D -> 
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gextp:

      for i,arg in enumerate(BX.mv.args):
        if(type(arg)==rejection):
          up = arg.up
          down = arg.down
          if (down in BX.mv.args):
            lst = list(BX.mv.args)
            lst[i] = (up^down) 
            return gextp(*lst)
          # (up in BX.mv.args): doesn't make much sense
      else :
        return expr
    else :
      return expr 
  else :
    return expr

############################

def gextpsimp():
  """Register gextp simplifier with default Option B backend."""
  gextpsimp_with_backend(DEFAULT_SANDHI_BACKEND)


def gextpsimp_with_backend(backend: str = DEFAULT_SANDHI_BACKEND):
  """Register gextp simplifier with explicit backend selection.

  Parameters
  ----------
  backend:
      - 'option_b' (default): virtual-variable / Capelli path (recommended)
      - 'option_c': Hopf-coproduct experimental path
  """
  sandhi_backend = _resolve_sandhi_backend(backend)
  gextp.gsimplify = exhaust(do_one(sandhi_backend, inv_gextp, proj_gextp, rej_gextp))