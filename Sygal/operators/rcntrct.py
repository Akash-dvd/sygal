from sympy.core.numbers import nan
# from .function import Function

from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,
  symbols, sqrt, Matrix,srepr,Function
)

from libs.Sygal.GExpr import GExpr

class rcntrct(GExpr):

  @property
  def grade(self):
    return self.args[1].grade-self.args[0].grade

  @classmethod
  def eval(cls, p, q):
    return
  
  def __str__(self):
    str = '('+(self.args[0]).__str__()\
    +'>'\
    +(self.args[1]).__str__()+')'
    return str

  __repr__ = __str__

  def __hash__(self):
    h = self._mhash
    if h is None:
      h = hash((type(self).__name__) + \
        str(self.args[0].__hash__()) + \
        str(self.args[1].__hash__()))
      self._mhash = h
    return h
  
  def __eq__(self, other):
    return (
      (type(other) == type(self))  and
      self.__hash__() == other.__hash__()
    )