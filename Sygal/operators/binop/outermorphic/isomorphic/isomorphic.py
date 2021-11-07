from libs.Sygal.GExpr import GExpr
from libs.Sygal.operators.binop import binop
from libs.Sygal.operators.binop.outermorphic.outermorphic import outermorphic

from libs.Sygal.operators.assop.gmul import gmul

class isomorphic(outermorphic):
  def isomorphicExpander(expr):
    if(type(expr.up)==gmul):
      new = type(expr)
      t = [new(expr.down,arg) for arg in expr.up.args]
      return gmul(*t)
    else :
      return expr
  
  def isometricExpander(expr):
    pass