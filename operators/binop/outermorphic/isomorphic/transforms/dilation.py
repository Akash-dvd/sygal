# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.sympy_basic import Mul, S
from Sygal.imports.typing_helpers import Optional, Union
from Sygal.imports.utils import is_devmode
from Sygal.imports.sympy_basic import StrPrinter

# Only import operators actually used
from Sygal.operators.binop.outermorphic.isomorphic.transforms.transforms import transforms


class dilation(transforms):
  # __name__ = "inversion"
  def __new__(cls,sub:"GExpr",obj:"GExpr")->Optional[Box]:
    # sub has exponential arguements as box
    # sub -> [p1^oo,th]
    raise NotImplemented

    t = (sub,obj)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))
    tmvs = [t1[0].mv,t1[1].mv]
    coeff = Mul(t1[0].coeff,t1[1].coeff)
    
    # Pattern match for grade value
    # Check for scalars
    if(coeff==S(0)):
      return(GExpr.Znl)

    if (is_invertible(tmvs[0])):
      obj = GExpr.__new__(dilation,tmvs[0],tmvs[1])
    else :
      raise ValueError
    return Box.__new__(Box,obj,coeff)

  @property
  def grade(self:"dilation") -> Union[set,frozenset]:
    return self.up.grade


  def sympystr(self,expr:"dilation") -> str:
    return str(expr)

  def sympyrepr(self,expr:"dilation") -> str:
    return expr.__repr__()

  def __str__(self:"dilation") -> str:
    str = '('+(self.down).__str__()\
    +'\033[1;33;40mDIL\033[0;37;40m'\
    +(self.up).__str__()+')'
    return str

  def __repr__(self:"dilation") -> str:
    str = '('+(self.down).__repr__()\
    +'DIL'\
    +(self.up).__repr__()+')'
    return str

  def __hash__(self:"dilation") -> int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self:"dilation", other:"GExpr") -> bool:
    # THIS DEFINITION CAN BE MODIFIED BY EXPANDING THE EXPRESSION
    return (
      (type(other) == type(self)) and
      self.__hash__() == other.__hash__()
    )

  @property
  def down(self:"dilation")->"GExpr":
    return self.args[0]

  @property
  def up(self:"dilation")->"GExpr":
    return self.args[1]






from Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion
from Sygal.operators.binop.outermorphic.isomorphic.higher.inversionhigher import inversionhigher
from Sygal.operators.binop.outermorphic.isomorphic.canon.inversioncanon import inversioncanon
from Sygal.operators.binop.outermorphic.isomorphic.expand.inversionexpand import inversionexpand

if is_devmode():
  StrPrinter._print_inversion = inversion.sympyrepr
else :
  StrPrinter._print_inversion = inversion.sympystr

inversionhigher()
inversioncanon()
inversionexpand()