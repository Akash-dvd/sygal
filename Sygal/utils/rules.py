from sympy.core.singleton import S

from libs.Sygal.GV import GV,gv

from libs.Sygal.operators import (add,anticomm,comm,extp,
inprdct,lcntrct,mul,rcntrct)

from sympy.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from sympy.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from sympy.strategies.tools import subs, typed ,canon
from sympy.strategies.traverse import (top_down, bottom_up, sall, top_down_once,bottom_up_once, basic_fns)
from sympy.strategies.tree import treeapply, greedy, allresults, brute

def conjugation(rl1,rl2):
  return chain(rl1,rl2,rl1)
  

def rlZero(expr,fns=basic_fns):
  op, new, children, leaf = map(fns.get, ('op', 'new', 'children', 'leaf'))
  if leaf(expr):
    return expr
  elif (S(0) in expr.args):
    return S(0)
  else : 
    return expr

