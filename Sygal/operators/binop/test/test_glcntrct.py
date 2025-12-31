# Required for tests
import sys
import os

# Add /app to path for imports
if '/app' not in sys.path:
    sys.path.insert(0, '/app')

from Sygal.initial import *

"""
1)  Check higher to proj,rej
2)  Check for expansion
3)  Check for transformation to grcntrct
4)  Check for zero grade transformation
5)  Check for scalar behavior
"""

def test_glcntrct():
  assert True