from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union

from functools import reduce
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
from libs.Sygal.utils import Boxify,rlGSortArgs,is_unMixedGrade,parity

class gextp(GExpr):

  identity = Box.Onl

  def __new__(cls, *args:Tuple["GExpr"],**kwargs) -> Box:
    if not args:
      return cls.identity

    t1 = tuple(map(Boxify, args))
    
    deBoxargs = [bx.args[1] for bx in t1 if bx.args[1]!=Box.nl]
    if deBoxargs == []:
      deBoxargs=[Box.nl]

    obj = Basic.__new__(gextp, *deBoxargs)
    coeffs = [bx.args[0] for bx in t1]
    
    obj1 = canonicalize1(obj)
    coeff = Mul(*coeffs).simplify()
    
    # chkList = [is_parityGrade(val) for val in deBoxargs1]
    # check = reduce(lambda a,b:a and b ,chkList)
    # if(check):

    # THis obj1 below is very bad it seems
    # Logically is correct but very deep logic
    # MAy be write tests for boundary cases
    if(is_unMixedGrade(obj1)):
      # check for boundary cases
      # For single arguement typed wont let cannocalize work
      # gextp(gextp(gextp())) .... Not possible coz its binary op
      # Or only scalar present .. Done 
      # rather every element of immediate child is of odd or even grade
      obj2 = canonicalize2(obj1)
      
      coeffs.append(parity(obj2.args,obj1.args))
      coeff = Mul(*coeffs).simplify()
    else :
      obj2 = obj1
    obj3 = Box.__new__(Box,obj2,coeff)
    
    # if ((len(args)-len(set(args))) == 0): 
    # IMplement After Pseudo sclalr  
    #   obj = Basic.__new__(cls, *t1)
    # else :
    #   t3 = super().Znl
    #   return Basic.__new__(cls, *t3)

    check = kwargs.get('check', False)
    if check:
      # Use this for pseudoscalar checks
      pass
      
      # if all(not isinstance(i, MatrixExpr) for i in args):
      #   return Add.fromiter(args)
      # validate(*args)

    
    return obj3

  @property
  def grade(self:"gextp") -> set:
    if(len(self.args)==1):
      return self.args[0].grade
    else:
      t1 = set()
      t2 = set()
      t1.update(self.args[0].grade)
      for i,argi in enumerate(self.args):
        j=i+1
        if(j<len(self.args)):
          t2.clear()
          arg2 = self.args[j].grade
          for elem1 in t1:
            for elem2 in arg2:
              t2.add((elem2+elem1))
          t1.clear()
          t1.update(t2)
    return t2

  def __str__(self:"gextp") -> str:
    ls = self.args
    str = '('
    for o in ls:
      str += o.__str__()+'^'
    str = str[:-1]
    str += ')'
    return str

  __repr__ = __str__

  def __hash__(self:"gextp") -> int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self:"gextp", other:"GExpr") -> bool:
    return (
      (type(other) == type(self)) and
      self.__hash__() == other.__hash__()
    )

  def __neg__(self:"gextp") -> "gextp":
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
  

# rules = (
#   unpack, rm_id(lambda x: x == 1), flatten,rlGSortArgs
#   )
rules1 = (
    unpack,flatten
  )
rules2 = (
    unpack,rlGSortArgs
  )


canonicalize1 = exhaust(typed({gextp: do_one(*rules1)}))
canonicalize2 = exhaust(typed({gextp: do_one(*rules2)}))
