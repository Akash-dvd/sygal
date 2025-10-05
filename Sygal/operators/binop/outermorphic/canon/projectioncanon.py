# Perpendicular and parallel
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


def projection_canon(expr:Box)->Optional[Box]:
  if (type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == projection:
      sub = BX.mv.down
      obj = BX.mv.up
      if is_perpendicularPair(obj,sub):
        return GExpr.Znl
      else :
        return expr
    else :
      return expr
  else :
    return expr

def projectioncanon():
  projection.gcanonicalization = exhaust(do_one(projection_canon,))