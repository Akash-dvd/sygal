from libs.Sygal.imports.import1head import *
from libs.Sygal.imports.import1tail import *
from libs.Sygal.GExpr import GExpr
from libs.Sygal.operators.binop.binop import binop
from libs.Sygal.operators.assop.gextp import gextp


class outermorphic(binop):
  pass

from libs.Sygal.operators.binop.outermorphic.expand.outermorphicexpand import outermorphicexpand

outermorphicexpand()