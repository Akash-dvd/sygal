# Core imports - Import directly to avoid circular dependency
# (imports.core imports GAtom which may trigger _preprocess which needs gextp)
from Sygal.GExpr import GExpr
from Sygal.Box import Box
from Sygal.imports.sympy_basic import Basic, Mul, S
from Sygal.imports.typing_helpers import Tuple
from Sygal.imports.strategies import exhaust, typed, do_one
from Sygal.imports.utils import rlGSortArgs, parity, is_unMixedGrade
from Sygal.imports.typing_helpers import product
from Sygal.imports.psc import spclst
from Sygal.imports.utils import is_devmode
from Sygal.imports.sympy_basic import StrPrinter

from Sygal.operators.assop.assop import assop

# defDic = defaultdict(lambda x:None)

class gextp(assop):

  def __new__(cls, args0:GExpr,*args:Tuple[GExpr],**kwargs) -> "Box":
    # gextp(Box,Optional[Box,Box.....])

    # Pattern Matching for # of args for associative op# Pattern Matching for # of args for associative op
    t =  [args0]
    t.extend(args)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))

    # every element has grade !={0}
    # Here Altering with args so pattern matching is required
    tmvs = [bx.mv for bx in t1 if bx.mv!=Box.nl]
    cfs = [bx.coeff for bx in t1]
    cf = Mul(*cfs)

    if cf == S(0):
      return(GExpr.Znl)
    
    # Pattern Matching for # of args for associative op
    if tmvs == []:
      return Box.__new__(Box,mv=Box.nl,coeff=cf)
    elif len(tmvs)==1:
      return Box.__new__(Box,mv=tmvs[0],coeff=cf)
    else:
      MV1 = Basic.__new__(gextp, *tmvs)
      

      # For flattening
      # Here Altering with args so pattern matching is required
      # But this canocalize doesn't reduce the args ever
      MV2 = canonicalize1(MV1)
      
      # More patternmatching
      if(len(MV2.args)<=1):
        # Not possible
        # to arrive here
        raise ValueError("How did u arrive here for gextp")
      
      # Repitition Check
      ###########################
      if ((len(MV2.args)-len(set(MV2.args))) > 0):  
        return GExpr.Znl

      MV3 = gextp.meta_treatment(MV2)
      if MV3 == GExpr.Znl:
        return GExpr.Znl

      # ordering
      ###########################
      if(is_unMixedGrade(MV3)):
        # For signed sorting
        MV4 = canonicalize2(MV3)
        cf1 = Mul(parity(MV3.args,MV4.args),cf)

      else :
        MV4 = MV3
        cf1 = cf

      MV4.mtDt = MV3.mtDt
      bx = Box.__new__(Box,mv=MV4,coeff=cf1)
      return bx


  def sympystr(self,expr:"gextp") -> str:
    return str(expr)

  def sympyrepr(self,expr:"gextp") -> str:
    return expr.__repr__()

  def __str__(self:"gextp") -> str:
    tup_head = self.args[:-1]
    tail = self.args[-1]
    
    strng = '('
    for o in tup_head:
      strng += o.__str__()+'\033[1;31;40m^\033[0;37;40m'
    strng += tail.__str__()
    strng += ')'
    return strng

  def __repr__(self:"gextp") -> str:
    tup_head = self.args[:-1]
    tail = self.args[-1]
    
    strng = '('
    for o in tup_head:
      strng += o.__repr__()+'^'
    strng += tail.__repr__()
    strng += ')'
    return strng

  def __hash__(self:"gextp") -> int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self:"gextp", other:"GExpr") -> bool:
    return (
      (type(other) == type(self)) and
      self.__hash__() == other.__hash__()
    )

  def reversion(self:"gextp")->"Box":
    t = [arg.reversion() for arg in self.args]
    t.reverse()
    return gextp(*t)

  def grade_involution(self:"gextp")->"Box":
    if is_unMixedGrade(self):
      sign1 = next(iter(self.grade))%2
      sign  = (S(-2)*sign1)+1
      return Box.__new__(Box,self,sign)
    else :
      raise NotImplemented
      # return Box.__new__(Box,self)
  
  def clifford_conjugation(self:"gextp")->"Box":
    t = self.grade_involution()
    t1 = t.reversion()
    return t1

  def meta_treatment(expr:"gextp")->"gextp":
    

    # if null list extend -> null list
    # if null dict update -> null dict
    acc_mtDt = spclst([])
    spc_lst = spclst([])
    spc_lst.extend(expr.args[0].mtDt)

    for arg in expr.args[1:]:
      # TODO
      # Iterate over only the upere half on product    
      acc_mtDt.extend([dct1+dct2 for dct1,dct2 in product(spc_lst,arg.mtDt)])

      if bool(acc_mtDt):
        spc_lst.clear()
        spc_lst.extend(acc_mtDt)
        acc_mtDt.clear()
    
      else:
        return GExpr.nl
    
    if bool(spc_lst):
      expr.mtDt = spc_lst
      return expr
    else :
      return GExpr.Znl


from Sygal.operators.assop.higher.gextphigher import gextphigher
from Sygal.operators.assop.canon.gextpcanon import gextpcanon
from Sygal.operators.assop.expand.gextpexpand import gextpexpand

from Sygal.imports.strategies import unpack, flatten

rules1 = (
  unpack,flatten
  )
rules2 = (
  rlGSortArgs,
  )


canonicalize1 = exhaust(typed({gextp: do_one(*rules1)}))
canonicalize2 = exhaust(typed({gextp: do_one(*rules2)}))

gextphigher()
gextpcanon()
gextpexpand()



if is_devmode():
  StrPrinter._print_gextp = gextp.sympyrepr
else :
  StrPrinter._print_gextp = gextp.sympystr


  # @property
  # def grade(self:"gextp") -> Union[set,frozenset]:
  #   t1 = set()
  #   t2 = set()
  #   t1.update(self.args[0].grade)
  #   for i,argi in enumerate(self.args):
  #     j=i+1
  #     if(j<len(self.args)):
  #       t2.clear()
  #       arg2 = self.args[j].grade
  #       for elem1,elem2 in product(t1,arg2):
  #         t2.add((elem2+elem1))
  #       t1.clear()
  #       t1.update(t2)
  #   return t2
