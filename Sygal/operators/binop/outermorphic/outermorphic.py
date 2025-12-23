# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.operators.binop.binop import binop


class outermorphic(binop):
  pass

from Sygal.operators.binop.outermorphic.expand.outermorphicexpand import outermorphicexpand

outermorphicexpand()