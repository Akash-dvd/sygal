from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union


from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,
  symbols, sqrt, Matrix,srepr,AtomicExpr
)

from libs.Sygal.GExpr import GExpr
from libs.Sygal.Box import Box
from sympy.core.cache import cacheit


class GB(GExpr,AtomicExpr):

  def __new__(cls, args0:str,args1:Union[int,List[int],Tuple[int]],args2:GExpr=lambda x:GExpr.I13,args3:Expr=S(1), dotdict:Dict={}) -> "Box":
    # args0 = name .args1 = grade set ,args2 gextp, args3 = coeff
    # Put a check on set length
    
    # Much wow
    # It can be placed smwhe else also
    GB.preprocess()

    # null grade zero element is unique
    if(args1=={0}):
        args0 = "_nl"


    if not isinstance(args0, str):
      raise TypeError("name should be a string, not %s" % repr(type(args0)))
    
    if isinstance(args1,int):
      if(args1<0):
        return GExpr.Znl
      arg_grade = frozenset([args1])
    elif isinstance(args1, list) or isinstance(args1, Tuple):
      filtgrade = [i for i in args1 if i>=0]
      if(len(filtgrade)==0):
        return GExpr.Znl
      arg_grade = frozenset(filtgrade)
    else :
      raise TypeError("grade should be int or list or tuple not %s" % repr(type(args1)))


    # Pattern match for args2,args3
    if not issubclass(type(args2),GExpr):
      raise TypeError("coeff should be a gextp, not %s" % repr(type(args2)))

    if not issubclass(type(args3),Expr) or issubclass(type(args3),GExpr):
      raise TypeError("coeff should be a sympy obj, not %s" % repr(type(args3)))


    nargs = (args0,arg_grade,args2,args3)
    obj = GB.__xnew_cached_(GB, *nargs)
    obj.args[1].dotdict = dotdict
    return obj

  def __new_stage2__(cls, *args) -> "GB":
    # Pattern match for arguements
    # CAn be better with pattern matching
    
    mv = GExpr.__new__(cls)
    mv.name = args[0]
    mv.is_commutative = (args[1]] == {0})
    mv.is_atom = True
    mv.grade = args[1]

    obj = Box.__new__(Box,mv,args[2])
    
    return obj

  __xnew__ = staticmethod(
    __new_stage2__)            # never cached (e.g. dummy)
  __xnew_cached_ = staticmethod(
    cacheit(__new_stage2__))   # symbols are always cached

    

  def preprocess():

    if(not GExpr.initialized):
      _o   = GExpr.__new__(GExpr) 
      _oo  = GExpr.__new__(GExpr)
      _x   = GExpr.__new__(GExpr)
      _y   = GExpr.__new__(GExpr)
      _rx  = GExpr.__new__(GExpr)
      _x1  = GExpr.__new__(GExpr)
      _x2  = GExpr.__new__(GExpr)
      _x3  = GExpr.__new__(GExpr)
      _x4  = GExpr.__new__(GExpr)
      _x5  = GExpr.__new__(GExpr)
      _x6  = GExpr.__new__(GExpr)
      _x7  = GExpr.__new__(GExpr)
      _x8  = GExpr.__new__(GExpr)

      names = ['_o','_oo','_x','_y','_rx','_x1','_x2','_x3','_x4','_x5','_x6','_x7','_x8']

      lst = [_o,_oo,_x,_y,_rx,_x1,_x2,_x3,_x4,_x5,_x6,_x7,_x8]

      rel_dot = [[_o,_oo,S(-1)],[_oo,_o,S(-1)],[_x,_x,S(1)],[_y,_y,S(1)],[_rx,_rx,S(-1)],[_x1,_x1,S(1)],[_x2,_x2,S(1)],[_x3,_x3,S(1)],[_x4,_x4,S(1)],[_x5,_x5,S(1)],[_x6,_x6,S(1)],[_x7,_x7,S(1)],[_x8,_x8,S(1)]]
      
      dotdict = {}
      tmpdict = {}
      
      for ele in lst:
        tmpdict[ele] = S(0)
      for ele in lst:
        dotdict[ele] = tmpdict

      for ele1,ele2,ele3 in rel_dot:
        dotdict[ele1][ele2] = ele3
      
      prim = []
      for i,mv in enumerate(lst):
        args0 = lst[i]
        args1 = frozenset([1])
        args2 = lambda args0:x
        args3 = S(1)
        nargs = (args0,args1,args2,args3)
        obj = GB.__xnew_cached_(GB, *nargs)
        obj.args[1].dotdict = dotdict
        
        prim.append(obj)


      GExpr.prim = prim

      GExpr.I3 = _x^_y^_oo
      GExpr.I41 = _o^_x^_y^_oo
      GExpr.I42 = _x^_y^_rx^_oo
      GExpr.I5 = _o^_x^_y^_rx^_oo

      GExpr.I8 = _x1^_x2^_x3^_x4^_x5^_x6^_x7^_x8
      GExpr.I13 = GExpr.I5^GExpr.I8
      GExpr.initialized = True 
