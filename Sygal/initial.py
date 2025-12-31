# Use new clean import modules
from Sygal.imports.core import GAtom, GExpr, Box
from Sygal.imports.sympy_basic import (
  Basic, diff, Rational, Symbol, S, Mul, Add, Expr, Pow,
  expand, simplify, eye, trigsimp, cos, sin, subsets,
  symbols, sqrt, Matrix, SympifyError, sympify
)
from Sygal.imports.typing_helpers import reduce, Iterable, defaultdict
from Sygal.imports.strategies import (
  rm_id, glom, flatten, unpack, sort, distribute, subs, rebuild,
  null_safe, exhaust, memoize, condition, chain, tryit, do_one, debug, switch, minimize,
  typed, canon,
  top_down, bottom_up, bxsall, top_down_once, bottom_up_once, spe_traverse, gen_traverse,
  treeapply, greedy, allresults, brute,
  higher_iter, canon_iter, expand_iter, bx_typed
)
from Sygal.imports.utils import (
  kbin_distri, parity, GSortArgs, rlGSortArgs, bx_sift,
  is_unMixedGrade, is_primitive, is_pSC, is_uniGraded,
  is_vecPerpendicularPair, is_perpendicularPair, is_vecnull, is_null,
  is_nzScalarPair, is_scalarPair, is_blade, is_vecBlade, is_versor, get_grade
)
from Sygal.imports.psc import grd, spcdct, spclst
# Operators import moved after _preprocess() to avoid circular dependency
# from Sygal.imports.operators import (
#   gadd, gextp, gmul,
#   ganticomm, gcomm, sclrprdct, grcntrct, glcntrct,
#   projection, rejection, outermorphic,
#   inversion, isomorphic,
#   transforms, dilation, rotation, translation
# )

i = sqrt(-1)
(X,X1,Y,Y1,X2,Y2,Z) = symbols('x x1 y y1 x2 y2 z')

(psi,psi1,psi2,psi3,psi4) = symbols('psi psi_1 psi_2 psi_3 psi_4', real=True)
(th,th1,th2,th3,th4) = symbols('theta theta_1 theta_2 theta_3 theta_4', positive=True)
(ph,ph1,ph2,ph3,ph4) = symbols('phi phi_1 phi_2 phi_3 phi_4', real=True)
(lam,lam1,lam2,lam3,lam4) = symbols('lambda lambda_1 lambda_2 lambda_3 lambda_4', real=True)

(g,g1,g2,g3,g4) = symbols('g g1 g2 g3 g4', real=True)
(h,h1,h2,h3,h4) = symbols('h h1 h2 h3 h4', real=True)
(k,k1,k2,k3,k4) = symbols('k k1 k2 k3 k4', real=True)

(t,t1,t2,t3,t4) = symbols('t t1 t2 t3 t4', real=True)
(r,r1,r2,r3,r4) = symbols('r r1 r2 r3 r4', positive=True)

(al,al1,al2,al3,al4) = symbols('alpha alpha_1 alpha_2 alpha_3 alpha_4', real=True)
(bt,bt1,bt2,bt3,bt4) = symbols('beta beta_1 beta_2 beta_3 beta_4', real=True)

(a,b,c,d,e,f) = symbols('a b c d e f', real=True)
(a1,b1,c1,d1,e1,f1) = symbols('a_1 b_1 c_1 d_1 e_1 f_1', real=True)
(a2,b2,c2,d2,e2,f2) = symbols('a_2 b_2 c_2 d_2 e_2 f_2', real=True)
(a3,b3,c3,d3,e3,f3) = symbols('a_3 b_3 c_3 d_3 e_3 f_3', real=True)

(A,B,C,D,E,F) = symbols('A B C D E F', commutative=False)
(B1,B2,B3,B4,B5,B6) = symbols('B1 B2 B3 B4 B5 B6', commutative=False)

# relDt removed - no longer required

# Initialize GExpr after all imports are complete to avoid circular imports
# This MUST be called before using GExpr.I13, GExpr.primbx, GExpr._rx, etc.
if not GExpr.initialized:
  from Sygal.GAtom import GAtom
  GAtom._preprocess()

# Now define mtDt after _preprocess() has created GExpr.I13
# mtDt = {GExpr.I41:1}
mtDt = {GExpr.I13:1}
# GExpr.I13

a1 = GAtom("a1",mtDt)
a2 = GAtom("a2",mtDt)
a3 = GAtom("a3",mtDt)
a4 = GAtom("a4",mtDt)
b1 = GAtom("b1",mtDt)
b2 = GAtom("b2",mtDt)
b3 = GAtom("b3",mtDt)
b4 = GAtom("b4",mtDt)
c1 = GAtom("c1",mtDt)
c2 = GAtom("c2",mtDt)
c3 = GAtom("c3",mtDt)
c4 = GAtom("c4",mtDt)
d1 = GAtom("d1",mtDt)
d2 = GAtom("d2",mtDt)
d3 = GAtom("d3",mtDt)
d4 = GAtom("d4",mtDt)

# Now import operators after _preprocess() is complete and all modules are initialized
# This avoids the circular dependency: imports.core -> GAtom -> (no _preprocess) -> operators -> imports.core
from Sygal.imports.operators import (
  gadd, gextp, gmul,
  ganticomm, gcomm, sclrprdct, grcntrct, glcntrct,
  projection, rejection, outermorphic,
  inversion, isomorphic,
  transforms, dilation, rotation, translation
)

# Note: primbx, _rx, _oo are no longer available in simplified system
# These may need to be recreated if still needed
o = None
rx = None
oo = None

na1 = GAtom("na1",mtDt)
na2 = GAtom("na2",mtDt)
na3 = GAtom("na3",mtDt)
nb1 = GAtom("nb1",mtDt)
nb2 = GAtom("nb2",mtDt)
nb3 = GAtom("nb3",mtDt)
nc1 = GAtom("nc1",mtDt)
nc2 = GAtom("nc2",mtDt)
nc3 = GAtom("nc3",mtDt)
nd1 = GAtom("nd1",mtDt)
nd2 = GAtom("nd2",mtDt)
nd3 = GAtom("nd3",mtDt)

mtDt1 = {GExpr.I41:1}

A1 = GAtom("A1",mtDt1)
A2 = GAtom("A2",mtDt1)
A3 = GAtom("A3",mtDt1)
A4 = GAtom("A4",mtDt1)
B1 = GAtom("B1",mtDt1)
B2 = GAtom("B2",mtDt1)
B3 = GAtom("B3",mtDt1)
B4 = GAtom("B4",mtDt1)
C1 = GAtom("C1",mtDt1)
C2 = GAtom("C2",mtDt1)
C3 = GAtom("C3",mtDt1)
C4 = GAtom("C4",mtDt1)
D1 = GAtom("D1",mtDt1)
D2 = GAtom("D2",mtDt1)
D3 = GAtom("D3",mtDt1)
D4 = GAtom("D4",mtDt1)