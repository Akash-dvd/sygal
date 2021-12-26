from libs.Sygal.imports.import1head import *
from libs.Sygal.operators.binop.binop import binop
from libs.Sygal.operators.binop.sclrprdct import sclrprdct

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
    elif (is_singleGrade(tmvs[0])) and (tmvs[0].grade == tmvs[1].grade):
      MV = Basic.__new__(sclrprdct, *GSortArgs(tmvs))
      MV.mtDt = spclst([{GExpr.nl:grd(0,0)}])
      MV.rlDt = relDt()
      return(Box.__new__(Box,MV,coeff))
    else:
      MV = Basic.__new__(glcntrct, *tmvs)
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
          t = all([down_dct[k]>=p1[i] for i,k in enumerate(tup)])

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

def meta_treatment1(expr:glcntrct)->glcntrct:
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


    for size in range(1,len(down_dct)+1):

      keys_tup = list(subsets(down_dct,size))

      # x1 = (list(kbins([1]*x, size, ordered=None)))
      lst_distri = (list(kbins([1]*up_dct_grd, size)))

      lst_distri1 = []
      for ele1 in lst_distri:
        lst1 = []
        for ele2 in ele1:
          lst1.append(reduce(lambda x,y:x+y,ele2))
        lst_distri1.append(lst1)

      # subsets(down_dct) -> keys_tup -> k_tup_i
      # [(k1,k2...)] -> [(k1,k2),(k2,k3)] -> (k2,k3)
      # kbins([1]*up_dct_grd -> lst_distri -> lst_distri1 -> lst_distri1_i
      # [[[1,1,1]]] -> [[1,1],[1]] -> [[2],[2,3]] -> [2,3]
      for k_tup_i,lst_distri1_i in product(keys_tup,lst_distri1):
        t_dct1 = spcdct({})
        t_dct2 = spcdct({})
        t_lst = [down_dct[k].value>=lst_distri1_i[i] for i,k in enumerate(k_tup_i)]
        t = reduce(lambda x,y:x and y,t_lst)
        if t :
          t_dct1.update({k:grd(lst_distri1_i[i],down_dct[k].limit) for i,k in enumerate(k_tup_i)})

          for k,v in down_dct.items():
            t1 = down_dct[k].value-(t_dct1.get(k,Zval)).value
            if t1:
              t_dct2.update({k:grd(t1,down_dct[k].limit)})
          
          t2 = up_dct|t_dct1

          if t2 :
            spc_lst.append(t_dct2)

        else:
          continue
  if bool(spc_lst):
    expr.mtDt = spc_lst
    return expr
  else :
    return GExpr.Znl



from libs.Sygal.imports.import1tail import *

if is_devmode():
  StrPrinter._print_glcntrct = glcntrct.sympyrepr
else :
  StrPrinter._print_glcntrct = glcntrct.sympystr


from libs.Sygal.operators.binop.higher.glcntrcthigher import glcntrcthigher
from libs.Sygal.operators.binop.simplify.glcntrctsimp import glcntrctsimp
from libs.Sygal.operators.binop.expand.glcntrctexpand import glcntrctexpand

glcntrcthigher()
glcntrctsimp()
glcntrctexpand()