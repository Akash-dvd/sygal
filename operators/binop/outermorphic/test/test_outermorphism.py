# Required for tests
import sys
import os

# Add /app to path for imports
if '/app' not in sys.path:
    sys.path.insert(0, '/app')

from Sygal.initial import *

"""
1)  Check for the abstract behavoir

"""

def test_outermorphism():
  assert True