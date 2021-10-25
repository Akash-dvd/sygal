from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,sympify,
  symbols, sqrt, Matrix,srepr,bottom_up
)
from sympy.strategies.tools import subs as strtSubs

from libs.Sygal.GExpr import GExpr


class Box(GExpr):

  # def __new__(cls,mv:"GExpr"=S(1),coeff:Expr=S(1))->"Box":
  #   # Pattern matching for types
  #   fct1 = issubclass(type(mv),GExpr)
  #   # fct2 is for scalar multivectors
  #   fct2 = True if fct1 and (mv.grade == {0}) else False
  #   fct3 = issubclass(type(mv),Box)


  #   if fct3:
  #     return GExpr.__new__(Box,mv.mv,Mul(coeff,mv.coeff).simplify())
  #   elif fct2:
  #     return GExpr.__new__(Box,GExpr.nl,Mul(coeff,mv).simplify())
  #   elif fct1:
  #     return GExpr.__new__(Box,mv,coeff)
  #   else :
  #     # Here only mv is supplied as scalar
  #     if(coeff!=S(1)):
  #       raise
  #     return GExpr.__new__(Box,GExpr.nl,sympify(mv))

  def __new__(cls,mv:"GExpr"=S(1),coeff:Expr=S(1))->"Box":
    if(type(coeff)==Box):
      raise ValueError
    

    # Pattern matching for types
    fct1 = issubclass(type(mv),GExpr)
    # fct2 is for scalar multivectors
    fct2 = True if fct1 and (mv.grade == {0}) else False
    fct3 = issubclass(type(mv),Box)
    fct4 = fct3 and fct2
    
    new = GExpr.__new__
    
    if fct4:
      BX = mv
      # Here well formed Box must have nl as mv
      if(BX.mv!=GExpr.nl):
        raise
      return new(Box,GExpr.nl,Mul(coeff,BX.coeff))
    elif fct3:
      BX = mv
      # Check if the arrived box encloses gadd
      if(type(BX.mv)==gadd):
        # Well formed gadd box always has S(1) coeff
        if(BX.coeff!=S(1)):
          raise
        t = [new(Box,bx.mv,Mul(bx.coeff,coeff)) for bx in BX.mv.args]
        return new(Box,new(gadd,*t),S(1))
      else:
        return new(Box,BX.mv,Mul(coeff,BX.coeff))
    
    # Not box mvs
    # Zero grade
    elif fct2:
      # NO need to check for gadd
      if(mv == GExpr.nl):
        return new(Box,GExpr.nl,coeff)
      else:
        return new(Box,GExpr.nl,Mul(mv,coeff))
    # Non Zero grade
    elif fct1:
      if(type(mv)==gadd):
        # t = [new(Box,bx.mv,Mul(bx.coeff,coeff).simplify()) for bx in mv.args]
        t = [new(Box,bx.mv,Mul(bx.coeff,coeff)) for bx in mv.args]
        return new(Box,new(gadd,*t),S(1))
      else:
        return new(Box,mv,coeff)
    
    # Scalars boxing
    else :
      # Here only mv is supplied as scalar
      if(coeff!=S(1)):
        raise
      return new(Box,GExpr.nl,sympify(mv))

  
  def __str__(self:"Box") -> str:
    strcf = self.coeff.__str__()
    strmv = self.mv.__str__()
    if self.coeff == S(1):
      istr = ""
      lstr = ""
      str1 = ""
    else :
      str1 = "["+strcf+"]"+"*" 
      istr = "("
      lstr = ")"
    if __debug__:
      str = "|B|"+istr+str1+strmv+lstr
    else:
      str = istr+str1+strmv+lstr
    return str

  __repr__ = __str__

  def __hash__(self:"Box")->int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h

  def __eq__(self:"Box", other:"Box")->Tuple[bool]:
    # returns a tuple of values (#,#) 
    # ( cf, mv )
    return (
      other.__hash__() == self.__hash__() and
      other.__class__ == self.__class__
    )

  def __eq1__(self:"Box", other:"Box")->Tuple[bool]:
    # returns a tuple of values (#,#) 
    # ( cf, mv )
    return (
      (other.coeff == self.coeff and
      other.__class__ == self.__class__),
      (other.mv == self.mv and
      other.__class__ == self.__class__)
    )

  def __neg__(self:"Box")->"Box":
    return Box.__new__(Box,mv=self.mv,coeff=Mul(self.coeff,S(-1)))

  @property
  def grade(self:"Box") -> set:
    return self.mv.grade

  @property
  def pSC(self:"Box") -> "GExpr":
    return self.mv.pSC

  @property
  def coeff(self:"Box") -> "GExpr":
    return self.args[1]
  
  @property
  def mv(self:"Box") -> "GExpr":
    return self.args[0]

  def gsimplify(self:"Box"):
    return self.mv.gsimplify()

  def gexpand(self:"Box"):
    return Box.__new__(Box,self.mv.gexpand(),self.coeff)

  def ghigher(self:"Box"):
    return self.mv.ghigher()
# Standard import style
from libs.Sygal.operators.assop.gadd import gadd
# Non standard style
# from libs.Sygal.operators import (gadd,ganticomm,gcomm,gextp,ginprdct,glcntrct,gmul,grcntrct)
