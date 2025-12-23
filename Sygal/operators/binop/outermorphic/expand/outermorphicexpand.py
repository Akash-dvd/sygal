# Core imports - Import directly to avoid circular dependency
from Sygal.Box import Box

# Only import operators actually used
from Sygal.operators.assop.gextp import gextp
from Sygal.operators.binop.outermorphic.outermorphic import outermorphic

def outermorphicExpander(expr):
  if (type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if issubclass(type(BX.mv),outermorphic):
      if(type(BX.mv.up)==gextp):
        new = type(BX.mv)
        t = [new(BX.mv.down,arg) for arg in BX.mv.up.args]
        return gextp(*t)*cf
      else :
        return expr
    else :
      return expr
  else :
    return expr

def outermorphicexpand():
  outermorphic.gexpand = outermorphicExpander