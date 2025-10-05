from Sygal.imports.import1head import *
from Sygal.imports.import1tail import *

from Sygal.operators.assop.gadd import gadd
from Sygal.operators.assop.gextp import gextp
from Sygal.operators.assop.gmul import gmul

from Sygal.operators.binop.ganticomm import ganticomm
from Sygal.operators.binop.gcomm import gcomm
from Sygal.operators.binop.sclrprdct import sclrprdct
from Sygal.operators.binop.glcntrct import glcntrct
from Sygal.operators.binop.grcntrct import grcntrct
from Sygal.operators.binop.sclrprdct import sclrprdct

from Sygal.imports.import_util2 import *

from Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion
from Sygal.operators.binop.outermorphic.projection import projection
from Sygal.operators.binop.outermorphic.rejection import rejection

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



