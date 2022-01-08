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

# MAy be can be better programmed with moads monoids eyc \_(..)_/
def sclrprdctconcat_rl(expr):
  if isinstance(expr,sclrprdct):
    if(type(expr.down)==glcntrct):
      tu = expr.up
      tdu = expr.down.up
      tdd = expr.down.down
      t1 = [tu,tdu]
      t2 = gextp(*t1)
      t3 = sclrprdct(t2,tdd)
      return t3
    elif(type(expr.down)==grcntrct):
      tu = expr.up
      tdu = expr.down.up
      tdd = expr.down.down
      if( is_unMixedGrade(tdu) and is_unMixedGrade(tdd)):
        t1 = [tu,tdu]
        t2 = gextp(*t1)
        t3 = sclrprdct(t2,tdd)
        sign1 = next(iter(tdu.grade))%2
        sign2 = (next(iter(tdd.grade))-1)%2
        sign = S(-2)*((sign1*sign2))+1
        return t3*sign
      else:
        return expr
    elif(type(expr.up)==grcntrct):
      td = expr.down
      tuu = expr.up.up
      tud = expr.up.down
      t1 = [tuu,td]
      t2 = gextp(*t1)
      t3 = sclrprdct(t2,tud)
      return t3
    elif(type(expr.up)==glcntrct):
      td = expr.down
      tuu = expr.up.up
      tud = expr.up.down
      if( is_unMixedGrade(tuu) and is_unMixedGrade(tud)):
        t1 = [tuu,td]
        t2 = gextp(*t1)
        t3 = sclrprdct(tud,t2)
        sign1 = next(iter(tud.grade))%2
        sign2 = (next(iter(tuu.grade))-1)%2
        sign = S(-2)*((sign1*sign2))+1
        return t3*sign
      else:
        return expr
    else:
      return expr
  else:
    return expr



def sclrprdctcanon():
  sclrprdct.gcanonicalization = exhaust(do_one(sclrprdctconcat_rl,))
