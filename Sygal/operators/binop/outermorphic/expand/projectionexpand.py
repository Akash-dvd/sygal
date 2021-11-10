from ...importshead import *
from ...importstail import *


from libs.Sygal.operators.assop.gadd import gadd
from libs.Sygal.operators.assop.gextp import gextp
from libs.Sygal.operators.assop.gmul import gmul

from libs.Sygal.operators.binop.ganticomm import ganticomm
from libs.Sygal.operators.binop.gcomm import gcomm
from libs.Sygal.operators.binop.sclrprdct import sclrprdct
from libs.Sygal.operators.binop.grcntrct import grcntrct
from libs.Sygal.operators.binop.glcntrct import glcntrct

from libs.Sygal.utils.utils1 import is_invertible,is_blade

from libs.Sygal.operators.binop.outermorphic.projection import projection



def projection_expand(expr:"projection")->Optional[Box]:
  if type(expr) == projection:
    sub = expr.down
    obj = expr.up
    if is_invertible(sub):
      coeff = Pow((sub<sub),-1)
      return Box.__new__(Box,(obj<sub)<sub,coeff)
    else :
      raise
  else :
    return expr

def projectionexpand():
  projection.gexpand = projection_expand

