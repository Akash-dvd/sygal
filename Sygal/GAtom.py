from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from functools import reduce
from collections import Iterable,defaultdict

from libs.Sygal.utils.util import *

from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,sympify,
  symbols, sqrt, Matrix,srepr,AtomicExpr
)

from libs.Sygal.GExpr import GExpr
from libs.Sygal.pSC.grd import grd
from libs.Sygal.pSC.spcdct import spcdct
from libs.Sygal.pSC.spclst import spclst
from sympy.core.cache import cacheit
from libs.Sygal.Box import Box
from libs.Sygal.utils.utils1 import rlGSortArgs,parity,is_unMixedGrade,bx_sift,GSortArgs,is_devmode
from libs.Sygal.operators.assop.gextp import gextp
# from libs.Sygal.pSC.pextp import pextp
# defDic = defaultdict(lambda x:None)



def pextp(*args) -> "Box":
  coeff = args[0]
  tmv = [arg.mv for arg in args[1:]]
  MV1 = Basic.__new__(gextp, *tmv)
  bx = Basic.__new__(Box,MV1,coeff)
  MV1.mtDt = spclst([])
  grdval = len(args)-1
  grade = grd(grdval,grdval)
  dct = spcdct({})
  dct.sup_update({bx:grade})
  MV1.mtDt.append(dct)
  MV1.rlDt = defaultdict(lambda:None)
  
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
    if not mtDt:
      mtDt = [{GExpr.I13:13}]
    elif isinstance(mtDt,Iterable):
      mtDt = spclst([mtDt])

    # Pattern match for rlDt -> dict
    if not rlDt:
      rlDt = defaultdict(lambda x:None)
      rlDt.update({GExpr._oo:S(-1)})
    
    # Scalar Check
    if mtDt:
      if mtDt == [{GExpr.Onl:grd(0,0)}]:
        return GExpr.Onl
      else :
        pass
    else :
      return GExpr.Znl

    # BOX INITIALIZER
    bx = GAtom.__xnew_cached_(GAtom, name)
    bx.mv.mtDt = mtDt
    # DICT INITIALIZER
    GAtom.dict_initializer(bx,rlDt)
  
    return bx

  def dict_initializer(bx,t_rlDt):
    rlDt = defaultdict(lambda:None)

    for k,v in t_rlDt.items():
      if k =="self":
        rlDt[bx] = v
      elif type(k) == Box:
        rlDt[k] = v
      else :
        raise NotImplemented
    bx.mv.rlDt.update(rlDt)

  def __new_stage2__(cls, name) -> Box:
    
    mv = GExpr.__new__(GAtom,name)
    mv.is_atom = True

    mv.mtDt = defaultdict(lambda:None)
    mv.rlDt = defaultdict(lambda:None)
    
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


      # t_grd._value = 0
      GExpr.Onl = GAtom.__xnew_cached_(GAtom,"\u0950")
      t_dct = dict.__new__(spcdct)
      t_dct.sup_update({GExpr.Onl:grd(0,0)})
      GExpr.Onl.mv.mtDt = spclst([t_dct])
      GExpr.Onl.mv.rlDt = defaultdict(lambda x:None)
      # GExpr.Onl.mv.mtDt = spclst([{GExpr.Onl:t_grd}])
      # GExpr.Onl.mv.rlDt = defDic derived from GExpr

      # To make sure Both Znl and Onl share same _nl
      GExpr.Znl = Basic.__new__(Box,GExpr.Onl.mv,S(0)) 
      GExpr.Znl.mv.mtDt = spclst([t_dct])
      GExpr.Znl.mv.rlDt = defaultdict(lambda x:None)
      
      GExpr.nl = GExpr.Znl.mv
      
      #######################

      names = ['_o','_x','_y','_rx','_oo','_x1','_x2','_x3','_x4','_x5','_x6','_x7','_x8']
      
      prim = []
      
      for name in names:
        bx = GAtom.__xnew_cached_(GAtom, name)
        t_dct1 = dict.__new__(spcdct)
        t_dct1.sup_update({bx:grd(1,1)})
        bx.mv.mtDt = spclst([t_dct1])
        prim.append(bx)

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
      
      accu_def_rlDt = defaultdict(lambda :None)
      tmpdict = defaultdict(lambda :None)
      
      for bx in prim:
        tmpdict[bx] = S(0)
      for bx in prim:
        newtmpdict = tmpdict.copy()
        accu_def_rlDt[bx] = newtmpdict

      for bx1,bx2,cf in rel_dot:
        accu_def_rlDt[bx1][bx2] = cf
      for bx in prim:
        bx.mv.rlDt = accu_def_rlDt[bx]

      #######################
          
      GExpr._oo = _oo 
      GExpr._rx = _rx
      
      GExpr.prim = prim

      # GExpr.I31 = _x^_y^_oo
      # GExpr.I32 = _o^_x^_y
      # GExpr.I41 = _o^_x^_y^_oo
      # GExpr.I42 = _x^_y^_rx^_oo
      # GExpr.I43 = _o^_x^_y^_rx
      # GExpr.I5 = _o^_x^_y^_rx^_oo


      # GExpr.I8 = _x1^_x2^_x3^_x4^_x5^_x6^_x7^_x8
      # GExpr.I13 = GExpr.I5^GExpr.I8

      GExpr.I31 = pextp(S(1),_oo,_x,_y)
      GExpr.I32 = pextp(S(1),_o,_x,_y)
      GExpr.I41 = pextp(S(1),_o,_oo,_x,_y)
      GExpr.I42 = pextp(S(-1),_oo,_rx,_x,_y)
      GExpr.I43 = pextp(S(1),_o,_rx,_x,_y)
      GExpr.I5  = pextp(S(-1),_o,_oo,_rx,_x,_y)


      GExpr.I8 = pextp(S(1),_x1,_x2,_x3,_x4,_x5,_x6,_x7,_x8)
      GExpr.I13 = pextp(S(-1),_o,_oo,_rx,_x,_x1,_x2,_x3,_x4,_x5,_x6,_x7,_x8,_y)


      GExpr.pSClst = [GExpr.Onl,_oo,_x,_y,GExpr.I31,_o,GExpr.I32,GExpr.I41,_rx,GExpr.I42,GExpr.I43,GExpr.I5,_x1,_x2,_x3,_x4,_x5,_x6,_x7,_x8,GExpr.I8,GExpr.I13]
      GExpr.pSCiFrmlst = [GExpr.Onl,_o*S(-1),_x,_y,GExpr.I32,_oo*S(-1),GExpr.I31,GExpr.I41*S(-1),_rx*S(-1),GExpr.I43*S(-1),GExpr.I42*S(-1),GExpr.I5,_x1,_x2,_x3,_x4,_x5,_x6,_x7,_x8,GExpr.I8,GExpr.I13]

      GExpr.grdlmt = [
        # replace 9 by infinity
      
        [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
        [9,0,0,0,0,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,1],
        [9,0,1,0,1,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,1],
        [9,0,0,1,1,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,1],
        [9,0,1,1,2,1,3,3,0,2,3,3,0,0,0,0,0,0,0,0,0,2],
        [9,1,0,0,1,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,1],
        [9,1,1,1,3,0,2,3,0,3,2,3,0,0,0,0,0,0,0,0,0,3],
        [9,1,1,1,3,1,3,4,0,3,3,4,0,0,0,0,0,0,0,0,0,4],
        [9,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
        [9,0,1,1,2,1,3,3,1,3,4,4,0,0,0,0,0,0,0,0,0,4],
        [9,1,1,1,3,0,2,3,1,4,3,4,0,0,0,0,0,0,0,0,0,4],
        [9,1,1,1,3,1,3,4,1,4,4,5,0,0,0,0,0,0,0,0,0,5],
        [9,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1],
        [9,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1],
        [9,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1],
        [9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1],
        [9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1],
        [9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1],
        [9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1],
        [9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
        [9,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,8,8],
        [9,1,1,1,3,1,3,4,1,4,4,5,1,1,1,1,1,1,1,1,8,13],
      ]
      GExpr.initialized = True 
  
  __xnew__ = staticmethod(
    __new_stage2__)            # never cached (e.g. dummy)
  __xnew_cached_ = staticmethod(
    cacheit(__new_stage2__))   # symbols are always cached
  # __xnew_cached_ = staticmethod(
  #   __new_stage2__)   # never cached (e.g. dummy)

GAtom._preprocess()


# [
#   [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
#   [9,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,1],
#   [9,0,1,0,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,1],
#   [9,0,0,1,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,1],
#   [9,0,1,1,2,1,3,0,2,3,0,0,0,0,0,0,0,0,0,2],
#   [9,1,0,0,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,1],
#   [9,1,1,1,3,1,4,0,3,4,0,0,0,0,0,0,0,0,0,4],
#   [9,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
#   [9,0,1,1,2,1,3,1,3,4,0,0,0,0,0,0,0,0,0,4],
#   [9,1,1,1,3,1,4,1,4,5,0,0,0,0,0,0,0,0,0,5],
#   [9,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1],
#   [9,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1],
#   [9,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1],
#   [9,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1],
#   [9,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1],
#   [9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1],
#   [9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1],
#   [9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
#   [9,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,8,8],
#   [9,1,1,1,3,1,4,1,4,5,1,1,1,1,1,1,1,1,8,13],
# ]
