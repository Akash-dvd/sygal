# Core imports - Import directly to avoid circular dependency
from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.sympy_basic import Mul, S
from Sygal.imports.typing_helpers import Optional
from Sygal.imports.psc import spclst
from Sygal.imports.utils import is_devmode
from Sygal.imports.sympy_basic import StrPrinter

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

    if is_nzScalarPair(tmvs[0],tmvs[0].reversion()):
      MV1 = GExpr.__new__(projection,tmvs[0],tmvs[1])
      MV2 = meta_treatment(MV1)
      if MV2 == GExpr.Znl:
        return GExpr.Znl
      else :
        bx = Box.__new__(Box,mv=MV2,coeff=coeff)
        return bx

    else :
      raise ValueError("Non-Invertible base of projection")

  # @property
  # def grade(self:"projection") -> Union[set,frozenset]:
  #   return self.up.grade
  
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

def meta_treatment(expr:projection)->projection:
  
  up = expr.up
  down = expr.down
  Zval = grd(0,0)
  t_spc_lst = spclst([])
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
              t_spc_lst.append(t_dct11)

          else:
            continue
      else:
        break
      
  # Special handling for t_spc_lst = [{[ॐ]: <0|0>}]

  if t_spc_lst == spclst([spcdct({GExpr.nl:grd(0,0)})]):
    spc_lst.extend(down.mtDt)
  else :
    for up_dct,down_dct in product(t_spc_lst,down.mtDt):

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
  StrPrinter._print_projectionn = projection.sympyrepr
else :
  StrPrinter._print_projection = projection.sympystr


from Sygal.operators.binop.outermorphic.higher.projectionhigher import projectionhigher
from Sygal.operators.binop.outermorphic.canon.projectioncanon import projectioncanon
from Sygal.operators.binop.outermorphic.expand.projectionexpand import projectionexpand

projectionhigher()
projectioncanon()
projectionexpand()
