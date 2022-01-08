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
    # down<up
    
    t = (args0,args1)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))
    tmvs = [t1[0].mv,t1[1].mv]
    coeff = Mul(t1[0].coeff,t1[1].coeff)

    if coeff == S(0):
      return(GExpr.Znl)

    # Pattern match for grade value
    # Check for scalars
    if(tmvs[1]==Box.nl):
        return(Box.__new__(Box,tmvs[0],coeff))
    
    # scalar>scalar != 0
    elif(tmvs[0]==Box.nl):
      return Box.Znl

    # Check if zero grade .. Then call sclrprdct
    elif is_uniGraded(tmvs[0]) and (tmvs[0].grade == tmvs[1].grade):
      MV = sclrprdct(*tmvs)
      return MV
    else:
      MV = Basic.__new__(grcntrct, *tmvs)
      # pseudoscalar and rlDt check
      ###########################      
      MV1 = meta_treatment(MV)
      if MV1 == GExpr.Znl:
        return GExpr.Znl
      else :
        MV1.rlDt = relDt()
        bx = Box.__new__(Box,mv=MV1,coeff=coeff)
        return bx

  # @property
  # def grade(self:"grcntrct")-> Union[set,frozenset]:
  #   # Two arguements will always be present
 
  #   t = set()
  #   arg1 = self.args[0].grade
  #   arg2 = self.args[1].grade

  #   for elem1 in arg1:
  #     for elem2 in arg2:
  #       if((elem1-elem2)>=0): 
  #         t.add((elem1-elem2))
  #   return t

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

def meta_treatment(expr:grcntrct)->grcntrct:
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


from libs.Sygal.imports.import1tail import *

from libs.Sygal.operators.binop.higher.grcntrcthigher import grcntrcthigher
from libs.Sygal.operators.binop.canon.grcntrctcanon import grcntrctcanon
from libs.Sygal.operators.binop.expand.grcntrctexpand import grcntrctexpand


if is_devmode():
  StrPrinter._print_grcntrct = grcntrct.sympyrepr
else :
  StrPrinter._print_grcntrct = grcntrct.sympystr

grcntrcthigher()
grcntrctcanon()
grcntrctexpand()