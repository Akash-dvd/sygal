# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.utils import is_vecBlade, parity
from Sygal.imports.sympy_basic import subsets, S, Mul
from Sygal.operators.assop.gextp import gextp
from Sygal.operators.assop.gadd import gadd
from Sygal.operators.binop.glcntrct import glcntrct

# Only import operators actually used
from Sygal.operators.assop.gmul import gmul

def difflist(t1,t2):
  return [ele for ele in t1 if ele not in t2]



def gmul_expand(expr,A=gmul,grade="all"):
  """
  Doesn't support Gatom of grade >1
  """
  if(type(expr)==Box):
    BX = GExpr.gdistribute(expr)
    cf = BX.coeff
    if(type(BX.mv)==A):
      for i,ele in enumerate(BX.mv.args):
        j=i+1
        if(j<len(BX.mv.args)):
          lst = list(BX.mv.args)
          # check if BX.mv.args[i] and BX.mv.args[j] are blades
          if(is_vecBlade(BX.mv.args[i]) and is_vecBlade(BX.mv.args[j])):
            lst[i] = mulexpansion(BX.mv.args[i],BX.mv.args[j])
            del lst[j]
            t = gmul(*lst)*cf
            t1 = GExpr.gdistribute(t)
            return t1

      return BX
    else:
      return BX
  elif(issubclass(type(expr),GExpr) and not expr.is_atom):
    mv = expr
    
  else :
    return expr

def mulexpansion(A,B):
  # Too smart arguement
  # If th e grade is one it cannot be binop 
  # Only sum is possible -> it will be converted to iter
  A_args = [A] if A.grade == {1}  else A.args
  B_args = [B] if B.grade == {1}  else B.args

  lst = []
  for i in range(0,min(len(A_args),len(B_args))+1):
    for Aset in subsets(A_args,i):
      for Bset in subsets(B_args,i):
        diffA = difflist(A_args,Aset)
        cpydiffA = []
        cpydiffA.extend(diffA)
        cpydiffA.extend(Aset)
        signA = parity(A_args,cpydiffA)
        diffB = difflist(B_args,Bset)
        cpydiffB = []
        cpydiffB.extend(Bset)
        cpydiffB.extend(diffB)
        signB = parity(B_args,cpydiffB)
        sign = signA*signB
        if Aset:
          up = gextp(*Aset)
          low = gextp(*Bset)
          coeff1 = glcntrct(up,low).coeff
        else:
          coeff1 = S(1)
        diffA.extend(diffB)
        if diffA:
          mv = gextp(*diffA)
          bx = Box.__new__(Box,mv,Mul(sign,coeff1))
          lst.append(bx)
        else :
          bx = Box.__new__(Box,GExpr.nl,Mul(sign,coeff1))
          lst.append(bx)
  t = gadd(*lst)
  return t


def gmulexpand():
  gmul.gexpand = gmul_expand