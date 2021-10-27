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

from sympy.printing.str import StrPrinter
from libs.Sygal.utils.utils1 import is_devmode


class projection(hdef):

  def __new__(cls,sub:"GExpr",obj:"GExpr")->Optional[Box]:
    # Pattern Match for two arguements
    if (is_invertible(sub)):
      obj = GExpr.__new__(projection,sub,obj)
    else :
      raise ValueError
    return Box.__new__(Box,obj)

  @property
  def grade(self:"projection") -> Union[set,frozenset]:
    return {1}
    expanded = self.gexpand()
    return expanded.grade

  
  def sympystr(self,expr:"projection") -> str:
    return str(expr)

  def sympyrepr(self,expr:"projection") -> str:
    return expr.__repr__()

  def __str__(self:"projection") -> str:
    str = '('+(self.down).__str__()\
    +'\033[1;33;40mPRO\033[0;37;40m'\
    +(self.up).__str__()+')'
    return str

  def __repr__(self:"projection") -> str:
    str = '('+(self.down).__repr__()\
    +'PRO'\
    +(self.up).__repr__()+')'
    return str

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

  @property
  def down(self:"projection")->"GExpr":
    return self.args[0]

  @property
  def up(self:"projection")->"GExpr":
    return self.args[1]

if is_devmode():
  StrPrinter._print_projectionn = projection.sympyrepr
else :
  StrPrinter._print_projection = projection.sympystr


from libs.Sygal.operators.binop.hdef.higher.projctionhigher import projctionhigher
from libs.Sygal.operators.binop.hdef.simplify.projctionsimp import projctionsimp
from libs.Sygal.operators.binop.hdef.expand.projctionexpand import projctionexpand

projctionhigher()
projctionsimp()
projctionexpand()
