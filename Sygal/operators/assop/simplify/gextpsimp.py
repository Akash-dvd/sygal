from libs.Sygal.imports.import1head import *
from libs.Sygal.imports.import1tail import *
from libs.Sygal.operators.assop.gadd import gadd
from libs.Sygal.operators.assop.gextp import gextp
from libs.Sygal.operators.assop.gmul import gmul

from libs.Sygal.operators.binop.ganticomm import ganticomm
from libs.Sygal.operators.binop.gcomm import gcomm
from libs.Sygal.operators.binop.sclrprdct import sclrprdct
from libs.Sygal.operators.binop.grcntrct import grcntrct
from libs.Sygal.operators.binop.glcntrct import glcntrct
from libs.Sygal.imports.import_util2 import *

from libs.Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion
from libs.Sygal.operators.binop.outermorphic.projection import projection
from libs.Sygal.operators.binop.outermorphic.rejection import rejection



new = gextp.__new__

"""
7)  Check simplification for inv,pro,rej
TODO
TODO
TODO
TODO
((a1^a2..a_r)<((b1..br)^(c1..cm)))^((a1..a_r)<((b1..br)^(d1..dn))) ==
(a1^a2..a_r)<((b1..br)^(c1..cm)^(d1..dn))
Will be done after implementing dot product and multiplication.
"""

class concat():  
    
  @staticmethod
  def sandhi(expr:GExpr,depth:int = 0) -> GExpr:
    """bottom up conjugation by rlzero of single layer sub_sandhi
    
    """
    fn1 = concat.sandhi0(depth)
    fn = bottom_up(conjugation(rlZero,fn1))
    return fn(expr)

  @staticmethod
  def sandhi0(depth:int):
    def sandhi1(expr:GExpr) -> GExpr:
      
      """
      Sandhi Implementation
      =====================

      This function is meant for accomplishing single layer merge for x1^x2^a<(b^c)^a<(c^d) structure.
      It filters indexes having lncrt or rncrt.
      [(_rx, 0), (_rx, 1), (_oo, 2),(_oo,3),(_rx,4)]
      Then calls aggregator function to merge the indexes of lncrt or rncrt structures.
      lst2 = [(_rx, 0, 1, 4), (_oo, 2, 3)]

      Following this it call sub_sandhi1 on each tuple.(_rx, 0, 1, 4). BBut instead of indexes supplies list of denominator values of corresponding indexes.
      It expects the merhed version of the supplied indexes.
      It keeps appening the results to the arg list and After the list is exhausted it deletes the older arguements.
      Then recreates the expr with new args and returns.
      """
    
      lst1 = []
      # Pattern Match (<Grade-1>)(<>)(Exterior Product)
      # TODO Write a pattern matching api call
      if(isinstance(expr,gextp)):
        for i, x in enumerate(expr.args):
          if (isinstance(x,glcntrct) or isinstance(x,grcntrct)) and\
              (x.args[0].grade == {1}) and isinstance(x.args[1],gextp):
            lst1.append((x.args[0],i))
      # lst1 = [(_rx, 0), (_rx, 1), (_oo, 2),(_oo,3),(_rx,4)]
      
      # Only execute if above filter has matches present.
      if(len(lst1)>0):
        lst2 = concat.aggregator(lst1)
        # lst2 = [(_rx, 0, 1, 4), (_oo, 2, 3)]

        """
        Two sequential for loops
        Loop1
        
        Expects - expr and lst2
        Behavoir -  Loop over the lst2 tuples .
        1) Supply sub_sandhi1 with denominator w.r.t the indexes present.
        2) Appends the corresponding numerator and appends them to temporary arg list(T).
        3) Accumulate the indexes accross the tuples into cum_indx.
        
        Loop2
        1) Mark the elements T corrsponding to the indexes in cum_indx
        """
        T = list(expr.args)
        cum_indx = []
        for elem in lst2:
          indx = list(elem[1:])
          cum_indx.extend(indx)
          # (0,1,4)
          vec = elem[0]
          T1 = [expr.args[i].args[1] for i in indx]
          # T1 -> [a1^a2,a2^a3..]
          T2 = concat.sub_sandhi1(T1,depth+1)
          # T2 -> [a1^a2^a3..]
          T3 = [vec<(x) for x in T2]
          # T3 = rx<(a1^a^a3),...
          T.extend(T3)
        
        
        for indx in cum_indx:
          T[indx] = None
      
        
        expr = new(expr.__class__, *tuple(filter((None).__ne__, T)))
      
      return expr
    return sandhi1 
  @staticmethod
  def aggregator(lst:List[GExpr]) -> List[GExpr]:
    """
    Explanation


    lst is list of binary tuples.
    Tule's 1st part is symbol and 2nd is index
    lst = [(_rx, 0), (_rx, 1), (_oo, 2),(_oo,3),(_rx,4)]
    aggregator(lst) == [(_rx, 0, 1, 4), (_oo, 2, 3)]
    """
    mapp = defaultdict(list) 
    for x, y in lst: 
      mapp[x].append(y) 
      lst2 = [(x, *y) for x, y in mapp.items()] 
    return lst2
  
  @staticmethod
  def sub_sandhi1(exprList:List[GExpr],depth:int) -> List[GExpr]:
    index = [0,1]
    exprList1 = exprList.copy()
    # lstln = lambda lst:len(lst)
    while index[0]<len(exprList1):
      index[1]=index[0]+1
      while index[1]<len(exprList1):
        exprList1 = concat.sub_sub_sandhi1(index,exprList1,depth)
        index[1]+=1
      index[0]+=1
      
    return exprList1

  @staticmethod
  def sub_sub_sandhi1(index:List,exprList:List[GExpr],depth:int ) -> List[GExpr]: 
    expr1 = exprList[index[0]] 
    expr2 = exprList[index[1]]
    ln1 = len(expr1.args)+len(expr2.args)
    # grd1= expr1.grade
    # grd2= expr2.grade
    expr3Set = set(expr1.args)
    expr3Set.update(set(expr2.args))
    ln2 = len(expr3Set)
    

    arg1 = tuple(expr3Set)
    sub1 = expr1.func(*arg1)

    x = ln1-ln2-depth
    # print("x=",x,"depth=",depth,"len1=",ln1,"len2=",ln2)
    # print(expr1)
    # print(expr2)
    
    if(x<0):
      Tsub1 = concat.sandhi(sub1,depth)
      if(Tsub1==sub1):
        return exprList
      else:
        exprList[index[0]] = Tsub1
        del exprList[index[1]]
        index[1]=index[0]
        return exprList        
    
    elif (x==0):
      #####
      exprList[index[0]] = concat.sandhi(sub1,depth)
      #####
      del exprList[index[1]]
      index[1]=index[0]
      return exprList      

    else:
      return [S(0)]


# expr = a2^(a1<((b1<(a1^a2)^b2)))^(a1<((b1<(a3^a2)^b3)))
# concat.sandhi(expr)

def inv_gextp(expr):

  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gextp:

      for i,arg in enumerate(BX.mv.args):
        if(type(arg)==inversion):
          up = arg.up
          down = arg.down
          if(up in BX.mv.args) or (down in BX.mv.args):
            lst = list(BX.mv.args)
            # INV -> Gmul
            # sub*obj*sub/(sub<sub)
            t = arg.gexpand()
            # Gmul -> Gadd
            t1 = t.gexpand()
            # distribute over sum
            lst[i] = t1
            t2 = gextp(*t1)
            t3 = t2.gdistribute()
            return t3
      else :
        return expr
    else :
      return expr 
  else :
    return expr

# sign issues
def proj_gextp(expr):
  # DproU^D -> 0
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gextp:

      for i,arg in enumerate(BX.mv.args):
        if(type(arg)==projection):
          up = arg.up
          down = arg.down
          if (down in BX.mv.args):
            return GExpr.Znl
          # (up in BX.mv.args): doesn't make much sense
      else :
        return expr
    else :
      return expr 
  else :
    return expr

# sign issues
def rej_gextp(expr):
  # DrejU^D -> 
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gextp:

      for i,arg in enumerate(BX.mv.args):
        if(type(arg)==rejection):
          up = arg.up
          down = arg.down
          if (down in BX.mv.args):
            lst = list(BX.mv.args)
            lst[i] = (up^down) 
            return gextp(*lst)
          # (up in BX.mv.args): doesn't make much sense
      else :
        return expr
    else :
      return expr 
  else :
    return expr

############################
# mtDt ceiling touch simple and complex
# replace or merge when ceiling is touched
# {I3:3,I41:1} -> replace with I3
# {I3:2,I41:2} -> {I41:4}
def rej_mtDt(expr):
  return expr
  ################
  # replace or merge when ceiling is touched
  # {I3:3,I41:1} -> replace with I3
  # {I3:2,I41:2} -> {I41:4}
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    for i,k,v in enumerate(BX.mv.mtDt.items()):
      if not k == GExpr.nl:
        if v == set(len(k.mv.args)):
          lst = [ele for ele in BX.mv.args if ele.mtDt[k] and len(ele.mtDt)==1 and len(ele.mtDt[k])==1]
          if len(k.mv.args) == reduce(lambda x,y:x.mv.mtDt[k]+y.mv.mtDt[k],lst) :
            diffA = [ele for ele in BX.mv.args if ele not in lst]
            cpydiffA = []
            cpydiffA.extend(diffA)
            cpydiffA.extend(lst)
            sign1 = parity(BX.mv.args,cpydiffA)
            cpydiffB = []
            cpydiffB.extend(diffA)
            cpydiffB.extend(k.mv.args)
            t_lst = gextp(*lst)
            iFrame = GExpr.pSCiFrmlst(GExpr.pSClst.index(k))
            bx = gextp(*cpydiffB)*(t_lst|iFrame)*sign1*cf
            bx.mv.mtDt = relDt()
            bx.mv.rlDt = relDt()
            return bx
  
        else :
          pass
      else:
        pass
  else :
    return expr

def gextpsimp():
  gextp.gsimplify = exhaust(do_one(concat.sandhi,inv_gextp,proj_gextp,rej_gextp))