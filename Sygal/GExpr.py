from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union, TYPE_CHECKING
from collections.abc import Iterable
from collections import defaultdict
from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,sympify,
  symbols, sqrt, Matrix,srepr,bottom_up,
)
from sympy.strategies.tools import subs as strtSubs
from sympy.strategies.rl import rebuild

# from sympy.core.decorators import call_highest_priority, sympify_return

if TYPE_CHECKING:
    from Sygal.operators.assop.gadd import gadd
    from Sygal.operators.assop.gextp import gextp
    from Sygal.operators.assop.gmul import gmul
    from Sygal.operators.binop.ganticomm import ganticomm
    from Sygal.operators.binop.gcomm import gcomm
    from Sygal.operators.binop.sclrprdct import sclrprdct
    from Sygal.operators.binop.grcntrct import grcntrct
    from Sygal.operators.binop.glcntrct import glcntrct


class GExpr(Expr):

  is_atom:bool = False
  name = "zzzzzGExpr"
  initialized:bool = False

  @property
  def is_commutative(expr) -> bool:
    return expr.grade == {0}

  def __add__(self:"GExpr", A:"GExpr") -> "GExpr":
    from Sygal.operators.assop.gadd import gadd
    return gadd(self, A)

  def __radd__(self:"GExpr", A:"GExpr") -> "GExpr":
    from Sygal.operators.assop.gadd import gadd
    return gadd(A, self)

  def __sub__(self:"GExpr", A:"GExpr") -> "GExpr":
    from Sygal.operators.assop.gadd import gadd
    from Sygal.operators.assop.gmul import gmul
    return gadd(self,gmul(A,-1))

  def __rsub__(self:"GExpr", A:"GExpr") -> "GExpr":
    from Sygal.operators.assop.gadd import gadd
    from Sygal.operators.assop.gmul import gmul
    return gadd(A,gmul(self,-1))

  def __mul__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # * geometric product
    from Sygal.operators.assop.gmul import gmul
    return gmul(self, dopr)

  def __rmul__(self:"GExpr", dopl:"GExpr") -> "GExpr":  # * geometric product
    from Sygal.operators.assop.gmul import gmul
    return gmul(self,dopl)

  def __xor__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # ^ outer product
    from Sygal.operators.assop.gextp import gextp
    return gextp(self,dopr)

  def __rxor__(self:"GExpr", dopl:"GExpr") -> "GExpr":  # ^ outer product
    from Sygal.operators.assop.gextp import gextp
    return gextp(dopl,self)

  def __lt__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # < left contraction
    from Sygal.operators.binop.glcntrct import glcntrct
    return glcntrct(self, dopr)

  def __gt__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # > right contraction
    from Sygal.operators.binop.grcntrct import grcntrct
    return grcntrct(self, dopr)

  def __or__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # | inner product
    from Sygal.operators.binop.sclrprdct import sclrprdct
    return sclrprdct(self, dopr)

  def __ror__(self:"GExpr", dopl:"GExpr") -> "GExpr":  # | inner product
    from Sygal.operators.binop.sclrprdct import sclrprdct
    return sclrprdct(dopl,self)

  def __lshift__(self:"GExpr", A:"GExpr") -> "GExpr":  # anti-comutator (<<)
    from Sygal.operators.binop.ganticomm import ganticomm
    return ganticomm(self, A)

  def __rshift__(self:"GExpr", A:"GExpr") -> "GExpr":  # comutator (>>)
    from Sygal.operators.binop.gcomm import gcomm
    return gcomm(self, A)

  def __rlshift__(self:"GExpr", A:"GExpr") -> "GExpr":  # anti-comutator (<<)
    from Sygal.operators.binop.ganticomm import ganticomm
    return ganticomm(A, self)
  
  def __rrshift__(self:"GExpr", A:"GExpr") -> "GExpr":  # comutator (>>)
    from Sygal.operators.binop.gcomm import gcomm
    return gcomm(A,self)

  def __pow__(self:"GExpr",power:int):
    from Sygal.operators.assop.gmul import gmul
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

  # def sSubs(self:"GExpr", args):
  #   raise NotImplemented
  #   # def replace(old,new):
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

    if isinstance(map,dict):
      expr = strtSubs(map)(self)
      expr1 = rebuild(expr)
      # expr1 = expr.func(*expr.args)
      return expr1
    else :
      raise  

    #   for old,new in map.items:
    #     expr = strtSubs({old:new})(self)
    #     expr1 = expr.func(*expr.args)
    #   return expr1
    
    # elif isinstance(map,list):
    #   for old,new in map:
    #     expr = strtSubs({old:new})(self)
    #     expr1 = expr.func(*expr.args)
    #   return expr1
      
    # elif isinstance(map,tuple):
    #   old,new = map
    #   expr = strtSubs({old:new})(self)
    #   expr1 = expr.func(*expr.args)
    #   # expression needs to be rebui;d
    #   return expr1
    # else :
    #   raise