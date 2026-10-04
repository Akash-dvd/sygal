from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from functools import reduce, lru_cache
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
from Sygal.Box import Box
from Sygal.utils.utils1 import rlGSortArgs,parity,is_unMixedGrade,bx_sift,GSortArgs,is_devmode

@lru_cache(maxsize=128)
def _dct_is_joint_impl(psc1: str, psc2: str):
  """Internal cached implementation of dct_is_joint."""
  for grp in GExpr.Disjoint_Grp:
    if psc1 in grp and psc2 in grp:
      return True
  return False

def dct_is_joint(psc1: str, psc2: str):
  """Check if two pseudoscalar identifiers are in the same disjoint group.
  
  Cached for performance - normalizes argument order for better cache hits.
  """
  # Normalize order BEFORE cache lookup for better cache efficiency
  if psc1 > psc2:
    return _dct_is_joint_impl(psc2, psc1)
  return _dct_is_joint_impl(psc1, psc2)

class GAtom(GExpr,AtomicExpr):

  def __new__(cls, name:str,mtDt:Union[List[Dict],Dict]) -> Box:

    # Pattern match for name -> str
    # TODO check for earlier symbols
    if not isinstance(name, str):
      raise TypeError("name should be a string, not %s" % repr(type(name)))
    
    # Pattern match for mtdt -> dict
    if issubclass(type(mtDt),dict):
      mtDt = spclst([mtDt])
    elif issubclass(type(mtDt),list):
      mtDt = spclst(mtDt)
    else:
      raise ValueError("Iterable must be a list")
    
    # Scalar Check
    if mtDt == [{GExpr.nl:grd(0,0)}]:
      return GExpr.Onl
    else:
      pass

    # BOX INITIALIZER
    bx = GAtom.__xnew_cached_(GAtom, name)
    bx.mv.mtDt = mtDt
    return bx

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

      # Scalar null
      GExpr.Onl = GAtom.__xnew_cached_(GAtom,"\u0950")
      t_dct = dict.__new__(spcdct)
      t_dct.sup_update({GExpr.Onl.mv:grd(0,0)})
      GExpr.Onl.mv.mtDt = spclst([t_dct])
      GExpr.nl = GExpr.Onl.mv

      # To make sure Both Znl and Onl share same _nl
      GExpr.Znl = Basic.__new__(Box,GExpr.nl,S(0)) 
      GExpr.Znl.mv.mtDt = spclst([t_dct])
      
      #######################
      # Define pseudoscalar identifiers as strings
      GExpr.I31 = "I31"
      GExpr.I32 = "I32"
      GExpr.I41 = "I41"
      GExpr.I42 = "I42"
      GExpr.I43 = "I43"
      GExpr.I5 = "I5"
      GExpr.I8 = "I8"
      GExpr.I13 = "I13"
      # Large fermionic / many-body metric (QC benchmarks); not CGA
      GExpr.I1000 = "I1000"
      
      # pSClst contains string identifiers (plus nl for scalar)
      GExpr.pSClst = [
        GExpr.nl,  # Keep nl as special case (multivector)
        "I31", "I32", "I41", "I42", "I43", "I5", "I8", "I13", "I1000"
      ]
      
      # Grade limits mapping: identifier -> Clifford vector dimension n (max grade n)
      GExpr.grdlmt_map = {
        "I31": 3, "I32": 3, "I41": 4, "I42": 4,
        "I43": 4, "I5": 5, "I8": 8, "I13": 13, "I1000": 1000
      }
      
      # Disjoint groups (for is_joint function)
      GExpr.Disjoint_Grp = [
        ["I31", "I32", "I41", "I42", "I43", "I5"],
        ["I8"],
        ["I13"],
        ["I1000"],
      ]
      
      # pSCiFrmlst - kept for backward compatibility but may not be needed
      # This would need to be redefined if still used
      GExpr.pSCiFrmlst = []
      
      # grdlmt table - kept for backward compatibility
      # This is a 2D table indexed by pSClst position
      # For now, we'll keep it but it may need updating
      # Legacy joint-grade table: rows/cols follow pSClst order (see spcdct.__or__)
      _grd0 = [I, 0, 0, 0, 0, 0, 0, 0, 1, 0]
      GExpr.grdlmt = [
        [I, I, I, I, I, I, I, I, I, I],
        _grd0,
        [I, 0, 1, 0, 1, 1, 1, 0, 1, 0],
        [I, 0, 0, 1, 1, 1, 1, 0, 1, 0],
        [I, 0, 1, 1, 2, 2, 2, 0, 1, 0],
        [I, 0, 1, 1, 2, 2, 2, 0, 1, 0],
        [I, 0, 1, 1, 2, 2, 2, 0, 1, 0],
        [I, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [I, 1, 1, 1, 1, 1, 1, 1, 13, 0],
        [I, 0, 0, 0, 0, 0, 0, 0, 0, 1000],
      ]
      
      # primmv and primbx - may still be needed for some operations
      # For now, we'll keep them empty or minimal
      GExpr.primbx = []
      GExpr.primmv = []
      
      # _oo (point at infinity) - vector grade 1, required by frptConf for CGA metric and objMap
      mtDt_41 = {GExpr.I41: 1}
      GExpr._oo = GAtom("_oo", mtDt_41)
      # I41 pseudoscalar - grade 4 (like _oo is grade 1), for contractions blade<I41
      mtDt_I41_ps = {GExpr.I41: 4}
      GExpr.I41_ps = GAtom("I41_ps", mtDt_I41_ps)
      # I1000 pseudoscalar - grade 1000 (optional; use for blade < I1000_ps in I1000-only algebra)
      mtDt_I1000_ps = {GExpr.I1000: 1000}
      GExpr.I1000_ps = GAtom("I1000_ps", mtDt_I1000_ps)
      # _rx - not currently used, keep None
      GExpr._rx = None
      
      GExpr.initialized = True 
  
  __xnew__ = staticmethod(
    __new_stage2__)            # never cached (e.g. dummy)
  __xnew_cached_ = staticmethod(
    cacheit(__new_stage2__))   # symbols are always cached
