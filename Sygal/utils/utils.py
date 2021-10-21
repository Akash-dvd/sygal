from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union


from collections import defaultdict
from functools import cmp_to_key
import operator
from sympy.core import facts

from sympy.core.sympify import sympify
from sympy.core.basic import Basic
from sympy.core.singleton import S
from sympy.core.operations import AssocOp
from sympy.core.cache import cacheit
from sympy.core.logic import fuzzy_not, _fuzzy_group, fuzzy_and
from sympy.core.compatibility import reduce
from sympy.core.expr import Expr
from sympy.core.parameters import global_parameters

from sympy.combinatorics.permutations import Permutation

from sympy.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from sympy.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from sympy.strategies.tools import subs, typed ,canon
from sympy.strategies.traverse import (top_down, bottom_up, sall, top_down_once,bottom_up_once, basic_fns)
from sympy.strategies.tree import treeapply, greedy, allresults, brute

from libs.Sygal.GExpr import GExpr
from libs.Sygal.Box import Box


# def Boxify(arg:Union[Box,GExpr,Expr])->Box:
#   """Takes only one arguement at a time"""

#   # Pattern matching for types
#   fct1 = issubclass(type(arg),GExpr)
#   # fct2 is for scalar multivectors
#   fct2 = True if fct1 and (arg.grade == {0}) else False
#   fct3 = issubclass(type(arg),Box)


#   if fct3:
#     return arg
#   elif fct2:
#     return Box.__new__(Box,mv=Box.nl,coeff=arg)
#   elif fct1:
#     return Box.__new__(Box,mv=arg)
#   else :
#     return Box.__new__(Box,mv=Box.nl,coeff=sympify(arg))

def is_unMixedGrade(args:GExpr)->bool:
  t = set()
  t.update((i%2 for i in args.grade))
  return True if len(t)==1 else False


def parity(args1:List["GExpr"],args2:List["GExpr"])->S:
  # ASSUMPTIONS
  # both arguements have unmixed grades
  # remove even grades , they are transparent to positional changes
  
  # Reimplement using something from permutation library
  t1 = [i for i in args1 if next(iter(i.grade))%2==1 ]
  d1 = dict()
  t2 = [i for i in args2 if next(iter(i.grade))%2==1 ]
  
  for index, value in enumerate(t1):
    d1[value.__hash__()] = [index]

  for index, value in enumerate(t2):
    d1[value.__hash__()].append(index)
  
  perm = []
  for index, (key, value) in enumerate(d1.items()):
    perm.append(value)
  
  perm1 = sorted(perm,key=lambda ele:ele[1])
  perm2 = [i[0] for i in perm1]

  p = Permutation(perm2)

  return S((p.parity()*-2)+1)

def bx_sift(seqBx:Tuple[Box], keyfunc:Callable, count:Callable)->List[Box]:

  m = defaultdict(lambda:S(0))
  for i in seqBx:
    m[keyfunc(i)] +=count(i)
    m[keyfunc(i)] = m[keyfunc(i)].simplify()
  lst = []
  for key, value in m.items():
    lst.append(Box.__new__(Box,key,value))
  return lst

def is_invertible(expr):
  return True