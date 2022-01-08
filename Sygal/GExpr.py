from operator import inv
from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union
from collections import Iterable,defaultdict
from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,sympify,
  symbols, sqrt, Matrix,srepr,bottom_up
)
from sympy.strategies.tools import subs as strtSubs

# from sympy.core.decorators import call_highest_priority, sympify_return


class GExpr(Expr):

  is_atom:bool = False
  name = "zzzzzGExpr"
  initialized:bool = False

  @property
  def is_commutative(expr) -> bool:
    return expr.grade == {0}

  def __add__(self:"GExpr", A:"GExpr") -> "GExpr":
    return gadd(self, A)

  def __radd__(self:"GExpr", A:"GExpr") -> "GExpr":
    return gadd(A, self)

  def __sub__(self:"GExpr", A:"GExpr") -> "GExpr":
    return gadd(self,gmul(A,-1))

  def __rsub__(self:"GExpr", A:"GExpr") -> "GExpr":
    return gadd(A,gmul(self,-1))

  def __mul__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # * geometric product
    return gmul(self, dopr)

  def __rmul__(self:"GExpr", dopl:"GExpr") -> "GExpr":  # * geometric product
    return gmul(self,dopl)

  def __xor__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # ^ outer product
    return gextp(self,dopr)

  def __rxor__(self:"GExpr", dopl:"GExpr") -> "GExpr":  # ^ outer product
    return gextp(dopl,self)

  def __lt__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # < left contraction
    return glcntrct(self, dopr)

  def __gt__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # > right contraction
    return grcntrct(self, dopr)

  def __or__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # | inner product
    return sclrprdct(self, dopr)

  def __ror__(self:"GExpr", dopl:"GExpr") -> "GExpr":  # | inner product
    return sclrprdct(dopl,self)

  def __lshift__(self:"GExpr", A:"GExpr") -> "GExpr":  # anti-comutator (<<)
    return ganticomm(self, A)

  def __rshift__(self:"GExpr", A:"GExpr") -> "GExpr":  # comutator (>>)
    return gcomm(self, A)

  def __rlshift__(self:"GExpr", A:"GExpr") -> "GExpr":  # anti-comutator (<<)
    return ganticomm(A, self)
  
  def __rrshift__(self:"GExpr", A:"GExpr") -> "GExpr":  # comutator (>>)
    return gcomm(A,self)

  def __pow__(self:"GExpr",power:int):
    power1 = sympify(power)
    t = []
    
    if power1.is_Integer:
      if power1 >= S(0):
        t.append(self)
        t1 = t*power1
        t2 = gmul(*t1)
        return t2
      else:
        raise ValueError("Exponent must be >=0")
    else:
      raise ValueError("Illegal Exponent")


  ###########################
  @property
  def pSC(self:"GExpr") -> set:
    t = set()
    for spdt in self.mtDt:
      for k,v in spdt.items():
        t.add(k)
    return t

  @property
  def grade(self:"GExpr") -> set:
    t = set()
    for spdt in self.mtDt:
      t1 = 0
      for k,v in spdt.items():
        t1 += v.value
      t.add(t1)
    return t

  
  reversion = lambda x:x
  grade_involution = lambda x:x
  clifford_conjugation = lambda x:x
  

  gsimplify = lambda x:x

  gexpand = lambda x:x

  ghigher = lambda x:x
  ###########################

  def sSubs(self:"GExpr", args):
    raise NotImplemented
    # def replace(old,new):
    #   if new is None:
    #     exprlst.remove(old)
    #   else:
    #     for index, item in enumerate(exprlst):
	  #       if item == old:
		#         exprlst[index] = new

    # exprlst = list(self.args)
    # if isinstance(args,list):

    #   for elem in args:
    #     replace(*elem)
    #   rv = self.func(*tuple(exprlst))
    #   return rv
      
    # elif isinstance(args,tuple):
    #   replace(*args)
    #   rv = self.func(*tuple(exprlst))
    #   return rv
    # else :
    #   raise

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
  
  # # Definitions links inside GExpr
  # @staticmethod
  # def inversion() -> "GExpr":
  #   return  ginversion
  
  # @staticmethod
  # def rejection() -> "GExpr":
  #   return  grejection
  # @staticmethod
  # def projection() -> "GExpr":
  #   return  gprojection

  # @staticmethod
  # def isomorphic() -> "GExpr":
  #   return  gisomorphic

  # @staticmethod
  # def outermorphic() -> "GExpr":
  #   return  goutermorphic




from libs.Sygal.operators.assop.gadd import gadd
from libs.Sygal.operators.assop.gextp import gextp
from libs.Sygal.operators.assop.gmul import gmul

from libs.Sygal.operators.binop.ganticomm import ganticomm
from libs.Sygal.operators.binop.gcomm import gcomm
from libs.Sygal.operators.binop.sclrprdct import sclrprdct
from libs.Sygal.operators.binop.grcntrct import grcntrct
from libs.Sygal.operators.binop.glcntrct import glcntrct

from libs.Sygal.operators.binop.outermorphic.outermorphic import outermorphic
from libs.Sygal.operators.binop.outermorphic.projection import projection 
from libs.Sygal.operators.binop.outermorphic.rejection import rejection  

from libs.Sygal.operators.binop.outermorphic.isomorphic.isomorphic import isomorphic
from libs.Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion  

from libs.Sygal.operators.binop.outermorphic.isomorphic.transforms.dilation import dilation 
from libs.Sygal.operators.binop.outermorphic.isomorphic.transforms.translation import translation 
from libs.Sygal.operators.binop.outermorphic.isomorphic.transforms.rotation import rotation