from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,
  symbols, sqrt, Matrix,srepr,bottom_up
)
from sympy.strategies.tools import subs as strtSubs

from libs.Sygal.GExpr import GExpr

# from sympy.core.decorators import call_highest_priority, sympify_return

class Box(GExpr):

  def __new__(cls,mv:"GExpr",coeff:Expr=S(1))->"Box":
    obj = GExpr.__new__(Box,coeff,mv)

    return obj
  
  
  def __str__(self:"Box") -> str:
    strcf = self.args[0].__str__()
    strmv = self.args[1].__str__()
    if self.args[0] == S(1):
      istr = ""
      lstr = ""
      str1 = ""
    else :
      str1 = "{"+strcf+"}"+"*" 
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
      other.args[1] == self.args[1] and
      other.__class__ == self.__class__
    )

  def __eq1__(self:"Box", other:"Box")->Tuple[bool]:
    # returns a tuple of values (#,#) 
    # ( cf, mv )
    return (
      (other.args[0] == self.args[0] and
      other.__class__ == self.__class__),
      (other.args[1] == self.args[1] and
      other.__class__ == self.__class__)
    )

    tup = (other.cf == (self.cf),other.mv == (self.mv))
    return tup

  @property
  def grade(self:"Box") -> set:
    return self.args[1].grade