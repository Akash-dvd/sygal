from .importshead1 import *

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
