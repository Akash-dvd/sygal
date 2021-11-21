# Required for tests
import sys
sys.path.append('/app/solver')

from libs.Sygal.initial import *

"""
1)  Check adjacent scalar simplification
2)  Check expansion
3)  Check behavoir if add is present in arguements
5)  Check pseudoscalar 
6)  Check local pseudoscalar 
7)  Check higher def to inv,pro,rej
8)  Check for null*a1*a2...*null \
    does it lead to rej*rej*rej 

"""

def test_gmul():
  assert True