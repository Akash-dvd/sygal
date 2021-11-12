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

def is_invertible(expr):
  return True

def is_blade(expr):
  # arguements must be either be of grade 1 or gextp each composed of grade 1 elements
  # Othercase is not implemented yet
  if expr.grade == {1}:
    return True
  elif type(expr) == gextp:
    return reduce(lambda x, y: x and y, [ele.grade == {1} for ele in expr.args])
  else :
    return False
