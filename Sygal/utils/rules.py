from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from sympy import Basic
from sympy.core.expr import Expr
from sympy.core.singleton import S

from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,
  symbols, sqrt, Matrix,srepr,bottom_up
)

from sympy.utilities.iterables import sift

from sympy.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from sympy.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from sympy.strategies.tools import subs, typed ,canon
from sympy.strategies.traverse import (top_down, bottom_up, sall, top_down_once,bottom_up_once, basic_fns)
from sympy.strategies.tree import treeapply, greedy, allresults, brute


from libs.Sygal.GExpr import GExpr

# from libs.Sygal.operators import (gadd,ganticomm,gcomm,gextp,ginprdct,glcntrct,gmul,grcntrct)

new = Basic.__new__
# TODO add new to arguements

def conjugation(rl1,rl2):
  return chain(rl1,rl2,rl1)



def rlZero(expr:"GExpr",fns=basic_fns) -> "GExpr" :
  op, new, children, leaf = map(fns.get, ('op', 'new', 'children', 'leaf'))
  if leaf(expr):
    return expr
  elif (S(0) in expr.args):
    return S(0)
  else : 
    return expr

def rlChkDup(expr:GExpr)->GExpr:
  if ((len(expr.args)-len(set(expr.args))) == 0):
    return expr
  else:
    return S(0)

def rlGSortArgs(expr:"GExpr",reverse:bool=False) -> "GExpr":
  """
  Sort Paritioned arguements based on Grades,names
  Complex arguement are put at last sorted by sum of their weights
  """
  newseq = sorted(expr.args,key=lambda ele:(len(ele.grade),next(iter(ele.grade)),ele.name,ele.__hash__()),reverse=reverse)
  return new(expr.__class__, *newseq)

def GSortArgs(seq:Union[list,tuple],reverse:bool=False) -> Union[list,tuple]:
  """
  Sort Paritioned arguements based on Grades,names
  Complex arguement are put at last sorted by sum of their weights
  """

  newseq = sorted(seq,key=lambda ele:(len(ele.grade),next(iter(ele.grade)),ele.name,ele.__hash__()),reverse=reverse)
  return newseq


def rlglom(key, count, combine):
  """ 
  Replaced sum of glom with Add here
  """
  def conglomerate(expr):
    """ Conglomerate together identical args x + x -> 2x """
    groups = sift(expr.args, key)
    counts = dict((k, Add(map(count, args))) for k, args in groups.items())
    newargs = [combine(cnt, mat) for mat, cnt in counts.items()]
    if set(newargs) != set(expr.args):
      return new(type(expr), *newargs)
    else:
      return expr
  return conglomerate