# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.imports.sympy_basic import Expr, S
from Sygal.imports.typing_helpers import Union, List, Iterable, reduce
from Sygal.imports.strategies import expand_iter

# Lazy import operators to avoid circular dependency
# Operators are imported inside functions where they're used
# This prevents KeyError: 'Sygal.operators' during module initialization

"""
USAGE --

ALLOWED    - PROJECTION, INVERSION, DILATION
NOTALLOWED - GMUL, GADD, GLCNTRCT ETC  
"""


# def appendtoDict(eleBX,dict):
#   if issubclass(type(eleBX),GExpr):
#     # Unbox
#     ele_mv = eleBX.mv if type(eleBX) == Box else eleBX
#     for k,v in dict.items():
#       if issubclass(type(k),GExpr):
#         # Unbox
#         k_mv = k.mv if type(k) == Box else k
#         ele_mv.dotdict[k_mv] = v
#         # Making symmetric changes
#         if k_mv.dotdict[ele_mv] == v:
#           continue
#         elif k_mv.dotdict[ele_mv] == None:
#           k_mv.dotdict[ele_mv] = v
#         else :
#           raise ValueError("Inrprdct Values unsymmetic")
#       else :
#         raise ValueError("Element must be from GExpr decent.")      
#   else :
#     raise ValueError("Element must be from GExpr decent.")

def is_vecPerpendicularPair(args0:Union[Expr,GExpr],args1:Union[Expr,GExpr])->bool:
  # vec can be gadd(a1,a2) also
  if(args0.grade == {1} and args1.grade == {1}):
    from Sygal.operators.binop.sclrprdct import sclrprdct
    t = sclrprdct(args0,args1)
    t1 = expand_iter(sclrprdct)(t)
    return t1 == GExpr.Znl
  else :
    return False

def is_perpendicularPair(args0:Union[Expr,GExpr],args1:Union[Expr,GExpr])->bool:
  from Sygal.operators.assop.gmul import gmul
  from Sygal.operators.binop.sclrprdct import sclrprdct
  t = args0*args1
  t1 = expand_iter(gmul)(t)
  t2 = sclrprdct.gexpand1(t1)
  if t2.grade == {0}:
    return t2.coeff == S(0)
  else:
    return False

def is_vecnull(expr:Union[Expr,GExpr])->bool:
  if expr.grade == {1}:
    from Sygal.operators.binop.sclrprdct import sclrprdct
    t = sclrprdct(expr,expr)
    t1 = t.gexpand()
    return t1 == GExpr.Znl
  else :
    return False

def is_null(expr:Union[Expr,GExpr])->bool:
  if len(expr.grade) == 1:
    from Sygal.operators.binop.sclrprdct import sclrprdct
    t = sclrprdct(expr,expr)
    t1 = t.gexpand()
    return t1 == GExpr.Znl
  else :
    return False

def is_nzScalarPair(args0:Union[Expr,GExpr],args1:Union[Expr,GExpr])->bool:
  from Sygal.operators.assop.gmul import gmul
  from Sygal.operators.binop.sclrprdct import sclrprdct
  t = args0*args1
  t1 = expand_iter(gmul)(t)
  t2 = sclrprdct.gexpand1(t1)
  if t2.grade == {0}:
    return t2.coeff != S(0)
  else:
    return False

def is_scalarPair(args0:Union[Expr,GExpr],args1:Union[Expr,GExpr])->bool:
  from Sygal.operators.assop.gmul import gmul
  from Sygal.operators.binop.sclrprdct import sclrprdct
  t = args0*args1
  t1 = expand_iter(gmul)(t)
  t2 = sclrprdct.gexpand1(t1)
  if t2.grade == {0}:
    return True

def is_blade(expr:Union[Expr,GExpr])->bool:
  raise NotImplementedError

def is_vecBlade(arg:Union[Expr,GExpr])->bool:
  # arguements must be either be of grade 1 or gextp each composed of grade 1 elements
  # Othercase is not implemented yet
  from Sygal.Box import Box
  from Sygal.operators.assop.gextp import gextp
  if issubclass(type(arg),GExpr):
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
  else :
    return False

def is_versor(arg:Union[Expr,GExpr])->bool:
  from Sygal.Box import Box
  from Sygal.operators.assop.gmul import gmul
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
    
    # Lazy import to avoid circular dependency
    from Sygal.operators.assop.gadd import gadd

    if (BX.grade == grd):
      return BX
    elif(BX.mv.is_atom):
      if(BX.grade == grd):
        return BX
      else:
        return GExpr.Znl
    elif(type(BX.mv)==gadd):
      # BX.coeff will be S(1)
      t = [arg for arg in BX.mv.args if arg.grade in grd]
      if t:
        return gadd(*t)
      else : 
        return GExpr.Znl
    else:
      return GExpr.Znl
  else :
    if 0 in grd:
      return expr
    else:
      return GExpr.Znl

  
