from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union


from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,sympify,
  symbols, sqrt, Matrix,srepr,AtomicExpr
)

from libs.Sygal.GExpr import GExpr
from libs.Sygal.Box import Box
from sympy.core.cache import cacheit


class GB(GExpr,AtomicExpr):

  def __new__(cls, name:str,grade:Union[int,List[int],Tuple[int]],pSC:Box=lambda :GExpr.I13,coeff:Expr=S(1), dotdict:Dict={}) -> "Box":
    # name = name:str 
    # grade = grade:Union[int,List[int]]
    # pSC = pseudoscalar:Union[callable,gextp]
    # coeff = coeff:GExpr
    
    # Pattern match for name -> str
    if not isinstance(name, str):
      raise TypeError("name should be a string, not %s" % repr(type(name)))
    elif name.startswith('_'):
      raise TypeError("name should not start with  _")


    # Pattern match for grade -> grade_1:Frozenset
    if(grade==0):
      # name = "\u03C6"
      name = "\u0950"
      return GExpr.Onl
    elif isinstance(grade,int):
      if(grade<0):
        return GExpr.Znl
      grade_1 = frozenset([grade])
    elif isinstance(grade, list) or isinstance(grade, Tuple):
      filtgrade = [i for i in grade if i>=0]
      if(len(filtgrade)==0):
        return GExpr.Znl
      grade_1 = frozenset(filtgrade)
    else :
      raise TypeError("grade should be int or list or tuple not %s" % repr(type(grade)))


    # Pattern match for pSC
    if(not callable(pSC)):
      pSC_1 = lambda :pSC
    else :
      pSC_1 = pSC

    
    # Pattern match for coeff
    if not issubclass(type(coeff),Expr) or issubclass(type(coeff),GExpr):
      raise TypeError("coeff should be a sympy obj, not %s" % repr(type(coeff)))


    nargs = (name,grade_1,pSC_1,coeff)
    
    bx = GB.__xnew_cached_(GB, *nargs)
    bx.mv.dotdict = dotdict
    
    return bx

  def __new_stage2__(cls, name,grade,pSC,coeff) -> Box:
    
    # name = name:str 
    # grade = grade:frozenset
    # pSC = pseudoscalar:Union[callable,gextp]
    # coeff = coeff:GExpr
    
    # Pattern match for arguements
    # CAn be better with pattern matching
    
    mv = GExpr.__new__(cls,name,grade,pSC)
    mv.is_commutative = (grade == {0})
    mv.is_atom = True

    obj = Box.__new__(Box,mv,coeff)    
    return obj


  def __str__(self):
    return "\033[1;37;40m"+self.args[0]+"\033[0;37;40m"

  def __repr__(self):
    return self.args[0]

  def __hash__(self):
    return hash(self.name)

  def __eq__(self, other):
    return (
      (type(other) == type(self))  and
      self.__hash__() == other.__hash__()
      # Check if hash is not present in the object
    )

  @property
  def name(self):
    return self.args[0]

  @property
  def grade(self):
    return self.args[1]

  @property
  def pSC(self):
    return self.args[2]

  def _preprocHelper(cls,name,grade,pSC,coeff):
    # For initialization
    # Box.__new__ cannot be called b4 initialization
    mv = GExpr.__new__(cls,name,grade,pSC)
    mv.is_commutative = (grade == {0})
    mv.is_atom = True

    return Basic.__new__(Box,mv,coeff)



  def _preprocess():
    if GExpr.initialized:
      raise ValueError
    else:
      #######################
    

      GExpr.Onl = GB.__new_helper(GB,"\u0950",frozenset({0}),lambda :GExpr.Onl,S(1)) 

      # GExpr.Onl = GB.__new_helper(GB,"\u03C6",frozenset({0}),lambda :GExpr.Onl,S(1)) 

      # To make sure Both Znl and Onl share same _nl
      GExpr.Znl = Basic.__new__(Box,GExpr.Onl.mv,S(0)) 

      GExpr.nl = GExpr.Znl.mv

      #######################

      names = ['_o','_x','_y','_rx','_oo','_x1','_x2','_x3','_x4','_x5','_x6','_x7','_x8']
      
      prim = []
      for i,name in enumerate(names):
        name = name
        grade = frozenset({1})
        pSC = lambda i:GExpr.prim[i]
        coeff = S(1)
        nargs = (name,grade,pSC,coeff)
        bx = GB.__xnew_cached_(GB, *nargs)      
        prim.append(bx)

      #######################
      _o  = prim[0]
      _x  = prim[1]
      _y  = prim[2]
      _rx = prim[3]
      _oo = prim[4]
      _x1 = prim[5]
      _x2 = prim[6]
      _x3 = prim[7]
      _x4 = prim[8]
      _x5 = prim[9]
      _x6 = prim[10]
      _x7 = prim[11]
      _x8 = prim[12]
      
      rel_dot = [[_o,_oo,S(-1)],[_x,_x,S(1)],[_y,_y,S(1)],[_rx,_rx,S(-1)],[_oo,_o,S(-1)],[_x1,_x1,S(1)],[_x2,_x2,S(1)],[_x3,_x3,S(1)],[_x4,_x4,S(1)],[_x5,_x5,S(1)],[_x6,_x6,S(1)],[_x7,_x7,S(1)],[_x8,_x8,S(1)]]
      
      # p1 = GExpr.Znl
      # m1 = -1*GExpr.Znl
      
      # rel_dot = [[_o,_oo,m1],[_x,_x,p1],[_y,_y,p1],_rx,_rx,m1],[_oo,_o,m1],[_x1,_x1,p1],_x2,_x2,p1],[_x3,_x3,p1],[_x4,_x4,p1],[_x5,_x5,p1],[_x6,_x6,p1],[_x7,_x7,p1],[_x8,_x8,p1]]

      accu_dotdict = {}
      tmpdict = {}
      
      for bx in prim:
        tmpdict[bx.mv] = S(0)
      for bx in prim:
        newtmpdict = tmpdict.copy()
        accu_dotdict[bx.mv] = newtmpdict

      for bx1,bx2,ele3 in rel_dot:
        accu_dotdict[bx1.mv][bx2.mv] = ele3
      for bx in prim:
        bx.mv.dotdict = accu_dotdict[bx.mv]

      #######################
          
      GExpr._oo = _oo 
      GExpr._rx = _rx
      
      GExpr.prim = prim

      GExpr.I3 = _x^_y^_oo
      GExpr.I41 = _o^_x^_y^_oo
      GExpr.I42 = _x^_y^_rx^_oo
      GExpr.I5 = _o^_x^_y^_rx^_oo

      GExpr.I8 = _x1^_x2^_x3^_x4^_x5^_x6^_x7^_x8
      GExpr.I13 = GExpr.I5^GExpr.I8
      GExpr.initialized = True 
  
  __xnew__ = staticmethod(
    __new_stage2__)            # never cached (e.g. dummy)
  __xnew_cached_ = staticmethod(
    cacheit(__new_stage2__))   # symbols are always cached
  __new_helper = staticmethod(
    cacheit(_preprocHelper))   # cached symbols for preproc 

GB._preprocess()