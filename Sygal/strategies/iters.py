from libs.Sygal.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from libs.Sygal.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from libs.Sygal.strategies.tools import subs, typed ,canon
from libs.Sygal.strategies.traverse import (top_down, bottom_up, bxsall, top_down_once,bottom_up_once,spe_traverse,gen_traverse)
from libs.Sygal.strategies.tree import treeapply, greedy, allresults, brute

def key1():
  from libs.Sygal.Box import Box
  from libs.Sygal.operators.assop.gadd import gadd
  from libs.Sygal.operators.assop.gextp import gextp
  from libs.Sygal.operators.assop.gmul import gmul

  from libs.Sygal.operators.binop.ganticomm import ganticomm
  from libs.Sygal.operators.binop.gcomm import gcomm
  from libs.Sygal.operators.binop.sclrprdct import sclrprdct
  from libs.Sygal.operators.binop.grcntrct import grcntrct
  from libs.Sygal.operators.binop.glcntrct import glcntrct

  from libs.Sygal.operators.binop.outermorphic.outermorphic import outermorphic
  from libs.Sygal.operators.binop.outermorphic.projection import projection
  from libs.Sygal.operators.binop.outermorphic.rejection import rejection
  
  from libs.Sygal.operators.binop.outermorphic.isomorphic.isomorphic import isomorphic
  from libs.Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion

  from libs.Sygal.operators.binop.outermorphic.isomorphic.transforms.transforms import transforms
  from libs.Sygal.operators.binop.outermorphic.isomorphic.transforms.dilation import dilation
  from libs.Sygal.operators.binop.outermorphic.isomorphic.transforms.rotation import rotation
  from libs.Sygal.operators.binop.outermorphic.isomorphic.transforms.translation import translation


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

def invoker_simplify(op):
  def simplifier(expr):
    return op.gsimplify(expr)
  return simplifier

def invoker_higher(op):
  def highier(expr):
    return op.ghigher(expr)
  return highier

def higher_iter(op,flag = gen_traverse):  
  return exhaust(bottom_up(bx_typed({op: invoker_higher(op)}),flag))

def simplify_iter(op,flag = gen_traverse):  
  return exhaust(bottom_up(bx_typed({op: invoker_simplify(op)}),flag))

def expand_iter(op,flag = gen_traverse):  
  return exhaust(bottom_up(bx_typed({op: invoker_expand(op)}),flag))
