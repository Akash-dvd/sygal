from .importshead import *

class gadd(assop):

  def __new__(cls, args0:GExpr,*args:Tuple["GExpr"]) -> "Box":
    # gadd(Box,Optional[Box,Box.....])

    # Pattern Matching for # of args for associative op
    t =  [args0]
    t.extend(args)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))
    
    if(len(t1)==1):
      return t1[0]
    else :
      
      expr = canonicalize(Basic.__new__(gadd, *t1))

      # Here Altering with args so pattern matching is required
      if(len(expr.args)>1):
        return Box.__new__(Box,expr)
      elif (len(expr.args)==1):
        singarg = expr.args[0]
        return Box.__new__(Box,singarg)
      else:
        return Box.Znl

  @property
  def grade(self:"gadd") -> Union[set,frozenset]:
    t = set()
    for i in self.args:
      t.update(i.grade)
    return t

  def sympystr(self,expr:"gadd") -> str:
    return str(expr)

  def sympyrepr(self,expr:"gadd") -> str:
    return expr.__repr__()

  def __str__(self:"gadd") -> str:
    tup_head = self.args[:-1]
    tail = self.args[-1]
    
    strng = '('
    for o in tup_head:
      strng += o.__str__()+'\033[1;31;40m+\033[0;37;40m'
    strng += tail.__str__()
    strng += ')'
    return strng

  def __repr__(self:"gadd") -> str:
    tup_head = self.args[:-1]
    tail = self.args[-1]
    
    strng = '('
    for o in tup_head:
      strng += o.__repr__()+'+'
    strng += tail.__repr__()
    strng += ')'
    return strng


  def __hash__(self:"gadd") -> int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self:"gadd", other:"GExpr") -> bool:
    return (
      (type(other) == type(self)) and
      self.__hash__() == other.__hash__()
    )
  
  
  def reversion(self:"gadd")->"Box":
    t = [arg.reversion() for arg in self.args]
    return gadd(*t)

  def grade_involution(self:"gadd")->"Box":
    t = [arg.grade_involution() for arg in self.args]
    return gadd(*t)
  
  def clifford_conjugation(self:"gadd")->"Box":
    t = [arg.clifford_conjugation() for arg in self.args]
    return gadd(*t)


def rlgaddFlatten(expr):
  tbx = []
  # Flatten coz of gadd present inside Box
  for BX in expr.args:
    # Pattern Match
    # For ele == gadd inside Box or only Box
    if(type(BX.mv)==gadd):
      childbxes = BX.mv.args
      cf = BX.coeff
      flatbxes = [Box.__new__(Box,mv=bx.mv,coeff=Mul(bx.coeff,cf)) for bx in childbxes]

      tbx.extend(flatbxes)
  
    else :
      tbx.append(BX)
  
  expr1 = Basic.__new__(gadd, *tbx)
  return expr1

def rlgaddgroupsort(expr):
  sift_key = lambda x:x.mv
  sift_count = lambda x:x.coeff
  # sift_combine = lambda cnt,args:Box.__new__(Box,args,cnt.simplify())
  
  grouped = bx_sift(expr.args,sift_key,sift_count)
  filtered = [bx for bx in grouped if bx.coeff!=S(0)]
      
    
  Sortedseq = sorted(filtered,key=lambda bx:(len(bx.mv.grade),next(iter(bx.mv.grade)),bx.mv.name,bx.mv.__hash__()))

  return Basic.__new__(gadd, *Sortedseq)

rules1 = (
  rlgaddFlatten,rlgaddgroupsort
  )


# rules = (
#   unpack, rm_id(lambda x: x == 0), flatten,sort(lambda ele: ele.grade)
#   )

canonicalize = exhaust(typed({gadd: do_one(*rules1)}))


from libs.Sygal.operators.assop.higher.gaddhigher import gaddhigher
from libs.Sygal.operators.assop.simplify.gaddsimp import gaddsimp
from libs.Sygal.operators.assop.expand.gaddexpand import gaddexpand


gaddhigher()
gaddsimp()
gaddexpand()

from .importstail import *

if is_devmode():
  StrPrinter._print_gadd = gadd.sympyrepr
else :
  StrPrinter._print_gadd = gadd.sympystr