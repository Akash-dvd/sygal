from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union,NewType,Type,Any

from sympy import (
  diff, Rational, Symbol, S, Mul, Add, Expr,Pow,
  expand, simplify, eye, trigsimp,cos,sin,subsets,
  symbols, sqrt, Matrix, SympifyError, sympify
)

from libs.Sygal.Box import Box
from libs.Sygal.GExpr import GExpr

from libs.Sygal.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from libs.Sygal.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from libs.Sygal.strategies.tools import subs, typed ,canon
from libs.Sygal.strategies.traverse import (top_down, bottom_up, bxsall, top_down_once,bottom_up_once)
from libs.Sygal.strategies.tree import treeapply, greedy, allresults, brute



from libs.Sygal.operators.assop.gadd import gadd
from libs.Sygal.operators.assop.gextp import gextp
from libs.Sygal.operators.assop.gmul import gmul

from libs.Sygal.operators.binop.ganticomm import ganticomm
from libs.Sygal.operators.binop.gcomm import gcomm
from libs.Sygal.operators.binop.ginprdct import ginprdct
from libs.Sygal.operators.binop.grcntrct import grcntrct
from libs.Sygal.operators.binop.glcntrct import glcntrct

from libs.Sygal.utils.utils import is_invertible

# Assuming blade*blade = scalar
def gmul_simp(expr:"gmul")->Optional[GExpr]:
  if type(expr) == gmul and len(expr.args)>=2:
    for i,arg in enumerate(expr.args):
      if arg == expr.args[i+1] and is_invertible(arg):
        t = [element for j, element in enumerate(expr.args) if j not in {i,i+1}]
        t.append((expr.args[i]<expr.args[i+1]))
        t1 = gmul(*t)
        if t1.mv == GExpr.nl:
          return t1.coeff
        else :
          return t1.mv
    return expr 

  else :
    return expr

def gmulsimp():
  gmul.gsimplifyr = gmul_simp
