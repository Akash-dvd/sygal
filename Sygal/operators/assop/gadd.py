from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union,NewType,Type,Any

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


class gadd(GExpr) :

  def __new__(cls, args0:GExpr,*args:Tuple["GExpr"],**kwargs) -> "Box":
    # gadd(Box,Optional[Box,Box.....])

    # Pattern Matching for # of args for associative op
    t =  [args0]
    t.extend(args)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))
    
    if(len(t1)==1):
      return t1[0]
    else :
      
      expr = canonicalize(Basic.__new__(gadd, *t1))

      # Here Altering with args so pattern matching is required
      if(len(expr.args)>1):
        return Box.__new__(Box,expr)
      elif (len(expr.args)==1):
        singarg = expr.args[0]
        return Box.__new__(Box,singarg)
      else:
        return Box.Znl

  @property
  def grade(self:"gadd") -> Union[set,frozenset]:
    t = set()
    for i in self.args:
      t.update(i.grade)
    return t

  def __str__(self:"gadd") -> str:
    ls = self.args
    str = '('
    for o in ls:
      str += o.__str__()+'+'
    str = str[:-1]
    str += ')'
    return str

  __repr__ = __str__


  def __hash__(self:"gadd") -> int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self:"gadd", other:"GExpr") -> bool:
    return (
      (type(other) == type(self)) and
      self.__hash__() == other.__hash__()
    )
  
def rlgaddFlatten(expr):
  tbx = []
  # Flatten coz of gadd present inside Box
  for BX in expr.args:
    # Pattern Match
    # For ele == gadd inside Box or only Box
    if(type(BX.mv)==gadd):
      childbxes = BX.mv.args
      cf = BX.coeff
      flatbxes = [Box.__new__(Box,mv=bx.mv,coeff=Mul(bx.coeff,cf).simplify()) for bx in childbxes]

      tbx.extend(flatbxes)
  
    else :
      tbx.append(BX)
  
  expr1 = Basic.__new__(gadd, *tbx)
  return expr1

def rlgaddgroupsort(expr):
  sift_key = lambda x:x.mv
  sift_count = lambda x:x.coeff
  # sift_combine = lambda cnt,args:Box.__new__(Box,args,cnt.simplify())
  
  grouped = bx_sift(expr.args,sift_key,sift_count)
  filtered = [bx for bx in grouped if bx.coeff!=S(0)]
      
    
  Sortedseq = sorted(filtered,key=lambda bx:(len(bx.mv.grade),next(iter(bx.mv.grade)),bx.mv.name,bx.mv.__hash__()))

  return Basic.__new__(gadd, *Sortedseq)

rules1 = (
  rlgaddFlatten,rlgaddgroupsort
  )


# rules = (
#   unpack, rm_id(lambda x: x == 0), flatten,sort(lambda ele: ele.grade)
#   )

canonicalize = exhaust(typed({gadd: do_one(*rules1)}))

from libs.Sygal.Box import Box
from libs.Sygal.utils import bx_sift


from libs.Sygal.operators.assop.higher.gaddhigher import gaddhigher
from libs.Sygal.operators.assop.simplify.gaddsimp import gaddsimp
from libs.Sygal.operators.assop.expand.gaddexpand import gaddexpand