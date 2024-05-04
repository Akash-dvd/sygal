# Required for tests
# import sys
# sys.path.append('/app/solver')

from Sygal.initial import *



def test_subs():

  temp1 = ((a1<(a2^a3))^(b1<(b2^b3)))^(a1<(b1^b2^a3))^a3
  ts1 = a1<(b1^b2^a3)
  ts2 = b1
  temp11 = temp1.subs((ts1,ts2))
  print("eexpr",((a1<(a2^a3))^a3^(b1<(b2^b3)))^b1)
  assert( temp11 == ((a1<(a2^a3))^a3^(b1<(b2^b3)))^b1 )