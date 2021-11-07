from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union,NewType,Type,Any

from sympy import (
  diff, Rational, Symbol, S, Mul, Add, Expr,Pow,
  expand, simplify, eye, trigsimp,cos,sin,subsets,
  symbols, sqrt, Matrix, SympifyError, sympify
)

# from libs.Sygal.utils.utils import parity

from libs.Sygal.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from libs.Sygal.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from libs.Sygal.strategies.tools import subs, typed ,canon
from libs.Sygal.strategies.traverse import (top_down, bottom_up, bxsall, top_down_once,bottom_up_once)
from libs.Sygal.strategies.tree import treeapply, greedy, allresults, brute


from libs.Sygal.Box import Box
from libs.Sygal.GExpr import GExpr

from libs.Sygal.operators.assop.gadd import gadd
from libs.Sygal.operators.assop.gextp import gextp
from libs.Sygal.operators.assop.gmul import gmul

from libs.Sygal.operators.binop.ganticomm import ganticomm
from libs.Sygal.operators.binop.gcomm import gcomm
from libs.Sygal.operators.binop.ginprdct import ginprdct
from libs.Sygal.operators.binop.grcntrct import grcntrct
from libs.Sygal.operators.binop.glcntrct import glcntrct

from libs.Sygal.operators.binop.outermorphic.projection import projection

from libs.Sygal.utils.utils import is_invertible

def projection_expand(expr:"projection")->Optional[Box]:
  if type(expr) == projection:
    sub = expr.down
    obj = expr.up
    if is_invertible(sub):
      coeff = Pow((sub<sub),-1)
      return Box.__new__(Box,(obj<sub)<sub,coeff)
    else :
      raise
  else :
    return expr

def projectionexpand():
  projection.gexpand = projection_expand

