# Required for tests
import sys
sys.path.append('/app/solver')

from functools import reduce
from operator import and_

from libs.Sygal.GV import GV
from libs.Sygal.operators import (add,anticomm,comm,extp,
inprdct,lcntrct,mul,rcntrct)

from libs.Sygal.simplifications.simplify import concat

from sympy import (
    diff, Rational, Symbol, S, Mul, Add, Expr,
    expand, simplify, eye, trigsimp,cos,sin,
    symbols, sqrt, Matrix, SympifyError, sympify
)

from libs.Sygal.operators.operators1 import opextp,oplcntrct,opsum,opmul

from sympy.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from sympy.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from sympy.strategies.tools import subs, typed ,canon
from sympy.strategies.traverse import (top_down, bottom_up, sall, top_down_once,bottom_up_once, basic_fns)
from sympy.strategies.tree import treeapply, greedy, allresults, brute

a1 = GV('a_1')
a2 = GV('a_2')
a3 = GV('a_3')
b1 = GV('b_1')
b2 = GV('b_2')
b3 = GV('b_3')
c1 = GV('c_1')
c2 = GV('c_2')
c3 = GV('c_3')
d1 = GV('d_1')
d2 = GV('d_2')
d3 = GV('d_3')
rx = GV._rx
oo = GV._oo

test_cases1 = [
  (opextp(a1,a1,opsum(1,a1)),
  {2,3}),
  (opsum(opextp(a1,a1,opsum(1,a1)),opextp(a1,a1)),
  {2,3}),
  (opsum(1,opextp(a1,a1,a1)),
  {0,3}),
  (oplcntrct(opsum(opextp(a1,a1,opsum(1,a1)),opextp(a1,a1)),opsum(1,opextp(a1,a1,a1))),
  {1,0}),
  
]

def test_1():
  assert reduce(and_, [x.grade == y for x, y in test_cases1])

test_cases2 = [
  (opmul(a1,5,a2,oplcntrct(opextp(a1,a2),opextp(b1,b2,4))),
  {5,4,oplcntrct(opextp(a1,a2),opextp(b1,b2))}),
  (opmul(oplcntrct(a1,b1),a1),
  {oplcntrct(a1,b1)}),
  
]

def test_2():
  x = opmul(oplcntrct(a1,b1),a1)
  print(x.coeffs)
    # assert(set(x.coeffs) == y)
  # print([i.coeffs for i,j in test_cases2])
  # assert False
  # assert reduce(and_, [set(x.coeffs) == y for x, y in test_cases2])



test_2()