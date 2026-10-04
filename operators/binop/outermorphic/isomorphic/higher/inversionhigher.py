# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.typing_helpers import Optional
from Sygal.imports.strategies import exhaust, do_one

# Only import operators actually used
from Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion


# concat
def inversion_higher(expr:"Box")->Optional[Box]:
  if (type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == inversion:
      sub = BX.mv.down
      obj = BX.mv.up
      if type(obj) == inversion:
        obju = obj.up
        objd = obj.down
        return inversion((objd*sub),obju)*cf
      else :
        return expr
    else :
      return expr
  else :
    return expr

def inversionhigher():
  inversion.ghigher = inversion_higher
