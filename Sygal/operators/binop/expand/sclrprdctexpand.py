# Partition Expansion

from libs.Sygal.imports.import1head import *
from libs.Sygal.imports.import1tail import *

from libs.Sygal.operators.assop.gadd import gadd
from libs.Sygal.operators.assop.gextp import gextp
from libs.Sygal.operators.assop.gmul import gmul

from libs.Sygal.operators.binop.ganticomm import ganticomm
from libs.Sygal.operators.binop.gcomm import gcomm
from libs.Sygal.operators.binop.sclrprdct import sclrprdct
from libs.Sygal.operators.binop.grcntrct import grcntrct
from libs.Sygal.operators.binop.glcntrct import glcntrct
from libs.Sygal.operators.binop.sclrprdct import sclrprdct

from libs.Sygal.imports.import_util2 import *

from libs.Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion
from libs.Sygal.operators.binop.outermorphic.projection import projection
from libs.Sygal.operators.binop.outermorphic.rejection import rejection

def difflist(t1,t2):
  return [ele for ele in t1 if ele not in t2]

def sclprdct_expand(expr:Expr)->Union[Expr,Box]:
  # ###### HERE BOX IS NOT POSSIBLE

  if(type(expr)==sclrprdct):
    up = expr.up
    down = expr.down
    if is_vecBlade(up) and is_vecBlade(down):
      if(up.is_atom):#down will also be atom
        t1 = up.dotdict[down]
        t2 = down.dotdict[up]
        if t1 != None and t2 != None:
          if t1 == t2:
            return t1
          else :
            raise ValueError("Two different values for innerproduct")
        elif t1!= None:
          return t1
        elif t2!=None:
          return t2
        else :
          return expr
      else:
        lst = []
        for i,u_ele in enumerate(up.args):
          t3 = list(filter(lambda x:x is not None,[d_ele.dotdict[u_ele] for d_ele in down.args]))
          if t3:
            lst.append(u_ele)
        down_1 = down

        for ele in lst:
          t4 =  expand_iter(glcntrct)(ele<down_1)
          down_1 = t4 

        # up [a1,a2,ca3,a4,ca5] -> [a1,a2,a4,ca5,ca3] 
        diffup = difflist(up.args,lst)
        cpydiffup = []
        cpydiffup.extend(diffup)
        lst.reverse()
        cpydiffup.extend(lst)
        sign = parity(up.args,cpydiffup)
        if diffup:
          t5 = Box.__new__(Box,sclrprdct(gextp(*diffup),down_1),sign)
          return GExpr.gdistribute(t5)
        else :
          return GExpr.gdistribute(down_1*sign)
        
    else :
      return expr
  else:
    return expr

def sclprdct_expand1(expr:Expr)->Union[Expr,Box]:
  # ###### HERE BOX IS NOT POSSIBLE

  if(type(expr)==sclrprdct):
    up = expr.up
    down = expr.down
    if is_vecBlade(up) and is_vecBlade(down):
      if(up.is_atom):#down will also be atom
        t1 = up.dotdict[down]
        t2 = down.dotdict[up]
        if t1 != None and t2 != None:
          if t1 == t2:
            return t1
          else :
            raise ValueError("Two different values for innerproduct")
        elif t1!= None:
          return t1
        elif t2!=None:
          return t2
        else :
          return expr
      else:
        lst = list(up.args)
        down_1 = down

        for ele in reversed(lst):
          t4 =  expand_iter(glcntrct)(ele<down_1)
          down_1 = t4 

        return GExpr.gdistribute(down_1)
        
    else :
      return expr
  else:
    return expr




def sclrprdctexpand():
  sclrprdct.gexpand = exhaust(do_one(sclprdct_expand,))
  sclrprdct.gexpand1 = exhaust(bottom_up(do_one(typed({sclrprdct:sclprdct_expand1}))))
  
  # sclrprdct.gexpand1 = exhaust(bottom_up(bx_typed({sclrprdct: sclprdct_expand1}),gen_traverse))
  # sclrprdct.gexpand1 = sclprdct_expand1
