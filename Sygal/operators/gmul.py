from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from collections import defaultdict
from functools import cmp_to_key
import operator

from sympy.core.sympify import sympify
from sympy.core.basic import Basic
from sympy.core.singleton import S
from sympy.core.operations import AssocOp
from sympy.core.cache import cacheit
from sympy.core.logic import fuzzy_not, _fuzzy_group, fuzzy_and
from sympy.core.compatibility import reduce
from sympy.core.expr import Expr
from sympy.core.parameters import global_parameters

from sympy import (
    diff, Rational, Symbol, S, Mul, Add, Expr,
    expand, simplify, eye, trigsimp,cos,sin,
    symbols, sqrt, Matrix, SympifyError, sympify
)

from sympy.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from sympy.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from sympy.strategies.tools import subs, typed ,canon
from sympy.strategies.traverse import (top_down, bottom_up, sall, top_down_once,bottom_up_once, basic_fns)
from sympy.strategies.tree import treeapply, greedy, allresults, brute

from libs.Sygal.GExpr import GExpr
from libs.Sygal.Box import Box
from libs.Sygal.utils import Boxify,rlGSortArgs

class gmul(GExpr):

  identity = Box.Onl

  def __new__(cls, *args:Tuple["GExpr"],**kwargs) -> Box:
    if not args:
      return cls.identity

    t1 = tuple(map(Boxify, args))
    args1 = [bx.args[1] for bx in t1 if bx.args[1]!=Box.nl]
    if args1 == []:
      args1=[Box.nl]
    coeffs = [bx.args[0] for bx in t1]
    coeff = Mul(*coeffs).simplify()

    obj = Basic.__new__(gmul, *args1)
    obj1 = canonicalize(obj)

    obj2 = Box.__new__(Box,obj1,coeff)
    
    # if ((len(args)-len(set(args))) == 0):  
    #   obj = Basic.__new__(cls, *t1)
    # else :
    #   t3 = super().Znl
    #   return Basic.__new__(cls, *t3)

    check = kwargs.get('check', False)
    if check:
      # Use this for pseudoscalar checks
      pass
      
      # if all(not isinstance(i, MatrixExpr) for i in args):
      #   return Add.fromiter(args)
      # validate(*args)


    if all(not isinstance(i, GExpr) for i in t1):
      pass
      # append to appendage for grade 0


    
    return obj2


  @property
  def grade(self:"gmul") -> set:
    if(len(self.args)==1):
      return self.args[0].grade
    else:
      t1 = set()
      t2 = set()
      t1.update(self.args[0].grade)
      for i,argi in enumerate(self.args):
        j=i+1
        if(j<len(self.args)):
          t2.clear()
          arg2 = self.args[j].grade
          for elem1 in t1:
            for elem2 in arg2:
              t2.update(list(range(abs(elem2-elem1),(elem2+elem1+1),2)))
          t1.clear()
          t1.update(t2)
    return t2

  def __str__(self:"gmul") -> str:
    ls = self.args
    str = '('
    for o in ls:
      str += o.__str__()+'*'
    str = str[:-1]
    str += ')'
    return str

  __repr__ = __str__

  def __hash__(self:"gmul") -> int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self:"gmul", other:"GExpr") -> bool:
    return (
      (type(other) == type(self)) and
      self.__hash__() == other.__hash__()
    )

  def __neg__(self:"gmul") -> "gmul":
    c, args = self.as_coeff_mul()
    c = -c
    if c is not S.One:
      if args[0].is_Number:
        args = list(args)
        if c is S.NegativeOne:
          args[0] = -args[0]
        else:
          args[0] *= c
      else:
        args = (c,) + args
    return self._from_args(args, self.is_commutative)
  

def donone(expr):
  return expr
# rules = (
#   unpack, rm_id(lambda x: x == 1), flatten,rlGSortArgs
#   )
rules = (
   flatten,donone
  )

canonicalize = exhaust(typed({gmul: do_one(*rules)}))


