from os import times
from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union,NewType,Type,Any
from mpmath.libmp.libmpf import to_int

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

from libs.Sygal.operators.binop.hdef.inversion import inversion


from libs.Sygal.utils.utils import is_invertible

def gmul_2Inv(expr:"gmul")->Optional[GExpr]:
  if type(expr) == gmul and (len(expr.args)>=3):
      for i,arg in enumerate(expr.args):
        if arg in expr.args[i+1:] and is_invertible(arg):
          j = expr.args[i+1:].index(arg) + i + 1
          t_i = expr.args[:i]
          ti_ = expr.args[i+1:][:j]
          tj_ = expr.args[j+1:]
          t1 = gmul(*ti_)
          t2 = inversion(expr.args[i],t1)
          tall = []
          tall.extend(t_i)
          tall.append(t2)
          tall.extend(tj_)
          
          t3 = gmul(*tall)
          if t3.mv == GExpr.nl:
            return t3.coeff
          else :
            return t3.mv
      else :
        return expr
  else :
    return expr

def gmul_2Proj(expr:"gmul")->Optional[GExpr]:
  if type(expr) == gmul and (len(expr.args)>=3):
      for i,arg in enumerate(expr.args):
        if arg in expr.args[i+1:] and is_invertible(arg):
          j = expr.args[i+1:].index(arg) + i + 1
          t_i = expr.args[:i]
          ti_ = expr.args[i+1:][:j]
          tj_ = expr.args[j+1:]
          t1 = gmul(*ti_)
          t2 = inversion(expr.args[i],t1)
          tall = []
          tall.extend(t_i)
          tall.append(t2)
          tall.extend(tj_)
          
          t3 = gmul(*tall)
          if t3.mv == GExpr.nl:
            return t3.coeff
          else :
            return t3.mv
      else :
        return expr
  else :
    return expr

def gmul_2Rej(expr:"gmul")->Optional[GExpr]:
  if type(expr) == gmul and (len(expr.args)>=3):
      for i,arg in enumerate(expr.args):
        if arg in expr.args[i+1:] and is_invertible(arg):
          j = expr.args[i+1:].index(arg) + i + 1
          t_i = expr.args[:i]
          ti_ = expr.args[i+1:][:j]
          tj_ = expr.args[j+1:]
          t1 = gmul(*ti_)
          t2 = inversion(expr.args[i],t1)
          tall = []
          tall.extend(t_i)
          tall.append(t2)
          tall.extend(tj_)
          
          t3 = gmul(*tall)
          if t3.mv == GExpr.nl:
            return t3.coeff
          else :
            return t3.mv
      else :
        return expr
  else :
    return expr

def gmulhigher():
  gmul.ghigher = exhaust(do_one(gmul_2Inv,gmul_2Proj,gmul_2Rej))