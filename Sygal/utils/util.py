from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from collections.abc import Iterable

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


class relDt(dict):

  def __init__(self:"relDt",*args) -> None:
    if len(args) == 0:
      super().__init__()
    elif len(args) == 1:
      arg = args[0]
      if type(arg) == relDt:
        super().__init__(arg)
        return None
      elif issubclass(type(arg),dict):
        t_dict = {}
        for k,v in arg.items():
          if type(k).__name__ == "Box":
            if k.coeff == S(1): 
              k1 = k.mv
            else:
              raise ValueError("Box has non-1 coeff")
          else:
            k1 = k
          t_dict[k1] = v
        super().__init__(t_dict)
      else :
        raise ValueError("Dict required as arguement")
    else:
      raise ValueError("More tahn one arguement not allowed")
  
  def update(self:"relDt",arg:Union[dict,"relDt"]) -> None:
    if issubclass(type(arg), dict):
      t_dct = {}
      t_dct.update(self)
      for k,v in arg.items():
        if (type(k).__name__ == "Box"):
          k1 = k.mv
        else :
          k1 = k
        t_dct.update({k1:v})
      super().clear()
      super().update(t_dct)

    else :
      ValueError("Arg must be type spcdct")

  def __getitem__(self:"relDt", key)  -> "relDt" :
    if type(key).__name__ == "Box":
      key1 = key.mv
    else:
      key1 = key
    return self.get(key1,None)

  def __setitem__(self:"relDt", key, newvalue) -> "relDt":
    raise NotImplementedError
  
  def copy(self) -> "relDt":
    t = relDt(super().copy())
    return t