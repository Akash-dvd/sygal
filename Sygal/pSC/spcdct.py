from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union,Any

from functools import reduce,total_ordering
from collections import Iterable,defaultdict

from libs.Sygal.GExpr import GExpr 
from libs.Sygal.pSC.grd import grd

@total_ordering
class spcdct(dict):    # -> Union[spcdct,None]
  # will tale empty dcits
  def __init__(self:"spcdct",arg) -> None:
    if type(arg) == spcdct:
      super().__init__(arg)
    elif issubclass(type(arg),dict):
      t_arg = {}
      for k,v in arg.items():
        if (type(k).__name__ == "Box"):
          k1 = k.mv
        else :
          k1 = k
        t_arg.update({k1:v})

      t = spcdct.standardize(t_arg)
      super().__init__(t)
    else :
      raise ValueError("Dict required as arguement")

  def __getitem__(self, key):
    if type(key).__name__ == "Box":
      key1 = key.mv
    else:
      key1 = key
    if key1 in GExpr.pSClst:
      return self.get(key1,None)
    else :
      raise ValueError("Illegal pSC key")

  def __add__(self:"spcdct",other:"spcdct") -> "spcdct":
    if type(other) == spcdct:
      t_dct = {}
      # def_dct = spcdct({GExpr.Onl:grd(0,0)})
      # if self == def_dct:
      #   return other
      # elif other == def_dct:
      #   return self
      # else :
      for k1,v1 in self.items():
        if other[k1] == None:
          t_dct.update({k1:v1})
        else :
          t_v = grd(v1.value+other[k1].value,v1.limit)
          if t_v.value == None:
            return spcdct({}) 
          else:
            t_dct.update({k1:t_v})
      for k2,v2 in other.items():
        if self[k2] == None:
          t_dct.update({k2:v2})
        else :
          pass
      return spcdct(t_dct)
    else :
      raise ValueError("Dict required as arguement")

  # Preliminary test
  # TODO check grade-wise compatability 
  def __or__(self:"spcdct",other:"spcdct") -> bool:
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
        for k1,v1 in self.items():
          t_sum = 0
          for k2,v2 in other.items():
            i = GExpr.pSClst.index(k1)
            j = GExpr.pSClst.index(k2)
            t_sum += GExpr.grdlmt[i][j]
          if t_sum >0 :
            continue
          else:
            return False
        for k2,v2 in other.items():
          t_sum = 0
          for k1,v1 in self.items():
            i = GExpr.pSClst.index(k2)
            j = GExpr.pSClst.index(k1)
            t_sum += GExpr.grdlmt[i][j]
          if t_sum >0 :
            continue
          else:
            return False
        return True
      else :
        raise ValueError("Spaces must have same grade")
    else :
      raise ValueError("Dict required as arguement")

  def sup_update(self,arg) -> None:
    super().update(arg)

  def update(self:"spcdct",arg:Union[dict,"spcdct"]) -> None:
    if issubclass(type(arg), dict):
      t_dct = {}
      for k,v in arg.items():
        if (type(k).__name__ == "Box"):
          k1 = k.mv
        else :
          k1 = k
        t_dct.update({k1:v})
      t_dct.update(self)
      t_dct1 = spcdct.standardize(t_dct)
      super().clear()
      super().update(t_dct1)
    else :
      ValueError("Arg must be type spcdct")

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
      if ele<grlst_othr[i]:
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
    and (super(spcdct,self).__eq__(other)) )
    # and (self.value != other.value) )

  # TODO 
  ################
  # replace or merge when ceiling is touched
  # {I3:3,I41:1} -> replace with I3
  # {I3:2,I41:2} -> {I41:4}
  # Similar overflows
  def standardize(dct) -> dict:
    ##############
    # Key check
    # Null/overflow check
    # int -> grd conversion
    
    t_dct = {}
    for k,v in dct.items():
      if not k in GExpr.pSClst:
        raise ValueError("Invalid Key")
      if type(v) == grd:
        if v.value == None:
          return {}
        else:
          t_dct.update({k:v})

      elif type(v) == int:
        t_v = grd(v,len(k.args))
        if t_v.value == None:
          return {}
        else:
          t_dct.update({k:t_v})

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
    # Sorting  
    t_dct2 = dict(sorted(t_dct1.items(), key=lambda x:GExpr.pSClst.index(x[0])))

    ################
    # Prim attachement {_oo:{1},I41:{2}}->{I41:{3}}
    # {oo:1,o:1} -> {oo:1,o:1}
    # {oo:1,o:1,I41:1} -> {I41:3}
    t_dct3 = {}
    for i,(k,v) in enumerate(t_dct2.items()):
      if k not in GExpr.primmv:
        t_dct3.update({k:v})
      elif k in GExpr.primmv:
        for j,(k1,v1) in enumerate(list(t_dct2.items())[i+1:]):
          if k1 not in GExpr.primmv and k in k1.args:
            v1.add(1)
            if v1.value == None:
              return {}
            break
          else :
            continue
        # i+(j+1)+1 ,j+1 is for offset and last +1 is index vs length
        if i+1 == len(t_dct2):
          t_dct3.update({k:v})
        elif i+j+2 == len(t_dct2):
          t_dct3.update({k:v})
        else:
          pass
      else:
        raise ValueError("Illegal Key")

    return t_dct3
