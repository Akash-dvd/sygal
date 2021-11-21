# Required for tests
import sys
sys.path.append('/app/solver')


from libs.Sygal.initial import *

"""
1)  Check for expansion
2)  Check for inversion + GB expasion
3)  Check for higher IaIb -> Iab
4)  Check for pull back
5)  Check for push forward
"""

def test_dilation():
  assert True