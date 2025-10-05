from Sygal.imports.import1head import *
from Sygal.imports.import1tail import *
from Sygal.operators.assop.gadd import gadd
from Sygal.operators.assop.gextp import gextp
from Sygal.operators.assop.gmul import gmul

from Sygal.operators.binop.ganticomm import ganticomm
from Sygal.operators.binop.gcomm import gcomm
from Sygal.operators.binop.sclrprdct import sclrprdct
from Sygal.operators.binop.grcntrct import grcntrct
from Sygal.operators.binop.glcntrct import glcntrct
from Sygal.imports.import_util2 import *

from .outermorphic import outermorphic


class rejection(outermorphic):

  def __new__(cls,sub:"GExpr",obj:"GExpr")->Optional[Box]:
    # Pattern Match for two arguements
    t = (sub,obj)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))
    tmvs = [t1[0].mv,t1[1].mv]
    coeff = Mul(t1[0].coeff,t1[1].coeff)
    
    # Pattern match for grade value
    # Check for scalars
    if(coeff==S(0)):
      return(GExpr.Znl)


    if is_nzScalarPair(tmvs[0],tmvs[0].reversion()):
      MV1 = GExpr.__new__(rejection,tmvs[0],tmvs[1])
      MV2 = meta_treatment(MV1)
      if MV2 == GExpr.Znl:
        return GExpr.Znl
      else :
        MV2.rlDt = relDt()
        bx = Box.__new__(Box,mv=MV2,coeff=coeff)
        return bx

    else :
      raise ValueError("Non-Invertible base of rejection")

  @property
  def grade(self:"rejection") -> Union[set,frozenset]:
    return self.up.grade

  def sympystr(self,expr:"rejection") -> str:
    return str(expr)

  def sympyrepr(self,expr:"rejection") -> str:
    return expr.__repr__()

  def __str__(self:"rejection") -> str:
    str = '('+(self.down).__str__()\
    +'\033[1;33;40mREJ\033[0;37;40m'\
    +(self.up).__str__()+')'
    return str

  def __repr__(self:"rejection") -> str:
    str = '('+(self.down).__repr__()\
    +'REJ'\
    +(self.up).__repr__()+')'
    return str

  def __hash__(self:"rejection") -> int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self:"rejection", other:"GExpr") -> bool:
    # THIS DEFINITION CAN BE MODIFIED BY EXPANDING THE EXPRESSION
    return (
      (type(other) == type(self)) and
      self.__hash__() == other.__hash__()
    )

  @property
  def down(self:"rejection")->"GExpr":
    return self.args[0]

  @property
  def up(self:"rejection")->"GExpr":
    return self.args[1]

def meta_treatment(expr:rejection)->rejection:
  
  up = expr.up
  down = expr.down
  Zval = grd(0,0)
  t_spc_lst = spclst([])
  
  t_spc_lst.extend([dct1+dct2 for dct1,dct2 in product(up.mtDt,down.mtDt)])

  spc_lst = spclst([])

  for up_dct,down_dct in product(down.mtDt,t_spc_lst):

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
  StrPrinter._print_rejection = rejection.sympyrepr
else :
  StrPrinter._print_rejection = rejection.sympystr


from Sygal.operators.binop.outermorphic.higher.rejectionhigher import rejectionhigher
from Sygal.operators.binop.outermorphic.canon.rejectioncanon import rejectioncanon
from Sygal.operators.binop.outermorphic.expand.rejectionexpand import rejectionexpand

rejectionhigher()
rejectioncanon()
rejectionexpand()