from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union


from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,
  symbols, sqrt, Matrix,srepr,AtomicExpr
)

from libs.Sygal.GExpr import GExpr
from libs.Sygal.Box import Box
from sympy.core.cache import cacheit

class GB(GExpr,AtomicExpr):
  # Symbolic Blade class
  # Returns Box with coeff and grade values

  def __new__(cls, args0:str,args1:Union[int,List[int],Tuple[int]],args2:GExpr=GExpr.I13,args3:Expr=S(1), **kwargs) -> "Box":
    # args0 = name .args1 = grade set ,args2 gextp, args3 = coeff
    # Put a check on set length
    
    # 

    # null grade zero element is unique
    if(args1=={0}):
      args0 = "_nl"


    # Pattern match for args2,args3
    if not issubclass(type(args2),GExpr):
      raise TypeError("coeff should be a gextp, not %s" % repr(type(args2)))

    if not issubclass(type(args3),Expr) or issubclass(type(args3),GExpr):
      raise TypeError("coeff should be a sympy obj, not %s" % repr(type(args3)))

   

    nargs = (args0,args1,args2,args3)
      
    return GB.__xnew_cached_(GB, *nargs, **kwargs)

    

  def __new_stage2__(cls, *args, **kwargs) -> "GB":
    # Pattern match for arguements
    # CAn be better with pattern matching
    if not isinstance(args[0], str):
      raise TypeError("name should be a string, not %s" % repr(type(args[0])))
    if isinstance(args[1],int):
      if(args[1]<0):
        return GExpr.Znl
      arg_grade = frozenset([args[1]])
    elif isinstance(args[1], list) or isinstance(args[1], Tuple):
      filtgrade = [i for i in args[1] if i>=0]
      if(len(filtgrade)==0):
        return GExpr.Znl
      arg_grade = frozenset(filtgrade)
    else :
      raise TypeError("grade should be int or list or tuple not %s" % repr(type(args[1])))
    
    mv = GExpr.__new__(cls)
    mv.name = args[0]
    mv.is_commutative = (arg_grade == {0})
    mv.is_atom = True
    mv.grade = arg_grade

    obj = Box.__new__(Box,mv,args[2])
    
    return obj

  __xnew__ = staticmethod(
    __new_stage2__)            # never cached (e.g. dummy)
  __xnew_cached_ = staticmethod(
    cacheit(__new_stage2__))   # symbols are always cached
  
  def __str__(self):
    return self.name
  __repr__ = __str__

  def __hash__(self):
    return hash(self.name)

  def __eq__(self, other):
    return (
      (type(other) == type(self))  and
      self.name == other.name
    )
