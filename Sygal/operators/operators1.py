from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union


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

from libs.Sygal.GExpr import GExpr

from sympy.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from sympy.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from sympy.strategies.tools import subs, typed ,canon
from sympy.strategies.traverse import (top_down, bottom_up, sall, top_down_once,bottom_up_once, basic_fns)
from sympy.strategies.tree import treeapply, greedy, allresults, brute

from libs.Sygal.utils.rules import rlGSortArgs

ClassCreation = Callable[[Basic,Tuple[GExpr]],GExpr]

new = Basic.__new__

class opsum(GExpr):
  # treat like sum
  identity = S(0)
  def __new__(cls, *args:Tuple["GExpr"],**kwargs) -> Union["opsum",S]:
    if not args:
      return S(0)

    t1 = filter(lambda i: cls.identity != i, args)
    t2 = tuple(map(sympify, t1))
    
    return Basic.__new__(cls, *t2)



  @property
  def grade(self:"opsum") -> set:

    t = set()
    for i in self.args:
      t.update(nullsafeGrade(i))
    return t


class opextp(GExpr):
  # treat like extp
  identity = S(1)
  def __new__(cls, *args:Tuple["GExpr"],**kwargs) -> Union["opextp",S]:
    if not args:
      return S(0)

    t1 = filter(lambda i: cls.identity != i, args)
    t2 = tuple(map(sympify, t1))
    t3 = Basic.__new__(cls, *t2)
    
    obj = extpcanonicalize(t3) 
    return obj


  @property
  def grade(self:"opextp") -> Optional[set]:
    
    t1 = set()
    t2 = set()
    t1.update(nullsafeGrade(self.args[0]))
    for i,elem1 in enumerate(self.args):
      j=i+1
      if(j<len(self.args)):
        t2.clear()
        arg2 = nullsafeGrade(self.args[j])
        for elem1 in t1:
          for elem2 in arg2:
              t2.add((elem2+elem1))
        t1.clear()
        t1.update(t2)
    return t2


class opmul(GExpr):
  # treat like mul
  identity = S(1)
  def __new__(cls, *args:Tuple["GExpr"],**kwargs) -> Union["opmul",S]:
    if not args:
      return S(0)

    t1 = filter(lambda i: cls.identity != i, args)
    t2 = tuple(map(sympify, t1))
    t3 = Basic.__new__(cls, *t2)

    obj = mulcanonicalize(t3) 
    return obj
     


  @property
  def grade(self:"opmul") -> Optional[set]:
    if(len(self.args==2)):
      if ((nullsafeGrade(self.args[0]) == {0}) or (nullsafeGrade(self.args[1]) == {0})) :
        if (nullsafeGrade(self.args[0]) == {0}):
          return nullsafeGrade(self.args[1])
        else :
          return nullsafeGrade(self.args[0])
      else :
        return None    
    else :
      return None


class oplcntrct(GExpr):
  # treat like lcntrct
  identity = S(1)
  def __new__(cls, *args:Tuple["GExpr"],**kwargs) -> Union["oplcntrct",S]:
    if not args:
      return S(0)

    t1 = filter(lambda i: cls.identity != i, args)
    t2 = tuple(map(sympify, t1))
    t3 = Basic.__new__(cls, *t2)
    
    obj = lcntcanonicalize(t3) 
    return obj


  @property
  def grade(self:"oplcntrct") -> Optional[set]:
    arg1 = nullsafeGrade(self.args[0])
    arg2 = nullsafeGrade(self.args[1])
    t = set()
    for elem1 in arg1:
      for elem2 in arg2:
        if((elem2-elem1)>=0):
          t.add((elem2-elem1))

    return t

def rlmulextpCoeffs(expr:GExpr,new:ClassCreation=new) -> GExpr:
  # CRUD rlmulsumCoeffs operation should be null safe
  # expr = a1^S1*S2^b2 -> a1^b2 ,coeffs = S1*S2
  
  # Check for one arguement thing
  # Which is handled by rlGunpack
  cond = (isinstance(expr,opextp)) or (isinstance(expr,opmul)) 
  if(cond):

    T = list(expr.args)
    appn = []
    cum_indx = []
    for i, x in enumerate(expr.args):
      if (nullsafeGrade(x)=={0}):
        appn.append(x)
        cum_indx.append(i)
    
    for indx in cum_indx:
      T[indx] = None
    # If no changes then return
    if(appn !=[]):
      T1 = tuple(filter((None).__ne__, T))

      expr1 = new(expr.__class__, *T1)
      expr1.coeffs = expr.coeffs

      if(expr1.coeffs == [S(1)]):
        expr1.coeffs = appn  
      else :
        expr1.coeffs.extend(appn)
      return expr1
    else:
      return expr
    # Coz umask will remove the coefficient attached
    # T1 = tuple(filter((None).__ne__, T))
    # if len(T1) != 1:
    #   expr1 = new(expr.__class__, *T1)
    #   expr1.coeffs.extend(appn)
    #   return expr1
    # else :
    #   print(T1," ",expr)
    #   T1[0].coeffs.extend(appn)
    #   expr1 = new(expr.__class__, *T1)
    #   return expr1
  else :
    return expr

def rlCollectCoeffs(expr:GExpr,new:ClassCreation=new) -> GExpr:

  # CRUD coeff operation should be null safe
  # Leaves scalars encountered on the way
  # Here it will always for irrespect of parent and child types

  appn = []

  for i, x in enumerate(expr.args):
    # Check if x is extr or has 1 coeff
    if (nullsafeCoeff(x) != [S(1)]) and (nullsafeCoeff(x) != []):
      appn.extend(nullsafeCoeff(x))
      # Null safe update
      x.coeffs = [S(1)]
  if(nullsafeCoeff(expr)==[S(1)]):
    expr.coeffs = appn
  else:
    nullsafeCoeff(expr).extend(appn)
  return expr

def rlGunpack(expr:GExpr)->GExpr:
  # Structural Pattern Matching of types and cases(~S(1)) B4 unpacking
  # Here expr will always be from GExpr and never from Expr
  # It will always have coeffs

  # Case 1 - Type check
  if(nullsafeCoeff(expr)==[]):
    return expr
  else :
    # Case 2 - Eligibility Check
    if len(expr.args) == 1:

      PrtCoeff = nullsafeCoeff(expr)
      isPrtGood = (PrtCoeff!=[])
      
      ChldCoeff = nullsafeCoeff(expr.args[0])
      isChldGood = (ChldCoeff!=[])
      # Case a
      # Both parent and child are good
      if(isPrtGood and  isChldGood):
        if(ChldCoeff == [S(1)]):
          expr.args[0].coeffs = PrtCoeff  
        else :
           expr.args[0].coeffs.extend(PrtCoeff)
        
        
        return expr.args[0]
      # Case b
      # Parent is good but child is not
      elif (isPrtGood and (not isChldGood)):
        if(PrtCoeff == [S(1)]):
          expr.coeffs = expr.args[0]
        else :
          expr.coeffs.extend(expr.args[0])
        return expr
        # rlmulsumCoeffs's work
      else :
        # parent is bad
        # Not possible coz of the check above .. Still
        raise    

    elif len(expr.args) == 0:
      return expr
      # MAYbe change
    
    else:
      return expr


def nullsafeGrade(arg):
  try:
    return arg.grade
  except AttributeError:
    return {0}

def nullsafeCoeff(arg):
  try:
    return arg.coeffs
  except AttributeError:
    return []


rules = (
  rm_id(lambda x: x == S(1)),flatten,rlCollectCoeffs,rlmulextpCoeffs,rlGunpack
  )

lctrules = (rm_id(lambda x: x == S(1)),
  rlCollectCoeffs
  )



mulcanonicalize = exhaust(typed({opmul: do_one(*rules)}))
extpcanonicalize = exhaust(typed({opextp: do_one(*rules)}))
lcntcanonicalize = exhaust(typed({oplcntrct: do_one(*lctrules)}))
