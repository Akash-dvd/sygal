# Required for tests
# import sys
# sys.path.append('/app/solver')

from initial import *


def test_init():
  test_cases = [
  
  (bool([]),
  False),

  (bool({}),
  False),

  (bool([{}]),
  True),

  (bool(spclst([{}])),
  False),

  (bool(spclst([spcdct({})])),
  False),

  (spclst([{}]),
  []),

  ]

  assert all([ele1==ele2 for ele1,ele2 in test_cases])