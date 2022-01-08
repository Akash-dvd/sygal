# Required for tests
import sys
sys.path.append('/app/solver')

from libs.Sygal.initial import *


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
