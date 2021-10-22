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
from libs.Sygal.operators import (gadd,ganticomm,gcomm,gextp,
ginprdct,glcntrct,gmul,grcntrct)

from sympy.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from sympy.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from sympy.strategies.tools import subs, typed ,canon
from sympy.strategies.traverse import (top_down, bottom_up, sall, top_down_once,bottom_up_once, basic_fns)
from sympy.strategies.tree import treeapply, greedy, allresults, brute

new = gextp.__new__


"""
TODO
TODO
TODO
TODO
((a1^a2..a_r)<((b1..br)^(c1..cm)))^((a1..a_r)<((b1..br)^(d1..dn))) ==
(a1^a2..a_r)<((b1..br)^(c1..cm)^(d1..dn))
Will be done after implementing dot product and multiplication.
"""

class concat():  
    
  @staticmethod
  def sandhi(expr:GExpr,depth:int = 0) -> GExpr:
    """bottom up conjugation by rlzero of single layer sub_sandhi
    
    """
    fn1 = concat.sandhi0(depth)
    fn = bottom_up(conjugation(rlZero,fn1))
    return fn(expr)

  @staticmethod
  def sandhi0(depth:int):
    def sandhi1(expr:GExpr) -> GExpr:
      
      """
      Sandhi Implementation
      =====================

      This function is meant for accomplishing single layer merge for x1^x2^a<(b^c)^a<(c^d) structure.
      It filters indexes having lncrt or rncrt.
      [(_rx, 0), (_rx, 1), (_oo, 2),(_oo,3),(_rx,4)]
      Then calls aggregator function to merge the indexes of lncrt or rncrt structures.
      lst2 = [(_rx, 0, 1, 4), (_oo, 2, 3)]

      Following this it call sub_sandhi1 on each tuple.(_rx, 0, 1, 4). BBut instead of indexes supplies list of denominator values of corresponding indexes.
      It expects the merhed version of the supplied indexes.
      It keeps appening the results to the arg list and After the list is exhausted it deletes the older arguements.
      Then recreates the expr with new args and returns.
      """
    
      lst1 = []
      # Pattern Match (<Grade-1>)(<>)(Exterior Product)
      # TODO Write a pattern matching api call
      if(isinstance(expr,gextp)):
        for i, x in enumerate(expr.args):
          if (isinstance(x,glcntrct) or isinstance(x,grcntrct)) and\
              (x.args[0].grade == {1}) and isinstance(x.args[1],gextp):
            lst1.append((x.args[0],i))
      # lst1 = [(_rx, 0), (_rx, 1), (_oo, 2),(_oo,3),(_rx,4)]
      
      # Only execute if above filter has matches present.
      if(len(lst1)>0):
        lst2 = concat.aggregator(lst1)
        # lst2 = [(_rx, 0, 1, 4), (_oo, 2, 3)]

        """
        Two sequential for loops
        Loop1
        
        Expects - expr and lst2
        Behavoir -  Loop over the lst2 tuples .
        1) Supply sub_sandhi1 with denominator w.r.t the indexes present.
        2) Appends the corresponding numerator and appends them to temporary arg list(T).
        3) Accumulate the indexes accross the tuples into cum_indx.
        
        Loop2
        1) Mark the elements T corrsponding to the indexes in cum_indx
        """
        T = list(expr.args)
        cum_indx = []
        for elem in lst2:
          indx = list(elem[1:])
          cum_indx.extend(indx)
          # (0,1,4)
          vec = elem[0]
          T1 = [expr.args[i].args[1] for i in indx]
          # T1 -> [a1^a2,a2^a3..]
          T2 = concat.sub_sandhi1(T1,depth+1)
          # T2 -> [a1^a2^a3..]
          T3 = [vec<(x) for x in T2]
          # T3 = rx<(a1^a^a3),...
          T.extend(T3)
        
        
        for indx in cum_indx:
          T[indx] = None
      
        
        expr = new(expr.__class__, *tuple(filter((None).__ne__, T)))
      
      return expr
    return sandhi1 
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
  def sub_sandhi1(exprList:List[GExpr],depth:int) -> List[GExpr]:
    index = [0,1]
    exprList1 = exprList.copy()
    # lstln = lambda lst:len(lst)
    while index[0]<len(exprList1):
      index[1]=index[0]+1
      while index[1]<len(exprList1):
        exprList1 = concat.sub_sub_sandhi1(index,exprList1,depth)
        index[1]+=1
      index[0]+=1
      
    return exprList1

  @staticmethod
  def sub_sub_sandhi1(index:List,exprList:List[GExpr],depth:int ) -> List[GExpr]: 
    expr1 = exprList[index[0]] 
    expr2 = exprList[index[1]]
    ln1 = len(expr1.args)+len(expr2.args)
    # grd1= expr1.grade
    # grd2= expr2.grade
    expr3Set = set(expr1.args)
    expr3Set.update(set(expr2.args))
    ln2 = len(expr3Set)
    

    arg1 = tuple(expr3Set)
    sub1 = expr1.func(*arg1)

    x = ln1-ln2-depth
    # print("x=",x,"depth=",depth,"len1=",ln1,"len2=",ln2)
    # print(expr1)
    # print(expr2)
    
    if(x<0):
      Tsub1 = concat.sandhi(sub1,depth)
      if(Tsub1==sub1):
        return exprList
      else:
        exprList[index[0]] = Tsub1
        del exprList[index[1]]
        index[1]=index[0]
        return exprList        
    
    elif (x==0):
      #####
      exprList[index[0]] = concat.sandhi(sub1,depth)
      #####
      del exprList[index[1]]
      index[1]=index[0]
      return exprList      

    else:
      return [S(0)]


@staticmethod
def Rcntrct2Lcntrct():
  pass

@staticmethod
def Lcntrct2Rcntrct():
  pass


# expr = a2^(a1<((b1<(a1^a2)^b2)))^(a1<((b1<(a3^a2)^b3)))
# concat.sandhi(expr)