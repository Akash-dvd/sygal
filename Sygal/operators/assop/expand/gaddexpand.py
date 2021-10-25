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
from libs.Sygal.strategies.traverse import (top_down, bottom_up, bxsall, top_down_once,bottom_up_once, basic_fns)
from libs.Sygal.strategies.tree import treeapply, greedy, allresults, brute

from libs.Sygal.operators.assop.gadd import gadd
from libs.Sygal.operators.assop.gextp import gextp
from libs.Sygal.operators.assop.gmul import gmul

from libs.Sygal.operators.binop.ganticomm import ganticomm
from libs.Sygal.operators.binop.gcomm import gcomm
from libs.Sygal.operators.binop.ginprdct import ginprdct
from libs.Sygal.operators.binop.grcntrct import grcntrct
from libs.Sygal.operators.binop.glcntrct import glcntrct


from libs.Sygal.Box import Box
from libs.Sygal.GExpr import GExpr

  # def distribute_rl(expr):
  #   if isinstance(expr,Box):
  #     bx = expr
  #     if isinstance(bx.mv,A):
  #       MV = bx.mv
  #       cf = bx.coeff
  #       for i, arg in enumerate(MV.args):
  #         if isinstance(arg, gadd):
  #           first, b, tail = MV.args[:i], MV.args[i], MV.args[i+1:]
  #           tmplst = [A(*(first + (bx,) + tail)) for bx in b.args]
  #           t =  gadd(*tmplst)
  #           return Box.__new__(Box,t,cf)
  #       return expr
  #     else:
  #       return expr
  #   else :
  #     return expr
  # return distribute_rl

def distriOvrAdd(A):
# Notice multiple returns otherwise null is returned causing errors
  def distribute_rl(expr):
    if isinstance(expr,A):
      for i, arg in enumerate(expr.args):
        if isinstance(arg, gadd):
          first, b, tail = expr.args[:i], expr.args[i], expr.args[i+1:]
          tmplst = [A(*(first + (bx,) + tail)) for bx in b.args]
          t =  gadd(*tmplst)
          # CHANGED HERE
          if(t.mv==GExpr.nl):
            return t.coeff
          else:
            return t.mv
      return expr
    else:
      return expr

  return distribute_rl


    

gextpDist = distriOvrAdd(gextp)
gmulDist = distriOvrAdd(gmul)
glcntrctDist = distriOvrAdd(glcntrct)
grcntrctDist = distriOvrAdd(grcntrct)
# for binops different expansion will work

canonicalize11 = (bottom_up_once(gextpDist))
canonicalize12 = exhaust(bottom_up_once(do_one(gextpDist,gmulDist,glcntrctDist,grcntrctDist)))

GExpr.gdistribute = canonicalize12

def gaddexpand():
  pass


""" 
THIS FILE IS FOR GDISTRIBUTE
"""