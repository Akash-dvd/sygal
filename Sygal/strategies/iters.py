from libs.Sygal.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from libs.Sygal.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from libs.Sygal.strategies.tools import subs, typed ,canon
from libs.Sygal.strategies.traverse import (top_down, bottom_up, bxsall, top_down_once,bottom_up_once,spe_traverse,gen_traverse)
from libs.Sygal.strategies.tree import treeapply, greedy, allresults, brute


def bx_typed(ruletypes):
  from libs.Sygal.Box import Box
  return switch(lambda x:type(x.mv) if type(x)==Box else lambda x:None, ruletypes)

def invoker_expand(expr):
  return expr.gexpand()
def invoker_simplify(expr):
  return expr.gsimplify()
def invoker_higher(expr):
  return expr.ghigher()

def higher_iter(op,flag = gen_traverse):  
  return exhaust(bottom_up(bx_typed({op: invoker_higher}),flag))

def simplify_iter(op,flag = gen_traverse):  
  return exhaust(bottom_up(bx_typed({op: invoker_simplify}),flag))

def expand_iter(op,flag = gen_traverse):  
  return exhaust(bottom_up(bx_typed({op: invoker_expand}),flag))
