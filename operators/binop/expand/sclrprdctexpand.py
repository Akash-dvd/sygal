# Partition Expansion

# Core imports
# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.sympy_basic import Expr
from Sygal.imports.typing_helpers import Union
from Sygal.imports.strategies import exhaust, do_one, bottom_up, typed, expand_iter
from Sygal.imports.utils import is_vecBlade, parity

# Only import operators actually used - sclrprdct is safe to import at module level
from Sygal.operators.binop.sclrprdct import sclrprdct

# Lazy imports to avoid circular dependency - these are only used inside functions
# gextp, glcntrct will be imported inside functions

def difflist(t1,t2):
  return [ele for ele in t1 if ele not in t2]

def sclprdct_expand(expr:Expr)->Union[Expr,Box]:
  # Lazy imports to avoid circular dependency
  from Sygal.operators.binop.glcntrct import glcntrct
  from Sygal.operators.assop.gextp import gextp
  
  # ###### HERE BOX IS NOT POSSIBLE

  if(type(expr)==sclrprdct):
    up = expr.up
    down = expr.down
    if is_vecBlade(up) and is_vecBlade(down):
      if(up.is_atom):#down will also be atom
        # relDt removed - return expression unchanged
        return expr
      else:
        lst = []
        for i,u_ele in enumerate(up.args):
          # relDt removed - simplified logic
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
  # Lazy import to avoid circular dependency
  from Sygal.operators.binop.glcntrct import glcntrct
  
  # ###### HERE BOX IS NOT POSSIBLE

  if(type(expr)==sclrprdct):
    up = expr.up
    down = expr.down
    if is_vecBlade(up) and is_vecBlade(down):
      if(up.is_atom):#down will also be atom
        # relDt removed - return expression unchanged
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

# def sclprdct_expand1(expr:Expr)->Union[Expr,Box]:
#   # ###### HERE BOX IS NOT POSSIBLE

#   if(type(expr)==sclrprdct):
#     up = expr.up
#     down = expr.down
#     if is_vecBlade(up) and is_vecBlade(down):
#       if(up.is_atom):#down will also be atom
#         t1 = up.rlDt[down]
#         t2 = down.rlDt[up]
#         if t1 != None and t2 != None:
#           if t1 == t2:
#             return t1
#           else :
#             raise ValueError("Two different values for innerproduct")
#         elif t1!= None:
#           return t1
#         elif t2!=None:
#           return t2
#         else :
#           return expr
#       else:
#         lst = list(up.args)
#         down_1 = down

#         for ele in reversed(lst):
#           t4 =  expand_iter(glcntrct)(ele<down_1)
#           down_1 = t4 

#         return GExpr.gdistribute(down_1)
        
#     else :
#       return expr
#   else:
#     return expr



def sclrprdctexpand():
  sclrprdct.gexpand = exhaust(do_one(sclprdct_expand,))
  sclrprdct.gexpand1 = exhaust(bottom_up(do_one(typed({sclrprdct:sclprdct_expand1}))))
  
  # sclrprdct.gexpand1 = exhaust(bottom_up(bx_typed({sclrprdct: sclprdct_expand1}),gen_traverse))
  # sclrprdct.gexpand1 = sclprdct_expand1
