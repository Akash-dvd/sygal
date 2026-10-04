# Perpendicular and parallel

# Core imports
# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.typing_helpers import Optional
from Sygal.imports.strategies import exhaust, do_one
from Sygal.imports.utils import is_perpendicularPair

# Only import operators actually used
from Sygal.operators.binop.outermorphic.projection import projection


def projection_canon(expr:Box)->Optional[Box]:
  if (type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == projection:
      sub = BX.mv.down
      obj = BX.mv.up
      if is_perpendicularPair(obj,sub):
        return GExpr.Znl
      else :
        return expr
    else :
      return expr
  else :
    return expr

def projectioncanon():
  projection.gcanonicalization = exhaust(do_one(projection_canon,))