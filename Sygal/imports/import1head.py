import sys

from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union,NewType,Type,Any

from collections import defaultdict
from functools import cmp_to_key, reduce

from itertools import product

from sympy.printing.str import StrPrinter
from collections.abc import Iterable

from sympy.core.sympify import sympify
from sympy.core.basic import Basic
from sympy.core.singleton import S
from sympy.core.operations import AssocOp
from sympy.core.cache import cacheit
from sympy.core.logic import fuzzy_not, _fuzzy_group, fuzzy_and
# from sympy.core.compatibility import reduce
from sympy.core.expr import Expr
from sympy.core.parameters import global_parameters
from sympy.combinatorics.permutations import Permutation

from sympy import (
  diff, Rational, Symbol, S, Mul, Add, Expr,Pow,
  expand, simplify, eye, trigsimp,cos,sin,subsets,
  symbols, sqrt, Matrix, SympifyError, sympify
)

from sympy.utilities.iterables import partitions,multiset_partitions,kbins

from Sygal.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute, subs, rebuild)
from Sygal.strategies.core import (null_safe, exhaust, memoize, condition, chain, tryit, do_one, debug, switch, minimize)
from Sygal.strategies.tools import typed, canon
from Sygal.strategies.traverse import (top_down, bottom_up, bxsall, top_down_once,bottom_up_once,spe_traverse,gen_traverse)
from Sygal.strategies.tree import treeapply, greedy, allresults, brute
from Sygal.strategies.iters import bx_typed,higher_iter,canon_iter ,expand_iter



from Sygal.GExpr import GExpr
from Sygal.pSC.grd import grd
from Sygal.pSC.spcdct import spcdct
from Sygal.pSC.spclst import spclst

from Sygal.utils.util import *

Ngrd = grd(None,None)