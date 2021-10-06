from typing import List  # Note the upper-case letter

import sys
sys.path.append('/app/solver')
# print(sys.path)

from collections import defaultdict

from sympy import Basic
from sympy.core.singleton import S

from libs.Sygal.GV import GV,gv
from libs.Sygal.utils import rlZero ,conjugation
from libs.Sygal.GExpr import GExpr
from libs.Sygal.operators import (add,anticomm,comm,extp,
inprdct,lcntrct,mul,rcntrct)

from sympy.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from sympy.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from sympy.strategies.tools import subs, typed ,canon
from sympy.strategies.traverse import (top_down, bottom_up, sall, top_down_once,bottom_up_once, basic_fns)
from sympy.strategies.tree import treeapply, greedy, allresults, brute

a1 = GV('a_1')
a2 = GV('a_2')
a3 = GV('a_3')
b1 = GV('b_1')
b2 = GV('b_2')
b3 = GV('b_3')
c1 = GV('c_1')
c2 = GV('c_2')
c3 = GV('c_3')
d1 = GV('d_1')
d2 = GV('d_2')
d3 = GV('d_3')

new = Basic.__new__

class concat():  
  @staticmethod
  def sandhi(expr:GExpr) -> GExpr:
    """bottom up conjugation by rlzero of single layer sub_sandhi
    
    """
    fn = bottom_up(conjugation(rlZero,concat.sandhi1))
    return fn(expr)

  @staticmethod
  # Function for single layer Sandhi
  def sandhi1(expr:GExpr) -> GExpr:

    lst1 = []
    # Pattern Match (<Grade-1>)(<>)(Exterior Product)
    # TODO Write a pattern matching api call
    for i, x in enumerate(expr.args):
      if (isinstance(x,lcntrct) or isinstance(x,rcntrct)) and\
          (x.args[0].grade == 1) and isinstance(x.args[1],extp):
        lst1.append((x.args[0],i))
    # lst1 = [(_rx, 0), (_rx, 1), (_oo, 2),(_oo,3),(_rx,4)]
    if(len(lst1)>0):
      lst2 = concat.aggregator(lst1)
      # lst2 = [(_rx, 0, 1, 4), (_oo, 2, 3)]
      T = list(expr.args)
      cum_indx = []
      
      for elem in lst2:
        indx = list(elem[1:])
        cum_indx.extend(indx)
        # (0,1,4)
        vec = elem[0]
        T1 = [expr.args[i].args[1] for i in indx]
        # T1 -> [a1^a2,a2^a3..]
        T2 = concat.sub_sandhi1(T1)
        # T2 -> [a1^a2^a3..]
        T3 = [vec<(x) for x in T2]
        # T3 = rx<(a1^a^a3),...
        T.extend(T3)
        
      for index in indx:
        del T[index]
      
      expr = new(type(expr), tuple(T3))


    return expr
  
  @staticmethod
  def aggregator(lst:List[GExpr]) -> List[GExpr]:
    """
    Explanation


    lst is list of binary tuples.
    Tule's 1st part is symbol and 2nd is index
    lst = [(_rx, 0), (_rx, 1), (_oo, 2),(_oo,3),(_rx,4)]
    aggregator(lst) == [(_rx, 0, 1, 4), (_oo, 2, 3)]
    """
    mapp = defaultdict(list) 
    for x, y in lst: 
      mapp[x].append(y) 
      lst2 = [(x, *y) for x, y in mapp.items()] 
    return lst2
  
  @staticmethod
  def sub_sandhi1(exprList:List[GExpr]) -> List[GExpr]:
    index = [0,1]
    exprList1 = exprList.copy()
    # lstln = lambda lst:len(lst)
    while index[0]<len(exprList1):
      index[1]=index[0]+1
      while index[1]<len(exprList1):
        exprList1 = concat.sub_sub_sandhi1(index,exprList1)
      index[0]+=1
      
    return exprList1

  @staticmethod
  def sub_sub_sandhi1(index:List,exprList:List[GExpr]) -> List[GExpr]: 
    expr1 = exprList[index[0]] 
    expr2 = exprList[index[1]]
    ln1 = len(expr1.args)+len(expr2.args)
    expr3Set = set(expr1.args)
    expr3Set.update(set(expr2.args))
    ln2 = len(expr3Set)

    arg1 = tuple(expr3Set)
    sub1 = expr1.func(*arg1)

    x = ln1-ln2
    if (x==0):
      index[1]+=1
      return exprList
    elif(x==1):
      exprList[index[0]] = sub1
      del exprList[index[1]]
      index[1]=index[0]+1
      return exprList
    else :
      return [S(0)]

@staticmethod
def Rcntrct2Lcntrct():
  pass

@staticmethod
def Lcntrct2Rcntrct():
  pass


expr = (a1<(b1^b2^a2))^(a1<(b2^b3))^(b2<(b1^b3))^(b2<(a2^b3))
concat.sandhi(expr)