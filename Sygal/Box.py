import sys

from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,sympify,
  symbols, sqrt, Matrix,srepr,bottom_up
)
from sympy.strategies.tools import subs as strtSubs

from sympy.printing.str import StrPrinter

from libs.Sygal.GExpr import GExpr


def is_devmode():
  t = 'pydevd' in sys.modules
  return t


class Box(GExpr):

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

  def sympystr(self,expr:"Box") -> str:
    return str(expr)

  def sympyrepr(self,expr:"Box") -> str:
    return repr(expr)
  
  def __str__(self:"Box") -> str:
    strcf = self.coeff.__str__()
    strmv = self.mv.__str__()
    istr = "\033[1;37;40m[\033[0;37;40m"
    mstr = "\033[1;36;40m!\033[0;37;40m"
    lstr = "\033[1;37;40m]\033[0;37;40m"

    if self.coeff == S(1):
      strcf = ""
      mstr = ""

    str = istr+strcf+mstr+strmv+lstr
    return str
  
  def __repr__(self:"Box") -> str:
    strcf = self.coeff.__repr__()
    strmv = self.mv.__repr__()
    istr = "["
    mstr = "!"
    lstr = "]"
    if self.coeff == S(1):
      strcf = ""
      mstr = ""
    str = istr+strcf+mstr+strmv+lstr
    return str

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
    func = type(self.mv).gsimplify
    return func(self)

  def gexpand(self:"Box"):
    func = type(self.mv).gexpand
    return func(self)

  def ghigher(self:"Box"):
    func = type(self.mv).ghigher
    return func(self)

  def reversion(self:"Box")->"Box":
    t = self.mv.reversion()
    return Box.__new__(Box,t,self.coeff)

  def grade_involution(self:"Box")->"Box":
    t = self.mv.grade_involution()
    return Box.__new__(Box,t,self.coeff)
  
  def clifford_conjugation(self:"Box")->"Box":
    t = self.mv.clifford_conjugation()
    return Box.__new__(Box,t,self.coeff)
  
# Standard import style
# These extra imports cause issue with strategies import
from libs.Sygal.operators.assop.gadd import gadd
# from libs.Sygal.operators.assop.gextp import gextp
# from libs.Sygal.operators.assop.gmul import gmul

# from libs.Sygal.operators.binop.ganticomm import ganticomm
# from libs.Sygal.operators.binop.gcomm import gcomm
# from libs.Sygal.operators.binop.sclrprdct import sclrprdct
# from libs.Sygal.operators.binop.grcntrct import grcntrct
# from libs.Sygal.operators.binop.glcntrct import glcntrct



if is_devmode():
  StrPrinter._print_Box = Box.sympyrepr
else :
  StrPrinter._print_Box = Box.sympystr
