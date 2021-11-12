from libs.Sygal.imports.import1head import *
from libs.Sygal.imports.import1tail import *

from libs.Sygal.operators.assop.gmul import gmul
from libs.Sygal.operators.binop.outermorphic.isomorphic.isomorphic import isomorphic

def isomorphicExpander(expr):
  if (type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if(type(BX.mv.up)==gmul):
      new = type(BX.mv)
      t = [new(BX.mv.down,arg) for arg in BX.mv.up.args]
      return Box.__new__(Box,gmul(*t),cf)
    else :
      return expr
  else :
    return expr

def isomorphicexpand():
  isomorphic.gexpand = isomorphicExpander