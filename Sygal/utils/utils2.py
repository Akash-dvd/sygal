from sympy.core.compatibility import iterable
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

def appendtoDict(eleBX,dict):
  for k,v in dict.items():
    if type(k) == Box:
      eleBX.dotdict[k.mv] = v
    elif issubclass(k,GExpr):
      eleBX.dotdict[k] = v
    else :
      raise NotImplemented


def is_vecPerpendicularPair(args0:Union[Expr,GExpr],args1:Union[Expr,GExpr])->bool:
  # vec can be gadd(a1,a2) also
  if(args0.grade == {1} and args1.grade == {1}):
    t = sclrprdct(args0,args1)
    t1 = expand_iter(sclrprdct)(t)
    return t1 == GExpr.Znl
  else :
    return False

def is_perpendicularPair(args0:Union[Expr,GExpr],args1:Union[Expr,GExpr])->bool:
  t = args0*args1
  t1 = expand_iter(gmul)(t)
  if t1.grade == {0}:
    return t1.coeff == S(0)
  else:
    return False

def is_vecnull(expr:Union[Expr,GExpr])->bool:
  if expr.grade == {1}:
    t = sclrprdct(expr,expr)
    t1 = t.gexpand()
    return t1 == GExpr.Znl
  else :
    return False

def is_null(expr:Union[Expr,GExpr])->bool:
  if len(expr.grade) == 1:
    t = sclrprdct(expr,expr)
    t1 = t.gexpand()
    return t1 == GExpr.Znl
  else :
    return False

def is_invertiblePair(args0:Union[Expr,GExpr],args1:Union[Expr,GExpr])->bool:
  t = args0*args1
  t1 = expand_iter(gmul)(t)
  if t1.grade == {0}:
    return t1.coeff != S(0)
  else:
    return False

def is_invertible(expr:Union[Expr,GExpr])->bool:
  return True

def is_blade(expr:Union[Expr,GExpr])->bool:
  raise NotImplemented

def is_vecBlade(arg:Union[Expr,GExpr])->bool:
  # arguements must be either be of grade 1 or gextp each composed of grade 1 elements
  # Othercase is not implemented yet
  if(type(arg)==Box):
    expr = arg.mv
  else :
    expr = arg
  if expr.grade == {1}:
    return True
  elif type(expr) == gextp:
    return reduce(lambda x, y: x and y, [ele.grade == {1} for ele in expr.args])
  else :
    return False

def is_versor(arg:Union[Expr,GExpr])->bool:
  if(type(arg)==Box):
    expr = arg.mv
  else :
    expr = arg

  if is_blade(expr):
    return True
  elif type(expr) == gmul:
    return reduce(lambda x, y: x and y, [ele.grade == {1} for ele in expr.args])
  else :
    return False

def get_grade(expr:GExpr,r:Union[int,set,frozenset,List[int]]) -> Union[Expr,GExpr]:
  
  # Should check for negative grades ???

  if type(r) == int:
    grd = {r}
  elif isinstance(r, Iterable):
    grd = set(r)
  else:
    raise ValueError("Not supported Error")

  if issubclass(type(expr),GExpr):
    BX = GExpr.gdistribute(expr)
    

    if (BX.grade == grd):
      return BX
    elif(BX.mv.is_atom):
      if(BX.grade == grd):
        return BX
      else:
        return GExpr.Znl
    elif(type(BX.mv)==gadd):
      # BX.coeff will be S(1)
      t = [arg for arg in BX.mv if arg.grade in grd]
      return gadd(*t)
    else:
      return GExpr.Znl
  else :
    if 0 in grd:
      return expr
    else:
      return GExpr.Znl

  
