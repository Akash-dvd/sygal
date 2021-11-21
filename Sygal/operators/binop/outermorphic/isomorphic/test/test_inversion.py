# Required for tests
import sys
sys.path.append('/app/solver')


from libs.Sygal.initial import *

"""
1)  Check for expansion
2)  Check for higher IaIb -> Iab
3)  Check for higher to dilation,rotation,translation 
3)  Check for pull back
4)  Check for push forward
5)  Check for aIb = -a ,+a simplification
6)  Check for scalar sub and obj case
"""

def test_inversion():
  assert True