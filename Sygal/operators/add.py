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

class add(GExpr, AssocOp):
    pass
