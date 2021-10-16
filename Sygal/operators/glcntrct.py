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
from libs.Sygal.utils import Boxify,rlGSortArgs,is_unMixedGrade,parity


class glcntrct(GExpr):
  """
  Left Contraction < operator
  Is non-associative, non-commutative
  """
  identity = Box.Znl

  # Currently both arguements should be boxed! extp/GB
  def __new__(cls, args0:GExpr,args1:GExpr) -> Box:
    # Already matched pattern for binary op
    
    t = tuple(args0,args1)
    t1 = tuple(map(Boxify, t))
    t2 = [t1[0].args[1],t1[1].args[1]]
    coeff = Mul(t1[0].args[0],t1[1].args[0]).simplify()
    
    # Pattern match for grade value
    # Check for scalars
    if(t1[0].args[1]==Box.nl):
      return(Box.__new__(Box,t1[1].args[1],Mul(t1[0].args[0],t1[1].args[0]).simplify()))
    
    elif(t1[1].args[1]==Box.nl):
      return Box.Znl

    else:
      mv = Basic.__new__(glcntrct, *t2)
      return(Box.__new__(Box,mv,coeff))


  @property
  def grade(self:"glcntrct"):
    # Two arguements will always be present
 
    t = set()
    arg1 = self.args[0].grade
    arg2 = self.args[1].grade

    for elem1 in arg1:
      for elem2 in arg2:
        if((elem2-elem1)>=0): 
          t.add((elem2-elem1))
    return t

  def __str__(self:"glcntrct"):
    str = '('+(self.args[0]).__str__()\
    +'<'\
    +(self.args[1]).__str__()+')'
    return str

  __repr__ = __str__

  def __hash__(self:"glcntrct"):
    h = self._mhash
    if h is None:
      h = hash((type(self).__name__) + \
        str(self.args[0].__hash__()) + \
        str(self.args[1].__hash__()))
      self._mhash = h
    return h
  
  def __eq__(self:"glcntrct", other:"GExpr"):
    return (
      (type(other) == type(self))  and
      self.__hash__() == other.__hash__()
    )
  