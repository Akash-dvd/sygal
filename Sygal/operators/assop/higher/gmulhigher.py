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



def gmul_2Inv(expr:"gmul")->Optional[GExpr]:
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gmul and (len(BX.mv.args)>=3):
      for i,arg in enumerate(BX.mv.args):
        if arg in BX.mv.args[i+1:] and is_invertible(arg):
          j = BX.mv.args[i+1:].index(arg) + i + 1
          t_i = BX.mv.args[:i]
          ti_ = BX.mv.args[i+1:][:j-i-1]
          tj_ = BX.mv.args[j+1:]
          t1 = gmul(*ti_)
          t2 = inversion(arg,t1)
          tall = []
          tall.extend(t_i)
          tall.append(t2)
          tall.extend(tj_)
          
          coeff = (BX.mv.args[i]<BX.mv.args[i]).coeff
          t3 = gmul(*tall)
          if t3.mv == GExpr.nl:
            return t3.coeff
          else :
            return Box.__new__(Box,t3.mv,coeff)
      return expr
    else :
      return expr
  else :
      return expr

def gmul_2Proj(expr:"gmul")->Optional[GExpr]:
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gmul and (len(BX.mv.args)>=2):
      for i,arg in enumerate(BX.mv.args):
        if type(arg) == glcntrct:
          # Blade invertible should be of single grade
          if is_invertible(arg.down) and is_blade(arg.down):
            # This pattern matching for preceding and ahead arguement will check only one indexed element
            # Either leaf or gextp will be present
            _arg = BX.mv.args[i-1] if i!=0 else None
            arg_ = BX.mv.args[i+1] if len(BX.mv.args)>(i+1) else None
            
            if _arg == arg.down and arg_ == arg.down:
              raise ValueError("Inversion Should have caught it.")
            elif _arg == arg.down :
              ti = projection(arg.down,arg.up)*(arg.down<arg.down)
              t_i = BX.mv.args[:i-1]
              ti_ = BX.mv.args[i+1:]
              tall = []
              tall.extend(t_i)
              tall.append(ti)
              tall.extend(ti_)
              sign1 = (next(iter(BX.mv.args[i].grade)))%2
              sign2 = (next(iter(BX.mv.args[i-1].grade))-1)%2
              sign = S(-2)*(sign1*sign2)+1
              t3 = gmul(*tall)*cf*sign
              return Box.__new__(Box,t3)
            elif arg_ == arg.down:
              ti = projection(arg.down,arg.up)*(arg.down<arg.down)
              t_i = BX.mv.args[:i]
              ti_ = BX.mv.args[i+2:]
              tall = []
              tall.extend(t_i)
              tall.append(ti)
              tall.extend(ti_)
              sign = S(1)
              t3 = gmul(*tall)*cf*sign
              return Box.__new__(Box,t3)
            else :
              pass

        elif type(arg) == grcntrct:
          if is_invertible(arg.down) and is_blade(arg.down):
            _arg = BX.mv.args[i-1] if i!=0 else None
            arg_ = BX.mv.args[i+1] if len(BX.mv.args)>(i+1) else None
            
            if _arg == arg.down and arg_ == arg.down:
              raise ValueError("Inversion Should have caught it.")
            elif _arg == arg.down :
              ti = projection(arg.down,arg.up)*(arg.down<arg.down)
              t_i = BX.mv.args[:i-1]
              ti_ = BX.mv.args[i+1:]
              tall = []
              tall.extend(t_i)
              tall.append(ti)
              tall.extend(ti_)
              sign = S(1)
              t3 = gmul(*tall)*cf*sign
              return Box.__new__(Box,t3)
            elif arg_ == arg.down:
              ti = projection(arg.down,arg.up)*(arg.down<arg.down)
              t_i = BX.mv.args[:i]
              ti_ = BX.mv.args[i+2:]
              tall = []
              tall.extend(t_i)
              tall.append(ti)
              tall.extend(ti_)
              sign1 = (next(iter(BX.mv.args[i].up.grade)))%2
              sign2 = (next(iter(BX.mv.args[i+1].grade))-1)%2
              sign = S(-2)*(sign1*sign2)+1
              t3 = gmul(*tall)*cf*sign
              return Box.__new__(Box,t3)
            else :
              pass
      else :
        return expr
    else :
      return expr
  else :
    return expr

def gmul_2Rej(expr:"gmul")->Optional[GExpr]:
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gmul and (len(BX.mv.args)>=2):
      for i,arg in enumerate(BX.mv.args):
        if type(arg) == gextp:
          if is_invertible(arg) and is_blade(arg):
            _arg = BX.mv.args[i-1] if i!=0 else None
            arg_ = BX.mv.args[i+1] if len(BX.mv.args)>(i+1) else None
            
            if _arg in arg.args and arg_ in arg.args:
              raise ValueError("Inversion Should have caught it.")
            elif _arg in arg.args :
              obj = [ele for ele in arg.args if ele!=_arg]
              ti = rejection(_arg,gextp(*obj))*(_arg<_arg)
              t_i = BX.mv.args[:i-1]
              ti_ = BX.mv.args[i+1:]
              tall = []
              tall.extend(t_i)
              tall.append(ti)
              tall.extend(ti_)

              lst = [_arg]
              lst.extend(arg.args)
              ind = arg.args.index(_arg)
              del lst[ind+1]
              sign = parity(lst,arg.args)
              
              t3 = gmul(*tall)*cf*sign
              return Box.__new__(Box,t3)            
            elif arg_ in arg.args:
              obj = [ele for ele in arg.args if ele!=arg_]
              ti = rejection(arg_,gextp(*obj))*(arg_<arg_)
              t_i = BX.mv.args[:i]
              ti_ = BX.mv.args[i+2:]
              tall = []
              tall.extend(t_i)
              tall.append(ti)
              tall.extend(ti_)
              
              lst = list(arg.args)
              ind = arg.args.index(arg_)
              del lst[ind]
              lst.append(arg_)
              sign = parity(lst,arg.args)

              t3 = gmul(*tall)*cf*sign
              return Box.__new__(Box,t3)
            else :
              pass
      else :
        return expr
    else :
      return expr
  else :
    return expr

def gmulhigher():
  gmul.ghigher = exhaust(do_one(gmul_2Inv,gmul_2Proj,gmul_2Rej))