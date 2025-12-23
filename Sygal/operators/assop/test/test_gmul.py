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


# Test cases for canonicalization
test_cases_canon = [
  (a1*a2*a2*a1*b1, (a1|a1)*b1*(a2|a2)),
  (na1*na1*a1, GExpr.Znl),
]

def test_gmul_simp():
  """Check adjacent scalar simplification."""
  transformation = canon_iter(gmul)
  assert all([transformation(x) == y for x, y in test_cases_canon])

# Higher

# Test cases for higher form to inversion
test_cases_higher_inv = [
  (a1*a1, a1|a1),
  (a1*a2*b1*a2*a1, inversion(a1,inversion(a2,b1))*(a1|a1)*(a2|a2)),
  (b1*(((a1|a2)+(a1^a2))*c1*c2*((a1|a2)+(a2^a1))),
   b1*inversion(((a1|a2)+(a2^a1)),c1*c2)*((a1|a1)*(a2|a2))),
  # This one needs upgrade
  (((a1|a2)+(a2^a1))*c1*c2*a1*a2, ((a1|a2)+(a2^a1))*c1*c2*a1*a2),
  ((a1^a2)*b1*(a1^a2), inversion(a1^a2,b1)*((a1^a2)|(a1^a2))),
  ((a1^a2)*b1*b2*(a1^a2), inversion(a1^a2,b1*b2)*((a1^a2)|(a1^a2))),
  (na1*na1*a1, GExpr.Znl),
  (na1*a1*na1, (na1|a1)*na1*2),
  (na1*a1*a1*na1, GExpr.Znl),
  # This one needs upgrade
  (na1*a1*a2*na1, na1*a1*a2*na1),
  (na1*a1*a2*na1*nb1*b1*nb1, na1*a1*a2*na1*2*(nb1|b1)*nb1),
]

def test_gmul_2Inv():
  """Check higher def to inv."""
  transformation = higher_iter(gmul)
  assert all([transformation(x) == y for x, y in test_cases_higher_inv])


# Test cases for higher form to projection
test_cases_higher_proj = [
  (((a1*a2)<(b1^b2^b3))*(b1^b2^b3),
   projection(b1^b2^b3,a1*a2)*((b1^b2^b3)|(b1^b2^b3))),
  (((b1^b2^b3)>(a1*a2))*(b1^b2^b3),
   projection(b1^b2^b3,a1*a2)*((b1^b2^b3)|(b1^b2^b3))),
]

def test_gmul_2Proj():
  """Check higher def to pro."""
  transformation = higher_iter(gmul)
  assert all([transformation(x) == y for x, y in test_cases_higher_proj])





# Test cases for higher form to rejection
test_cases_higher_rej = [
  (((b1^b2^b3^a1)*(a1), rejection(a1,b1^b2^b3)*(a1|a1))),
  ((a1*(b1^b2^b3^a1), rejection(a1,b1^b2^b3)*(a1|a1)*S(-1))),
  (((b1^b2^b3)^(a1*a2))*(b1^b2^b3),
   rejection(b1^b2^b3,a1*a2)*((b1^b2^b3)|(b1^b2^b3))),
  ((b1^b2^b3)*((b1^b2^b3)^(a1*a2)),
   rejection(b1^b2^b3,a1*a2)*((b1^b2^b3)|(b1^b2^b3))),
]

def test_gmul_2Rej():
  """Check higher def to rej."""
  transformation = higher_iter(gmul)
  assert all([transformation(x) == y for x, y in test_cases_higher_rej])

