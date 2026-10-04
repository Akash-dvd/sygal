# Perpendicular and parallel

# Core imports
# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.sympy_basic import S
from Sygal.imports.typing_helpers import Optional
from Sygal.imports.strategies import exhaust, do_one

# Only import operators actually used
from Sygal.operators.binop.outermorphic.rejection import rejection


def rejection_canon(expr:Box)->Optional[Box]:
  if (type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == rejection:
      sub = BX.mv.down
      obj = BX.mv.up
      if (obj^sub).coeff == S(0):
        return GExpr.Znl
      else :
        return expr
    else :
      return expr
  else :
    return expr

def rejectioncanon():
  rejection.gcanonicalization = exhaust(do_one(rejection_canon,))
