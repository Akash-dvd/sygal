from collections import defaultdict
from functools import cmp_to_key
import operator

from sympy.core.sympify import sympify
from sympy.core.basic import Basic
from sympy.core.singleton import S
from sympy.core.operations import AssocOp
from sympy.core.cache import cacheit
from sympy.core.logic import fuzzy_not, _fuzzy_group, fuzzy_and
from sympy.core.compatibility import reduce
from sympy.core.expr import Expr
from sympy.core.parameters import global_parameters

from libs.Sygal.GExpr import GExpr

from sympy.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from sympy.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from sympy.strategies.tools import subs, typed ,canon
from sympy.strategies.traverse import (top_down, bottom_up, sall, top_down_once,bottom_up_once, basic_fns)
from sympy.strategies.tree import treeapply, greedy, allresults, brute


class extp(GExpr):

  identity = S(1)

  def __new__(cls, *args,**kwargs):
    if not args:
      return cls.identity

    # This must be removed aggressively in the constructor to avoid
    # TypeErrors from GenericZeroMatrix().shape
    args = filter(lambda i: cls.identity != i, args)
    args = list(map(sympify, args))
    
    if ((len(args)-len(set(args))) == 0):  
      args = cls.sort_seq(args)
    else :
      args = [S(0)]

    obj = Basic.__new__(cls, *args)

    check = kwargs.get('check', False)
    if check:
      # Use this for pseudoscalar checks
      pass
      
      # if all(not isinstance(i, MatrixExpr) for i in args):
      #   return Add.fromiter(args)
      # validate(*args)


    if all(not isinstance(i, GExpr) for i in args):
      pass
      # append to appendage for grade 0


    obj = canonicalize(obj)

    return obj


  @property
  def grade(self):
    return sum([nullsafe((lambda x:x)(x)) for x in self.args])

  
  @classmethod
  def sort_seq(cls,seq):

    seq0 = [elem for elem in seq if not isinstance(elem,GExpr) and isinstance(elem,Expr)]

    seq1 = [elem for elem in seq if isinstance(elem,GExpr) and elem.is_atom]

    seq2 = [elem for elem in seq if isinstance(elem,GExpr) and not elem.is_atom]

    newseq1 = sorted(seq1,key=lambda ele: ele.name)
    newseq2 = sorted(seq2,key=lambda ele: ele.__hash__())
    
    seq0.extend(newseq1)
    seq0.extend(newseq2)
    
    return seq0

  def __str__(self):
    ls = self.args
    str = '('
    for o in ls:
      str += o.__str__()+'^'
    str = str[:-1]
    str += ')'
    return str

  __repr__ = __str__

  def __hash__(self):
    h = self._mhash
    if h is None:
      strng = (type(self).__name__)
      for elem in self.args:
        strng += str(elem.__hash__())
      h = hash(strng)
      self._mhash = h
    return h
  
  def __eq__(self, other):
    return (
      self.__class__ == other.__class__ and
      self.__hash__() == other.__hash__()
    )

  def __neg__(self):
    c, args = self.as_coeff_mul()
    c = -c
    if c is not S.One:
      if args[0].is_Number:
        args = list(args)
        if c is S.NegativeOne:
          args[0] = -args[0]
        else:
          args[0] *= c
      else:
        args = (c,) + args
    return self._from_args(args, self.is_commutative)
  


rules = (
  unpack, rm_id(lambda x: x == 1), flatten
  )

canonicalize = exhaust(typed({extp: do_one(*rules)}))

def nullsafe(arg):
  try:
    return arg.grade
  except AttributeError:
    return 0
