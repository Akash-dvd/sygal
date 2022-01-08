# Required for tests
import sys
sys.path.append('/app/solver')

from libs.Sygal.initial import *

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

def test_0():  
  assert( (a1^a2).mv == (a2^a1).mv 
  and ((a1^a2).coeff + (a2^a1).coeff) == 0 
  )




def test_sandhi():
  # TODO SORT FOR EQUALITY

  test_cases = [
  ((A1<(B1^B2))^(A1<(B2^B3)),
  A1<(B1^B2^B3)),

  ((B3^(A1<(B1^B2^A2)))^(A1<(B2^B3))^(B2<(B1^B3))^(B2<(A2^B3)),
  (B3^(A1<(B1^B2^B3^A2)))^(B2<(A2^B1^B3))),

  (A2^(A1<(((B1<(A1^A2))^B2^B3)))^(A1<(((B1<(A1^A2))^A2))),
  A2^(A1<(((B1<(A1^A2))^A2^B2^B3)))), 

  (A2^(A1<(((B1<(A1^A2^A3))^B2)))^(A1<(((B1<(A1^A2))^B3))),
  A2^(A1<(((B1<(A1^A2^A3))^B2^B3)))), 

  ((A1<(B1^(B3<(A1^(B2<(A1^A2^A3^B1))))))^(A1<(B2^(B3<(A2^(B2<(A1^A2^A3)))))),
  A1<(B1^B2^(B3<(A1^A2^(B2<(A1^A2^A3^B1)))))),

  ((A1<(A2^A3^(rx<(A1^A2))))^(A1<(B2^B3^(rx<(A1^A2)))),
  A1<(A2^A3^B2^B3^(rx<(A1^A2)))),

  ((rx<(A2^A1))^A1^((oo<(A2^A1))<(A3^A2^((rx<(A2^A1)))))^(rx<(A1^A3))^((oo<(A2^A1))<(A1^B2^(rx<(A2^A1))))^(rx<(B1^B2))^(rx<(B2^B3)),
  (A1^(rx<(B1^B2^B3))^((oo<(A1^A2))<(A1^A2^A3^B2^(rx<(A1^A2))))^(rx<(A1^A2^A3))))

  ]

  assert all([(canon_iter(gextp)(x)).mv == y.mv for x, y in test_cases])


def test_gmul_2Proj():
  test_cases = [
  ((a1<(a2^a3))^(a1<(a3^a4)),
  (a1|a3)*(a1<(a2^a3^a4))),

  (((A1^A2)<(B1^B2^C1^C2))^((A1^A2)<(B1^B2^D1^D2))^((A1^A2)<(D1^D2^B4^C4)),
  (((A1^A2)|(B1^B2))*((A1^A2)|(D1^D2)))*((A1^A2)<(B1^B2^C1^C2^D1^D2^B4^C4))),
 
  (((A1^A2)<(B1^B2^B3))^((A1)<((A2<(B1^B2))^B3)),
  ((A1^A2)|(B1^B2))*((A1)<(B3^(A2<(B1^B2^B3))))),

  (((A1^A2^A3)<(B1^B2^B3^C1^C2))^((A1^A2^A3)<(B1^B2^B3^D1^D2))^((A1^A2^A3)<(B1^B2^B3^B4^C4)),
  ((A1^A2^A3)|(B1^B2^B3))**2*((A1^A2^A3)<(B1^B2^B3^C1^C2^D1^D2^B4^C4))),

  ((D1<(A1^A2^(D2<(B1^B2^(D3<(C1^C2^C3))))))^(D1<(A3^A4^(D2<(B3^B4^(D3<(C1^C2^C3^C4)))))),
  ((D1^D2^D3)|(C1^C2^C3))*(D1<(A1^A2^A3^A4^(D2<(B1^B2^B3^B4^(D3<(C1^C2^C3^C4))))))),

  (((A1^A2)<(B1^B2^B3))^(A1<((A2<(B1^B2))^B4)),
  ((A1^A2)|(B1^B2))*(A1<((A2<(B1^B2^B3))^B4)))

  ]

  assert all([canon_iter(gextp)(x) == y for x, y in test_cases])


def test_3():
  
  temp = (rx<(a1^a2))^(rx<(a2^a3))^(rx<(a3^b1))^oo
  rv = canon_iter(gextp)(temp)
  print(rv)
  assert(rv == (rx<(b1^a1^a2^a3))^oo )



def test_zero():
  pass

