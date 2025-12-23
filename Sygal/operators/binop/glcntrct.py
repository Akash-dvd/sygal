# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.sympy_basic import Basic, Mul, S, subsets
from Sygal.imports.typing_helpers import product
from Sygal.imports.utils import is_uniGraded, is_devmode
from Sygal.imports.psc import grd, spclst, spcdct
from Sygal.imports.utils import kbin_distri
from Sygal.imports.sympy_basic import StrPrinter

from Sygal.operators.binop.binop import binop
from Sygal.operators.binop.sclrprdct import sclrprdct

class glcntrct(binop):
  """
  Left Contraction < operator
  Is non-associative, non-commutative
  """

  # Currently both arguements should be boxed! extp/GB
  def __new__(cls, args0:GExpr,args1:GExpr) -> "Box":
    # up>down
    
    t = (args0,args1)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))
    tmvs = (t1[0].mv,t1[1].mv)
    coeff = Mul(t1[0].coeff,t1[1].coeff)

    if coeff == S(0):
      return(GExpr.Znl)
    
    # Pattern match for grade value
    # Check for scalars
    if(tmvs[0]==Box.nl):
        return(Box.__new__(Box,tmvs[1],coeff))
    
    # scalar>scalar != 0
    elif(tmvs[1]==Box.nl):
      return Box.Znl

    # Check if zero grade .. Then call sclrprdct
    elif (is_uniGraded(tmvs[0])) and (tmvs[0].grade == tmvs[1].grade):
      MV = sclrprdct(*tmvs)
      return MV
    else:
      MV = Basic.__new__(glcntrct, *tmvs)
      # pseudoscalar and rlDt check
      ###########################      
      MV1 = meta_treatment(MV)
      if MV1 == GExpr.Znl:
        return GExpr.Znl
      else :
        bx = Box.__new__(Box,mv=MV1,coeff=coeff)
        return bx



  # @property
  # def grade(self:"glcntrct")->Union[set,frozenset]:
  #   # Two arguements will always be present
 
  #   t = set()
  #   arg1 = self.args[0].grade
  #   arg2 = self.args[1].grade

  #   for elem1 in arg1:
  #     for elem2 in arg2:
  #       if((elem2-elem1)>=0): 
  #         t.add((elem2-elem1))
  #   return t

  def sympystr(self,expr:"glcntrct") -> str:
    return str(expr)

  def sympyrepr(self,expr:"glcntrct") -> str:
    return expr.__repr__()

  def __str__(self:"glcntrct")->str:
    str = '('+(self.up).__str__()\
    +'\033[1;33;40m\u230B\033[0;37;40m'\
    +(self.down).__str__()+')'
    return str

  def __repr__(self:"glcntrct")->str:
    str = '('+(self.up).__repr__()\
    +'<'\
    +(self.down).__repr__()+')'
    return str

  def __hash__(self:"glcntrct")->int:
    h = self._mhash
    if h is None:
      h = hash((type(self).__name__) + \
        str(self.args[0].__hash__()) + \
        str(self.args[1].__hash__()))
      self._mhash = h
    return h
  
  def __eq__(self:"glcntrct", other:"GExpr")->bool:
    return (
      (type(other) == type(self))  and
      self.__hash__() == other.__hash__()
    )
  
  @property
  def up(self:"glcntrct")->"GExpr":
    return self.args[0]

  @property
  def down(self:"glcntrct")->"GExpr":
    return self.args[1]

def meta_treatment(expr:glcntrct)->glcntrct:
  up = expr.up
  down = expr.down
  Zval = grd(0,0)
  spc_lst = spclst([])
  for up_dct,down_dct in product(up.mtDt,down.mtDt):

    up_dct_grd = 0
    down_dct_grd = 0

    for k,v in up_dct.items():
      up_dct_grd+=v.value
    
    for k,v in down_dct.items():
      down_dct_grd+=v.value
    
    if up_dct_grd>down_dct_grd:
      continue

    down_dct_keys_tup = subsets(down_dct)
    next(down_dct_keys_tup)
    for tup in down_dct_keys_tup:
      if up_dct_grd>=len(tup):
        part1 = kbin_distri(up_dct_grd,len(tup))
        for p1 in part1:
          t_dct1 = spcdct({})
          t_dct11 = spcdct({})
          t = all([down_dct[k].value>=p1[i] for i,k in enumerate(tup)])

          if t :
            t_dct1.update({k:grd(p1[i],down_dct[k].limit) for i,k in enumerate(tup)})

            for k,v in down_dct.items():
              t1 = down_dct[k].value-(t_dct1.get(k,Zval)).value
              t_dct11.update({k:grd(t1,down_dct[k].limit)})
            
            if up_dct|t_dct1 :
              spc_lst.append(t_dct11)

          else:
            continue
      else:
        break
  if bool(spc_lst):
    expr.mtDt = spc_lst
    return expr
  else :
    return GExpr.Znl


if is_devmode():
  StrPrinter._print_glcntrct = glcntrct.sympyrepr
else :
  StrPrinter._print_glcntrct = glcntrct.sympystr


# Lazy import to avoid circular dependency
# These modules import glcntrct, so initialization is moved to binop/__init__.py
# This ensures all operators are imported before initialization happens
def _initialize_glcntrct():
  """Initialize glcntrct higher, canon, and expand rules."""
  from Sygal.operators.binop.higher.glcntrcthigher import glcntrcthigher
  from Sygal.operators.binop.canon.glcntrctcanon import glcntrctcanon
  from Sygal.operators.binop.expand.glcntrctexpand import glcntrctexpand
  
  glcntrcthigher()
  glcntrctcanon()
  glcntrctexpand()

# Don't initialize here - initialization happens in binop/__init__.py after all imports