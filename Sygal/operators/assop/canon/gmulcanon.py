from Sygal.imports.import1head import *
from Sygal.imports.import1tail import *
from Sygal.operators.assop.gadd import gadd
from Sygal.operators.assop.gextp import gextp
from Sygal.operators.assop.gmul import gmul

from Sygal.operators.binop.ganticomm import ganticomm
from Sygal.operators.binop.gcomm import gcomm
from Sygal.operators.binop.sclrprdct import sclrprdct
from Sygal.operators.binop.grcntrct import grcntrct
from Sygal.operators.binop.glcntrct import glcntrct
from Sygal.imports.import_util2 import *

from Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion
from Sygal.operators.binop.outermorphic.projection import projection
from Sygal.operators.binop.outermorphic.rejection import rejection


# Assuming blade*blade = scalar

def gmul_canon(expr:"gmul")->Optional[GExpr]:
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

def gmulcanon():
  gmul.gcanonicalization = gmul_canon
