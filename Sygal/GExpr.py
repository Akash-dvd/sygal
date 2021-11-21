from operator import inv
from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union
from collections import Iterable,defaultdict
from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,
  symbols, sqrt, Matrix,srepr,bottom_up
)
from sympy.strategies.tools import subs as strtSubs

# from sympy.core.decorators import call_highest_priority, sympify_return


class GExpr(Expr):
  
  grade:Union[set,frozenset] = {}

  is_atom:bool = False
  __slots__ = ()
  coeffs:List["GExpr"] = [S(1)]
  name = "zzzzzGExpr"
  initialized:bool = False

  dotdict = defaultdict(lambda:None)

  @property
  def is_commutative(expr) -> bool:
    return expr.grade == {0}

  reversion = lambda x:x
  grade_involution = lambda x:x
  clifford_conjugation = lambda x:x
  
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
  
  # Definitions links inside GExpr
  @staticmethod
  def inversion() -> "GExpr":
    return  ginversion
  
  @staticmethod
  def rejection() -> "GExpr":
    return  grejection
  @staticmethod
  def projection() -> "GExpr":
    return  gprojection

  @staticmethod
  def isomorphic() -> "GExpr":
    return  gisomorphic

  @staticmethod
  def outermorphic() -> "GExpr":
    return  goutermorphic

  
  gsimplify = lambda x:x

  # @classmethod
  # def gexpand(expr):
  #   return expr
  gexpand = lambda x:x

  ghigher = lambda x:x

  # gdistribute = lambda x:x
  # def gsimplify(self):
  #   return gsimplification(self)


from libs.Sygal.operators.assop.gadd import gadd
from libs.Sygal.operators.assop.gextp import gextp
from libs.Sygal.operators.assop.gmul import gmul

from libs.Sygal.operators.binop.ganticomm import ganticomm
from libs.Sygal.operators.binop.gcomm import gcomm
from libs.Sygal.operators.binop.sclrprdct import sclrprdct
from libs.Sygal.operators.binop.grcntrct import grcntrct
from libs.Sygal.operators.binop.glcntrct import glcntrct

from libs.Sygal.operators.binop.outermorphic.outermorphic import outermorphic
from libs.Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion as ginversion
from libs.Sygal.operators.binop.outermorphic.projection import projection as gprojection
from libs.Sygal.operators.binop.outermorphic.rejection import rejection as grejection 

from libs.Sygal.operators.binop.outermorphic.isomorphic.isomorphic import isomorphic as gisomorphic
from libs.Sygal.operators.binop.outermorphic.outermorphic import outermorphic as goutermorphic


# This style causes errors
# from libs.Sygal.operators import (gadd,ganticomm,gcomm,gextp,ginprdct,glcntrct,gmul,grcntrct)

# from libs.Sygal.operators.hdef import hdef,inversion as ginversion,projection as gprojection,rejection as grejection