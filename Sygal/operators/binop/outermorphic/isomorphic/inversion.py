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
from libs.Sygal.imports.import_util2 import *

from libs.Sygal.operators.binop.outermorphic.isomorphic.isomorphic import isomorphic


class inversion(isomorphic):
  # __name__ = "inversion"
  def __new__(cls,sub:"GExpr",obj:"GExpr")->Optional[Box]:
    t = (sub,obj)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))
    tmvs = [t1[0].mv,t1[1].mv]
    coeff = Mul(t1[0].coeff,t1[1].coeff)
    
    # Pattern match for grade value
    # Check for scalars
    if(coeff==S(0)):
      return(GExpr.Znl)

    if is_nzScalarPair(tmvs[0],tmvs[0].reversion()):
      MV1 = GExpr.__new__(inversion,tmvs[0],tmvs[1])
      MV2 = meta_treatment(MV1)
      if MV2 == GExpr.Znl:
        return GExpr.Znl
      else :
        MV2.rlDt = relDt()
        bx = Box.__new__(Box,mv=MV2,coeff=coeff)
        return bx

    else :
      raise ValueError("Non-Invertible base of inversion")

  @property
  def grade(self:"inversion") -> Union[set,frozenset]:
    return self.up.grade

  def sympystr(self,expr:"inversion") -> str:
    return str(expr)

  def sympyrepr(self,expr:"inversion") -> str:
    return expr.__repr__()

  def __str__(self:"inversion") -> str:
    str = '('+(self.down).__str__()\
    +'\033[1;33;40mINV\033[0;37;40m'\
    +(self.up).__str__()+')'
    return str

  def __repr__(self:"inversion") -> str:
    str = '('+(self.down).__repr__()\
    +'INV'\
    +(self.up).__repr__()+')'
    return str

  def __hash__(self:"inversion") -> int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self:"inversion", other:"GExpr") -> bool:
    # THIS DEFINITION CAN BE MODIFIED BY EXPANDING THE EXPRESSION
    return (
      (type(other) == type(self)) and
      self.__hash__() == other.__hash__()
    )

  @property
  def down(self:"inversion")->"GExpr":
    return self.args[0]

  @property
  def up(self:"inversion")->"GExpr":
    return self.args[1]

def meta_treatment(expr:inversion)->inversion:

  # if null list extend -> null list
  # if null dict update -> null dict
  up = expr.up
  down = expr.down
  spc_lst = spclst([])
  spc_lst.extend(up.mtDt)
  
  if True:
    spc_lst.extend(down.mtDt)
  else :
    pass

  if bool(spc_lst):
    expr.mtDt = spc_lst
    return expr
  else :
    return GExpr.Znl




from libs.Sygal.operators.binop.outermorphic.isomorphic.higher.inversionhigher import inversionhigher
from libs.Sygal.operators.binop.outermorphic.isomorphic.canon.inversioncanon import inversioncanon
from libs.Sygal.operators.binop.outermorphic.isomorphic.expand.inversionexpand import inversionexpand

# from libs.Sygal.utils.utils import is_devmode

if is_devmode():
  StrPrinter._print_inversion = inversion.sympyrepr
else :
  StrPrinter._print_inversion = inversion.sympystr

inversionhigher()
inversioncanon()
inversionexpand()