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

from libs.Sygal.operators.binop.outermorphic.isomorphic.transforms.transforms import transforms
from libs.Sygal.operators.binop.outermorphic.isomorphic.transforms.dilation import dilation
from libs.Sygal.operators.binop.outermorphic.isomorphic.transforms.rotation import rotation
from libs.Sygal.operators.binop.outermorphic.isomorphic.transforms.translation import translation




def distriOvr_GAdd(expr):
  if (type(expr)==Box):
    BX = expr
    cf = BX.coeff
    # if type(BX.mv)==A:
    if(issubclass(type(BX.mv),GExpr) and not BX.mv.is_atom):
      for i, arg in enumerate(BX.mv.args):
        # Case for inversion, rotation dilation translation etc
        if((issubclass(type(BX.mv),inversion) or type(BX.mv) == projection) and i==0):
          continue
        elif (type(BX.mv) == rejection and i==1):
          continue
        else:
          if isinstance(arg, gadd):
            first, b, tail = BX.mv.args[:i], BX.mv.args[i], BX.mv.args[i+1:]
            tmplst = [type(BX.mv)(*(first + (bx,) + tail))*cf for bx in b.args]
            t =  gadd(*tmplst)
            return t
      return expr
    else:
      return expr
  # This will come only when Expr args invoke them
  # Inversion ,projection rejection,rotation,dilation etc will not appear here

  # THey can appear there
  # Like aINVb1+b2<cINVd1+d2
  # ###############
  elif(issubclass(type(expr),GExpr) and not expr.is_atom):
    for i, arg in enumerate(expr.args):
      if isinstance(arg, gadd):
        first, b, tail = expr.args[:i], expr.args[i], expr.args[i+1:]
        tmplst = [type(expr)(*(first + (bx,) + tail)) for bx in b.args]
        t =  gadd(*tmplst)
        # CHANGED HERE
        if(t.mv==GExpr.nl):
          return t.coeff
        else:
          return t.mv
    return expr
  else :
    return expr




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

    
canonicalize = exhaust(bottom_up_once(do_one(distriOvr_GAdd,distriOvr_Add)))


def gaddexpand():
  GExpr.gdistribute = canonicalize
  gadd.gexpand = canonicalize
