from libs.Sygal.imports.import1head import *
from libs.Sygal.operators.binop.binop import binop

class sclrprdct(binop):
  """
  Scalar Product of two multi-vectors
  """

  # Currently both arguements should be boxed! extp/GB
  def __new__(cls, args0:GExpr,args1:GExpr) -> "Box":
    # Already matched pattern for binary op
    
    # 

    t = (args0,args1.reversion())
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))
    # Coz simplify gexpand etc work only on boxes
    tbxs = [Box.__new__(Box,t1[0].mv),Box.__new__(Box,t1[1].mv)]
    coeff = Mul(t1[0].coeff,t1[1].coeff).simplify()
    tmvs = [tbxs[0].mv,tbxs[1].mv]
    # Not completely implemented

    t2 =  (tbxs[0].gexpand()<tbxs[1].gexpand())
    t3 = t2.gdistribute()
    
    if(t3.grade=={0}):
      mv = Basic.__new__(sclrprdct, *tmvs)
      return(Box.__new__(Box,mv,coeff))

    else :
      return GExpr.Znl
    # Pattern match for grade value
    # Check for scalars

  @property
  def grade(self:"sclrprdct")->Union[set,frozenset]:
    # Two arguements will always be present
 
    t = set()
    arg1 = self.args[0].grade
    arg2 = self.args[1].grade

    for elem1 in arg1:
      for elem2 in arg2:
        if((elem2-elem1)>=0): 
          t.add((elem2-elem1))
    return t

  def sympystr(self,expr:"sclrprdct") -> str:
    return str(expr)

  def sympyrepr(self,expr:"sclrprdct") -> str:
    return expr.__repr__()

  def __str__(self:"sclrprdct")->str:
    str = '('+(self.up).__str__()\
    +'\033[1;33;40m|\033[0;37;40m'\
    +(self.down).__str__()+')'
    return str

  def __repr__(self:"sclrprdct")->str:
    str = '('+(self.up).__repr__()\
    +'<'\
    +(self.down).__repr__()+')'
    return str

  def __hash__(self:"sclrprdct")->int:
    h = self._mhash
    if h is None:
      h = hash((type(self).__name__) + \
        str(self.args[0].__hash__()) + \
        str(self.args[1].__hash__()))
      self._mhash = h
    return h
  
  def __eq__(self:"sclrprdct", other:"GExpr")->bool:
    return (
      (type(other) == type(self))  and
      self.__hash__() == other.__hash__()
    )
  
  @property
  def up(self:"sclrprdct")->"GExpr":
    return self.args[0]

  @property
  def down(self:"sclrprdct")->"GExpr":
    return self.args[1]

from libs.Sygal.imports.import1tail import *

if is_devmode():
  StrPrinter._print_sclrprdct = sclrprdct.sympyrepr
else :
  StrPrinter._print_sclrprdct = sclrprdct.sympystr