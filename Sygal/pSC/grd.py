from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union,Any

from functools import reduce,total_ordering
from collections import Iterable,defaultdict

from libs.Sygal.GExpr import GExpr 


# @total_ordering
class grd():
  def __init__(self,value:int,limit:int=None) -> None:
    if value == None or limit == None :
      self._limit = None
      self._value = None
    elif type(limit) == int and type(value) == int:
      if value in range(limit+1):
        self._limit = limit
        self._value = value
      else :
        self._limit = None
        self._value = None
    else :
      raise ValueError("Illegal Arguements") 
  @property
  def value(self):
    return self._value

  @property
  def limit(self):
    return self._limit

  def __str__(self) -> str:
    strng = "<"
    strng += str(self.value)
    strng += "|"
    strng += str(self.limit)
    strng += ">"
    return str(strng)

  def __repr__(self) -> str:
    strng = "<"
    strng += str(self.value)
    strng += "|"
    strng += str(self.limit)
    strng += ">"
    return str(strng)

  def set(self,arg:int) -> None:
    if (arg in range(self.limit+1)):
      self._value = arg
    else :
      self._value = None
      self._limit = None
      
  def add(self,arg:int) -> None:
    if (arg+self.value in range(self.limit+1)):
      self._value = arg+self.value
    else :
      self._value = None
      self._limit = None

  def __eq__(self, other):
    return ( (type(self) == type(other)) 
    and  (self._value == other._value)
    and (self._limit == other._limit))
    # and (self.value != other.value) )

  # def __lt__(self, other):
  #   return ( (type(self) == type(other)) 
  #   and self._value < other._value)
