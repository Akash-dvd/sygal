from Sygal.imports.import1head import *
from Sygal.operators.assop.assop import assop


class gmul(assop):

  def __new__(cls, args0:GExpr,*args:Tuple[GExpr]) -> "Box":
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
    
    if cf == S(0):
      return(GExpr.Znl)

    # Pattern Matching for # of args for associative op
    if tmvs == []:
      return Box.__new__(Box,mv=Box.nl,coeff=cf)
    elif len(tmvs)==1:
      return Box.__new__(Box,mv=tmvs[0],coeff=cf)
    else:
      MV1 = Basic.__new__(gmul, *tmvs)
      # Here Altering with args so pattern matching is required
      # But this canocalize doesn't reduce the args ever
      MV2 = canonicalize(MV1)
      

      # More patternmatching
      if(len(MV2.args)<=1):
        # Not possible
        # to arrive here
        raise ValueError
      
      MV3 = meta_treatment(MV2)
      if MV3 == GExpr.Znl:
        return GExpr.Znl
      elif MV3.grade == {0}:
        if len(MV3.args) != 2:
          raise NotImplementedError
        MV4 = sclrprdct(MV3.args[0],MV3.args[1])
        t = MV4*cf
        return t
      else :
        bx = Box.__new__(Box,mv=MV3,coeff=cf)
        return bx

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

def meta_treatment(expr:gmul)->gmul:

  Zval = grd(0,0)
  acc_spc_lst = spclst([])
  spc_lst = spclst([])
  spc_lst.extend(expr.args[0].mtDt)
  for arg in expr.args[1:]:
    
    acc_spc_lst.clear()
    for pre_dct,post_dct in product(spc_lst,arg.mtDt):
      # [(a,),(a,b)] 

      # Add ^ to lst 
      acc_spc_lst.append(pre_dct+post_dct)

      pre_keys_tup = subsets(pre_dct)
      next(pre_keys_tup)
      # [(a,),(a,b)]
      post_keys_tup = subsets(post_dct)
      next(post_keys_tup)
      # (a,b,c) , (a,b)

      for tup1,tup2 in product(pre_keys_tup,post_keys_tup):
        tup1_grd = reduce(lambda x,y:x+y,[pre_dct[k].value for k in tup1])
        tup2_grd = reduce(lambda x,y:x+y,[post_dct[k].value for k in tup2])

        ceil_size = min(tup1_grd,tup2_grd)
        flr_size  = max(len(tup1),len(tup2))


        for size in range(flr_size,ceil_size+1):  
        
          part1 = kbin_distri(size,len(tup1))
          part2 = kbin_distri(size,len(tup2))

          # part1 = [[1,2,1],[3,1]]
          # part2 = [[1,2,1],[3,1]]
          # p1 = [1,2,1]
          # p2 = [1,3]

          for p1,p2 in product(part1,part2):
            t1 = all([pre_dct[k].value>=p1[i] for i,k in enumerate(tup1)])
            t2 = all([post_dct[k].value>=p2[i] for i,k in enumerate(tup2)])

            if t1 and t2:

              t_dct1  = spcdct({})
              t_dct11 = spcdct({})
              t_dct2  = spcdct({})
              t_dct21 = spcdct({})
              

              t_dct1.update({k:grd(p1[i],pre_dct[k].limit) for i,k in enumerate(tup1)})

              for k,v in pre_dct.items():
                t3 = pre_dct[k].value-(t_dct1.get(k,Zval)).value
                t_dct11.update({k:grd(t3,pre_dct[k].limit)})
            

              t_dct2.update({k:grd(p2[i],post_dct[k].limit) for i,k in enumerate(tup2)})

              for k,v in post_dct.items():
                t4 = post_dct[k].value-(t_dct2.get(k,Zval)).value
                t_dct21.update({k:grd(t4,post_dct[k].limit)})
              

              if t_dct1|t_dct2 :
                acc_spc_lst.append(t_dct11+t_dct21)

            
            else :
              continue
    
    
    spc_lst.clear()
    if bool(acc_spc_lst):
      spc_lst.extend(acc_spc_lst)
    else :
      break
  
  if bool(spc_lst):
    expr.mtDt = spc_lst
    return expr
  else :
    return GExpr.Znl



rules = (
   flatten,
  )


from Sygal.operators.assop.higher.gmulhigher import gmulhigher
from Sygal.operators.assop.canon.gmulcanon import gmulcanon
from Sygal.operators.assop.expand.gmulexpand import gmulexpand



canonicalize = exhaust(typed({gmul: do_one(*rules)}))

gmulhigher()
gmulcanon()
gmulexpand()

from Sygal.imports.import1tail import *

if is_devmode():
  StrPrinter._print_gmul = gmul.sympyrepr
else :
  StrPrinter._print_gmul = gmul.sympystr

# THIS WAS LIKE AN AD_HOC INSERTION HERE
# PUTTING ON TOP GIVES DEPENDENCY ERROR
# BUT LOOKS FINE ALSO :|
from Sygal.operators.binop.sclrprdct import sclrprdct


  # @property
  # def grade(self:"gmul") -> Union[set,frozenset]:
  #   if(len(self.args)==1):
  #     return self.args[0].grade
  #   else:
  #     t1 = set()
  #     t2 = set()
  #     t1.update(self.args[0].grade)
  #     for i,argi in enumerate(self.args):
  #       j=i+1
  #       if(j<len(self.args)):
  #         t2.clear()
  #         arg2 = self.args[j].grade
  #         for elem1,elem2 in product(t1,arg2):
  #           t2.update(set(range(abs(elem2-elem1),(elem2+elem1+1),2)))
  #         t1.clear()
  #         t1.update(t2)
  #   return t2