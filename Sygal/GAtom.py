from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from functools import reduce
from collections.abc import Iterable
from collections import defaultdict

from Sygal.utils.util import *

from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,sympify,
  symbols, sqrt, Matrix,srepr,AtomicExpr
)
from sympy import oo as I
from sympy.core.cache import cacheit

from Sygal.GExpr import GExpr
from Sygal.pSC.grd import grd
from Sygal.pSC.spcdct import spcdct
from Sygal.pSC.spclst import spclst
from Sygal.relDt.relDt import relDt
from Sygal.Box import Box
from Sygal.utils.utils1 import rlGSortArgs,parity,is_unMixedGrade,bx_sift,GSortArgs,is_devmode
from Sygal.operators.assop.gextp import gextp
# from Sygal.pSC.pextp import pextp
# defDic = defaultdict(lambda x:None)

def dct_is_joint(mv1:GExpr,mv2:GExpr):
  fct = False
  for grp in GExpr.Disjoint_Grp:
    if mv1 in grp and mv2 in grp:
      fct = True
    else:
      continue
  return fct


def pextp(*args) -> "Box":
  coeff = args[0]
  tmvs = [arg.mv for arg in args[1:]]
  MV = Basic.__new__(gextp, *tmvs)
  MV.mtDt = spclst([])
  grdval = len(args)-1
  grade = grd(grdval,grdval)
  dct = spcdct({})
  dct.sup_update({MV:grade})
  MV.mtDt.append(dct)
  MV.rlDt = relDt()
  bx = Basic.__new__(Box,MV,coeff)
  return bx

class GAtom(GExpr,AtomicExpr):

  def __new__(cls, name:str,mtDt:Union[List[Dict],Dict],rlDt:Dict) -> Box:
    
    # Pattern match for name -> str
    # TODO check for earlier symbols
    if not isinstance(name, str):
      raise TypeError("name should be a string, not %s" % repr(type(name)))
    elif name.startswith('_'):
      raise TypeError("name should not start with  _")

    # Pattern match for mtdt -> dict
    # if not bool(mtDt):
    #   mtDt = spclst([{GExpr.I13:1}])
    if issubclass(type(mtDt),dict):
      mtDt = spclst([mtDt])
    elif issubclass(type(mtDt),list):
      mtDt = spclst(mtDt)
    else:
      raise ValueError("Iterable must be a list")

    # Pattern match for rlDt -> dict
    # if not bool(rlDt):
    #   rlDt = relDt()
    #   rlDt.update({GExpr._oo:S(-1)})
    
    # Scalar Check

    if mtDt == [{GExpr.nl:grd(0,0)}]:
      return GExpr.Onl
    else :
      pass

    # BOX INITIALIZER
    bx = GAtom.__xnew_cached_(GAtom, name)
    bx.mv.mtDt = mtDt
    # DICT INITIALIZER
    GAtom.dict_initializer(bx,rlDt)
  
    return bx

  def dict_initializer(bx,t_rlDt):
    rlDt = relDt()

    for k,v in t_rlDt.items():
      if k =="self":
        rlDt.update({bx:v})
      elif issubclass(type(k),GExpr):
        rlDt.update({k:v})
      else :
        raise NotImplemented
    bx.mv.rlDt = rlDt

  def __new_stage2__(cls, name) -> Box:
    
    mv = GExpr.__new__(GAtom,name)
    mv.is_atom = True

    bx = Basic.__new__(Box,mv,S(1))   
    return bx

  def __str__(self):
    return "\033[1;37;40m"+self.args[0]+"\033[0;37;40m"

  def __repr__(self):
    return self.args[0]

  def __hash__(self):
    return hash(self.name)

  def __eq__(self, other):
    return (
      (type(other) == type(self))  and
      self.__hash__() == other.__hash__()
      # Check if hash is not present in the object
    )



  @property
  def name(self):
    return self.args[0]

  def _preprocess():
    if GExpr.initialized:
      raise ValueError
    else:
      #######################
      spcdct.is_joint = dct_is_joint

      # t_grd._value = 0
      GExpr.Onl = GAtom.__xnew_cached_(GAtom,"\u0950")
      t_dct = dict.__new__(spcdct)
      t_dct.sup_update({GExpr.Onl.mv:grd(0,0)})
      GExpr.Onl.mv.mtDt = spclst([t_dct])
      GExpr.Onl.mv.rlDt = relDt()
      # GExpr.Onl.mv.mtDt = spclst([{GExpr.nl:t_grd}])
      # GExpr.Onl.mv.rlDt = defDic derived from GExpr

      GExpr.nl = GExpr.Onl.mv

      # To make sure Both Znl and Onl share same _nl
      GExpr.Znl = Basic.__new__(Box,GExpr.nl,S(0)) 
      GExpr.Znl.mv.mtDt = spclst([t_dct])
      GExpr.Znl.mv.rlDt = relDt()
      
      
      
      #######################

      names = ['_o','_x','_y','_rx','_oo','_x1','_x2','_x3','_x4','_x5','_x6','_x7','_x8']
      
      prim = []
      primmv = []
      
      for name in names:
        bx = GAtom.__xnew_cached_(GAtom, name)
        t_dct1 = dict.__new__(spcdct)
        t_dct1.sup_update({bx.mv:grd(1,1)})
        bx.mv.mtDt = spclst([t_dct1])
        prim.append(bx)
        primmv.append(bx.mv)

      #######################
      _o  = prim[0]
      _x  = prim[1]
      _y  = prim[2]
      _rx = prim[3]
      _oo = prim[4]
      _x1 = prim[5]
      _x2 = prim[6]
      _x3 = prim[7]
      _x4 = prim[8]
      _x5 = prim[9]
      _x6 = prim[10]
      _x7 = prim[11]
      _x8 = prim[12]
      
      rel_dot = [[_o,_oo,S(-1)],[_x,_x,S(1)],[_y,_y,S(1)],[_rx,_rx,S(-1)],[_oo,_o,S(-1)],[_x1,_x1,S(1)],[_x2,_x2,S(1)],[_x3,_x3,S(1)],[_x4,_x4,S(1)],[_x5,_x5,S(1)],[_x6,_x6,S(1)],[_x7,_x7,S(1)],[_x8,_x8,S(1)]]
      
      accu_def_rlDt = relDt()
      tmpdict = relDt()
      
      for bx in prim:
        tmpdict.update({bx:S(0)})
      for bx in prim:
        newtmpdict = tmpdict.copy()
        accu_def_rlDt.update({bx:newtmpdict})

      for bx1,bx2,cf in rel_dot:
        accu_def_rlDt[bx1].update({bx2:cf})
      for bx in prim:
        bx.mv.rlDt = accu_def_rlDt[bx]

      #######################
          
      GExpr._oo = _oo 
      GExpr._rx = _rx
      
      GExpr.primbx = prim
      GExpr.primmv = primmv
      
      GExpr.I31 = pextp(S(1),_oo,_x,_y)
      GExpr.I32 = pextp(S(1),_o,_x,_y)
      GExpr.I41 = pextp(S(1),_o,_oo,_x,_y)
      GExpr.I42 = pextp(S(-1),_oo,_rx,_x,_y)
      GExpr.I43 = pextp(S(1),_o,_rx,_x,_y)
      GExpr.I5  = pextp(S(-1),_o,_oo,_rx,_x,_y)


      GExpr.I8 = pextp(S(1),_x1,_x2,_x3,_x4,_x5,_x6,_x7,_x8)
      GExpr.I13 = pextp(S(-1),_o,_oo,_rx,_x,_x1,_x2,_x3,_x4,_x5,_x6,_x7,_x8,_y)


      GExpr.pSClst = [GExpr.nl,_oo.mv,_x.mv,_y.mv,GExpr.I31.mv,_o.mv,GExpr.I32.mv,GExpr.I41.mv,_rx.mv,GExpr.I42.mv,GExpr.I43.mv,GExpr.I5.mv,_x1.mv,_x2.mv,_x3.mv,_x4.mv,_x5.mv,_x6.mv,_x7.mv,_x8.mv,GExpr.I8.mv,GExpr.I13.mv]

      GExpr.pSCiFrmlst = [GExpr.Onl,_o*S(-1),_x,_y,GExpr.I32*S(-1),_oo*S(-1),GExpr.I31*S(-1),GExpr.I41*S(-1),_rx*S(-1),GExpr.I43*S(-1),GExpr.I42,GExpr.I5,_x1,_x2,_x3,_x4,_x5,_x6,_x7,_x8,GExpr.I8,GExpr.I13]

      GExpr.grdlmt = [
        # replace 9 by infinity
      
        [I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I],
        [I,0,0,0,0,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,1],
        [I,0,1,0,1,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,1],
        [I,0,0,1,1,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,1],
        [I,0,1,1,2,1,3,3,0,2,3,3,0,0,0,0,0,0,0,0,0,2],
        [I,1,0,0,1,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,1],
        [I,1,1,1,3,0,2,3,0,3,2,3,0,0,0,0,0,0,0,0,0,3],
        [I,1,1,1,3,1,3,4,0,3,3,4,0,0,0,0,0,0,0,0,0,4],
        [I,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
        [I,0,1,1,2,1,3,3,1,3,4,4,0,0,0,0,0,0,0,0,0,4],
        [I,1,1,1,3,0,2,3,1,4,3,4,0,0,0,0,0,0,0,0,0,4],
        [I,1,1,1,3,1,3,4,1,4,4,5,0,0,0,0,0,0,0,0,0,5],
        [I,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1],
        [I,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1],
        [I,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1],
        [I,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1],
        [I,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1],
        [I,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1],
        [I,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1],
        [I,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
        [I,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,8,8],
        [I,1,1,1,3,1,3,4,1,4,4,5,1,1,1,1,1,1,1,1,8,13],
      ]
      
      GExpr.Disjoint_Grp = [[_o.mv,_x.mv,_y.mv,_rx.mv,_oo.mv],[_x1.mv,_x2.mv,_x3.mv,_x4.mv,_x5.mv,_x6.mv,_x7.mv,_x8.mv]] 
      
      
      GExpr.initialized = True 
  
  __xnew__ = staticmethod(
    __new_stage2__)            # never cached (e.g. dummy)
  __xnew_cached_ = staticmethod(
    cacheit(__new_stage2__))   # symbols are always cached
  # __xnew_cached_ = staticmethod(
  #   __new_stage2__)   # never cached (e.g. dummy)

GAtom._preprocess()

