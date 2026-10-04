# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.typing_helpers import Optional
from Sygal.imports.strategies import exhaust, do_one, expand_iter
from Sygal.imports.utils import is_scalarPair
from Sygal.operators.binop.sclrprdct import sclrprdct

# Only import operators actually used
from Sygal.operators.assop.gmul import gmul


# Assuming blade*blade = scalar

def gmul_canon(expr:"gmul")->Optional[GExpr]:
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gmul and len(BX.mv.args)>=2:
      # loop before the last element
      for i,arg in enumerate(BX.mv.args[:-1]):
        # check if the adjacent element leads to scalar
        t = is_scalarPair(arg,BX.mv.args[i+1])
        if t:
          t1 = [element for j, element in enumerate(BX.mv.args) if j not in {i,i+1}]
          coeff = expand_iter(sclrprdct)(BX.mv.args[i]<BX.mv.args[i+1])
          if t1:
            return gmul(*t1)*cf*coeff
          else :
            return coeff*cf
      return expr
    else :
      return expr 

  else :
    return expr

def gmulcanon():
  gmul.gcanonicalization = gmul_canon
