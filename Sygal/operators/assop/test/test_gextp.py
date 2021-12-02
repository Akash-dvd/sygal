# Required for tests
import sys
sys.path.append('/app/solver')

from libs.Sygal.initial import *


from functools import reduce
from operator import and_

from libs.Sygal.operators.assop.simplify.gextpsimp import concat

"""
1)  Check anti-commutivity
2)  Check sorting ,hash order independent
3)  Check concatenation mv
4)  Check concatenation correct coefficient
5)  Check pseudoscalar 
6)  Check local pseudoscalar 
7)  Check simplification for inv,pro,rej
8)  Check for concatenated <,> -> ^ 
9)  Check for grade zero symplification \
    a>(b^c)^a -> a<(b^c^a)
10) Check for local pseudoscalar concat symp \
    a>(c^d)^b<(e^f) -> a^b<(c^d^e^f) when a|e,f = b|c,d = 0 
11) Check for proj^proj^proj ... simplification
12) Check for rej^rej^rej ... simplification
13) Check unmixed grade ordering a1^(a2*a3)^a4
TODO
1) ((a1^a2..a_r)<((b1..br)^(c1..cm)))^((a1..a_r)<((b1..br)^(d1..dn))) ==
(a1^a2..a_r)<((b1..br)^(c1..cm)^(d1..dn))
Will be done after implementing dot product and multiplication.
"""

def test_aggregator():

  # lst = [(rx, 0), (rx, 1), (oo, 2),(oo,3),(rx,4)]
  lst = [(a1,0),(a1,1),(b1,2),(c1,3),(c1,4),(b1,5),(a1,6),(c1,7),(b1,8)]
  lst1 = concat.aggregator(lst)
  # print(lst1)
  assert(lst1 == [(a1, 0, 1, 6), (b1, 2, 5, 8), (c1, 3, 4, 7)])

def test_0():  
  assert( (a1^a2).mv == (a2^a1).mv 
  and ((a1^a2).coeff + (a2^a1).coeff) == 0 
  )


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

