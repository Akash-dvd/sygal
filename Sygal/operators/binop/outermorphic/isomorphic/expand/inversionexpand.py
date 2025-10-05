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



def inversion_expand(expr:"Box")->Optional[Box]:
  if (type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == inversion:
      sub = BX.mv.down
      obj = BX.mv.up
      #  But while creating this was checked
      if(type(sub) in [gmul,gextp]):  
        if is_nzScalarPair(sub,sub.reversion()):
          t = expand_iter(gmul)((sub*(sub.reversion())))
          if t.mv == GExpr.nl:
            coeff = Pow(t.coeff,-1)
            return (sub.reversion())*obj*sub*coeff
          else :
            raise ValueError("Couldn't reduce coeff to scalar")
        else :
          raise ValueError("INV with null base")
      elif type(sub) == projection:
        subu = sub.up
        subd = sub.down
        if subu == obj and is_nzScalarPair(subd,subd.reversion()):
          coeff = Pow((subd<(subd.reversion())),-1)
          return (subd.reversion())*obj*subd*coeff
        else :
          return expr
      elif (sub.grade=={1}):
        coeff = Pow((sub<sub),-1)
        return sub*obj*sub*coeff*cf
      else :
        return expr
    else :
      return expr
  else :
    return expr
def inversionexpand():
  inversion.gexpand = inversion_expand

