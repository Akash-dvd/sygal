from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from collections.abc import Iterable
from sympy.combinatorics.permutations import Permutation
from sympy.utilities.iterables import kbins
from functools import reduce
from collections import defaultdict

from sympy import S, Basic

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

def is_sortable_blade_arg(expr) -> bool:
  """True if ``expr`` may appear in ``gextp`` sort / parity (not str/scalar)."""
  if expr is None or isinstance(expr, str):
    return False
  if isinstance(expr, (int, float, bool)):
    return False
  if isinstance(expr, Basic) and expr is S.One:
    return False
  if not hasattr(expr, "grade"):
    return False
  try:
    g = expr.grade
  except Exception:
    return False
  if not g or g == {0}:
    return False
  return True


def filter_sortable_blade_args(args) -> tuple:
  """Drop strings, scalars, and other non-blades from ``gextp`` arg tuples."""
  return tuple(a for a in args if is_sortable_blade_arg(a))


def parity(args1:List,args2:List)->S:
  # ASSUMPTIONS
  # both arguements have unmixed grades
  # remove even grades , they are transparent to positional changes
  
  # Reimplement using something from permutation library
  a1 = filter_sortable_blade_args(args1)
  a2 = filter_sortable_blade_args(args2)
  if not a1 or not a2:
    return S.One
  t1 = [i for i in a1 if next(iter(i.grade)) % 2 == 1]
  d1 = dict()
  t2 = [i for i in a2 if next(iter(i.grade)) % 2 == 1]
  
  for index, value in enumerate(t1):
    d1[value.__hash__()] = [index]

  for index, value in enumerate(t2):
    d1[value.__hash__()].append(index)
  
  perm = []
  for index, (key, value) in enumerate(d1.items()):
    perm.append(value)
  
  perm1 = sorted(perm,key=lambda ele:ele[1])
  perm2 = [i[0] for i in perm1]

  p = Permutation(perm2)

  return S((p.parity()*-2)+1)

def GSortArgs(seq:Union[list,tuple],reverse:bool=False) -> Union[list,tuple]:
  """
  Sort Paritioned arguements based on Grades,names
  Complex arguement are put at last sorted by sum of their weights
  """

  newseq = sorted(seq,key=lambda ele:(len(ele.grade),next(iter(ele.grade)),ele.name,ele.__hash__()),reverse=reverse)
  return newseq
