from libs.Sygal.imports.import1head import *
from libs.Sygal.operators.binop.binop import binop

class sclrprdct(binop):
  """
  Inner Product of two equal single graded MVs
  """

  def __new__(cls, args0:GExpr,args1:GExpr) -> "Box":

    t = (args0,args1)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))
    tmvs = [t1[0].mv,t1[1].mv]
    coeff = Mul(t1[0].coeff,t1[1].coeff)
    
    if coeff == S(0):
      return(GExpr.Znl)
      
    if( len(tmvs[0].grade) == 1 and len(tmvs[1].grade) == 1):
      if tmvs[0].grade == tmvs[1].grade:
        if tmvs[0].grade == {0}:
          return GExpr.Onl*coeff
        else :
          MV = Basic.__new__(sclrprdct, *GSortArgs(tmvs))
          MV.mtDt = spclst([{GExpr.nl:grd(0,0)}])
          MV.rlDt = relDt()
          t = (Box.__new__(Box,MV,coeff))
          return t

      else:
        raise ValueError("Both args must be of single equal grade")
    else:
      raise ValueError("Both args must be of single grade")

  # @property
  # def grade(self:"sclrprdct")->Union[set,frozenset]:
  #   # Two arguements will always be present
 
  #   t = set()
  #   arg1 = self.args[0].grade
  #   arg2 = self.args[1].grade

  #   for elem1 in arg1:
  #     for elem2 in arg2:
  #       if((elem2-elem1)>=0): 
  #         t.add((elem2-elem1))
  #   return t

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
    +'|'\
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

from libs.Sygal.operators.binop.higher.sclrprdcthigher import sclrprdcthigher
from libs.Sygal.operators.binop.simplify.sclrprdctsimp import sclrprdctsimp
from libs.Sygal.operators.binop.expand.sclrprdctexpand import sclrprdctexpand

sclrprdcthigher()
sclrprdctsimp()
sclrprdctexpand()