from Sygal.imports.import1head import *
from Sygal.imports.import1tail import *
from Sygal.operators.assop.gadd import gadd
from Sygal.operators.assop.gextp import gextp
from Sygal.operators.assop.gmul import gmul

from Sygal.operators.binop.ganticomm import ganticomm
from Sygal.operators.binop.gcomm import gcomm
from Sygal.operators.binop.sclrprdct import sclrprdct
from Sygal.operators.binop.grcntrct import grcntrct
from Sygal.operators.binop.glcntrct import glcntrct
from Sygal.imports.import_util2 import *

from Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion
from Sygal.operators.binop.outermorphic.projection import projection
from Sygal.operators.binop.outermorphic.rejection import rejection


new = gextp.__new__


"""
7)  Check simplification for inv,pro,rej

TODO
a1<(I4)^(a1<(b1^c1)) = 0

"""

class concat():
    
  @staticmethod
  def sandhi(expr:Box,blade1:GExpr = lambda:GExpr.Onl) -> Box:
    """
    This procedure requires bottom_up -> top_down iterator.
    simplify_iter/canoncalize_iter does the bottom_up part
    Following top_down is accomplished via ad-hoc method here.
    Instead of metadata bruteforce is used. metadat incomplete implementation is present in the comments
    """
    if callable(blade1):
      blade1 = blade1()

    if type(expr)==Box and is_uniGraded(expr) and is_uniGraded(blade1):
      BX = expr
      if type(BX.mv) == gextp:

        # t = concat.metaData(BX,blade)
        # t1 = concat.iter(BX,blade,t)
        t1 = concat.iter(BX,blade1)
        return t1
      else:
        return expr
    else :
      return expr
 
  @staticmethod
  def remake(oexpr:Box,nexpr:Box,ind1:int,ind2:int) -> Box:
    # sign2 = parity(n_args3,n_args2)
    t = [ele for i,ele in enumerate(oexpr.mv.args) if i!= ind1 and i!=ind2]
    t1 = t.copy()
    t1.append(oexpr.mv.args[ind1])
    t1.append(oexpr.mv.args[ind2])
    sign = parity(oexpr.mv.args,t1)
    t2 = t.copy()
    t2.append(nexpr)
    bx = gextp(*t2)*sign
    return bx

  @staticmethod
  def iter(bx:Box,blade1:GExpr) -> Box:
    plck_lst1 = [i for i, x in enumerate(bx.mv.args) if type(x) == glcntrct and type(x.down) == gextp]

    for ind1,ind2 in subsets(plck_lst1,2):
      T1 = [bx.mv.args[ind1],bx.mv.args[ind2]]
      flag,expr1 = concat.binary_op(T1[0],T1[1],blade1)
      if flag:
        if expr1 == GExpr.Znl:
          return expr1
        else:
          bx_n = concat.remake(bx,expr1,ind1,ind2)*bx.coeff
          return bx_n
      else:
        continue            
    return bx

  @staticmethod
  def binary_op(expr1:glcntrct,expr2:glcntrct,blade1:GExpr) -> Tuple[bool,Box]: 
    # ln12 = len(expr1.args)+len(expr2.args)
    up1 = expr1.up
    up2 = expr2.up
    dn1 = expr1.down
    dn2 = expr2.down

    if up1 == up2:
      blade12 = up1
      blade2 = blade1^blade12
    elif (up1.is_atom and type(up2) == gextp):
      t1 = up1 in up2.args
      if t1:
        blade12 = up1
        blade2 = blade1^blade12

        n_args_up2 = [up1]
        args_dn2_up2 = [ele for ele in up2.args if ele!=up1]
        
        n_args_up2.extend(args_dn2_up2)

        sign = parity(up2.args,n_args_up2)
        dn2 = (gextp(*args_dn2_up2)<dn2)*sign
      else:
        return (False,GExpr.Znl)
    elif (type(up1) == gextp and up2.is_atom ):
      t2 = up2 in up1.args
      if t2:
        blade12 = up2
        blade2 = blade1^blade12

        n_args_up1 = [up2]
        args_dn1_up1 = [ele for ele in up1.args if ele!=up2]
        
        n_args_up1.extend(args_dn1_up1)

        sign = parity(up1.args,n_args_up1)
        dn1 = (gextp(*args_dn1_up1)<dn1)*sign
      else:
        return (False,GExpr.Znl)
    elif (type(up1) == gextp) and (type(up1) == gextp):
      t1 = all([ele in up2.args for ele in up1.args])
      # UP1 IS PROPER SUBSET OF UP2
      t2 = all([ele in up1.args for ele in up2.args])
      # UP2 IS PROPER SUBSET OF UP1
      if t1 and t2:
        raise ValueError("Should have been caught earlier")
      elif t1:
        # up2 must be type gextp
        blade12 = up1
        blade2 = blade1^blade12

        n_args_up2 = list(up1.args)
        args_dn2_up2 = [ele for ele in up2.args if ele not in up1.args]
        
        n_args_up2.extend(args_dn2_up2)

        sign = parity(up2.args,n_args_up2)
        dn2 = (gextp(*args_dn2_up2)<dn2)*sign
      elif t2:
        # up1 must be type gextp
        blade12 = up2
        blade2 = blade1^blade12

        n_args_up1 = list(up2.args)
        args_dn1_up1 = [ele for ele in up1.args if ele not in up2.args]
        
        n_args_up1.extend(args_dn1_up1)

        sign = parity(up1.args,n_args_up1)
        dn1 = (gextp(*args_dn1_up1)<dn1)*sign
      else:
        return (False,GExpr.Znl)
    else:
        return (False,GExpr.Znl)

    dmvs = []
    cf = S(1)
    if type(dn1) == Box:
      dmvs.append(dn1.mv)
      cf *= dn1.coeff
    else:
      dmvs.append(dn1)

    if type(dn2) == Box:
      dmvs.append(dn2.mv)
      cf *= dn2.coeff
    else:
      dmvs.append(dn2)
    
    dn11 = dmvs[0]
    dn21 = dmvs[1]

    grd12 = dn11.grade.pop() + dn21.grade.pop()

    dargs_U = []

    # TODO
    # Add gatom support for grade >1
    if (type(dn11) == gextp) and (type(dn21) == gextp):
      args_intersct = [ele for ele in dn11.args if ele in dn21.args]

      args1_2 = [ele for ele in dn11.args if ele not in args_intersct]
      n_args11 = []
      n_args11.extend(args1_2)
      n_args11.extend(args_intersct)
      sign1 = parity(dn11.args,n_args11)
      
      args2_1 = [ele for ele in dn21.args if ele not in args_intersct]
      n_args21 = []
      n_args21.extend(args_intersct)
      n_args21.extend(args2_1)
      sign2 = parity(dn21.args,n_args21)

      dargs_U.extend(dn11.args)
      dargs_U.extend(args2_1)
      # dargs_U.extend([ele for ele in dn21.args if ele not in dn11.args])
      
    elif (type(dn11) == gextp):
      
      if dn21 in dn11.args:

        args1_2 = [ele for ele in dn11.args if ele!=dn21]
        n_args11 = []
        n_args11.extend(args1_2)
        n_args11.append(dn21)
        sign1 = parity(dn11.args,n_args11)
        sign2 = S(1)

        dargs_U.extend(dn11.args)

      else:

        sign1 = S(1)
        sign2 = S(1)

        dargs_U.extend(dn11.args)
        dargs_U.append(dn21)

    elif (type(dn21) == gextp):
      if dn11 in dn21.args:
        args2_1 = [ele for ele in dn21.args if ele!=dn11]
        n_args21 = []
        n_args21.append(dn11)
        n_args21.extend(args2_1)
        sign2 = parity(dn21.args,n_args21)
        sign1 = S(1)

        dargs_U.extend(dn21.args)       
      else:
        
        sign1 = S(1)
        sign2 = S(1)

        dargs_U.append(dn11)
        dargs_U.extend(dn21.args)  
    
    else:
      raise NotImplementedError

    dbx_U = gextp(*dargs_U)*cf*sign1*sign2

    x = grd12 - dbx_U.grade.pop() - blade2.grade.pop()

    if(x<0):
      Tsub1 = concat.sandhi(dbx_U,blade2)
      if(Tsub1==dbx_U):
        return (False,GExpr.Znl)
        # Check again
      else:
        return (True,blade12<Tsub1)
    
    elif (x==0):
      # More check is required
      Tsub1 = concat.sandhi(dbx_U,blade2)
      if Tsub1 == dbx_U:
        # TEST the sign values

        args_intersct = [ele for ele in dn11.args if ele in dn21.args]
        expr_intersect = gextp(*args_intersct)

        args1_2 = [ele for ele in dn11.args if ele not in args_intersct]
        n_args11 = []
        n_args11.extend(args1_2)
        n_args11.extend(args_intersct)
        sign1 = parity(dn11.args,n_args11)
        
        args2_1 = [ele for ele in dn21.args if ele not in args_intersct]
        n_args21 = []
        n_args21.extend(args_intersct)
        n_args21.extend(args2_1)
        sign2 = parity(dn21.args,n_args21)

        coeff = (blade2|expr_intersect)*sign1*sign2
        
        bx = (blade12<dbx_U)*coeff
        return (True,bx)    
      else :
        return (True,GExpr.Znl)    

    else:
      # return [S(0)]
      return (True,GExpr.Znl)


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

def gextpcanon():
  # gextp.gcanonicalization = exhaust(do_one(grcntrct.gcanonicalization,concat.sandhi,inv_gextp,proj_gextp,rej_gextp))
  gextp.gcanonicalization = exhaust(do_one(concat.sandhi,inv_gextp,proj_gextp,rej_gextp))
  # gextp.gcanonicalization = exhaust(do_one(concat.sandhi,))



  # @staticmethod
  # def metaData(bx:Box,blade:GExpr) -> list:

  #   # grcntrct -> glcntrct already done b4 this
  #   # pluck glcntrct with gextp in down element

  #   plck_lst1 = [{x.up:[i]} for i, x in enumerate(bx.mv.args) if type(x) == glcntrct and type(x.down) == gextp]
  #  # plck_lst1=[{a^b:[0]}, {_rx:[1]}, {_rx:[2]},{_oo^_rx:[3]}, {_oo:[4]}]

  #   # check for unigradedness here
  #   mapp = defaultdict(list) 
  #   for x, y in plck_lst1: 
  #     mapp[x].append(y) 
  #     plck_lst2 = [(x, *y) for x, y in mapp.items()] 

  #   # plck_lst2 = [{a^b:[0]}, {_rx:[1,2],_oo^_rx:[3]}, {_oo:[4],_oo^_rx:[3]}]
    
  #   return plck_lst2

  # @staticmethod
  # def iter(bx:Box,blade:GExpr) -> Box:
  #   plck_lst1 = [(x.up,i) for i, x in enumerate(bx.mv.args) if type(x) == glcntrct and type(x.down) == gextp]

    
  #   for dct in plck_lst1:
  #     for k in subsets(dct,1):
  #       for i,j in subsets(dct[k],2) :
  #         T1 = [bx.mv.args[i],bx.mv.args[j]]
  #         flag,expr1 = concat.binary_op(T1,blade)
  #         if flag:
  #           if expr1 == GExpr.Znl:
  #             return expr1
  #           else:
  #             # create expr again
  #             # n_args3 = GSortArgs(n_args2)
  #             # sign2 = parity(n_args3,n_args2)
  #             return concat.remake(bx,expr1,i,j)
  #         else:
  #           continue            
  #     for k1,k2 in subsets(dct,2):            
  #       for i,j in product(subsets(dct[k1],1),subsets(dct[k2],1)):
  #         T1 = [bx.mv.args[i],bx.mv.args[j]]
  #         flag,expr1 = concat.binary_op(T1,blade)
  #         if flag:
  #           if expr1 == GExpr.Znl:
  #             return expr1
  #           else:
  #             # create expr again
  #             # n_args3 = GSortArgs(n_args2)
  #             # sign2 = parity(n_args3,n_args2)
  #             return concat.remake(bx,expr1,i,j)
  #         else:
  #           continue               

  #   return bx


          # if (type(blade.mv) == gextp) and (type(blade1.mv) == gextp):
        #   blade_args_intersect = [ele for ele in blade1.mv.args if ele not in blade.mv.args]
        #   blade_I = gextp(*blade_args_intersect)

        # elif (type(blade1.mv) == gextp):
        #   blade_args_intersect = [ele for ele in blade1.mv.args if ele!=blade.mv]
        #   blade_I = gextp(*blade_args_intersect)
        # elif blade == GExpr.Onl:
        #   blade_I = blade1
        # else:
        #   raise ValueError("How arrived here")

        # if (type(blade.mv) == gextp) and (type(blade1.mv) == gextp):
        #   blade_args_intersect = [ele for ele in blade1.mv.args if ele not in blade.mv.args]
        #   blade_I = gextp(*blade_args_intersect)

        # elif (type(blade1.mv) == gextp):
        #   blade_args_intersect = [ele for ele in blade1.mv.args if ele!=blade.mv]
        #   blade_I = gextp(*blade_args_intersect)
        # elif blade == GExpr.Onl:
        #   blade_I = blade1
        # else:
        #   raise ValueError("How arrived here")