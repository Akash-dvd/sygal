# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.sympy_basic import Expr, Mul
from Sygal.imports.typing_helpers import Union
from Sygal.imports.strategies import exhaust, do_one
from Sygal.imports.utils import is_vecBlade, parity
from Sygal.imports.sympy_basic import subsets

# Only import operators actually used - glcntrct is safe to import at module level
from Sygal.operators.binop.glcntrct import glcntrct

# Lazy imports to avoid circular dependency - these are only used inside functions
# gextp, sclrprdct, gadd will be imported inside functions

def difflist(t1,t2):
  return [ele for ele in t1 if ele not in t2]

def glcntrct_expand(expr:Expr)->Union[Expr,Box]:
  # Lazy imports to avoid circular dependency
  from Sygal.operators.assop.gextp import gextp
  from Sygal.operators.binop.sclrprdct import sclrprdct
  from Sygal.operators.assop.gadd import gadd
  
  if(type(expr)==Box):
    BX = GExpr.gdistribute(expr)
    cf = BX.coeff
    if(type(BX.mv)==glcntrct):
      up = BX.mv.up
      down = BX.mv.down
      if is_vecBlade(up) and is_vecBlade(down):
        up_args = [up] if up.grade == {1}  else up.args
        down_args = [down] if down.grade == {1}  else down.args

        lst = []

        for Bset in subsets(down_args,len(up_args)):

          diffdown = difflist(down_args,Bset)
          cpydiffdown = []
          cpydiffdown.extend(Bset)
          cpydiffdown.extend(diffdown)
          signdown = parity(down_args,cpydiffdown)
          upper = gextp(*up_args)
          lower = gextp(*Bset)
          coeff1 = sclrprdct(upper,lower).coeff
          if diffdown:
            mv = gextp(*diffdown)
            bx = mv*Mul(signdown,coeff1,cf)
            lst.append(bx)
          else :
            # bx = Box.__new__(Box,GExpr.Onl*Mul(coeff,coeff1))
            bx = GExpr.nl*Mul(signdown,coeff1,cf)
            lst.append(bx)
        t = gadd(*lst)
        return t
          
      else :
        return BX
    else:
      return BX
  else :
    return expr



def glcntrctexpand():
  glcntrct.gexpand = exhaust(do_one(glcntrct_expand,))


