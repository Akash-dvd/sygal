from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,
  symbols, sqrt, Matrix,srepr,bottom_up
)
from sympy.strategies.tools import subs as strtSubs

# from sympy.core.decorators import call_highest_priority, sympify_return


class GExpr(Expr):
  
  grade:Union[set,frozenset] = {}
  is_commutative:bool = False
  is_atom:bool = False
  __slots__ = ()
  coeffs:List["GExpr"] = [S(1)]
  name = "zzzzzGExpr"
  initialized:bool = False

  # Both are boxes
  @property
  def Onl(self):
    from libs.Sygal.GB import GB
    return GB("_nl",frozenset({0})) 
  
  @property
  def Znl(self):
    from libs.Sygal.GB import GB
    return GB("_nl",frozenset({0}),S(0))
  
  @property
  def nl():
    from libs.Sygal.GB import GB
    return GB("_nl",frozenset({0})).args[1]
 
  @property
  def oo():
    return GExpr.prim[1]

  @property
  def rx():
    return GExpr.prim[4]

  @property
  def I3():
    from libs.Sygal.GV import GV
    return GV._I3

  @property
  def I41():
    from libs.Sygal.GV import GV
    return GV._I41

  @property
  def I42():
    from libs.Sygal.GV import GV
    return GV._I42

  @property
  def I5():
    from libs.Sygal.GV import GV
    return GV._I5

  @property
  def I8():
    from libs.Sygal.GV import GV
    return GV._I8

  @property
  def I13():
    from libs.Sygal.GV import GV
    return GV._I13


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
    return gmul(dopl,self)

  def __xor__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # ^ outer product
    return gextp(self,dopr)

  def __rxor__(self:"GExpr", dopl:"GExpr") -> "GExpr":  # ^ outer product
    return gextp(dopl,self)

  def __lt__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # < left contraction
    return glcntrct(self, dopr)

  def __gt__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # > right contraction
    return grcntrct(self, dopr)

  def __or__(self:"GExpr", dopr:"GExpr") -> "GExpr":  # | inner product
    return ginprdct(self, dopr)

  def __ror__(self:"GExpr", dopl:"GExpr") -> "GExpr":  # | inner product
    return ginprdct(dopl,self)

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

from libs.Sygal.operators import (gadd,ganticomm,gcomm,gextp,
ginprdct,glcntrct,gmul,grcntrct)

