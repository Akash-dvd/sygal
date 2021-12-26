from collections.abc import Iterable

from sympy.utilities.iterables import kbins
from functools import reduce

"""
USAGE --

ALLOWED    - EVERYWHERE
NOTALLOWED - NOWHERE 
"""

def kbin_distri(range:int,bin:int) -> list:
  part = (list(kbins([1]*range, bin)))
  part1 = []
  for ele1 in part:
    lst1 = []
    for ele2 in ele1:
      lst1.append(reduce(lambda x,y:x+y,ele2,0))
    part1.append(lst1)
  return part1
