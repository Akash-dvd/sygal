# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.sympy_basic import S
from Sygal.imports.typing_helpers import Optional
from Sygal.imports.strategies import expand_iter, exhaust, do_one

# Only import operators actually used - inversion is safe to import at module level
from Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion

# Lazy imports to avoid circular dependency - these are only used inside functions
# glcntrct, sclrprdct will be imported inside functions


# sub|obj = 0
# TODO -- expand it for more complex sub
def inversion_canon(expr:"Box")->Optional[Box]:
  # Lazy imports to avoid circular dependency
  from Sygal.operators.binop.glcntrct import glcntrct
  from Sygal.operators.binop.sclrprdct import sclrprdct
  
  if (type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == inversion:
      sub = BX.mv.down
      obj = BX.mv.up
      #  try iteratively type(sub).gexpand following sclprdct.gexpand
      t = expand_iter(glcntrct)(obj<sub)
      t1 = expand_iter(sclrprdct)(t)
      if t1.coeff == S(0):
        return sub*S(-1)
      else :
        return expr
    else :
      return expr
  else :
    return expr

def inversioncanon():
  inversion.gcanonicalization = exhaust((do_one(inversion_canon,)))
  
