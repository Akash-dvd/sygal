# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.sympy_basic import Expr, Mul, subsets
from Sygal.imports.typing_helpers import Union
from Sygal.imports.strategies import exhaust, do_one
from Sygal.imports.utils import is_vecBlade, parity

# Only import operators actually used
from Sygal.operators.assop.gadd import gadd
from Sygal.operators.assop.gextp import gextp
from Sygal.operators.binop.sclrprdct import sclrprdct
from Sygal.operators.binop.grcntrct import grcntrct

def difflist(t1,t2):
  return [ele for ele in t1 if ele not in t2]

def grcntrct_expand(expr:Expr)->Union[Expr,Box]:
  if(type(expr)==Box):
    BX = GExpr.gdistribute(expr)
    cf = BX.coeff
    if(type(BX.mv)==grcntrct):
      up = BX.mv.up
      down = BX.mv.down
      if is_vecBlade(up) and is_vecBlade(down):
        up_args = [up] if up.grade == {1}  else up.args
        down_args = [down] if down.grade == {1}  else down.args

        lst = []

        for Bset in subsets(down_args,len(up_args)):

          diffdown = difflist(down_args,Bset)
          cpydiffdown = []
          cpydiffdown.extend(diffdown)
          cpydiffdown.extend(Bset)
          signdown = parity(down_args,cpydiffdown)
          upper = gextp(*up_args)
          lower = gextp(*Bset)
          coeff1 = sclrprdct(lower,upper).coeff
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



def grcntrctexpand():
  grcntrct.gexpand = exhaust(do_one(grcntrct_expand,))



