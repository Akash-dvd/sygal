from libs.Sygal.imports.import1head import *
from libs.Sygal.operators.assop.assop import assop

class gmul(assop):

  def __new__(cls, args0:GExpr,*args:Tuple["GExpr"]) -> "Box":
    # gmul(Box,Optional[Box,Box.....])


    t =  [args0]
    t.extend(args)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))

    # every element has grade !={0}
    # Here Altering with args so pattern matching is required
    tmvs = [bx.mv for bx in t1 if bx.mv!=Box.nl]
    cfs = [bx.coeff for bx in t1]
    # cf = Mul(*cfs).simplify()
    cf = Mul(*cfs)
    
    # Pattern Matching for # of args for associative op
    if tmvs == []:
      return Box.__new__(Box,mv=Box.nl,coeff=cf)
    elif len(tmvs)==1:
      return Box.__new__(Box,mv=tmvs[0],coeff=cf)
    else:
      expr1 = Basic.__new__(gmul, *tmvs)
      # Here Altering with args so pattern matching is required
      # But this canocalize doesn't reduce the args ever
      expr2 = canonicalize(expr1)
      
      # More patternmatching
      if(len(expr2.args)<=1):
        # Not possible
        # to arrive here
        raise ValueError
      
      
      bx = Box.__new__(Box,mv=expr2,coeff=cf)
      
      # if ((len(args)-len(set(args))) == 0):  
      #   obj = Basic.__new__(cls, *t1)
      # else :
      #   t3 = super().Znl
      #   return Basic.__new__(cls, *t3)


      if all(not isinstance(i, GExpr) for i in t1):
        pass
        # append to appendage for grade 0


      
      return bx


  @property
  def grade(self:"gmul") -> Union[set,frozenset]:
    if(len(self.args)==1):
      return self.args[0].grade
    else:
      t1 = set()
      t2 = set()
      t1.update(self.args[0].grade)
      for i,argi in enumerate(self.args):
        j=i+1
        if(j<len(self.args)):
          t2.clear()
          arg2 = self.args[j].grade
          for elem1 in t1:
            for elem2 in arg2:
              t2.update(list(range(abs(elem2-elem1),(elem2+elem1+1),2)))
          t1.clear()
          t1.update(t2)
    return t2


  def sympystr(self,expr:"gmul") -> str:
    return str(expr)

  def sympyrepr(self,expr:"gmul") -> str:
    return expr.__repr__()

  def __str__(self:"gmul") -> str:
    tup_head = self.args[:-1]
    tail = self.args[-1]
    
    strng = '('
    for o in tup_head:
      strng += o.__str__()+'\033[1;31;40m*\033[0;37;40m'
    strng += tail.__str__()
    strng += ')'
    return strng

  def __repr__(self:"gmul") -> str:
    tup_head = self.args[:-1]
    tail = self.args[-1]
    
    strng = '('
    for o in tup_head:
      strng += o.__repr__()+'*'
    strng += tail.__repr__()
    strng += ')'
    return strng


  def __hash__(self:"gmul") -> int:
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self:"gmul", other:"GExpr") -> bool:
    return (
      (type(other) == type(self)) and
      self.__hash__() == other.__hash__()
    )

  def reversion(self:"gmul")->"Box":
    t = [arg.reversion() for arg in self.args]
    t.reverse()
    return gmul(*t)

  def grade_involution(self:"gmul")->"Box":
    if is_unMixedGrade(self):
      sign1 = next(iter(self.grade))%2
      sign  = (S(-2)*sign1)+1
      return Box.__new__(Box,self,sign)
    else :
      raise NotImplemented
      # return Box.__new__(Box,self)
  
  def clifford_conjugation(self:"gmul")->"Box":
    t = self.grade_involution()
    t1 = t.reversion()
    return t1


rules = (
   flatten,
  )


from libs.Sygal.operators.assop.higher.gmulhigher import gmulhigher
from libs.Sygal.operators.assop.simplify.gmulsimp import gmulsimp
from libs.Sygal.operators.assop.expand.gmulexpand import gmulexpand

canonicalize = exhaust(typed({gmul: do_one(*rules)}))

gmulhigher()
gmulsimp()
gmulexpand()

from libs.Sygal.imports.import1tail import *

if is_devmode():
  StrPrinter._print_gmul = gmul.sympyrepr
else :
  StrPrinter._print_gmul = gmul.sympystr
