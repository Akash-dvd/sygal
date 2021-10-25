from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union,NewType,Type,Any

from functools import reduce

from sympy import (
  diff, Rational, Symbol, S, Mul, Add, Expr,Pow,
  expand, simplify, eye, trigsimp,cos,sin,subsets,
  symbols, sqrt, Matrix, SympifyError, sympify
)

from libs.Sygal.utils.utils import parity

from libs.Sygal.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from libs.Sygal.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from libs.Sygal.strategies.tools import subs, typed ,canon
from libs.Sygal.strategies.traverse import (top_down, bottom_up, bxsall, top_down_once,bottom_up_once, basic_fns)
from libs.Sygal.strategies.tree import treeapply, greedy, allresults, brute

from libs.Sygal.GExpr import GExpr
from libs.Sygal.Box import Box

from libs.Sygal.operators.assop.gadd import gadd
from libs.Sygal.operators.assop.gextp import gextp
from libs.Sygal.operators.assop.gmul import gmul

from libs.Sygal.operators.binop.ganticomm import ganticomm
from libs.Sygal.operators.binop.gcomm import gcomm
from libs.Sygal.operators.binop.ginprdct import ginprdct
from libs.Sygal.operators.binop.grcntrct import grcntrct
from libs.Sygal.operators.binop.glcntrct import glcntrct

def difflist(t1,t2):
  return [ele for ele in t1 if ele not in t2]


def gmulexpand(expr,func=gmul,grade="all"):
  if(type(expr)==func):
    for i,ele in enumerate(expr.args):
      j=i+1
      if(j<len(expr.args)):
        lst = list(expr.args)
        fct1 =  (expr.args[i].grade == {1} ) 
        fct2 =  (expr.args[j].grade == {1} ) 
        fct3 =  (type(expr.args[i]) == gextp ) 
        fct4 =  (type(expr.args[j]) == gextp )
        if fct3:
          fct5 = reduce(lambda x, y: x and y, [ele.grade == {1} for ele in expr.args[i].args])
          
        if fct4:
          fct6 = reduce(lambda x, y: x and y, [ele.grade == {1} for ele in expr.args[j].args])

        # Both arguements must be either be of grade 1 or gextp each composed of grade 1 elements
        if((fct1 or fct5) and (fct2 or fct6)):
          lst[i] = mulexpansion(expr.args[i],expr.args[j])
          del lst[j]
          t = gmul(*lst)
          return t
      # No else here
    # Loop ends but no output then return
    return expr
  else:
    return expr

def mulexpansion(A,B):
  # Too smart arguement
  # If th e grade is one it cannot be binop 
  # Only sum is possible -> it will be converted to iter
  A_args = [A] if A.grade == {1}  else A.args
  B_args = [B] if B.grade == {1}  else B.args

  lst = []
  for i in range(0,min(len(A_args),len(B_args))+1):
    for Aset in subsets(A_args,i):
      for Bset in subsets(B_args,i):
        diffA = difflist(A_args,Aset)
        cpydiffA = []
        cpydiffA.extend(diffA)
        cpydiffA.extend(Aset)
        signA = parity(A_args,cpydiffA)
        diffB = difflist(B_args,Bset)
        cpydiffB = []
        cpydiffB.extend(Bset)
        cpydiffB.extend(diffB)
        signB = parity(B_args,cpydiffB)
        coeff = signA*signB
        if Aset:
          up = gextp(*Aset)
          low = gextp(*Bset)
          coeff1 = glcntrct(up,low).coeff
        else:
          coeff1 = S(1)
        diffA.extend(diffB)
        if diffA:
          mv = gextp(*diffA)
          bx = Box.__new__(Box,mv,Mul(coeff,coeff1))
          lst.append(bx)
        else :
          # bx = Box.__new__(Box,GExpr.Onl*Mul(coeff,coeff1))
          bx = Box.__new__(Box,GExpr.nl,Mul(coeff,coeff1))
          lst.append(bx)
  t = gadd(*lst)
  return t

canonicalize = exhaust((do_one(gmulexpand)))




gmul.gexpand = canonicalize