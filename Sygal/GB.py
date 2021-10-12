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

  def __new__(cls, args0:str,args1:set,args2:Expr=S(1), **assumptions) -> "Box":
    # args0 = name .args1 = grade set , args2 = coeff
    # Put a check on set length
    
    # null grade zero element is unique
    if(args1=={0}):
      args0 = "_nl"


    nargs = (args0,args1,args2)
      
    return GB.__xnew_cached_(GB, *nargs, **assumptions)
    # return GB.__new_stage2__(GB, *nargs, **assumptions)
    

  def __new_stage2__(cls, *args, **assumptions) -> "GB":
    if not isinstance(args[0], str):
      raise TypeError("name should be a string, not %s" % repr(type(args[0])))
    if not isinstance(args[1], frozenset):
      raise TypeError("grade should be a frozenset in GB, not %s" % repr(type(args[1])))
    
    mv = GExpr.__new__(cls)
    mv.name = args[0]
    mv.is_commutative = (args[1] == {0})
    mv.is_atom = True
    mv.grade = args[1]

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
