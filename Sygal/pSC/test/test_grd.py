# Required for tests
import sys
import os

# Add /app to path for imports
if '/app' not in sys.path:
    sys.path.insert(0, '/app')

from Sygal.initial import *


def test_grd():

  test_cases = [
  (grd(1,2),
  grd(1,2)),
  (grd(2,1),
  grd(8,None)),
  (grd(-2,-1),
  grd(8,None)),
  (grd(-1,-2),
  grd(None,8)),
  ]

  assert all([ele1==ele2 for ele1,ele2 in test_cases])
