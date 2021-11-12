# Required for tests
import sys
sys.path.append('/app/solver')

from libs.Sygal.initial import *


from functools import reduce
from operator import and_

from libs.Sygal.operators.assop.simplify.gextpsimp import concat



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

