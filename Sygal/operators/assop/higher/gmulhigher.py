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

# prototype func
def diff_expand(args1,args2):
  # args1*args2 is knows to be of scalar type with maximum expansion
  t = expand_iter(gmul)(args1*args2)
  if t.grade =={0}:
    if type(t.coeff) == Add:
      return sclrprdct.gexpand1(t.coeff)
    else :
      return t.coeff
  else :
    raise ValueError("This expansion needs to be enhanced")

# TODO
# a2*a1*c1*(a1|a2+a1^a2) = INV(a1*a2,c1)
def gmul_2Inv(expr:Expr)->Union[Expr,Box]:
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gmul :
      for i,argi in enumerate(BX.mv.args):
        for argj in BX.mv.args[i+1:]:
          if is_scalarPair(argi,argj):
            # [_,_,argi,_,_,argj,_,_]
            # [t_i,argi,ti_,argj,tj_]
            j = BX.mv.args[i+1:].index(argj) + i + 1
            t_i = BX.mv.args[:i]
            ti_ = BX.mv.args[i+1:][:j-i-1]
            tj_ = BX.mv.args[j+1:]
            
            if is_nzScalarPair(argi,argj):
              coeff = diff_expand(argi,argj)*cf
              # Check if the inversion pair are agjacent
              # ti_ will be []
              if ti_:
                t1 = gmul(*ti_)
                t2 = inversion(argj,t1)
                tall = []
                tall.extend(t_i)
                tall.append(t2)
                tall.extend(tj_)
                t3 = gmul(*tall)
                return t3*coeff
              else :
                tall = []
                tall.extend(t_i)
                tall.extend(tj_)
                if tall:
                  t3 = gmul(*tall)
                  return t3*coeff
                else :
                    return GExpr.Onl*coeff
            else :
              # Check if the inversion pair are agjacent
              # ti_ will be []
              if len(ti_) == 1 :
                t1 = expand_iter(gmul)(argi*ti_[0]*argj)
                t2 = expand_iter(sclrprdct)(t1)
                tall = []
                tall.extend(t_i)
                tall.append(t2)
                tall.extend(tj_)
                t3 = gmul(*tall)
                return t3*cf
              elif len(ti_) >1 :
                continue
              else :
                return GExpr.Znl

      return expr
    else :
      return expr
  else :
      return expr

def gmul_2Proj(expr:Expr)->Union[Expr,Box]:
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gmul and (len(BX.mv.args)>=2):
      for i,arg in enumerate(BX.mv.args):
        if type(arg) == glcntrct:
          # Blade invertible should be of single grade
          if is_nzScalarPair(arg.down,(arg.down).reversion()) and is_vecBlade(arg.down):
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
          if is_nzScalarPair(arg.down,(arg.down).reversion()) and is_vecBlade(arg.down):
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


# Limited to scalar subspace
def gmul_2Rej(expr:Expr)->Union[Expr,Box]:
  if(type(expr)==Box):
    BX = expr
    cf = BX.coeff
    if type(BX.mv) == gmul :
      # Treat arg as base and check both sides
      for i,arg in enumerate(BX.mv.args):
        if type(arg) == gextp:
          # these are checked for sub
          _arg = BX.mv.args[i-1] if i!=0 else None
          arg_ = BX.mv.args[i+1] if len(BX.mv.args)>(i+1) else None
          if is_vecBlade(_arg):
            if type(_arg) == gextp:
              if reduce(lambda x,y:x and y ,[ele in arg.args for ele in _arg.args]):
                lst = list(_arg.args)
                lst.extend([ele for ele in arg.args if ele not in _arg.args])
                sign = parity(lst,arg.args)

                obj = [ele for ele in arg.args if ele not in _arg.args]
                ti = rejection(_arg,gextp(*obj))*(_arg<_arg)
                t_i = BX.mv.args[:i-1]
                ti_ = BX.mv.args[i+1:]
                tall = []
                tall.extend(t_i)
                tall.append(ti)
                tall.extend(ti_)

                return gmul(*tall)*cf*sign
            # grade 1
            else:
              if _arg in arg.args:
                lst = [_arg]
                lst.extend([ele for ele in arg.args if ele != _arg])
                sign = parity(lst,arg.args)
            
                obj = [ele for ele in arg.args if ele!=_arg]
                ti = rejection(_arg,gextp(*obj))*(_arg<_arg)
                t_i = BX.mv.args[:i-1]
                ti_ = BX.mv.args[i+1:]
                tall = []
                tall.extend(t_i)
                tall.append(ti)
                tall.extend(ti_)
                
                return gmul(*tall)*cf*sign

          elif is_vecBlade(arg_):
            if type(arg_) == gextp:
              if reduce(lambda x,y:x and y ,[ele in arg.args for ele in arg_.args]):
                lst = [ele for ele in arg.args if ele not in arg_.args]
                lst.extend(arg_.args)
                sign = parity(lst,arg.args)

                obj = [ele for ele in arg.args if ele not in arg_.args]
                ti = rejection(arg_,gextp(*obj))*(arg_<arg_)
                t_i = BX.mv.args[:i]
                ti_ = BX.mv.args[i+2:]
                tall = []
                tall.extend(t_i)
                tall.append(ti)
                tall.extend(ti_)
                
                return gmul(*tall)*cf*sign
            # grade 1
            else:
              if arg_ in arg.args:
                lst = [ele for ele in arg.args if ele != arg_]
                lst.append(arg_)
                sign = parity(lst,arg.args)

                obj = [ele for ele in arg.args if ele!=arg_]
                ti = rejection(arg_,gextp(*obj))*(arg_<arg_)
                t_i = BX.mv.args[:i]
                ti_ = BX.mv.args[i+2:]
                tall = []
                tall.extend(t_i)
                tall.append(ti)
                tall.extend(ti_)
                
                return gmul(*tall)*cf*sign
          else:
            continue
      return expr
    
    else :
      return expr
  else :
    return expr

def gmulhigher():
  gmul.ghigher = exhaust(do_one(gmul_2Inv,gmul_2Proj,gmul_2Rej))