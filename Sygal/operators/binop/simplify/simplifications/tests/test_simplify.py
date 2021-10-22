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


def test_aggregator():
  a = GV("a")
  b = GV("b")
  c = GV("c")
  # lst = [(rx, 0), (rx, 1), (oo, 2),(oo,3),(rx,4)]
  lst = [(a,0),(a,1),(b,2),(c,3),(c,4),(b,5),(a,6),(c,7),(b,8)]
  lst1 = concat.aggregator(lst)
  # print(lst1)
  assert(lst1 == [(a, 0, 1, 6), (b, 2, 5, 8), (c, 3, 4, 7)])

def test_0():  
  assert( a1^a2 == a2^a1 )


# TODO SORT FOR EQUALITY

test_cases = [
((a1<(b1^b2))^(a1<(b2^b3)),
a1<(b1^b2^b3)),

((b3^(a1<(b1^b2^a2)))^(a1<(b2^b3))^(b2<(b1^b3))^(b2<(a2^b3)),
(b3^(a1<(b1^b2^b3^a2)))^(b2<(a2^b1^b3))),

(a2^(a1<(((b1<(a1^a2))^b2^b3)))^(a1<(((b1<(a1^a2))^a2))),
a2^(a1<(((b1<(a1^a2))^a2^b2^b3)))), 

(a2^(a1<(((b1<(a1^a2^a3))^b2)))^(a1<(((b1<(a1^a2))^b3))),
a2^(a1<(((b1<(a1^a2^a3))^b2^b3)))), 

((a1<(b1^(b3<(a1^(b2<(a1^a2^a3^b1))))))^(a1<(b2^(b3<(a2^(b2<(a1^a2^a3)))))),
a1<(b1^b2^(b3<(a1^a2^(b2<(a1^a2^a3^b1)))))),

((a1<(a2^a3^(rx<(a1^a2))))^(a1<(b2^b3^(rx<(a1^a2)))),
a1<(a2^a3^b2^b3^(rx<(a1^a2)))),

((rx<(a2^a1))^a1^((oo<(a2^a1))<(a3^a2^((rx<(a2^a1)))))^(rx<(a1^a3))^((oo<(a2^a1))<(a1^b2^(rx<(a2^a1))))^(rx<(b1^b2))^(rx<(b2^b3)),
(a1^(rx<(b1^b2^b3))^((oo<(a1^a2))<(a1^a2^a3^b2^(rx<(a1^a2))))^(rx<(a1^a2^a3))))

]

def test_sandhi():
    assert reduce(and_, [concat.sandhi(x) == y for x, y in test_cases])



def test_3():
  
  temp = (rx<(a1^a2))^(rx<(a2^a3))^(rx<(a3^b1))^oo
  rv = concat.sandhi(temp)
  print(rv)
  assert(rv == (rx<(b1^a1^a2^a3))^oo )



def test_zero():
  pass

