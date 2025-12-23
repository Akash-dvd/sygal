# # Required for tests
# import sys
# sys.path.append('/app/solver')

from Sygal.initial import *
from Sygal.strategies.iters import canon_iter

"""
1)  Check commutivity
2)  Check sorting ,hash order independent
3)  Check 1 coefficient
4)  Check for removal of zero coeffs
5)  Check distribution
6)  Check distribution inside coeff


TODO
1) gadd -> gmul , INV etc
"""
# Test cases for commutativity
test_cases_commu = [
  (a1+a2+(a2^a3), a1+(a2^a3)+a2),
]

def test_gadd_commu():
  """Test commutativity of gadd."""
  # Commutativity is a property, not a transformation - just check equality
  assert all([x == y for x, y in test_cases_commu])

# Test cases for coefficient handling
test_cases_coeff = [
  ((a1<a2)*(b1+2+(b2^b3))*3, 3*((a2<a1)*2+(a2<a1)*b1+(a2<a1)*(b2^b3))),
]

def test_gadd_coeff():
  """Test coefficient handling in gadd."""
  # Coefficient handling is a property - just check equality
  assert all([x == y for x, y in test_cases_coeff])

# Test cases for zero removal
test_cases_zero = [
  (a1+a2+(a2^a3)-a2, a1+(a2^a3)),
]

def test_gadd_zero():
  """Test zero removal in gadd."""
  # Zero removal could be considered canonicalization
  transformation = canon_iter(gadd)
  assert all([transformation(x) == y for x, y in test_cases_zero])

# Test cases for distribution over gadd
test_cases_distri = [
  ((a1^a2)+(a2^a1), GExpr.Znl),
  # This has issue not [0!a1^a2] [0!_nl] 
  
  ((a2+a2)^(b1), (a2^b1*2)),
  
  ((a1+a2)^(b1+b2), (a1^b1)+(a1^b2)+(a2^b1)+(a2^b2)),
  
  ((a1+a2)*(b1+b2), (a1*b1)+(a1*b2)+(a2*b1)+(a2*b2)),
  
  (projection(a1,a2+a3), projection(a1,a2)+projection(a1,a3)),
  
  (projection(a2+a3,a1), projection(a2+a3,a1)),
  
  (rejection(a2+a3,a1), rejection(a2,a1)+rejection(a3,a1)),
  
  (rejection(a1,a2+a3), rejection(a1,a2+a3)),
  
  (inversion(a1,a2+a3), inversion(a1,a2)+inversion(a1,a3)),
  
  (inversion(a1,a2+a3)<inversion(b1,b2+b3),
   (inversion(a1,a2)<inversion(b1,b2))+
   (inversion(a1,a2)<inversion(b1,b3))+
   (inversion(a1,a3)<inversion(b1,b2))+
   (inversion(a1,a3)<inversion(b1,b3))),
  
  ((a1+projection(a2,a3<((b1+b2)^c1))),
   a1+projection(a2,a3<(b1^c1))+projection(a2,a3<(b2^c1)))
]

def test_gadd_distri():
  """Test distribution over gadd."""
  transformation = GExpr.gdistribute
  assert all([transformation(x) == y for x, y in test_cases_distri])

# Test cases for distribution with coefficients
test_cases_distri_coeff = [
  ((a1<(a2+a3))*2, (a1<a2)*2+(a1<a3)*2),
  ((a2+a3*3)<a1, (a1<a2)+(a1<a3)*3),
]

def test_gadd_distri_coeff():
  """Test distribution over gadd with coefficients."""
  transformation = GExpr.gdistribute
  assert all([transformation(x) == y for x, y in test_cases_distri_coeff])


