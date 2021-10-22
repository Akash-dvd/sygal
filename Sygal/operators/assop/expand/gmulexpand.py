from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union,NewType,Type,Any

from sympy import (
  diff, Rational, Symbol, S, Mul, Add, Expr,Pow,
  expand, simplify, eye, trigsimp,cos,sin,subsets,
  symbols, sqrt, Matrix, SympifyError, sympify
)

from libs.Sygal.utils import parity

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

def difflist(t1,t2):
  return [ele for ele in t1 if ele not in t2]


def gmulexpand(self):
  expr = self

def expand(A,B):
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


gmul.gexpand = gmulexpand