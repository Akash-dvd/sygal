# from .importshead import *
from libs.Sygal.imports.import1head import *
from sympy.strategies.util import basic_fns
from libs.Sygal.GExpr import GExpr
from libs.Sygal.Box import Box

"""
USAGE --

ALLOWED    - GMUL, GADD, GLCNTRCT ETC
NOTALLOWED - GEXPR, BOX  
"""

new = Basic.__new__
# TODO add new to arguements

def conjugation(rl1,rl2):
  return chain(rl1,rl2,rl1)


def rlZero(expr:"GExpr",fns=basic_fns) -> "GExpr" :
  op, new, children, leaf = map(fns.get, ('op', 'new', 'children', 'leaf'))
  if leaf(expr):
    return expr
  elif (S(0) in expr.args):
    return S(0)
  else : 
    return expr


def rlGSortArgs(expr:GExpr,reverse:bool=False) -> GExpr:
  """
  Sort Paritioned arguements based on Grades,names
  Complex arguement are put at last sorted by sum of their weights
  """
  newseq = sorted(expr.args,key=lambda ele:(len(ele.grade),next(iter(ele.grade)),ele.name,ele.__hash__()),reverse=reverse)
  return new(expr.__class__, *newseq)


def GSortArgs(seq:Union[list,tuple],reverse:bool=False) -> Union[list,tuple]:
  """
  Sort Paritioned arguements based on Grades,names
  Complex arguement are put at last sorted by sum of their weights
  """

  newseq = sorted(seq,key=lambda ele:(len(ele.grade),next(iter(ele.grade)),ele.name,ele.__hash__()),reverse=reverse)
  return newseq


def parity(args1:List[GExpr],args2:List[GExpr])->S:
  # ASSUMPTIONS
  # both arguements have unmixed grades
  # remove even grades , they are transparent to positional changes
  
  # Reimplement using something from permutation library
  t1 = [i for i in args1 if next(iter(i.grade))%2==1 ]
  d1 = dict()
  t2 = [i for i in args2 if next(iter(i.grade))%2==1 ]
  
  for index, value in enumerate(t1):
    d1[value.__hash__()] = [index]

  for index, value in enumerate(t2):
    d1[value.__hash__()].append(index)
  
  perm = []
  for index, (key, value) in enumerate(d1.items()):
    perm.append(value)
  
  perm1 = sorted(perm,key=lambda ele:ele[1])
  perm2 = [i[0] for i in perm1]

  p = Permutation(perm2)

  return S((p.parity()*-2)+1)


def bx_sift(seqBx:Tuple[Box], keyfunc:Callable, count:Callable)->List[Box]:

  m = defaultdict(lambda:S(0))
  for bx in seqBx:
    m[keyfunc(bx)] = Add(count(bx),m[keyfunc(bx)])
    # m[keyfunc(i)] = m[keyfunc(i)].simplify()
    # m[keyfunc(i)] = m[keyfunc(i)]
  lst = []
  for key, value in m.items():
    lst.append(Box.__new__(Box,key,value))
  return lst


def is_devmode():
  t = 'pydevd' in sys.modules
  return t


def is_unMixedGrade(args:GExpr)->bool:
  t = set()
  t.update((i%2 for i in args.grade))
  return True if len(t)==1 else False


def is_primitive(arg:"Box")->bool:
  if type(arg) == Box:
    return arg in GExpr.primbx
  elif issubclass(type(arg),GExpr):
    bx = Box.__new__(Box,arg)
    return bx in GExpr.primmv
  else :
    return False


def is_pSC(arg:"GExpr")->bool:
  return arg in GExpr.pSC


def is_singleGrade(expr:Union[Expr,GExpr])->bool:
  if issubclass(type(expr),GExpr):
    gd = expr.grade
    return len(gd) == 1
  else:
    return False