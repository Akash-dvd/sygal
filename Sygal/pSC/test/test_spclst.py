# Required for tests
import sys
import os

# Add /app to path for imports
if '/app' not in sys.path:
    sys.path.insert(0, '/app')

from Sygal.initial import *
from Sygal.pSC.spclst import spclst
from Sygal.pSC.spcdct import spcdct


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