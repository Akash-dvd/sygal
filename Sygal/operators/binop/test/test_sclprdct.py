# Required for tests
import sys
import os

# Add /app to path for imports
if '/app' not in sys.path:
    sys.path.insert(0, '/app')

from Sygal.initial import *


"""
1)  Check for expansion insode scalar
2)  Check EVALUATION
3)  Check for zero grade transformation
4)  Check for inversion intraction with this
"""

def test_sclprdct():
  assert True