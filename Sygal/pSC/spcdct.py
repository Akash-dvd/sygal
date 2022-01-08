from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union,Any

from functools import reduce,total_ordering
from collections import Iterable,defaultdict
from itertools import product
from sympy import subsets

from libs.Sygal.GExpr import GExpr 
from libs.Sygal.pSC.grd import grd
from libs.Sygal.utils.util import * 

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
      else :
        super().__init__(arg)
    else :
      raise ValueError("Dict required as arguement")

  def __getitem__(self, key):
    if type(key).__name__ == "Box":
      key1 = key.mv
    else:
      key1 = key
    if key1 in GExpr.pSClst:
      # return self.get(key1,None)
      return self.get(key1,Ngrd)
    else :
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
    else :
      ValueError("Arg must be type dict")

  def __add__(self:"spcdct",other:"spcdct") -> "spcdct":
    if type(other) == spcdct:
      t_dct = {}
      for k1,v1 in self.items():
        if other[k1] == Ngrd:
          t_dct.update({k1:v1})
        else :
          t_v = grd(v1.value+other[k1].value,v1.limit)
          if t_v.value == None:
            return spcdct({}) 
          else:
            t_dct.update({k1:t_v})
      for k2,v2 in other.items():
        if self[k2] == Ngrd:
          t_dct.update({k2:v2})
        else :
          pass
      return spcdct(t_dct)
    else :
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
        t1 += v.value
      t2 = 0
      for k,v in self.items():
        t2 += v.value
      # t1 = reduce(lambda T1,T2:(T1.value)+(T2.value),list(self.values()))
      # t2 = reduce(lambda T1,T2:T1.value+T2.value,list(other.values()))
      if t1 == t2:
        t_sum = 0
        for (k1,v1),(k2,v2) in product(self.items(),other.items()):
          i = GExpr.pSClst.index(k1)
          j = GExpr.pSClst.index(k2)
          t_sum += GExpr.grdlmt[i][j]
          if t_sum >0 :
            return True
          else:
            continue
        return False
      else :
        raise ValueError("Spaces must have same grade")
    else :
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
    else :
      return False

  def __eq__(self, other):
    return ( issubclass(type(other),dict)
    and (super().__eq__(other)) )
    # and (self.value != other.value) )

  # TODO 
  ################
  # replace or merge when ceiling is touched
  # {I3:3,I41:1} -> replace with I3
  # {I3:2,I41:2} -> {I41:4}
  # Similar overflows
  def canonicalize(dct) -> dict:

    ##############
    # Key check
    # Null/overflow check
    # int -> grd conversion
    ##############
    t_dct = {}
    for k,v in dct.items():
      if (type(k).__name__ == "Box"):
        k1 = k.mv
      else :
        k1 = k

      if not k1 in GExpr.pSClst:
        raise ValueError("Invalid Key")

      if type(v) == grd:
        t_dct.update({k1:v})

      elif type(v) == int:
        t_v = grd(v,len(k1.args))
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
    if not bool(t_dct11) and fct :
      t_dct11.update({GExpr.nl:grd(0,0)})
      
    t_dct1.update(t_dct11)
    
    ################
    #   Sorting    # 
    ################
    t_dct2 = dict(sorted(t_dct1.items(), key=lambda x:GExpr.pSClst.index(x[0])))

    ################
    ### GROUPING ###
    ################

    l_dct_keys = list(t_dct2)
    t_dct34 = {}
    t_dct3 = {}

    ini = 0
    itr = 0
    stop = len(l_dct_keys)

    while itr < stop:

      itr = ini + 1
      key = l_dct_keys[ini]
      t_dct34.update({key:t_dct2[key]})

      while itr < stop:
        if spcdct.is_joint(l_dct_keys[ini],l_dct_keys[itr]):
          key = l_dct_keys[itr]
          t_dct34.update({key:t_dct2[key]})
          itr+=1
          continue
        else:
          ini = itr
          if len(t_dct34) > 1:
            t1 = GExpr.__new__(type(GExpr.I41.mv),*GSortArgs(list(t_dct34)))
            if t1 in GExpr.pSClst:

              t_dct3.update({t1:grd(len(t1.args),len(t1.args))})
              t_dct34.clear()
            else:
              t_dct3.update(t_dct34)
              t_dct34.clear()

          else:
            t_dct3.update(t_dct34)
            t_dct34.clear()
            
          break
    
    if len(t_dct34) > 1:
      t1 = GExpr.__new__(type(GExpr.I41.mv),*GSortArgs(list(t_dct34)))
      if t1 in GExpr.pSClst:

        t_dct3.update({t1:grd(len(t1.args),len(t1.args))})
        t_dct34.clear()
      else:
        t_dct3.update(t_dct34)
        t_dct34.clear()
    else:
      t_dct3.update(t_dct34)
      t_dct34.clear()

    ###############
    ### MERGING ###
    ###############

    # Prim attachement {_oo:{1},I41:{2}}->{I41:{3}}
    # {o:1,oo:1} -> {o:1,oo:1}
    # {oo:1,o:1,I41:1} -> {I41:3}
    
    t_dct34 = t_dct3.copy()
    t_dct4 = {}
    for i,(k,v) in enumerate(t_dct34.items()):

      if k in GExpr.primmv:
        done = False
        for k1,v1 in list(t_dct34.items())[i+1:]:
          if k1 not in GExpr.primmv and k in k1.args:
            t_dct34.update({k1:grd(v1.value+1,v1.limit)})
            if t_dct34[k1].value == None:
              return {}
            done = True
            break
          else :
            continue

        if not done:
          t_dct4.update({k:v})
        else:
          continue

      elif k not in GExpr.primmv :
        t_dct4.update({k:v})

      else:
        raise ValueError("Illegal Key")


    ###############
    ##  CUMU ADD ##
    ###############

    # Prim attachement {I31:{2},I41:{3}}-> 0

    t_dct5 = {k:v for k,v in t_dct4.items() if k not in GExpr.primmv}

    key_sets = subsets(t_dct5)
    next(key_sets)
    
    st_mv = set()
    val = 0
    for tup in key_sets:
      st_mv.clear()
      val = 0
      for ks in tup:
        st_mv.update(ks.args)
      for ks in tup:
        val += t_dct4[ks].value
      if val > len(st_mv):
        return {}
      else:
        continue

    return t_dct4

