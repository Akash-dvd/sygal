from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union,NewType,Type,Any

from sympy import (
  diff, Rational, Symbol, S, Mul, Add, Expr,Pow,
  expand, simplify, eye, trigsimp,cos,sin,subsets,
  symbols, sqrt, Matrix, SympifyError, sympify
)

from sympy.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from sympy.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from sympy.strategies.tools import subs, typed ,canon
from sympy.strategies.traverse import (top_down, bottom_up, sall, top_down_once,bottom_up_once, basic_fns)
from sympy.strategies.tree import treeapply, greedy, allresults, brute


from libs.Sygal.GExpr import GExpr
from libs.Sygal.Box import Box
from libs.Sygal.utils import Boxify,parity

from libs.Sygal.operators import (gadd,ganticomm,gcomm,gextp,
ginprdct,glcntrct,gmul,grcntrct)

from libs.Sygal.operators.hdef import hdef,projection,inversion,rejection

def gmulexpansion(mv):
  for i in range(0,min(len(A.args),len(B.args))+1):
    for Aset in subsets(A.args,i):
      for Bset in subsets(B.args,i):
        diffA = difflist(A.args,Aset)
        cpydiffA = []
        cpydiffA.extend(diffA)
        cpydiffA.extend(Aset)
        signA = parity(A.args,cpydiffA)
        diffB = difflist(B.args,Bset)
        cpydiffB = []
        cpydiffB.extend(Bset)
        cpydiffB.extend(diffB)
        signB = parity(B.args,cpydiffB)
        coeff = signA*signB
        coeff1 = cl2(Aset,Bset)
        diffA.extend(diffB)
        mv = cl1(*diffA)
        # print("({"+coeff+"}"+" "+mv+")")
        print("(", end='')
        print("{", end='')
        print(coeff, end=' ')
        print("*", end=' ')
        print(coeff1, end=' ')
        print("}", end=' ')
        print(mv, end='')
        print(")")
  
  
  pass


def gsimplification(expr:GExpr):
  # Pattern Matching for Box or bare expr
  if(type(expr)==Box):
    coeff = expr.args[0]
    mv = expr.args[1]
  else :
    coeff = S(1)
    mv = expr

  # sum distribution
  if(type(mv)==gadd):  
    distribute(gextp,gadd)
    distribute(gmul,gadd)

  # multiplication expansion
  if(type(mv)==gmul):
    gmulexpansion(mv)

  # right to left conversion
  if(type(mv)==grcntrct):
    pass


  # left , right contract concatenation

  if(type(mv) == glcntrct):
    
    

  # left and right expansion


  
  
  
  
  
  
  
  
    pass

def difflist(t1,t2):
  l1 = list(t1)
  l2 = list(t2)
  for ind,ele in enumerate(l1):
    if ele in l2:
      l1[ind] = None
  return list(filter((None).__ne__, l1))

gextpDist = distribute(gextp,gadd)
gmulDist = distribute(gmul,gadd)
glcntrctDist = distribute(glcntrct,gadd)
grcntrctDist = distribute(grcntrct,gadd)

gmulrules = (
  gmulexpansion,gmulDist
)

gextprules = (
  gmulDist
)




canonicalize = exhaust(typed({gmul: do_one(*gmulrules),
gextp:do_one(*gextprules)}))

