from libs.Sygal.GExpr import GExpr
from libs.Sygal.operators.binop.binop import binop
from libs.Sygal.operators.assop.gextp import gextp


class outermorphic(binop):
  def outermorphicExpander(expr):
    if(type(expr.up)==gextp):
      new = type(expr)
      t = [new(expr.down,arg) for arg in expr.up.args]
      return gextp(*t)
    else :
      return expr