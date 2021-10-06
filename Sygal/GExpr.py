from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,
  symbols, sqrt, Matrix,srepr,bottom_up
)
from sympy.strategies.tools import subs as strtSubs

# from sympy.core.decorators import call_highest_priority, sympify_return


import sys, os
# print(sys.path)

_K = TypeVar('_K')
_V = TypeVar('_V')

# a = GV(1)

# class GMV(Basic):
class GExpr(Expr):
  
  grade:set = {}
  is_atom:bool = False
  __slots__ = ()
  coeffs:List["GExpr"] = [S(1)]

  def __add__(self:"GExpr", A:"GExpr") -> "GExpr":
    return add(self, A)

  def __radd__(self:"GExpr", A:"GExpr") -> "GExpr":
    return add(A, self)

  def __sub__(self:"GExpr", A:"GExpr") -> "GExpr":
    return add(self,mul(A,-1))

  def __rsub__(self:"GExpr", A:"GExpr") -> "GExpr":
    return add(A,mul(self,-1))

  def __mul__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # * geometric product
    return mul(self, dopr)

  def __rmul__(self:"GExpr", dopl:"GExpr") -> "GExpr":  # * geometric product
    return mul(dopl,self)

  def __xor__(self:"GExpr", dopr:"GExpr") -> "extp":  # ^ outer product
    return extp(self,dopr)

  def __rxor__(self:"GExpr", dopl:"GExpr") -> "extp":  # ^ outer product
    return extp(dopl,self)

  def __lt__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # < left contraction
    return lcntrct(self, dopr)

  def __gt__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # > right contraction
    return rcntrct(self, dopr)

  def __or__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # | inner product
    return inprdct(self, dopr)

  def __ror__(self:"GExpr", dopl:"GExpr") -> "GExpr":  # | inner product
    return inprdct(dopl,self)

  def __lshift__(self:"GExpr", A:"GExpr") -> "GExpr":  # anti-comutator (<<)
    return anticomm(self, A)

  def __rshift__(self:"GExpr", A:"GExpr") -> "GExpr":  # comutator (>>)
    return comm(self, A)

  def __rlshift__(self:"GExpr", A:"GExpr") -> "GExpr":  # anti-comutator (<<)
    return anticomm(A, self)
  
  def __rrshift__(self:"GExpr", A:"GExpr") -> "GExpr":  # comutator (>>)
    return comm(A,self)

  def sSubs(self:"GExpr", args):
    def replace(old,new):
      if new is None:
        exprlst.remove(old)
      else:
        for index, item in enumerate(exprlst):
	        if item == old:
		        exprlst[index] = new

    exprlst = list(self.args)
    if isinstance(args,list):

      for elem in args:
        replace(*elem)
      rv = self.func(*tuple(exprlst))
      return rv
      
    elif isinstance(args,tuple):
      replace(*args)
      rv = self.func(*tuple(exprlst))
      return rv
    else :
      raise

  def subs(self:"GExpr",map) -> "GExpr":
    if isinstance(map,list):
      for old,new in map:
        expr = strtSubs({old:new})(self)
        expr1 = expr.func(*expr.args)
      return expr1
      
    elif isinstance(map,tuple):
      old,new = map
      expr = strtSubs({old:new})(self)
      expr1 = expr.func(*expr.args)
      # expression needs to be rebui;d
      return expr1
    else :
      raise

from libs.Sygal.operators import (add,anticomm,comm,extp,
inprdct,lcntrct,mul,rcntrct)