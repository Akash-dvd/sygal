from libs.Sygal.imports.import1head import *
from libs.Sygal.imports.import1tail import *

from libs.Sygal.operators.assop.gextp import gextp
from libs.Sygal.operators.binop.outermorphic.outermorphic import outermorphic

def outermorphicExpander(expr):
  if (type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if(type(BX.mv.up)==gextp):
      new = type(BX.mv)
      t = [new(BX.mv.down,arg) for arg in BX.mv.up.args]
      return Box.__new__(Box,gextp(*t),cf)
    else :
      return expr
  else :
    return expr

def outermorphicexpand():
  outermorphic.gexpand = outermorphicExpander