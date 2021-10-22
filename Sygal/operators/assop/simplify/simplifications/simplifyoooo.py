from libs.Sygal.operators import (add,anticomm,comm,extp,
inprdct,lcntrct,mul,rcntrct)

from libs.Sygal.GV import GV,gv
from collections import defaultdict 

class simplification():
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
  def sandhi(expr):

    if isinstance(expr,extp):
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
      lst2 = aggregator(lst1)

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
                _,rv = simplification.sandhi(expr1)
                return True, rv 
              else :
                raise
      return False, expr
    else :
      print("False")
      return False,expr

  @staticmethod
  def Rcntrct2Lcntrct():
    pass

  @staticmethod
  def Lcntrct2Rcntrct():
    pass

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