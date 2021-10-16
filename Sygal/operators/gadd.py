from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union,NewType,Type,Any

from collections import defaultdict
from functools import cmp_to_key
import operator


from sympy.core.sympify import sympify
from sympy.core.basic import Basic
from sympy.core.singleton import S
from sympy.core.operations import AssocOp
from sympy.core.cache import cacheit
from sympy.core.logic import fuzzy_not, _fuzzy_group, fuzzy_and
from sympy.core.compatibility import reduce
from sympy.core.expr import Expr
from sympy.core.parameters import global_parameters

from sympy import (
    diff, Rational, Symbol, S, Mul, Add, Expr,
    expand, simplify, eye, trigsimp,cos,sin,
    symbols, sqrt, Matrix, SympifyError, sympify
)

from sympy.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from sympy.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from sympy.strategies.tools import subs, typed ,canon
from sympy.strategies.traverse import (top_down, bottom_up, sall, top_down_once,bottom_up_once, basic_fns)
from sympy.strategies.tree import treeapply, greedy, allresults, brute

from libs.Sygal.GExpr import GExpr
from libs.Sygal.Box import Box
from libs.Sygal.utils import Boxify,bx_sift

class gadd(GExpr) :
  identity = Box.Znl

  sift_key = lambda x:x.args[1]
  sift_count = lambda x:x.args[0]
  sift_combine = lambda cnt,args:Box.__new__(Box,args,cnt.simplify())

  def __new__(cls, args0:GExpr,*args:Tuple["GExpr"],**kwargs) -> Box:
    # gadd(Box,Optional[Box,Box.....])

    # Pattern Matching for # of args for associative op
    t =  [args0]
    t.extend(args)
    t1 = tuple(map(Boxify, t))
    if(len(t1)==1):
      return t1
    
    
    t2 = []
    # Flatten coz of gadd present inside Box
    for BX in t1:
      # Pattern Match
      # For ele == gadd inside Box or only Box
      if(type(BX)==Box and type(BX.args[1])==gadd):
        
        # Pattern Match
        # For child == atom or list
        if(BX.args[1].is_atom):
          t2.append(BX)
        else:
          # Remove Gadd ,multiplyu its coeff with all child
          child = BX.args[1].args
          coeff = BX.args[0]
          lst = [Box.__new__(Box,bx.args[1],Mul(bx.args[0],coeff).simplify()) for bx in child]

          t2.extend(lst)
      
      else :
        t2.append(BX)
    
    obj = Basic.__new__(gadd, *t2)
    # Flatten rule is useless
    obj1 = canonicalize(obj)
    # Debox Gadd child to flatten it
    # Multiply Gadd coeff inside 

    # Sort Add arguements 
    # Pattern Match
    # For obj1 == gadd or GB or GExpr
    if(type(obj1)==gadd): 
      # Glom Boxes

      grouped = bx_sift(obj1.args,gadd.sift_key,gadd.sift_count)

      # Sort Boxes
    
      Sortedseq = sorted(grouped,key=lambda bx:(len(bx.args[1].grade),next(iter(bx.args[1].grade)),bx.args[1].name,bx.args[1].__hash__()))
      

      if(len(Sortedseq)>1):
        obj2 = Basic.__new__(gadd, *Sortedseq)
        return Boxify(obj2)
      elif (len(Sortedseq)==1):
        singarg = Sortedseq[0]
        return Boxify(singarg)
      else:
        # case for gadd(no arguements)
        raise
        
      
    elif(type(obj1)==Box):
      # When gadd is unmasked
      return obj1
    else :
      # Not possible
      raise 
    

    

  @property
  def grade(self:"gadd") -> int:
    t = set()
    for i in self.args:
      t.update(i.grade)
    return t

  def __str__(self:"gadd") -> str:
    ls = self.args
    str = '('
    for o in ls:
      str += o.__str__()+'+'
    str = str[:-1]
    str += ')'
    return str

  __repr__ = __str__


  def __hash__(self:"gadd") -> int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self:"gadd", other:"GExpr") -> bool:
    return (
      (type(other) == type(self)) and
      self.__hash__() == other.__hash__()
    )

  def __neg__(self:"gadd") -> "gadd":
    c, args = self.as_coeff_mul()
    c = -c
    if c is not S.One:
      if args[0].is_Number:
        args = list(args)
        if c is S.NegativeOne:
          args[0] = -args[0]
        else:
          args[0] *= c
      else:
        args = (c,) + args
    return self._from_args(args, self.is_commutative)



rules = (
  unpack, flatten
  # Flatten is useless
  )

# rules = (
#   unpack, rm_id(lambda x: x == 0), flatten,sort(lambda ele: ele.grade)
#   )

canonicalize = exhaust(typed({gadd: do_one(*rules)}))
