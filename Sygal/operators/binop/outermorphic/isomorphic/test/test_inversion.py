# Required for tests
# import sys
# sys.path.append('/app/solver')


from Sygal.initial import *

"""
1)  Check for expansion
2)  Check for higher IaIb -> Iab
3)  Check for higher to dilation,rotation,translation 
3)  Check for pull back
4)  Check for push forward
5)  Check for aIb = -a ,+a simplification
6)  Check for scalar sub and obj case
7)  Check simplification per,par

"""
# Test cases for higher form of inversion
test_cases_higher = [
  (inversion(a3,inversion(a2,inversion(a1,b1))), inversion(a1*a2*a3,b1)),
]

def test_inversion_higher():
  """Test higher form of inversion."""
  transformation = higher_iter(inversion)
  assert all([transformation(x) == y for x, y in test_cases_higher])

# appendtoDict(na2,{na1:S(0)})
# t10 = inversion(na1^na2,na2)
# print(t10)
# t10_1 = simplify_iter(inversion)(t10)
# print(t10_1)