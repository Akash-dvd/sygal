from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union,Any

from functools import reduce,total_ordering
from collections import Iterable,defaultdict

from libs.Sygal.GExpr import GExpr
from libs.Sygal.pSC.grd import grd
from libs.Sygal.pSC.spcdct import spcdct

class spclst(list):
  # Wont take empty dicts
  def __init__(self, lst) -> None:
    # check if every element is a dict
    if type(lst) == spclst:
      list.__init__(self, lst)
    # But GAtom does the wrapping
    elif issubclass(type(lst),dict):
      raise ValueError("Wrap the dict in a list")
    elif isinstance(lst,Iterable):
      t = [spcdct(ele) for ele in lst if bool(ele)]
      t1 = spclst.canonicalize(t)
      list.__init__(self,t1)
    else :
      raise ValueError("Illegal Arguements")

  def extend(self,itrble: Iterable) -> None:
    # No need to check for bool value
    # Already __init__ takes care of this
    if issubclass(type(itrble), list):
      super().extend(itrble)
      t = spclst.canonicalize(self)
      list.__init__(self,t)
    else :
      raise ValueError("type must be spclst")

  def append(self,obj: "spcdct") -> None:
    if type(obj) == spcdct :
      if bool(obj):
        super().append(obj)
        t = spclst.canonicalize(self)
        list.__init__(self,t)
      else :
        pass
    else :
      raise ValueError("type must be spcdct")
    
  # def insert(self, __index: SupportsIndex, __object: "spcdct") -> None:
  def insert(self, __index: int, __object: "spcdct") -> None:
    if type(__object) == spcdct :
      if bool(__object):
        super().insert(__index, __object)
        t = spclst.canonicalize(self)
        list.__init__(self,t)
      else :
        pass
    else :
      raise ValueError("type must be spcdct")
    
  def canonicalize(lst) -> list:
    # sort and deduplicate
    if not bool(lst) :
      return []
    elif len(lst) == 1:
      if bool(lst[0]):
        return [lst[0]]
      else :
        return []
    else :
      pass
    lst.sort()
    t_lst = []
    j=0
    for i,ele in enumerate(lst):
      if i==j:
        t_lst.append(lst[j])
      elif lst[i]==lst[j]:
        continue
      else:
        t_lst.append(lst[i])
        j=i
    
    return t_lst
