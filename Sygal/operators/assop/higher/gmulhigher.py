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

from libs.Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion
from libs.Sygal.operators.binop.outermorphic.projection import projection
from libs.Sygal.operators.binop.outermorphic.rejection import rejection

from libs.Sygal.utils.utils import parity


from libs.Sygal.utils.utils import is_invertible,is_blade

def gmul_2Inv(expr:"gmul")->Optional[GExpr]:
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gmul and (len(BX.mv.args)>=3):
      for i,arg in enumerate(BX.mv.args):
        if arg in BX.mv.args[i+1:] and is_invertible(arg):
          j = BX.mv.args[i+1:].index(arg) + i + 1
          t_i = BX.mv.args[:i]
          ti_ = BX.mv.args[i+1:][:j-i-1]
          tj_ = BX.mv.args[j+1:]
          t1 = gmul(*ti_)
          t2 = inversion(arg,t1)
          tall = []
          tall.extend(t_i)
          tall.append(t2)
          tall.extend(tj_)
          
          coeff = (BX.mv.args[i]<BX.mv.args[i]).coeff
          t3 = gmul(*tall)
          if t3.mv == GExpr.nl:
            return t3.coeff
          else :
            return Box.__new__(Box,t3.mv,coeff)
      return expr
    else :
      return expr
  else :
      return expr

def gmul_2Proj(expr:"gmul")->Optional[GExpr]:
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gmul and (len(BX.mv.args)>=2):
      for i,arg in enumerate(BX.mv.args):
        if type(arg) == glcntrct:
          # Blade invertible should be of single grade
          if is_invertible(arg.down) and is_blade(arg.down):
            # This pattern matching for preceding and ahead arguement will check only one indexed element
            # Either leaf or gextp will be present
            _arg = BX.mv.args[i-1] if i!=0 else None
            arg_ = BX.mv.args[i+1] if len(BX.mv.args)>(i+1) else None
            
            if _arg == arg.down and arg_ == arg.down:
              raise ValueError("Inversion Should have caught it.")
            elif _arg == arg.down :
              ti = projection(arg.down,arg.up)*(arg.down<arg.down)
              t_i = BX.mv.args[:i-1]
              ti_ = BX.mv.args[i+1:]
              tall = []
              tall.extend(t_i)
              tall.append(ti)
              tall.extend(ti_)
              sign1 = (next(iter(BX.mv.args[i].grade)))%2
              sign2 = (next(iter(BX.mv.args[i-1].grade))-1)%2
              sign = S(-2)*(sign1*sign2)+1
              t3 = gmul(*tall)*cf*sign
              return Box.__new__(Box,t3)
            elif arg_ == arg.down:
              ti = projection(arg.down,arg.up)*(arg.down<arg.down)
              t_i = BX.mv.args[:i-1]
              ti_ = BX.mv.args[i+1:]
              tall = []
              tall.extend(t_i)
              tall.append(ti)
              tall.extend(ti_)
              sign = S(1)
              t3 = gmul(*tall)*cf*sign
              return Box.__new__(Box,t3)
            else :
              pass

        elif type(arg) == grcntrct:
          if is_invertible(arg.down) and is_blade(arg.down):
            _arg = BX.mv.args[i-1] if i!=0 else None
            arg_ = BX.mv.args[i+1] if len(BX.mv.args)>(i+1) else None
            
            if _arg == arg.down and arg_ == arg.down:
              raise ValueError("Inversion Should have caught it.")
            elif _arg == arg.down :
              ti = projection(arg.down,arg.up)*(arg.down<arg.down)
              t_i = BX.mv.args[:i-1]
              ti_ = BX.mv.args[i+1:]
              tall = []
              tall.extend(t_i)
              tall.append(ti)
              tall.extend(ti_)
              sign = S(1)
              t3 = gmul(*tall)*cf*sign
              return Box.__new__(Box,t3)
            elif arg_ == arg.down:
              ti = projection(arg.down,arg.up)*(arg.down<arg.down)
              t_i = BX.mv.args[:i-1]
              ti_ = BX.mv.args[i+1:]
              tall = []
              tall.extend(t_i)
              tall.append(ti)
              tall.extend(ti_)
              sign1 = (next(iter(BX.mv.args[i].up.grade)))%2
              sign2 = (next(iter(BX.mv.args[i+1].grade))-1)%2
              sign = S(-2)*(sign1*sign2)+1
              t3 = gmul(*tall)*cf*sign
              return Box.__new__(Box,t3)
            else :
              pass
      else :
        return expr
    else :
      return expr
  else :
    return expr


def gmul_2Rej(expr:"gmul")->Optional[GExpr]:
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gmul and (len(BX.mv.args)>=2):
      for i,arg in enumerate(BX.mv.args):
        if type(arg) == gextp:
          # Blade invertible should be of single grade
          if is_invertible(arg) and is_blade(arg):
            _arg = BX.mv.args[i-1] if i!=0 else None
            arg_ = BX.mv.args[i+1] if len(BX.mv.args)>(i+1) else None
            
            if _arg in arg.args and arg_ in arg.args:
              raise ValueError("Inversion Should have caught it.")
            elif _arg in arg.args :
              obj = [ele for ele in arg.args if ele!=_arg]
              ti = rejection(_arg,gextp(*obj))*(_arg<_arg)
              t_i = BX.mv.args[:i-1]
              ti_ = BX.mv.args[i+1:]
              tall = []
              tall.extend(t_i)
              tall.append(ti)
              tall.extend(ti_)
              sign1 = (next(iter(BX.mv.args[i-1].grade)))%2
              sign2 = (next(iter(BX.mv.args[i].grade)))%2
              sign = S(-2)*(sign1*sign2)+1
              t3 = gmul(*tall)*cf*sign
              return Box.__new__(Box,t3)            
            elif arg_ in arg.args:
              obj = [ele for ele in arg.args if ele!=arg_]
              ti = rejection(arg_,gextp(*obj))*(arg_<arg_)
              t_i = BX.mv.args[:i]
              ti_ = BX.mv.args[i+2:]
              tall = []
              tall.extend(t_i)
              tall.append(ti)
              tall.extend(ti_)
              sign = S(1)
              t3 = gmul(*tall)*cf*sign
              return Box.__new__(Box,t3)
            else :
              pass
def gmulhigher():
  gmul.ghigher = exhaust(do_one(gmul_2Inv,gmul_2Proj,gmul_2Rej))