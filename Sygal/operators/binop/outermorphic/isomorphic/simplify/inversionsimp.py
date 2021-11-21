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


# sub|obj = 0
# TODO -- expand it for more complex sub
def inversion_simplify(expr:"Box")->Optional[Box]:
  if (type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == inversion:
      sub = BX.mv.down
      obj = BX.mv.up
      #  try iteratively type(sub).gexpand following sclprdct.gexpand
      t = expand_iter(glcntrct)(obj<sub)
      t1 = expand_iter(sclrprdct)(t)
      if t1.coeff == S(0):
        return sub*S(-1)
      else :
        return expr
    else :
      return expr
  else :
    return expr

def inversionsimp():
  inversion.gsimplify = exhaust((do_one(inversion_simplify,)))
  
