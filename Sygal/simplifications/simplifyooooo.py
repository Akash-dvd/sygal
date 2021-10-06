from libs.Sygal.operators import (add,anticomm,comm,extp,
inprdct,lcntrct,mul,rcntrct)

from libs.Sygal.GV import GV,gv
from collections import defaultdict 

class simplification():
  # Inorder Traversal Not done
  @staticmethod
  def sandhi(expr):
    print(GV._I5)
    if isinstance(expr,extp):
      lst = expr.args
      lst1 = []
      for i, x in enumerate(lst):
        if (isinstance(x,lcntrct) or isinstance(x,rcntrct)) and\
          (x.args[0].grade == 1) and\
          isinstance(x.args[1],extp):
          lst1.append((x.args[0],i))
      print("--")
      print(lst1)
      
      mapp = defaultdict(list) 
      for x, y in lst1: 
        mapp[x].append(y) 
      lst2 = [(x, *y) for x, y in mapp.items()] 
      print(lst2) 
      # [(_rx, 1, 2, 4, 6), (_oo, 3, 5)]

      for elem in lst2:
        dist = len(elem)
        # print("+++___")
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
    return

  @staticmethod
  def Lcntrct2Rcntrct():
    return
