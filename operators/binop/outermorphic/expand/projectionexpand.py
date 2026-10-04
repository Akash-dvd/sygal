# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.sympy_basic import Pow
from Sygal.imports.typing_helpers import Optional
from Sygal.imports.strategies import expand_iter
from Sygal.imports.utils import is_nzScalarPair

# Only import operators actually used
from Sygal.operators.assop.gmul import gmul
from Sygal.operators.binop.outermorphic.projection import projection


def projection_expand(expr:Box)->Optional[Box]:
  if (type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == projection:
      sub = BX.mv.down
      obj = BX.mv.up
      if is_nzScalarPair(sub,sub.reversion()):
        t = expand_iter(gmul)((sub*sub))  
        if t.mv == GExpr.nl:
          coeff = Pow(t.coeff,-1)
          return ((obj<sub)<sub)*coeff
        else :
          raise ValueError("Couldn't reduce coeff to scalar")
      else :
        return expr 
    else :
      return expr
  else :
    return expr

def projectionexpand():
  projection.gexpand = projection_expand

 