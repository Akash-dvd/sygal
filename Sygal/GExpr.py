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
  
  grade = []
  is_atom = False
  __slots__ = ()

  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __add__(self, A):
    return add(self, A)

  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __radd__(self, A):
    return add(A, self)

  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __sub__(self, A):
    return add(self,mul(A,-1))

  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __rsub__(self, A):
    return add(A,mul(self,-1))

  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __mul__(self, dopr):  # * geometric product
    return mul(self, dopr)

  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __rmul__(self, dopl):  # * geometric product
    return mul(dopl,self)

  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __xor__(self, dopr):  # ^ outer product
    return extp(self,dopr)

  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __rxor__(self, dopl):  # ^ outer product
    return extp(dopl,self)

  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __lt__(self, dopr):  # < left contraction
    return lcntrct(self, dopr)

  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __gt__(self, dopr):  # > right contraction
    return rcntrct(self, dopr)

  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __or__(self, dopr):  # | inner product
    return inprdct(self, dopr)

  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __ror__(self, dopl):  # | inner product
    return inprdct(dopl,self)

  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __lshift__(self, A):  # anti-comutator (<<)
    return anticomm(self, A)

  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __rshift__(self, A):  # comutator (>>)
    return comm(self, A)

  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __rlshift__(self, A):  # anti-comutator (<<)
    return anticomm(A, self)
  
  # @sympify_return([('other', 'Expr')], NotImplemented)
  def __rrshift__(self, A):  # comutator (>>)
    return comm(A,self)

  def sSubs(self, args):
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

  def subs(self,map):
    if isinstance(map,list):
      for old,new in map:
        self = strtSubs({old:new})(self)
      return self
      
    elif isinstance(map,tuple):
      old,new = map
      self = strtSubs({old:new})(self)
      return self
    else :
      raise

from libs.Sygal.operators import (add,anticomm,comm,extp,
inprdct,lcntrct,mul,rcntrct)