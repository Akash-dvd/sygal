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


# Assuming blade*blade = scalar

def gmul_simp(expr:"gmul")->Optional[GExpr]:
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gmul and len(BX.mv.args)>=2:
      # loop before the last element
      for i,arg in enumerate(BX.mv.args[:-1]):
        # check if the adjacent element leads to scalar
        t = is_scalarPair(arg,BX.mv.args[i+1])
        if t:
          t1 = [element for j, element in enumerate(BX.mv.args) if j not in {i,i+1}]
          coeff = expand_iter(sclrprdct)(BX.mv.args[i]<BX.mv.args[i+1])
          if t1:
            return gmul(*t1)*cf*coeff
          else :
            return coeff*cf
      return expr
    else :
      return expr 

  else :
    return expr

def gmulsimp():
  gmul.gsimplify = gmul_simp
