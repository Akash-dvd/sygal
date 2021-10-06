from libs.Sygal.simplifications.simplify import aggregator ,simplification
from libs.Sygal.GV import GV
from libs.Sygal.GExpr import GExpr
from libs.Sygal.operators import (add,anticomm,comm,extp,
inprdct,lcntrct,mul,rcntrct)

a1 = GV('a_1')
a2 = GV('a_2')
a3 = GV('a_3')
b1 = GV('b_1')
b2 = GV('b_2')
b3 = GV('b_3')

def test_aggregator():
  a = GV("a")
  b = GV("b")
  c = GV("c")
  # lst = [(GV._rx, 0), (GV._rx, 1), (GV._oo, 2),(GV._oo,3),(GV._rx,4)]
  lst = [(a,0),(a,1),(b,2),(c,3),(c,4),(b,5),(a,6),(c,7),(b,8)]
  lst1 = aggregator(lst)
  # print(lst1)
  assert(lst1 == [(a, 0, 1, 6), (b, 2, 5, 8), (c, 3, 4, 7)])

def test_0():  
  assert( a1^a2 == a2^a1 )

def test_1():

  temp1 = ((a1|a2)^a3^(b1|b2))^(a1|(b1^b2^b3))
  ts1 = a1|(b3^b2^b1)
  ts2 = b1
  temp11 = temp1.subs(ts1,ts2)
  assert( temp11 == ((a1|a2)^a3^(b1|b2)^b1) )

# TODO SORT FOR EQUALITY
def test_2():

  temp1 = (GV._rx<(a2^a1))^a1^((GV._oo<(a2^a1))<(a3^a2^((GV._rx<(a2^a1)))))^(GV._rx<(a1^a3))^((GV._oo<(a2^a1))<(a1^b2^(GV._rx<(a2^a1))))^(GV._rx<(b1^b2))^(GV._rx<(b2^b3))

  _,rv = simplification.sandhi(temp1)
  print(rv)
  temp2 = (a1^(GV._rx<(b1^b2^b3))^((GV._oo<(a1^a2))<(a1^a2^a3^b2^(GV._rx<(a1^a2))))^(GV._rx<(a1^a2^a3)))

  assert( set(rv.args) == set(temp2.args) )


def test_3():
  
  temp = (GV._rx<(a1^a2))^(GV._rx<(a2^a3))^(GV._rx<(a3^b1))^GV._oo
  _,rv = simplification.sandhi(temp)
  assert(rv == (GV._rx<(b1^a1^a2^a3))^GV._oo )

def test_4():
  temp = (GV._rx<(a1^a2))^(GV._rx<(a2^a3))^(GV._rx<(a3^b1))^GV._oo
  _,rv = simplification.sandhi(temp)
  print(rv)
  assert(rv == (GV._rx<(b1^a1^a2^a3))^GV._oo )

def test_5():
  temp = (GV._oo<(GV._rx<(a1^a2^a3)^b1))^(GV._oo<(GV._rx<(a2^a3)^a1))
  _,rv = simplification.sandhi(temp)
  print(rv)
  assert False



# print(a1._x)


# printstr.display(temp)

# SIMPLIFICATIONS
# print(temp.sign())
# print(temp.dup_check())
# print(temp.sign())

#  HASH FOR LCNTRCT RCNTRCT COMM

print(GExpr.__mro__)
print(extp.__mro__)
