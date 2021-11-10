from ..importshead import *
from ..importstail import *


from libs.Sygal.operators.assop.gadd import gadd
from libs.Sygal.operators.assop.gextp import gextp
from libs.Sygal.operators.assop.gmul import gmul

from libs.Sygal.operators.binop.ganticomm import ganticomm
from libs.Sygal.operators.binop.gcomm import gcomm
from libs.Sygal.operators.binop.sclrprdct import sclrprdct
from libs.Sygal.operators.binop.grcntrct import grcntrct
from libs.Sygal.operators.binop.glcntrct import glcntrct

from libs.Sygal.utils.utils1 import is_invertible,is_blade

def lcntrctconcat_rl(expr):
  if isinstance(expr,glcntrct):
    if(type(expr.down)==glcntrct):
      t1 = expr.up
      t2 = expr.down.up
      t3 = expr.down.down
      t4 = [t1,t2]
      t5 = gextp(*t4)
      t6 = glcntrct(t5,t3)
      if(t6.mv == GExpr.nl):
        return t6.coeff
      else :
        return t6.mv
    else:
      return expr
  else:
    return expr

def Lcntrct2Rcntrct():
  pass


def glcntrctsimp():
  glcntrct.gsimplify = lcntrctconcat_rl