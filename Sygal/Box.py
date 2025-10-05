from collections import defaultdict
from math import exp
import sys

from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,sympify,
  symbols, sqrt, Matrix,srepr,bottom_up
)
from sympy.strategies.tools import subs as strtSubs

from sympy.printing.str import StrPrinter

from Sygal.GExpr import GExpr
from Sygal.pSC.spclst import spclst
from Sygal.relDt.relDt import relDt
from Sygal.utils.util import *

import warnings

class Box(GExpr):
  # Chnage here for S(0) coeff
  def __new__(cls,mv:"GExpr",coeff:Expr=S(1))->"Box":
    if(type(coeff)==Box):
      coeff = coeff.coeff
      warnings.warn("Warning.......Box coeff is box again")
      
      # raise ValueError
    else :
      coeff = coeff
    
    # Pattern matching for types
    fct1  = issubclass(type(mv),GExpr)

    if fct1:
      mv = ceil_mtDt(mv)
    else :
      pass

    fct2 = fct1 and (mv.grade == {0})
    fct3  = issubclass(type(mv),Box)
    fct4  = fct3 and fct2
    # fct42  = fct3 and ceil_mtDt(mv.mv)

    # fct1  = issubclass(type(mv),GExpr)
    # fct2 = fct1 and (mv.grade == {0})
    # fct3  = issubclass(type(mv),Box)
    # fct4  = fct3 and fct2

    new = GExpr.__new__
    
    if fct4:
      BX = mv
      # Here well formed Box must have nl as mv
      if(BX.mv!=GExpr.nl):
        raise
      t = new(Box,GExpr.nl,Mul(coeff,BX.coeff))
      t.mv.mtDt = GExpr.nl.mtDt
      t.mv.rlDt = relDt()
      return t
    elif fct3:
      BX = mv
      # Check if the arrived box encloses gadd
      if(type(BX.mv).__name__ == "gadd"):
        # Well formed gadd box always has S(1) coeff
        if(BX.coeff!=S(1)):
          raise
        t = [new(Box,bx.mv,Mul(bx.coeff,coeff)) for bx in BX.mv.args]
        t1 = new(Box,new(type(BX.mv),*t),S(1))
        t1.mv.mtDt = BX.mv.mtDt.copy()
        t1.mv.rlDt = BX.mv.rlDt.copy()
        return t1
      else:
        t = new(Box,BX.mv,Mul(coeff,BX.coeff))
        t.mv.mtDt = BX.mv.mtDt.copy()
        t.mv.rlDt = BX.mv.rlDt.copy()
        return t
    
    # Not box mvs
    # Zero grade
    elif fct2:
      # NO need to check for gadd
      if(mv == GExpr.nl):
        t = new(Box,GExpr.nl,coeff)
        t.mv.mtDt = GExpr.nl.mtDt
        t.mv.rlDt = relDt()
        return t
      else:
        # Here mv has to be checked that it should only scprdct or gmul 
        if type(mv).__name__ == "sclrprdct":
          t = new(Box,GExpr.nl,Mul(mv,coeff))
          t.mv.mtDt = GExpr.nl.mtDt
          t.mv.rlDt = relDt()
          return t   
        else:
          raise NotImplementedError
    # Non Zero grade
    elif fct1:
      if(type(mv).__name__== "gadd"):
        # t = [new(Box,bx.mv,Mul(bx.coeff,coeff).simplify()) for bx in mv.args]
        t = [new(Box,bx.mv,Mul(bx.coeff,coeff)) for bx in mv.args]
        t1 = new(Box,new(type(mv),*t),S(1))
        t1.mv.mtDt = mv.mtDt.copy()
        t1.mv.rlDt = mv.rlDt.copy()
        return t1
      else:
        t = new(Box,mv,coeff)
        t.mv.mtDt = mv.mtDt.copy()
        t.mv.rlDt = mv.rlDt.copy()    
        return t
    
    # Scalars boxing
    else :
      # Here only mv is supplied as scalar
      if(coeff!=S(1)):
        raise
      t = new(Box,GExpr.nl,sympify(mv))
      t.mv.mtDt = GExpr.nl.mtDt
      t.mv.rlDt = relDt()
      return t

  def sympystr(self,expr:"Box") -> str:
    return str(expr)

  def sympyrepr(self,expr:"Box") -> str:
    return repr(expr)
  
  def __str__(self:"Box") -> str:
    strcf = self.coeff.__str__()
    strmv = self.mv.__str__()
    istr = "\033[1;37;40m[\033[0;37;40m"
    mstr = "\033[1;36;40m!\033[0;37;40m"
    lstr = "\033[1;37;40m]\033[0;37;40m"

    if self.coeff == S(1):
      strcf = ""
      mstr = ""

    str = istr+strcf+mstr+strmv+lstr
    return str
  
  def __repr__(self:"Box") -> str:
    strcf = self.coeff.__repr__()
    strmv = self.mv.__repr__()
    istr = "["
    mstr = "!"
    lstr = "]"
    if self.coeff == S(1):
      strcf = ""
      mstr = ""
    str = istr+strcf+mstr+strmv+lstr
    return str

  def __hash__(self:"Box")->int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h

  def __eq__(self:"Box", other:"Box")->Tuple[bool]:
    # returns a tuple of values (#,#) 
    # ( cf, mv )
    if type(self) == type(other):
      if self.coeff == S(0):
        return other.coeff == S(0)
      else :
        return (
          other.coeff == self.coeff 
          and
          other.mv == self.mv 
        )
    else :
      return False
  
  def __eq1__(self:"Box", other:"Box")->Tuple[bool]:
    # returns a tuple of values (#,#) 
    # ( cf, mv )
    return (
      (other.coeff == self.coeff and
      other.__class__ == self.__class__),
      (other.mv == self.mv and
      other.__class__ == self.__class__)
    )

  def __neg__(self:"Box")->"Box":
    return Box.__new__(Box,mv=self.mv,coeff=Mul(self.coeff,S(-1)))

  @property
  def pSC(self:"GExpr") -> set:
    return self.mv.pSC

  @property
  def grade(self:"GExpr") -> set:
    return self.mv.grade
  
  @property
  def mtDt(self:"Box")->spclst:
    return self.mv.mtDt

  @property
  def rlDt(self:"Box")->relDt:
    return self.mv.rlDt

  @property
  def coeff(self:"Box") -> "GExpr":
    return self.args[1]
  
  @property
  def mv(self:"Box") -> "GExpr":
    return self.args[0]

  def gsimplify(self:"Box"):
    func = type(self.mv).gsimplify
    return func(self)

  def gexpand(self:"Box"):
    func = type(self.mv).gexpand
    return func(self)

  def ghigher(self:"Box"):
    func = type(self.mv).ghigher
    return func(self)

  def reversion(self:"Box")->"Box":
    t = self.mv.reversion()
    return Box.__new__(Box,t,self.coeff)

  def grade_involution(self:"Box")->"Box":
    t = self.mv.grade_involution()
    return Box.__new__(Box,t,self.coeff)
  
  def clifford_conjugation(self:"Box")->"Box":
    t = self.mv.clifford_conjugation()
    return Box.__new__(Box,t,self.coeff)
  
  
# Standard import style
# These extra imports cause issue with strategies import
# from Sygal.operators.assop.gadd import gadd
# from Sygal.operators.assop.gextp import gextp
# from Sygal.operators.assop.gmul import gmul

# from Sygal.operators.binop.ganticomm import ganticomm
# from Sygal.operators.binop.gcomm import gcomm
# from Sygal.operators.binop.sclrprdct import sclrprdct
# from Sygal.operators.binop.grcntrct import grcntrct
# from Sygal.operators.binop.glcntrct import glcntrct


def is_devmode():
  t = 'pydevd' in sys.modules
  return t


if is_devmode():
  StrPrinter._print_Box = Box.sympyrepr
else :
  StrPrinter._print_Box = Box.sympystr


def ceil_mtDt(expr) ->bool:
  # return False

  # This will return is PSC has touched ceiling
  # Also will updat the mtDt
  ################
  # replace or merge when ceiling is touched
  # {I3:3,I41:1} -> replace with I3
  # {I3:2,I41:2} -> {I41:4}
  # TODO
  # {I31:2,I41:1} -> {I31:2,I41:1}
  # {I31:3,I5:1} -> {I5:4}
  # TODO
  # _oo^_x^_y^a1 -> +/-(a1|_oo)*_o^_x^_y^_oo
  return expr
  cls = type(expr)
  if type(expr).__name__== "gextp" and expr not in GExpr.pSClst:
    mv = expr
    if len(mv.mtDt) == 1:
      # is_Unigraded basically
      dct = mv.mtDt[0]
      keys_lst = list(dct)
      
      for i,k in enumerate(keys_lst):
        if dct[k].value == dct[k].limit and dct[k].limit>=1:
          
          pluck_ele = [ele for ele in mv.args if len(ele.mtDt)==1 and (ele.mtDt[0][k].value)]

          pluckmv = Basic.__new__(cls,*pluck_ele)
          pluckmv.rlDt = relDt()
          pluckmv = pluckmv.meta_treatment()
          pluckbx = Basic.__new__(Box,pluckmv,S(1))

          diff = [ele for ele in mv.args if ele not in pluck_ele]

          n_args1 = []
          n_args1.extend(diff)
          n_args1.extend(pluck_ele)
          sign1 = parity(mv.args,n_args1)

          n_args2 = []
          n_args2.extend(diff)
          j = GExpr.pSClst.index(k) 
          n_Frame = GExpr.pSCiFrmlst[j]
          n_args2.extend(k.args)

          coeff = pluckbx|n_Frame

          n_args3 = GSortArgs(n_args2)

          sign2 = parity(n_args3,n_args2)
          n_mv = Basic.__new__(cls,*n_args3)
          n_mv = n_mv.meta_treatment()
          n_mv.rlDt = expr.rlDt
          
          bx = Basic.__new__(Box,n_mv,Mul(sign2,sign1,coeff.coeff))
          return bx
        elif True:
          pass
        else :
          continue
      return expr
    else:
      return expr
  elif type(expr).__name__== "sclrprdct":
    return expr
    raise NotImplementedError
  else:
    return expr


