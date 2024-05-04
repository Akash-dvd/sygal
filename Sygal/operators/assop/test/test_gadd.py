# # Required for tests
# import sys
# sys.path.append('/app/solver')

from Sygal.initial import *

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
def test_gadd_commu():
  assert a1+a2+(a2^a3) == a1+(a2^a3)+a2

def test_gadd_coeff():
  t1 = (a1<a2)*(b1+2+(b2^b3))*3
  t2 = 3*((a2<a1)*2+(a2<a1)*b1+(a2<a1)*(b2^b3))
  assert t1 == t2

def test_gadd_zero():
  assert a1+a2+(a2^a3)-a2 == a1+(a2^a3)

test_cases1 = [
((a1^a2)+(a2^a1),
GExpr.Znl),
# This has issue not [0!a1^a2] [0!_nl] 

((a2+a2)^(b1),
(a2^b1*2)),

((a1+a2)^(b1+b2),
(a1^b1)+(a1^b2)+(a2^b1)+(a2^b2)),

((a1+a2)*(b1+b2),
(a1*b1)+(a1*b2)+(a2*b1)+(a2*b2)),

((a1+a2)*(b1+b2),
(a1*b1)+(a1*b2)+(a2*b1)+(a2*b2)),


(projection(a1,a2+a3),
projection(a1,a2)+projection(a1,a3)),

(projection(a2+a3,a1),
projection(a2+a3,a1)),

(rejection(a2+a3,a1),
rejection(a2,a1)+rejection(a3,a1)),

(rejection(a1,a2+a3),
rejection(a1,a2+a3)),

(inversion(a1,a2+a3),
inversion(a1,a2)+inversion(a1,a3)),

(inversion(a1,a2+a3)<inversion(b1,b2+b3),
(inversion(a1,a2)<inversion(b1,b2))+
(inversion(a1,a2)<inversion(b1,b3))+
(inversion(a1,a3)<inversion(b1,b2))+
(inversion(a1,a3)<inversion(b1,b3))
),

((a1+projection(a2,a3<((b1+b2)^c1))),
a1+projection(a2,a3<(b1^c1))+projection(a2,a3<(b2^c1)))
]

def test_gadd_distri():
  assert reduce(lambda x, y: x and y, [(GExpr.gdistribute(ele1) == ele2) for ele1,ele2 in test_cases1])

test_cases2 = [
((a1<(a2+a3))*2,
(a1<a2)*2+(a1<a3)*2),

((a2+a3*3)<a1,
(a1<a2)+(a1<a3)*3),

]

def test_gadd_distri_coeff():
  assert reduce(lambda x, y: x and y, [(GExpr.gdistribute(ele1) == ele2) for ele1,ele2 in test_cases2])


