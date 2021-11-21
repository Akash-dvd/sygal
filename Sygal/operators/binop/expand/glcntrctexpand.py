from libs.Sygal.imports.import1head import *
from libs.Sygal.imports.import1tail import *

from libs.Sygal.operators.assop.gadd import gadd
from libs.Sygal.operators.assop.gextp import gextp
from libs.Sygal.operators.assop.gmul import gmul

from libs.Sygal.operators.binop.ganticomm import ganticomm
from libs.Sygal.operators.binop.gcomm import gcomm
from libs.Sygal.operators.binop.sclrprdct import sclrprdct
from libs.Sygal.operators.binop.grcntrct import grcntrct
from libs.Sygal.operators.binop.glcntrct import glcntrct
from libs.Sygal.operators.binop.sclrprdct import sclrprdct

from libs.Sygal.imports.import_util2 import *

from libs.Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion
from libs.Sygal.operators.binop.outermorphic.projection import projection
from libs.Sygal.operators.binop.outermorphic.rejection import rejection

def difflist(t1,t2):
  return [ele for ele in t1 if ele not in t2]

def glcntrct_expand(expr:Expr)->Union[Expr,Box]:
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


