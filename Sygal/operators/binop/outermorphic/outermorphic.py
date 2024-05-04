from Sygal.imports.import1head import *
from Sygal.imports.import1tail import *
from Sygal.GExpr import GExpr
from Sygal.operators.binop.binop import binop
from Sygal.operators.assop.gextp import gextp


class outermorphic(binop):
  pass

from Sygal.operators.binop.outermorphic.expand.outermorphicexpand import outermorphicexpand

outermorphicexpand()