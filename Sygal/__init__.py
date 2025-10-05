# from Sygal.operators import assop,gadd,gextp,gmul,binop,ganticomm,gcomm,glcntrct,grcntrct,sclrprdct,outermorphic,projection,rejection,isomorphic,inversion,transforms,translation,rotation,dilation

# from Sygal.pSC import grd,spcdct,spclst

# from Sygal.relDt import relDt

# from Sygal.utils import kbin_distri,parity,GSortArgs,rlGSortArgs,bx_sift,is_unMixedGrade,is_primitive,is_pSC,is_uniGraded,is_vecPerpendicularPair,is_perpendicularPair,is_vecnull,is_null,is_nzScalarPair,is_scalarPair,is_blade,is_vecBlade,is_versor,get_grade

from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,Pow,
  expand, simplify, eye, trigsimp,cos,sin,subsets,
  symbols, sqrt, Matrix, SympifyError, sympify
)

from functools import reduce
from collections.abc import Iterable
from collections import defaultdict

# from Sygal.utils.util import *
from Sygal.utils.util import *


from Sygal.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from Sygal.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from Sygal.strategies.tools import subs, typed ,canon
from Sygal.strategies.traverse import (top_down, bottom_up, bxsall, top_down_once,bottom_up_once,spe_traverse,gen_traverse)
from Sygal.strategies.tree import treeapply, greedy, allresults, brute
from Sygal.strategies.iters import higher_iter,canon_iter ,expand_iter,bx_typed

from Sygal.GAtom import GAtom,GExpr,Box

from Sygal.operators.assop.gadd import gadd
from Sygal.operators.assop.gextp import gextp
from Sygal.operators.assop.gmul import gmul

from Sygal.operators.binop.ganticomm import ganticomm
from Sygal.operators.binop.gcomm import gcomm
from Sygal.operators.binop.sclrprdct import sclrprdct
from Sygal.operators.binop.grcntrct import grcntrct
from Sygal.operators.binop.glcntrct import glcntrct
from Sygal.operators.binop.sclrprdct import sclrprdct


from Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion
from Sygal.operators.binop.outermorphic.projection import projection
from Sygal.operators.binop.outermorphic.rejection import rejection

from Sygal.operators.binop.outermorphic.outermorphic import outermorphic


from Sygal.operators.binop.outermorphic.isomorphic.isomorphic import isomorphic

from Sygal.imports.import_util2 import *


__all__ = [

    'relDt'
]

__all__ = [
  # operators
  'assop','gadd','gextp','gmul',
  
  'binop','ganticomm','gcomm','glcntrct','grcntrct','sclrprdct',
  
  'outermorphic','projection','rejection',
  
  'isomorphic','inversion',

  'transforms','translation','rotation','dilation'


  # pSC
  "grd","spcdct","spclst",

  # relDt

  'relDt',

  # utils
  'kbin_distri','parity','GSortArgs',

  'rlGSortArgs','bx_sift','is_unMixedGrade,is_primitive','is_pSC','is_uniGraded',

  'is_vecPerpendicularPair','is_perpendicularPair','is_vecnull','is_null','is_nzScalarPair','is_scalarPair','is_blade','is_vecBlade','is_versor','get_grade'

    
]







