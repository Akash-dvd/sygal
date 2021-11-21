from libs.Sygal.imports.import1head import *
from libs.Sygal.operators.binop.binop import binop
from libs.Sygal.operators.binop.sclrprdct import sclrprdct


class grcntrct(binop):
  """
  Right Contraction > operator
  Is non-associative, non-commutative
  """

  # Currently both arguements should be boxed! extp/GB
  def __new__(cls, args0:GExpr,args1:GExpr) -> "Box":
    # Already matched pattern for binary op
    
    t = (args0,args1)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))
    tmvs = [t1[0].mv,t1[1].mv]
    coeff = Mul(t1[0].coeff,t1[1].coeff).simplify()
    
    # Pattern match
    # Check for scalars
    if(t1[1].mv==Box.nl):
      if(t1[1].coeff==S(0)):
        return(GExpr.Znl)
      else :
        return(Box.__new__(Box,t1[0].mv,Mul(t1[0].coeff,t1[1].coeff).simplify()))
    
    elif(t1[0].mv==Box.nl):
      return Box.Znl

    # Check if zero grade .. Then call sclrprdct
    elif ((len(tmvs[0].grade)==len(tmvs[1].grade)) and ((next(iter(tmvs[0].grade))-next(iter(tmvs[1].grade))==0)) and (len(tmvs[0].grade) == 1 )):
      mv = Basic.__new__(sclrprdct, *GSortArgs(tmvs))
      return(Box.__new__(Box,mv,coeff))
    else:
      mv = Basic.__new__(grcntrct, *tmvs)
      return(Box.__new__(Box,mv,coeff))

  @property
  def grade(self:"grcntrct")-> Union[set,frozenset]:
    # Two arguements will always be present
 
    t = set()
    arg1 = self.args[0].grade
    arg2 = self.args[1].grade

    for elem1 in arg1:
      for elem2 in arg2:
        if((elem1-elem2)>=0): 
          t.add((elem1-elem2))
    return t

  def sympystr(self,expr:"grcntrct") -> str:
    return str(expr)

  def sympyrepr(self,expr:"grcntrct") -> str:
    return expr.__repr__()


  def __str__(self:"grcntrct")->str:
    str = '('+(self.down).__str__()\
    +'\033[1;33;40m\u230A\033[0;37;40m'\
    +(self.up).__str__()+')'
    return str

  def __repr__(self:"grcntrct")->str:
    str = '('+(self.down).__repr__()\
    +'>'\
    +(self.up).__repr__()+')'
    return str

  def __hash__(self:"grcntrct")->int:
    h = self._mhash
    if h is None:
      h = hash((type(self).__name__) + \
        str(self.args[0].__hash__()) + \
        str(self.args[1].__hash__()))
      self._mhash = h
    return h
  
  def __eq__(self:"grcntrct", other:"GExpr")->bool:
    return (
      (type(other) == type(self))  and
      self.__hash__() == other.__hash__()
    )

  @property
  def up(self:"grcntrct")->"GExpr":
    return self.args[1]

  @property
  def down(self:"grcntrct")->"GExpr":
    return self.args[0]

from libs.Sygal.imports.import1tail import *

from libs.Sygal.operators.binop.higher.grcntrcthigher import grcntrcthigher
from libs.Sygal.operators.binop.simplify.grcntrctsimp import grcntrctsimp
from libs.Sygal.operators.binop.expand.grcntrctexpand import grcntrctexpand


if is_devmode():
  StrPrinter._print_grcntrct = grcntrct.sympyrepr
else :
  StrPrinter._print_grcntrct = grcntrct.sympystr

grcntrcthigher()
grcntrctsimp()
grcntrctexpand()