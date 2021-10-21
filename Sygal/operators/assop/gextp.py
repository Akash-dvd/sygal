from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from functools import reduce
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
from libs.Sygal.utils import rlGSortArgs,is_unMixedGrade,parity

class gextp(GExpr):

  def __new__(cls, args0:GExpr,*args:Tuple["GExpr"],**kwargs) -> Box:
    # gextp(Box,Optional[Box,Box.....])

    # Pattern Matching for # of args for associative op# Pattern Matching for # of args for associative op
    t =  [args0]
    t.extend(args)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))

    # every element has grade !={0}
    # Here Altering with args so pattern matching is required
    tmvs = [bx.mv for bx in t1 if bx.mv!=Box.nl]
    cfs = [bx.coeff for bx in t1]
    cf = Mul(*cfs).simplify()
    
    # Pattern Matching for # of args for associative op
    if tmvs == []:
      return Box.__new__(Box,mv=Box.nl,coeff=cf)
    elif len(tmvs)==1:
      return Box.__new__(Box,mv=tmvs[0],coeff=cf)
    else:
      expr1 = Basic.__new__(gextp, *tmvs)
      # For flattening
      # Here Altering with args so pattern matching is required
      # But this canocalize doesn't reduce the args ever
      expr2 = canonicalize1(expr1)
      
      # More patternmatching
      if(len(expr2.args)<=1):
        # Not possible
        # to arrive here
        raise ValueError
      
      # Repitition Check
      if ((len(expr2.args)-len(set(expr2.args))) > 0):  
        return GExpr.Znl

      if(is_unMixedGrade(expr2)):
        # For signed sorting
        expr3 = canonicalize2(expr2)
        # More patternmatching
        if(len(expr3.args)<=1):
        # Not possible
        # to arrive here
          raise ValueError

        cf1 = Mul(parity(expr2.args,expr3.args),cf).simplify()
      else :
        expr3 = expr2
        cf1 = cf
      bx = Box.__new__(Box,mv=expr3,coeff=cf1)
      



      if all(not isinstance(i, GExpr) for i in t1):
        pass
        # pseudoscalar check


      
      return bx


  @property
  def grade(self:"gextp") -> Union[set,frozenset]:
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
              t2.add((elem2+elem1))
          t1.clear()
          t1.update(t2)
    return t2

  def __str__(self:"gextp") -> str:
    ls = self.args
    str = '('
    for o in ls:
      str += o.__str__()+'^'
    str = str[:-1]
    str += ')'
    return str

  __repr__ = __str__

  def __hash__(self:"gextp") -> int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self:"gextp", other:"GExpr") -> bool:
    return (
      (type(other) == type(self)) and
      self.__hash__() == other.__hash__()
    )

  # def __neg__(self:"gextp") -> Box:
  #   coeff = Mul(S(-1),self.args[0]).simplify()
  #   mv = self.args[1]
  #   return Box.__new__(Box,mv,coeff)


# rules = (
#   unpack, rm_id(lambda x: x == 1), flatten,rlGSortArgs
#   )
rules1 = (
    unpack,flatten
  )
rules2 = (
    unpack,rlGSortArgs
  )


canonicalize1 = exhaust(typed({gextp: do_one(*rules1)}))
canonicalize2 = exhaust(typed({gextp: do_one(*rules2)}))
