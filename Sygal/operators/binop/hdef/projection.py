from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from sympy import (
  diff, Rational, Symbol, S, Mul, Add, Expr,Pow,
  expand, simplify, eye, trigsimp,cos,sin,
  symbols, sqrt, Matrix, SympifyError, sympify
)

from libs.Sygal.GExpr import GExpr
from libs.Sygal.Box import Box
from libs.Sygal.utils.utils  import is_invertible

from libs.Sygal.operators.assop.gadd import gadd
from libs.Sygal.operators.assop.gextp import gextp
from libs.Sygal.operators.assop.gmul import gmul

from libs.Sygal.operators.binop.ganticomm import ganticomm
from libs.Sygal.operators.binop.gcomm import gcomm
from libs.Sygal.operators.binop.ginprdct import ginprdct
from libs.Sygal.operators.binop.grcntrct import grcntrct
from libs.Sygal.operators.binop.glcntrct import glcntrct
from .hdef import hdef

class projection(hdef):

  def __new__(cls,sub:"GExpr",obj:"GExpr")->Optional[Box]:
    # Pattern Match for two arguements
    if (is_invertible(sub)):
      obj = GExpr.__new__(projection,sub,obj)
    else :
      raise ValueError
    return Box.__new__(obj)
  
  def gexpand(self:"projection")->Optional[Box]:
    sub = self.args[0]
    obj = self.args[1]
    if is_invertible(sub):
      coeff = Pow((sub>sub),-1)
      return Box.__new__(Box,(obj<sub)<sub,coeff)
    else :
      raise

  @property
  def grade(self:"projection") -> Union[set,frozenset]:
    expanded = self.gexpand()
    return expanded.grade

  def __str__(self:"projection") -> str:
    ls = self.args
    str = '( PROJ '
    for o in ls:
      str += o.__str__()+' '
    str = str[:-1]
    str += ')'
    return str

  __repr__ = __str__

  def __hash__(self:"projection") -> int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self:"projection", other:"GExpr") -> bool:
    # THIS DEFINITION CAN BE MODIFIED BY EXPANDING THE EXPRESSION
    return (
      (type(other) == type(self)) and
      self.__hash__() == other.__hash__()
    )


from libs.Sygal.operators.binop.hdef.higher.projctionhigher import projctionhigher
from libs.Sygal.operators.binop.hdef.simplify.projctionsimp import projctionsimp
from libs.Sygal.operators.binop.hdef.expand.projctionexpand import projctionexpand