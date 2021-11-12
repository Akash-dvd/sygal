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

from libs.Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion
from libs.Sygal.operators.binop.outermorphic.projection import projection
from libs.Sygal.operators.binop.outermorphic.rejection import rejection



def inversion_simplify(expr:"inversion")->Optional[Box]:
  if type(expr) == inversion:
    sub = expr.down
    obj = expr.up
    if is_invertible(sub):
      if(type(obj)== inversion):
        sub1 = obj.down
        obj1 = obj.up
        mv = inversion(sub*sub1,obj1)
        return Box.__new__(Box,mv)
    else :
      raise
  else :
    return expr

def inversionsimp():
  inversion.gsimplify = exhaust(inversion_simplify)
