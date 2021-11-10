from .importshead import *


class gextp(assop):

  def __new__(cls, args0:GExpr,*args:Tuple["GExpr"],**kwargs) -> "Box":
    # gextp(Box,Optional[Box,Box.....])

    # Pattern Matching for # of args for associative op# Pattern Matching for # of args for associative op
    t =  [args0]
    t.extend(args)
    t1 = tuple(map(lambda x:Box.__new__(Box,x),t))

    # every element has grade !={0}
    # Here Altering with args so pattern matching is required
    tmvs = [bx.mv for bx in t1 if bx.mv!=Box.nl]
    cfs = [bx.coeff for bx in t1]
    cf = Mul(*cfs).simplify()
    
    # Pattern Matching for # of args for associative op
    if tmvs == []:
      return Box.__new__(Box,mv=Box.nl,coeff=cf)
    elif len(tmvs)==1:
      return Box.__new__(Box,mv=tmvs[0],coeff=cf)
    else:
      expr1 = Basic.__new__(gextp, *tmvs)
      # For flattening
      # Here Altering with args so pattern matching is required
      # But this canocalize doesn't reduce the args ever
      expr2 = canonicalize1(expr1)
      
      # More patternmatching
      if(len(expr2.args)<=1):
        # Not possible
        # to arrive here
        raise ValueError
      
      # Repitition Check
      if ((len(expr2.args)-len(set(expr2.args))) > 0):  
        return GExpr.Znl

      if(is_unMixedGrade(expr2)):
        # For signed sorting
        expr3 = canonicalize2(expr2)
        # More patternmatching
        if(len(expr3.args)<=1):
        # Not possible
        # to arrive here
          raise ValueError

        cf1 = Mul(parity(expr2.args,expr3.args),cf).simplify()
      else :
        expr3 = expr2
        cf1 = cf
      bx = Box.__new__(Box,mv=expr3,coeff=cf1)
      



      if all(not isinstance(i, GExpr) for i in t1):
        pass
        # pseudoscalar check


      
      return bx


  @property
  def grade(self:"gextp") -> Union[set,frozenset]:
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
              t2.add((elem2+elem1))
          t1.clear()
          t1.update(t2)
    return t2


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


from libs.Sygal.operators.assop.higher.gextphigher import gextphigher
from libs.Sygal.operators.assop.simplify.gextpsimp import gextpsimp
from libs.Sygal.operators.assop.expand.gextpexpand import gextpexpand

from .importstail import *

rules1 = (
    unpack,flatten
  )
rules2 = (
    unpack,rlGSortArgs
  )


canonicalize1 = exhaust(typed({gextp: do_one(*rules1)}))
canonicalize2 = exhaust(typed({gextp: do_one(*rules2)}))

gextphigher()
gextpsimp()
gextpexpand()



if is_devmode():
  StrPrinter._print_gextp = gextp.sympyrepr
else :
  StrPrinter._print_gextp = gextp.sympystr
