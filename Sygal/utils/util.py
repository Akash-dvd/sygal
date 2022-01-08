from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from collections.abc import Iterable
from sympy.combinatorics.permutations import Permutation
from sympy.utilities.iterables import kbins
from functools import reduce
from collections import defaultdict

from sympy import S

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

def parity(args1:List,args2:List)->S:
  # ASSUMPTIONS
  # both arguements have unmixed grades
  # remove even grades , they are transparent to positional changes
  
  # Reimplement using something from permutation library
  t1 = [i for i in args1 if next(iter(i.grade))%2==1 ]
  d1 = dict()
  t2 = [i for i in args2 if next(iter(i.grade))%2==1 ]
  
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
