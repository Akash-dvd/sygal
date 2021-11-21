# Required for tests
import sys
sys.path.append('/app/solver')

from libs.Sygal.initial import *

"""
1)  Check for invertible pair
2)  Check for blade
3)  Check for vecblade
4)  Check for versor
5)  Check inversion
6)  Check get_grade
7)  Check for null

"""
test_cases1 = [
(a1*a2,
a2*a1),

((a1<a2)+(a1^a2),
((a1<a2)-(a1^a2))*3),

(inversion(a1,a2),
inversion(a1,a2)),


]

def test_is_invertiblePair():
  assert reduce(lambda x, y: x and y, [is_invertiblePair(ele1, ele2) for ele1,ele2 in test_cases1])


test_cases2 = [
(a1*a2,
a1*a2),


((a1<a2)+(a1^a2),
((a1<a2)+(a1^a2))*3),

((a1)<(b1^b2^b3),
(a1)<(b1^b2^b3))
]

def test_is_not_invertiblePair():
  assert not reduce(lambda x, y: x and y, [is_invertiblePair(ele1, ele2) for ele1,ele2 in test_cases2])


def test_is_null():
  assert True

def test_is_invertible():
  assert True

def test_is_blade():
  assert True

def test_is_vecBlade():
  assert True

def test_is_versor():
  assert True

def test_get_grade():
  assert True

