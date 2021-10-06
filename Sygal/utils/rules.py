from sympy import Basic
from sympy.core.expr import Expr
from sympy.core.singleton import S

from libs.Sygal.GExpr import GExpr

from libs.Sygal.operators import (add,anticomm,comm,extp,
inprdct,lcntrct,mul,rcntrct)

from sympy.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from sympy.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from sympy.strategies.tools import subs, typed ,canon
from sympy.strategies.traverse import (top_down, bottom_up, sall, top_down_once,bottom_up_once, basic_fns)
from sympy.strategies.tree import treeapply, greedy, allresults, brute


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

def rlGSortArgs(expr:"GExpr") -> "extp":
  """
  Sort Paritioned arguements based on Grades
  """
  def GSortArgs(seq):

    seq0 = [elem for elem in seq if not isinstance(elem,GExpr) and isinstance(elem,Expr)]

    seq1 = [elem for elem in seq if isinstance(elem,GExpr) and elem.is_atom]

    seq2 = [elem for elem in seq if isinstance(elem,GExpr) and not elem.is_atom]

    newseq1 = sorted(seq1,key=lambda ele: ele.name)
    newseq2 = sorted(seq2,key=lambda ele: ele.__hash__())
    
    seq0.extend(newseq1)
    seq0.extend(newseq2)
    
    return seq0
  return new(expr.__class__, *GSortArgs(expr.args))

    
def rlGSortGrades(expr:"GExpr") -> "mul":
  """
  Sort arguements based on Grades
  """
  def GrSortArgs(seq):

    seq0 = [elem for elem in seq if not isinstance(elem,GExpr) and isinstance(elem,Expr)]

    seq1 = [elem for elem in seq if isinstance(elem,GExpr) and elem.is_atom]

    seq2 = [elem for elem in seq if isinstance(elem,GExpr) and not elem.is_atom]

    newseq1 = sorted(seq1,key=lambda ele: ele.name)
    newseq2 = sorted(seq2,key=lambda ele: ele.__hash__())
    
    seq0.extend(newseq1)
    seq0.extend(newseq2)
    
    return seq0
  return new(expr.__class__, *GrSortArgs(expr.args))