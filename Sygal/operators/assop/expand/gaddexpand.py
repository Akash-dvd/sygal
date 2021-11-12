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




def distriOvr_GAdd(A):
# Notice multiple returns otherwise null is returned causing errors
  def distribute_rl(expr):
    if (type(expr)==Box):
      BX = expr
      cf = BX.coeff
      if type(BX.mv)==A:
        for i, arg in enumerate(BX.mv.args):
          # Add here for rotation dilation translation etc
          if((A == inversion or A == projection) and i==0):
            continue
          elif (A == rejection and i==1):
            continue
          else:
            if isinstance(arg, gadd):
              first, b, tail = BX.mv.args[:i], BX.mv.args[i], BX.mv.args[i+1:]
              tmplst = [A(*(first + (bx,) + tail))*cf for bx in b.args]
              t =  gadd(*tmplst)
              return t
        return expr
      else:
        return expr
    # This will come only when Expr args invoke them
    # Inversion ,projection rejection,rotation,dilation etc will not appear here
    elif(type(expr)==A):
      for i, arg in enumerate(expr.args):
        if isinstance(arg, gadd):
          first, b, tail = expr.args[:i], expr.args[i], expr.args[i+1:]
          tmplst = [A(*(first + (bx,) + tail)) for bx in b.args]
          t =  gadd(*tmplst)
          # CHANGED HERE
          if(t.mv==GExpr.nl):
            return t.coeff
          else:
            return t.mv
      return expr
    else :
      return expr

  return distribute_rl


def distriOvr_Add(expr):
  if isinstance(expr,Mul):
    for i, arg in enumerate(expr.args):
      if isinstance(arg, Add):
        first, b, tail = expr.args[:i], expr.args[i], expr.args[i+1:]
        tmplst = [Mul(*(first + (bx,) + tail)) for bx in b.args]
        t =  Add(*tmplst)
        # CHANGED HERE
        return t
    return expr
  else:
    return expr

    

gextpDist = distriOvr_GAdd(gextp)
gmulDist = distriOvr_GAdd(gmul)
glcntrctDist = distriOvr_GAdd(glcntrct)
grcntrctDist = distriOvr_GAdd(grcntrct)
gextpDist = distriOvr_GAdd(inversion)
gmulDist = distriOvr_GAdd(projection)
glcntrctDist = distriOvr_GAdd(rejection)
grcntrctDist = distriOvr_GAdd(grcntrct)
# for binops different expansion will work

canonicalize11 = (bottom_up_once(gextpDist))
canonicalize12 = exhaust(bottom_up_once(do_one(gextpDist,gmulDist,glcntrctDist,grcntrctDist,distriOvr_Add)))



def gaddexpand():
  GExpr.gdistribute = canonicalize12
