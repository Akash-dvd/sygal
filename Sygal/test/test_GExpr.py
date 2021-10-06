# Required for tests
import sys
sys.path.append('/app/solver')

from functools import reduce
from operator import and_

from libs.Sygal.simplifications.simplify import concat
from libs.Sygal.GV import GV
from libs.Sygal.GExpr import GExpr
from libs.Sygal.operators import (add,anticomm,comm,extp,
inprdct,lcntrct,mul,rcntrct)

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

def test_subs():

  temp1 = ((a1<(a2^a3))^(b1<(b2^b3)))^(a1<(b1^b2^a3))^a3
  ts1 = a1<(b1^b2^a3)
  ts2 = b1
  temp11 = temp1.subs((ts1,ts2))
  print("eexpr",((a1<(a2^a3))^a3^(b1<(b2^b3)))^b1)
  assert( temp11 == ((a1<(a2^a3))^a3^(b1<(b2^b3)))^b1 )