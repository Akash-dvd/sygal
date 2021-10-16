from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union


from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,
  expand, simplify, eye, trigsimp,
  symbols, sqrt, Matrix,srepr,AtomicExpr
)


from libs.Sygal.GB import GB
from sympy.core.cache import cacheit




# class gv(GExpr,AtomicExpr):

#   grade = {1}
#   is_atom = True

#   def __new__(cls, name:str, **assumptions) -> "gv":  
#     return gv.__xnew_cached_(cls, name, **assumptions)

#   def __new_stage2__(cls, name:str, **assumptions) -> "gv":
#     if not isinstance(name, str):
#       raise TypeError("name should be a string, not %s" % repr(type(name)))

#     obj = GExpr.__new__(cls)
#     obj.name = name

#     return obj

#   __xnew__ = staticmethod(
#     __new_stage2__)            # never cached (e.g. dummy)
#   __xnew_cached_ = staticmethod(
#     cacheit(__new_stage2__))   # symbols are always cached
  
#   def __str__(self):
#     return self.name
#   __repr__ = __str__

#   def __hash__(self):
#     return hash(self.name)

#   def __eq__(self, other):
#     return (
#       (type(other) == type(self))  and
#       self.name == other.name
#     )

class gv(GB):
  def __new__(cls, name:str, **assumptions) -> "gv":
    args = (name,1)
    return GB.__new__(GB,*args)

class GV(gv):
  _o  = gv('_o') 
  _oo = gv('_oo')
  _x  = gv('_x')
  _y  = gv('_y')
  _rx = gv('_rx')

  _I3 = _x^_y^_oo
  _I41 = _o^_x^_y^_oo
  _I42 = _x^_y^_rx^_oo
  _I5 = _o^_x^_y^_rx^_oo

  _x1  = gv('_x1')
  _x2  = gv('_x2')
  _x3  = gv('_x3')
  _x4  = gv('_x4')
  _x5  = gv('_x5')
  _x6  = gv('_x6')
  _x7  = gv('_x7')
  _x8  = gv('_x8')

  _I8 = _x1^_x2^_x3^_x4^_x5^_x6^_x7^_x8
  _I13 = _I5^_I8
