from collections import defaultdict
import sys

from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,sympify,
  symbols, sqrt, Matrix,srepr,bottom_up
)
from sympy.strategies.tools import subs as strtSubs

from sympy.printing.str import StrPrinter

from libs.Sygal.GExpr import GExpr
from libs.Sygal.pSC import spclst
from libs.Sygal.utils.util import relDt




class Box(GExpr):
  # Chnage here for S(0) coeff
  def __new__(cls,mv:"GExpr"=S(1),coeff:Expr=S(1))->"Box":
    if(type(coeff)==Box):
      raise ValueError
    

    # Pattern matching for types
    fct1 = issubclass(type(mv),GExpr)
    # fct2 is for scalar multivectors
    fct2 = fct1 and (mv.grade == {0})
    fct3 = issubclass(type(mv),Box)
    fct4 = fct3 and fct2
    
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
      if(type(BX.mv)==gadd):
        # Well formed gadd box always has S(1) coeff
        if(BX.coeff!=S(1)):
          raise
        t = [new(Box,bx.mv,Mul(bx.coeff,coeff)) for bx in BX.mv.args]
        t1 = new(Box,new(gadd,*t),S(1))
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
        t = new(Box,GExpr.nl,Mul(mv,coeff))
        t.mv.mtDt = GExpr.nl.mtDt
        t.mv.rlDt = relDt()
        return t
    # Non Zero grade
    elif fct1:
      if(type(mv)==gadd):
        # t = [new(Box,bx.mv,Mul(bx.coeff,coeff).simplify()) for bx in mv.args]
        t = [new(Box,bx.mv,Mul(bx.coeff,coeff)) for bx in mv.args]
        t1 = new(Box,new(gadd,*t),S(1))
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
from libs.Sygal.operators.assop.gadd import gadd
# from libs.Sygal.operators.assop.gextp import gextp
# from libs.Sygal.operators.assop.gmul import gmul

# from libs.Sygal.operators.binop.ganticomm import ganticomm
# from libs.Sygal.operators.binop.gcomm import gcomm
# from libs.Sygal.operators.binop.sclrprdct import sclrprdct
# from libs.Sygal.operators.binop.grcntrct import grcntrct
# from libs.Sygal.operators.binop.glcntrct import glcntrct


def is_devmode():
  t = 'pydevd' in sys.modules
  return t


if is_devmode():
  StrPrinter._print_Box = Box.sympyrepr
else :
  StrPrinter._print_Box = Box.sympystr


def rej_mtDt(expr):
  return
  ################
  # replace or merge when ceiling is touched
  # {I3:3,I41:1} -> replace with I3
  # {I3:2,I41:2} -> {I41:4}
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    for i,k,v in enumerate(BX.mv.mtDt.items()):
      if not k == GExpr.nl:
        if v == set(len(k.mv.args)):
          lst = [ele for ele in BX.mv.args if ele.mtDt[k] and len(ele.mtDt)==1 and len(ele.mtDt[k])==1]
          if len(k.mv.args) == reduce(lambda x,y:x.mv.mtDt[k]+y.mv.mtDt[k],lst) :
            diffA = [ele for ele in BX.mv.args if ele not in lst]
            cpydiffA = []
            cpydiffA.extend(diffA)
            cpydiffA.extend(lst)
            sign1 = parity(BX.mv.args,cpydiffA)
            cpydiffB = []
            cpydiffB.extend(diffA)
            cpydiffB.extend(k.mv.args)
            t_lst = gextp(*lst)
            iFrame = GExpr.pSCiFrmlst(GExpr.pSClst.index(k))
            bx = gextp(*cpydiffB)*(t_lst|iFrame)*sign1*cf
            bx.mv.mtDt = relDt()
            bx.mv.rlDt = relDt()
            return bx
  
        else :
          pass
      else:
        pass
  else :
    return expr