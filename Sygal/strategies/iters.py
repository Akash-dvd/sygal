from Sygal.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from Sygal.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from Sygal.strategies.tools import subs, typed ,canon
from Sygal.strategies.traverse import (top_down, bottom_up, bxsall, top_down_once,bottom_up_once,spe_traverse,gen_traverse)
from Sygal.strategies.tree import treeapply, greedy, allresults, brute

def key1():
  from Sygal.Box import Box
  from Sygal.operators.assop.gadd import gadd
  from Sygal.operators.assop.gextp import gextp
  from Sygal.operators.assop.gmul import gmul

  from Sygal.operators.binop.ganticomm import ganticomm
  from Sygal.operators.binop.gcomm import gcomm
  from Sygal.operators.binop.sclrprdct import sclrprdct
  from Sygal.operators.binop.grcntrct import grcntrct
  from Sygal.operators.binop.glcntrct import glcntrct

  from Sygal.operators.binop.outermorphic.outermorphic import outermorphic
  from Sygal.operators.binop.outermorphic.projection import projection
  from Sygal.operators.binop.outermorphic.rejection import rejection
  
  from Sygal.operators.binop.outermorphic.isomorphic.isomorphic import isomorphic
  from Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion

  from Sygal.operators.binop.outermorphic.isomorphic.transforms.transforms import transforms
  from Sygal.operators.binop.outermorphic.isomorphic.transforms.dilation import dilation
  from Sygal.operators.binop.outermorphic.isomorphic.transforms.rotation import rotation
  from Sygal.operators.binop.outermorphic.isomorphic.transforms.translation import translation


  def key(x):
    # This can be modified a lot
    if type(x) == Box:
      yield type(x.mv)
      if issubclass(type(x.mv),outermorphic):
        # lst = [projection,rejection,inversion,dilation,rotation,translation]
        yield outermorphic
      if issubclass(type(x.mv),isomorphic):
        # lst = [inversion,dilation,rotation,translation]
        yield isomorphic
      if issubclass(type(x.mv),transforms):
        # lst = [dilation,rotation,translation]
        yield transforms
    elif type(x) == sclrprdct:
      yield sclrprdct
    else :
      yield None
  return key

def mul_switch(keys, ruledict):
  def switch_rl(expr):
    lst_expr = keys(expr)
    for ele in lst_expr:
      rl = ruledict.get(ele, lambda x:x)
      expr = rl(expr)
    return expr
  return switch_rl

def bx_typed(ruletypes):
  # return mul_switch(key1(), ruletypes)
  return mul_switch(key1(), ruletypes)

def invoker_expand(op):
  def expander(expr):
    return op.gexpand(expr)
  return expander

def invoker_canon(op):
  def canonicalizer(expr):
    return op.gcanonicalization(expr)
  return canonicalizer

def invoker_higher(op):
  def highier(expr):
    return op.ghigher(expr)
  return highier

def higher_iter(op,flag = gen_traverse):  
  return exhaust(bottom_up(bx_typed({op: invoker_higher(op)}),flag))

def canon_iter(op,flag = gen_traverse):  
  return exhaust(bottom_up(bx_typed({op: invoker_canon(op)}),flag))

def expand_iter(op,flag = gen_traverse):  
  return exhaust(bottom_up(bx_typed({op: invoker_expand(op)}),flag))
