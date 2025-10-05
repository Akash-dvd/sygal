# Required for tests
# import sys
# sys.path.append('/app/solver')

from Sygal.initial import *

"""
1)  Check adjacent scalar simplification
2)  Check expansion
3)  Check behavoir if add is present in arguements
5)  Check pseudoscalar 
6)  Check local pseudoscalar 
7)  Check higher def to inv,pro,rej
8)  Check for null*a1*a2...*null \
    does it lead to rej*rej*rej 

"""



def test_gmul_expand():
  assert True


def test_gmul_simp():
  """
  1)  Check adjacent scalar simplification
  """
  test_cases1 = [
  (a1*a2*a2*a1*b1,
  (a1|a1)*b1*(a2|a2)),
  
  (na1*na1*a1,
  GExpr.Znl),
  
  ]

  assert reduce(lambda x,y: x and y, [canon_iter(gmul)(x) == y for x, y in test_cases1])

# Higher

def test_gmul_2Inv():
  """
  7)  Check higher def to inv
  """
  test_cases2 = [
  (a1*a1,
  a1|a1),
  
  (a1*a2*b1*a2*a1,
  inversion(a1,inversion(a2,b1))*(a1|a1)*(a2|a2)),

  (b1*(((a1|a2)+(a1^a2))*c1*c2*((a1|a2)+(a2^a1))) ,
  b1*inversion(((a1|a2)+(a2^a1)),c1*c2)*((a1|a1)*(a2|a2))),

  # This one needs upgrade
  (((a1|a2)+(a2^a1))*c1*c2*a1*a2,
  ((a1|a2)+(a2^a1))*c1*c2*a1*a2),


  ((a1^a2)*b1*(a1^a2)
  ,inversion(a1^a2,b1)*((a1^a2)|(a1^a2))),

  ((a1^a2)*b1*b2*(a1^a2)
  ,inversion(a1^a2,b1*b2)*((a1^a2)|(a1^a2))),

  (na1*na1*a1,
  GExpr.Znl),
  
  (na1*a1*na1,
  (na1|a1)*na1*2),

  (na1*a1*a1*na1,
  GExpr.Znl),

  # This one needs upgrade
  (na1*a1*a2*na1,
  na1*a1*a2*na1),
  
  (na1*a1*a2*na1*nb1*b1*nb1,
  na1*a1*a2*na1*2*(nb1|b1)*nb1),
  ]

  assert reduce(lambda x,y: x and y, [higher_iter(gmul)(x) == y for x, y in test_cases2])


def test_gmul_2Proj():
  """
  7)  Check higher def to pro
  """
  test_cases3 = [
  (((a1*a2)<(b1^b2^b3))*(b1^b2^b3),
  projection(b1^b2^b3,a1*a2)*((b1^b2^b3)|(b1^b2^b3))),

  (((b1^b2^b3)>(a1*a2))*(b1^b2^b3),
  projection(b1^b2^b3,a1*a2)*((b1^b2^b3)|(b1^b2^b3))),

  ]

  assert reduce(lambda x,y: x and y, [higher_iter(gmul)(x) == y for x, y in test_cases3])





def test_gmul_2Rej():

  """
  7)  Check higher def to rej
  """
  test_cases4 = [
  (((b1^b2^b3^a1)*(a1),
  rejection(a1,b1^b2^b3)*(a1|a1))),

  ((a1*(b1^b2^b3^a1),
  rejection(a1,b1^b2^b3)*(a1|a1)*S(-1))),

  (((b1^b2^b3)^(a1*a2))*(b1^b2^b3),
  rejection(b1^b2^b3,a1*a2)*((b1^b2^b3)|(b1^b2^b3))),

  ((b1^b2^b3)*((b1^b2^b3)^(a1*a2)),
  rejection(b1^b2^b3,a1*a2)*((b1^b2^b3)|(b1^b2^b3))),  

  ]
  xx = higher_iter(gmul)(((b1^b2^b3)^(a1*a2))*(b1^b2^b3))
  assert reduce(lambda x,y: x and y, [higher_iter(gmul)(x) == y for x, y in test_cases4])

