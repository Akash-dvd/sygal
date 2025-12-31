from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union,Any

from functools import reduce,total_ordering
from collections.abc import Iterable
from collections import defaultdict
from itertools import product
from sympy import subsets

from Sygal.GExpr import GExpr 
from Sygal.pSC.grd import grd
from Sygal.utils.util import * 

Ngrd = grd(None,None)

@total_ordering
class spcdct(dict):    # -> Union[spcdct,None]
  # will tale empty dcits
  def __init__(self:"spcdct",arg) -> None:
    if type(arg) == spcdct:
      super().__init__(arg)
    elif issubclass(type(arg),dict):
      if bool(arg):
        t = spcdct.canonicalize(arg)
        super().__init__(t)
      else:
        super().__init__(arg)
    else:
      raise ValueError("Dict required as arguement")

  def __getitem__(self, key):
    # Handle both string identifiers and Box objects (for backward compatibility)
    if type(key).__name__ == "Box":
      # For backward compatibility, try to convert Box to string identifier
      # This is a fallback - ideally keys should be strings
      key1 = key.mv
      # Try to find matching string identifier
      if hasattr(GExpr, 'I31') and isinstance(GExpr.I31, str):
        # New string-based system
        # For now, return Ngrd for Box keys in new system
        return Ngrd
      else:
        # Old system - use mv directly
        if key1 in GExpr.pSClst:
          return self.get(key1,Ngrd)
        else:
          raise ValueError("Illegal pSC key")
    elif isinstance(key, str):
      # String identifier
      if key in GExpr.pSClst:
        return self.get(key,Ngrd)
      else:
        raise ValueError("Illegal pSC key: %s" % key)
    else:
      # Try as-is (for nl which is a multivector)
      if key in GExpr.pSClst:
        return self.get(key,Ngrd)
      else:
        raise ValueError("Illegal pSC key")

  def sup_update(self,arg) -> None:
    super().update(arg)

  def update(self:"spcdct",dct:Union[dict,"spcdct"]) -> None:
    if issubclass(type(dct), dict):
      t_dct = {}
      t_dct.update(self)
      t_dct.update(dct)
      t_dct1 = spcdct.canonicalize(t_dct)
      super().clear()
      super().update(t_dct1)
    else:
      ValueError("Arg must be type dict")

  def __add__(self:"spcdct",other:"spcdct") -> "spcdct":
    if type(other) == spcdct:
      t_dct = {}
      for k1,v1 in self.items():
        if other[k1] == Ngrd:
          t_dct.update({k1:v1})
        else:
          t_v = grd(v1.value+other[k1].value,v1.limit)
          if t_v.value == None:
            return spcdct({}) 
          else:
            t_dct.update({k1:t_v})
      for k2,v2 in other.items():
        if self[k2] == Ngrd:
          t_dct.update({k2:v2})
        else:
          pass
      return spcdct(t_dct)
    else:
      raise ValueError("Dict required as arguement")

  # Preliminary test
  # TODO check grade-wise compatability 
  def __or__(self:"spcdct",other:"spcdct") -> bool:
    """
    HERE after grade-wise compatability NaN should be handled separately for Inf-Inf
    """
    if type(other) == spcdct:
      t1 = 0
      for k,v in self.items():
        if v.value is not None:
          t1 += v.value
      t2 = 0
      for k,v in other.items():
        if v.value is not None:
          t2 += v.value
      if t1 == t2:
        t_sum = 0
        for (k1,v1),(k2,v2) in product(self.items(),other.items()):
          i = GExpr.pSClst.index(k1)
          j = GExpr.pSClst.index(k2)
          t_sum += GExpr.grdlmt[i][j]
          if t_sum >0:
            return True
          else:
            continue
        return False
      else:
        raise ValueError("Spaces must have same grade")
    else:
      raise ValueError("spcdct required as arguement")

  def __lt__(self, other):
    if type(self) != type(other):
      raise ValueError("Wrong Types")
    lst_self = [GExpr.pSClst.index(k) for k,v in self.items()]
    grlst_self = [v for k,v in self.items()]
    lst_othr = [GExpr.pSClst.index(k) for k,v in other.items()]
    grlst_othr = [v for k,v in other.items()]
    limit = min(len(lst_self),len(lst_othr))
    for i,ele in enumerate(lst_self[:limit]):
      if ele<lst_othr[i]:
        return True
      elif ele == lst_othr[i]:
        continue
      else:
        return False
    for i,ele in enumerate(grlst_self[:limit]):
      if ele.value<grlst_othr[i].value:
        return True
      elif ele == grlst_othr[i]:
        continue
      else:
        return False
    if len(lst_self)<len(lst_othr):
      return True
    elif len(lst_self)==len(lst_othr):
      return True
    else:
      return False

  def __eq__(self, other):
    return ( issubclass(type(other),dict)
    and (super().__eq__(other)) )

  def canonicalize(dct) -> dict:
    ##############
    # Key check
    # Null/overflow check
    # int -> grd conversion
    ##############
    t_dct = {}
    for k,v in dct.items():
      # Handle Box objects (backward compatibility)
      if (type(k).__name__ == "Box"):
        # Try to convert to string identifier
        # For now, skip Box keys in new system
        continue
      else:
        k1 = k

      # Validate key is in pSClst
      if not k1 in GExpr.pSClst:
        raise ValueError("Invalid Key: %s" % k1)

      if type(v) == grd:
        t_dct.update({k1:v})
      elif type(v) == int:
        # Get limit from grdlmt_map for string identifiers
        if isinstance(k1, str) and hasattr(GExpr, 'grdlmt_map'):
          limit = GExpr.grdlmt_map.get(k1)
          if limit is None:
            raise ValueError("No limit found for identifier: %s" % k1)
          t_v = grd(v, limit)
        else:
          # Fallback for old system (nl is a multivector, not a string)
          # nl is special case - it's a multivector with grade 0
          if k1 == GExpr.nl:
            limit = 0
          else:
            # Unknown key type - this shouldn't happen in new system
            raise ValueError("Cannot determine limit for key: %s (type: %s)" % (k1, type(k1)))
          t_v = grd(v, limit)
        t_dct.update({k1:t_v})
      else:
        raise ValueError("Illegal Value")

    ################
    # Scalar removal from grades {I41:{0}}->{GExpr.Onl:{0}}
    # TODO {I41:{0},I8:1}->{I8:1}
    fct = False
    t_dct1 = {}
    t_dct11 = {}
    for k,v in t_dct.items():
      if v.value == 0:
        fct = True
        continue
      else:
        t_dct11.update({k:v})
    if not bool(t_dct11) and fct:
      t_dct11.update({GExpr.nl:grd(0,0)})
      
    t_dct1.update(t_dct11)
    
    ################
    #   Sorting    # 
    ################
    t_dct2 = dict(sorted(t_dct1.items(), key=lambda x:GExpr.pSClst.index(x[0])))

    ################
    ### MERGING ###
    ################
    
    # Simplified merging - no grouping needed for string identifiers
    # Just return the sorted dictionary
    t_dct4 = {}
    for k,v in t_dct2.items():
      # Skip primmv checks in new system (primmv is empty)
      if hasattr(GExpr, 'primmv') and k in GExpr.primmv:
        # Old system - handle primitives
        # For new system, primmv is empty, so this won't execute
        continue
      else:
        t_dct4.update({k:v})

    ###############
    ##  CUMU ADD ##
    ###############

    # For string identifiers, we don't need the complex subset checking
    # Just validate that values are not None
    for k,v in t_dct4.items():
      if v.value is None:
        return {}
      # For string identifiers, we can't check args
      # The validation is simpler - just check value is valid

    return t_dct4
