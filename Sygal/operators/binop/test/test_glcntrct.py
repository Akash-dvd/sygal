# Required for tests
import sys
sys.path.append('/app/solver')


from libs.Sygal.initial import *

"""
1)  Check higher to proj,rej
2)  Check for expansion
3)  Check for transformation to grcntrct
4)  Check for zero grade transformation
5)  Check for scalar behavior
"""

def test_glcntrct():
  assert True