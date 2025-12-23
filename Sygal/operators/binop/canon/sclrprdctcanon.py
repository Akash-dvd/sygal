# Core imports
from Sygal.imports.sympy_basic import S
from Sygal.imports.strategies import exhaust, do_one
from Sygal.imports.utils import is_unMixedGrade

# Lazy imports to avoid circular dependency - these are only used inside functions
# gextp, sclrprdct, glcntrct, grcntrct will be imported inside sclrprdctconcat_rl

# MAy be can be better programmed with moads monoids eyc \_(..)_/
def sclrprdctconcat_rl(expr):
  # Lazy imports to avoid circular dependency
  from Sygal.operators.assop.gextp import gextp
  from Sygal.operators.binop.sclrprdct import sclrprdct
  from Sygal.operators.binop.glcntrct import glcntrct
  from Sygal.operators.binop.grcntrct import grcntrct
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
  # Lazy import to avoid circular dependency
  from Sygal.operators.binop.sclrprdct import sclrprdct
  sclrprdct.gcanonicalization = exhaust(do_one(sclrprdctconcat_rl,))
