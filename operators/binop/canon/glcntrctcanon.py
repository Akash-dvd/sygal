# Core imports - Import directly to avoid circular dependency
from Sygal.Box import Box
from Sygal.imports.sympy_basic import S
from Sygal.imports.strategies import exhaust, do_one
from Sygal.imports.utils import is_unMixedGrade

# Only import operators actually used
from Sygal.operators.assop.gextp import gextp
from Sygal.operators.binop.glcntrct import glcntrct
from Sygal.operators.binop.grcntrct import grcntrct


def lcntrctconcat_rl(expr):
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if isinstance(BX.mv,glcntrct):
      if(type(BX.mv.down)==glcntrct):
        tu = BX.mv.up
        tdu = BX.mv.down.up
        tdd = BX.mv.down.down
        t1 = [tu,tdu]
        t2 = gextp(*t1)
        t3 = glcntrct(t2,tdd)
        return t3*cf
        # May not not ever coz of Rcntrct2Lcntrct
      elif(type(BX.mv.down)==grcntrct):
        tu = BX.mv.up
        tdu = BX.mv.down.up
        tdd = BX.mv.down.down
        if( is_unMixedGrade(tdu) and is_unMixedGrade(tdd)):
          t1 = [tu,tdu]
          t2 = gextp(*t1)
          t3 = glcntrct(t2,tdd)
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

def Lcntrct2Rcntrct(expr):
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if(type(BX.mv.down)==glcntrct):
      tu = BX.mv.up
      td = BX.mv.down
      if( is_unMixedGrade(tu) and is_unMixedGrade(td)):
        t1 = grcntrct(td,tu)
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


def glcntrctcanon():
  glcntrct.gcanonicalization = exhaust(do_one(lcntrctconcat_rl,))