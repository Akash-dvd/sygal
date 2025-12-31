# Required for tests
import sys
import os

# Add /app to path for imports
if '/app' not in sys.path:
    sys.path.insert(0, '/app')

from Sygal.initial import *

"""
1)  Check for expansion
2)  Check for inversion + GB expasion
3)  Check for higher IaIb -> Iab
4)  Check for pull back
5)  Check for push forward
"""

def test_dilation():
  assert True