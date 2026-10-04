# Core imports - Import directly to avoid circular dependency
from Sygal.Box import Box

# Only import operators actually used
from Sygal.operators.assop.gmul import gmul
from Sygal.operators.binop.outermorphic.isomorphic.isomorphic import isomorphic

def isomorphicExpander(expr):
  if (type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if issubclass(type(BX.mv),isomorphic):
      if(type(BX.mv.up)==gmul):
        new = type(BX.mv)
        t = [new(BX.mv.down,arg) for arg in BX.mv.up.args]
        return gmul(*t)*cf
      else :
        return expr
    else :
      return expr
  else :
    return expr

def isomorphicexpand():
  isomorphic.gexpand = isomorphicExpander