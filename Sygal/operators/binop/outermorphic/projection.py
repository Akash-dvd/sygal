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

from .outermorphic import outermorphic

class projection(outermorphic):

  def __new__(cls,sub:"GExpr",obj:"GExpr")->Optional[Box]:
    # Pattern Match for two arguements
    t = (sub,obj)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))
    tmvs = [t1[0].mv,t1[1].mv]
    coeff = Mul(t1[0].coeff,t1[1].coeff).simplify()
    
    # Pattern match for grade value
    # Check for scalars
    if(coeff==S(0)):
      return(GExpr.Znl)

    if (is_invertible(tmvs[0])):
      obj = GExpr.__new__(projection,tmvs[0],tmvs[1])
    else :
      raise ValueError
    return Box.__new__(Box,obj,coeff)

  @property
  def grade(self:"projection") -> Union[set,frozenset]:
    return self.up
  
  def sympystr(self,expr:"projection") -> str:
    return str(expr)

  def sympyrepr(self,expr:"projection") -> str:
    return expr.__repr__()

  def __str__(self:"projection") -> str:
    str = '('+(self.down).__str__()\
    +'\033[1;33;40mPRO\033[0;37;40m'\
    +(self.up).__str__()+')'
    return str

  def __repr__(self:"projection") -> str:
    str = '('+(self.down).__repr__()\
    +'PRO'\
    +(self.up).__repr__()+')'
    return str

  def __hash__(self:"projection") -> int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self:"projection", other:"GExpr") -> bool:
    # THIS DEFINITION CAN BE MODIFIED BY EXPANDING THE EXPRESSION
    return (
      (type(other) == type(self)) and
      self.__hash__() == other.__hash__()
    )

  @property
  def down(self:"projection")->"GExpr":
    return self.args[0]

  @property
  def up(self:"projection")->"GExpr":
    return self.args[1]

if is_devmode():
  StrPrinter._print_projectionn = projection.sympyrepr
else :
  StrPrinter._print_projection = projection.sympystr


from libs.Sygal.operators.binop.outermorphic.higher.projectionhigher import projectionhigher
from libs.Sygal.operators.binop.outermorphic.simplify.projectionsimp import projectionsimp
from libs.Sygal.operators.binop.outermorphic.expand.projectionexpand import projectionexpand

projectionhigher()
projectionsimp()
projectionexpand()
