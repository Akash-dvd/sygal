from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from sympy import (
  diff, Rational, Symbol, S, Mul, Add, Expr,Pow,
  expand, simplify, eye, trigsimp,cos,sin,
  symbols, sqrt, Matrix, SympifyError, sympify
)

from libs.Sygal.GExpr import GExpr
from libs.Sygal.Box import Box
from libs.Sygal.utils import is_invertible

from .hdef import hdef

from libs.Sygal.operators import (gadd,ganticomm,gcomm,gextp,
ginprdct,glcntrct,gmul,grcntrct)



class inversion(hdef):

  def __new__(cls,sub:"GExpr",obj:"GExpr")->Optional[Box]:
    # Pattern Match for two arguements
    if (is_invertible(sub)):
      obj = GExpr.__new__(inversion,sub,obj)
    else :
      raise ValueError
    return Box.__new__(obj)
  
  def expand(self:"inversion")->Optional[Box]:
    sub = self.args[0]
    obj = self.args[1]
    if is_invertible(sub):
      coeff = Pow((sub>sub),-1)
      return Box.__new__(Box,sub*obj*sub,coeff)
    else :
      raise

  @property
  def grade(self:"inversion") -> Union[set,frozenset]:
    expanded = self.expand()
    return expanded.grade

  def __str__(self:"inversion") -> str:
    ls = self.args
    str = '( INV '
    for o in ls:
      str += o.__str__()+' '
    str = str[:-1]
    str += ')'
    return str

  __repr__ = __str__

  def __hash__(self:"inversion") -> int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self:"inversion", other:"GExpr") -> bool:
    # THIS DEFINITION CAN BE MODIFIED BY EXPANDING THE EXPRESSION
    return (
      (type(other) == type(self)) and
      self.__hash__() == other.__hash__()
    )
