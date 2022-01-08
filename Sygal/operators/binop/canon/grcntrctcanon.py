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
from libs.Sygal.imports.import_util2 import *


def rcntrctconcat_rl(expr):
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if isinstance(BX.mv,grcntrct):
      if(type(BX.mv.down)==grcntrct):
        tu = BX.mv.up
        tdu = BX.mv.down.up
        tdd = BX.mv.down.down
        t1 = [tdu,tu]
        t2 = gextp(*t1)
        t3 = grcntrct(tdd,t2)
        return t3*cf
      elif(type(BX.mv.down)==glcntrct):
        tu = BX.mv.up
        tdu = BX.mv.down.up
        tdd = BX.mv.down.down
        if( is_unMixedGrade(tdu) and is_unMixedGrade(tdd)):
          t1 = [tdu,tu]
          t2 = gextp(*t1)
          t3 = grcntrct(tdd,t2)
          sign1 = next(iter(tdu.grade))%2
          sign2 = (next(iter(tdd.grade))-1)%2
          sign = S(-2)*((sign1*sign2))+1
          return t3*sign*cf
        else:
          return BX
      else :
        return BX
    else:
      return BX
  else:
    return expr

def Rcntrct2Lcntrct(expr):
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if(type(BX.mv.down)==grcntrct):
      tu = BX.mv.up
      td = BX.mv.down
      if( is_unMixedGrade(tu) and is_unMixedGrade(td)):
        t1 = glcntrct(tu,td)
        sign1 = next(iter(tu.grade))%2
        sign2 = (next(iter(td.grade))-1)%2
        sign = S(-2)*((sign1*sign2))+1
        return t1*sign*cf
      else:
        return BX
    else:
      return BX
  else:
    return expr


def grcntrctcanon():
  grcntrct.gcanonicalization = exhaust(do_one(Rcntrct2Lcntrct,rcntrctconcat_rl))
