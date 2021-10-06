import sys
sys.path.append('/app/solver')
# print(sys.path)

from libs.Sygal.GV import GV,gv
from libs.Sygal.utils import rlZero

from collections import defaultdict
from libs.Sygal.GExpr import GExpr
from libs.Sygal.operators import (add,anticomm,comm,extp,
inprdct,lcntrct,mul,rcntrct)
from collections import defaultdict


from sympy.core.singleton import S

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


class simplification():  

  def sandhi(expr):
    # extend for more checks
    expr = bottom_up(rlZero)(expr)
    if expr == S(0):
      return S(0)
    else :
      lst1 = []

      # Pattern Match (<Grade-1>)(<>)(Exterior Product)
      # TODO Write a pattern matching api call
      for i, x in enumerate(expr.args):
        if (isinstance(x,lcntrct) or isinstance(x,rcntrct)) and\
          (x.args[0].grade == 1) and isinstance(x.args[1],extp):
          lst1.append((x.args[0],i))
      
      lst2 = simplification.aggregator(lst1)
      print(lst2)
      for elem in lst2:
        tlst = elem[1:]
        vec = elem[0]
        T = [expr.args[i] for i in tlst]
        # T -> [a1^a2,a2^a3..]
        T1 = simplification.sandhi1(T)
        # T1 -> [a1^a2^a3..]
        for index in tlst:
          if index < len(T1):
            expr.args[index] = (vec<(T1[index]))
          else :
            del expr.args[index]

      
      # For others A>B 
      # Recursively the parent sandhi oon A,B and replace if changed 

      others = []
      for i, x in enumerate(expr.args):
        if (isinstance(x,lcntrct) or isinstance(x,rcntrct)) and\
          (x.args[0].grade > 1) and isinstance(x.args[1],extp):
          x.args[0] = simplification.sandhi(x.args[0])
          x.args[1] = simplification.sandhi(x.args[1])
          
      
      
      return expr
  
  def aggregator(lst):
    """
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

  def sub_sandhi1(index,exprList):
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

      exprList = simplification.sandhi(sub1)
      #  Create sandhi for (o1,1,3,4),(rx,5,6,7)
      index[1]+=1
      return exprList
    elif(x==1):
      exprList[index[0]] = sub1
      del exprList[index[1]]
      index[1]=index[0]+1
      return exprList
    else :
      exprList[index[0]] = sub1
      del exprList[index[1]]
      index[1]=index[0]+1

      return S(0)
  
  def sandhi1(exprList):
    index = [0,1]
    exprList1 = exprList.copy()
    # lstln = lambda lst:len(lst)
    while index[0]<len(exprList1):
      index[1]=index[0]+1
      while index[1]<len(exprList1):
        exprList1 = simplification.sub_sandhi1(index,exprList1)
        if (exprList1 == S(0)):
          return S(0)
      index[0]+=1
      
    return exprList1




# Inorder Traversal Not done
@staticmethod
def sandhiRule(expr):
  if isinstance(expr,extp):
    lst = expr.args
    lst1 = []
    for i, x in enumerate(lst):
      if (isinstance(x,lcntrct) or isinstance(x,rcntrct)) and\
        (x.args[0].grade == 1) and\
        isinstance(x.args[1],extp):
        lst1.append((x.args[0],i))
  
  return new(expr.__class__, *args)

@staticmethod
def sandhi2(expr):

  # pattern1 = pattern(pat1)
  # merger =
  # sandhi = chain(pattern1,aggregator,merger)
  # rv = sandhi(expr)

  lst = expr.args
  lst1 = []

  # Pattern Match (<Grade-1>)(<>)(Exterior Product)
  # TODO Write a pattern matching api call
  for i, x in enumerate(lst):
    if (isinstance(x,lcntrct) or isinstance(x,rcntrct)) and\
      (x.args[0].grade == 1) and isinstance(x.args[1],extp):
      lst1.append((x.args[0],i))
  
  # lst = [(_rx, 0), (_rx, 1), (_oo, 2),(_oo,3),(_rx,4)]
  # aggregator(lst) == [(_rx, 0, 1, 4), (_oo, 2, 3)]
  lst2 = aggregator1(lst1)
  lst3 = []


  for elem in lst2:
    dist = len(elem)
    
    for i in range(1,dist):
      for j in range(i+1,dist):
        el1 = lst[elem[i]].args[1]
        el2 = lst[elem[j]].args[1]
        # print('{}-{}'.format(el1,el2))
        intsctn = set(el1.args) & set(el2.args) 
        if (intsctn):

          # if len(intsctn)>1:
          #   raise
          # else :
          instlst = list(intsctn)
          # inst1 = intsctn.pop()
          inst1 = instlst[0]
          instlst.pop(0)
          if inst1.grade == 1:
            arg1 = list(set(el1.args) | set(el2.args))
            arg1.extend(instlst)
            arg2 = tuple(arg1)
            sub1 = lst[elem[i]].args[1].func(*arg2)
            arg3 = tuple([lst[elem[i]].args[0],sub1])
            sub2 = lst[elem[i]].func(*arg3)
            expr1 = expr.sSubs([(lst[elem[i]],sub2),(lst[elem[j]],None)])
            print(expr1)
            _,rv = simplification.sandhi2(expr1)
            return True, rv 
          else :
            raise
  return False, expr

@staticmethod
def Rcntrct2Lcntrct():
  pass

@staticmethod
def Lcntrct2Rcntrct():
  pass


def aggregator1(expr):
  """
  lst is list of binary tuples.
  Tule's 1st part is symbol and 2nd is index
  lst = [(_rx, 0), (_rx, 1), (_oo, 2),(_oo,3),(_rx,4)]
  aggregator(lst) == [(_rx, 0, 1, 4), (_oo, 2, 3)]
  """
  lst = expr.args
  veclst = []
  onevecls = []
  others = []
  lst1 = []

  # Pattern Match (<Grade-1>)(<>)(Exterior Product)
  # TODO Write a pattern matching api call
  for i, x in enumerate(lst):
    if (isinstance(x,lcntrct) or isinstance(x,rcntrct)) and\
      (x.args[0].grade == 1) and isinstance(x.args[1],extp):
      lst1.append((x.args[0],i))
  
  
  # For others A>B 
  # Recursively the parent sandhi oon A,B and replace if changed 


  for i, x in enumerate(lst):
    if (isinstance(x,lcntrct) or isinstance(x,rcntrct)) and\
      (x.args[0].grade > 1) and isinstance(x.args[1],extp):
      others.append((x.args[0],i))
  
  mapp = defaultdict(list) 
  for x, y in lst: 
    mapp[x].append(y) 
    lst2 = [(x, *y) for x, y in mapp.items()] 
  return lst2 

expr = ((a1<(b1^b2))^(a1<(b2^b3))^(b2<(b1^b3))^(b2<(a2^b3)))
simplification.sandhi(expr)