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


from libs.Sygal.operators.binop.outermorphic.isomorphic.isomorphic import isomorphic


class transforms(inversion):
  # __name__ = "inversion"
  def __new__(cls,sub:"GExpr",obj:"GExpr")->Optional[Box]:
    # sub has exponential arguements as box
    # sub -> [p1^oo,th]
    raise NotImplemented
    t = (obj,)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))
    tmvs = t1[0].mv
    coeff = t1[0].coeff

    if type(sub)==Box and sub.grade == {2}:
      BX = sub
      dot = ((sub.mv)<(sub.mv)).eval()
      if dot == 0:
        t = translation(sub,obj)
        Box.__new__(Box,t,coeff)
      elif dot == S(1):
        t = dilation(sub,obj)
        Box.__new__(Box,t,coeff)
      elif dot == S(-1):
        t = rotation(sub,obj)
        Box.__new__(Box,t,coeff)
      else :
        t = GExpr.__new__(transforms,sub,obj)
        Box.__new__(Box,t,coeff)
    
    t = (sub,obj)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))
    tmvs = [t1[0].mv,t1[1].mv]
    coeff = Mul(t1[0].coeff,t1[1].coeff)
    
    # Pattern match for grade value
    # Check for scalars
    if(coeff==S(0)):
      return(GExpr.Znl)

    if (is_invertible(tmvs[0])):
      obj = GExpr.__new__(transforms,tmvs[0],tmvs[1])
    else :
      raise ValueError
    return Box.__new__(Box,obj,coeff)




from .dilation import dilation
from .rotation import rotation
from .translation import translation