from Sygal.imports.import1head import *
from Sygal.imports.import1tail import *

from Sygal.operators.assop.gadd import gadd
from Sygal.operators.assop.gextp import gextp
from Sygal.operators.assop.gmul import gmul

from Sygal.operators.binop.ganticomm import ganticomm
from Sygal.operators.binop.gcomm import gcomm
from Sygal.operators.binop.sclrprdct import sclrprdct
from Sygal.operators.binop.grcntrct import grcntrct
from Sygal.operators.binop.glcntrct import glcntrct
from Sygal.operators.binop.sclrprdct import sclrprdct

from Sygal.imports.import_util2 import *

from Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion
from Sygal.operators.binop.outermorphic.projection import projection
from Sygal.operators.binop.outermorphic.rejection import rejection


def glcntrct_2Proj(expr:Expr)->Union[Expr,Box]:
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == glcntrct:
      tu = BX.mv.up #MV
      td = BX.mv.down

      if type(tu) ==  glcntrct:
        tuu = tu.up
        tud = tu.down
        
        if(td == tud):
          if not is_perpendicularPair(td,tud) and is_vecBlade(td):
            coeff = sclrprdct(td,td)*cf
            mv = projection(td,tuu)
            return mv*coeff
          elif is_perpendicularPair(td,tud) and is_vecBlade(td):
            raise ValueError("MAybe answer is GExpr.Znl")
          else :
            return expr 
        else :
          return expr

      elif type(tu) ==  grcntrct:
        tuu = tu.up # MV
        tud = tu.down # Blade
        
        if(td == tud):
          if not is_perpendicularPair(td,tud) and is_vecBlade(td):
            coeff = sclrprdct(td,td)*cf
            mv = projection(td,tuu)
            # if( is_unMixedGrade(tu) and is_unMixedGrade(td)):
            # no need to check for is_unMixedGrade coz of is_vecBlade
            sign1 = next(iter(tuu.grade))%2
            sign2 = (next(iter(tud.grade))-1)%2
            sign = S(-2)*((sign1*sign2))+1
            return mv*coeff*sign
          elif is_perpendicularPair(td,tud) and is_vecBlade(td):
            raise ValueError("MAybe answer is GExpr.Znl")
          else :
            return expr 
        else :
          return expr     
      else :
        return expr
    else :
      return expr
  else :
    return expr


def glcntrct_2Rej(expr:Expr)->Union[Expr,Box]:
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == glcntrct :
      tu = BX.mv.up # Blade
      td = BX.mv.down # Blade + MV

      # if type(td) == gextp and is_vecBlade(tu) and not is_perpendicularPair(tu,tu):
      if type(td) == gextp and is_vecBlade(tu):
        tu_set = {tu} if tu.grade == {1} else set(tu.args)
        td_set = set(td.args)
        if(tu_set == tu_set.intersection(td_set)):
          if(not is_perpendicularPair(tu,tu)):
            coeff = (sclrprdct(tu,tu)*cf)
            tmv1 = list(td_set - tu_set)
            tmv2 = gextp(*tmv1)

            td1 = ([tu] if tu.grade == {1} else list(tu.args))
            td1.extend(tmv1) 
            sign = parity(td1,td.args)

            return rejection(tu,tmv2)*coeff*sign  
          elif(is_perpendicularPair(tu,tu)):
            raise NotImplementedError
          else :
            return expr
        else:
          return expr
      else :
        return expr
    else :
      return expr
  else :
    return expr

def glcntrcthigher():
  glcntrct.ghigher = exhaust(do_one(glcntrct_2Proj,glcntrct_2Rej))
