from ....importshead import *
from ....importstail import *


from libs.Sygal.operators.assop.gadd import gadd
from libs.Sygal.operators.assop.gextp import gextp
from libs.Sygal.operators.assop.gmul import gmul

from libs.Sygal.operators.binop.ganticomm import ganticomm
from libs.Sygal.operators.binop.gcomm import gcomm
from libs.Sygal.operators.binop.sclrprdct import sclrprdct
from libs.Sygal.operators.binop.grcntrct import grcntrct
from libs.Sygal.operators.binop.glcntrct import glcntrct

from libs.Sygal.utils.utils1 import is_invertible,is_blade

from libs.Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion



def inversion_expand(expr:"inversion")->Optional[Box]:
  if type(expr) == inversion:
    sub = expr.down
    obj = expr.up
    #  But while creating this was checked
    if is_invertible(sub):
      if(type(sub)==gmul):
        coeff = Pow((sub<(sub.reversion())),-1)
        return Box.__new__(Box,(sub.reversion())*obj*sub,coeff)
      elif (sub.grade=={1}):
        coeff = Pow((sub<sub),-1)
        return Box.__new__(Box,sub*obj*sub,coeff)
      else:
        raise NotImplemented
    else :
      raise NotImplemented
  else :
    return expr

def inversionexpand():
  inversion.gexpand = inversion_expand

