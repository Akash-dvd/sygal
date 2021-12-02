from sympy import (
  Basic,diff, Rational, Symbol, S, Mul, Add, Expr,Pow,
  expand, simplify, eye, trigsimp,cos,sin,subsets,
  symbols, sqrt, Matrix, SympifyError, sympify
)

from functools import reduce
from collections import Iterable,defaultdict

from libs.Sygal.strategies.rl import (rm_id, glom, flatten, unpack, sort, distribute,subs, rebuild)
from libs.Sygal.strategies.core import (null_safe, exhaust, memoize, condition,chain, tryit, do_one, debug, switch, minimize)
from libs.Sygal.strategies.tools import subs, typed ,canon
from libs.Sygal.strategies.traverse import (top_down, bottom_up, bxsall, top_down_once,bottom_up_once,spe_traverse,gen_traverse)
from libs.Sygal.strategies.tree import treeapply, greedy, allresults, brute
from libs.Sygal.strategies.iters import higher_iter,simplify_iter ,expand_iter,bx_typed

from libs.Sygal.GB import GB,GExpr,Box

from libs.Sygal.operators.assop.gadd import gadd
from libs.Sygal.operators.assop.gextp import gextp
from libs.Sygal.operators.assop.gmul import gmul

from libs.Sygal.operators.binop.ganticomm import ganticomm
from libs.Sygal.operators.binop.gcomm import gcomm
from libs.Sygal.operators.binop.sclrprdct import sclrprdct
from libs.Sygal.operators.binop.grcntrct import grcntrct
from libs.Sygal.operators.binop.glcntrct import glcntrct
from libs.Sygal.operators.binop.sclrprdct import sclrprdct


from libs.Sygal.operators.binop.outermorphic.isomorphic.inversion import inversion
from libs.Sygal.operators.binop.outermorphic.projection import projection
from libs.Sygal.operators.binop.outermorphic.rejection import rejection

from libs.Sygal.operators.binop.outermorphic.outermorphic import outermorphic


from libs.Sygal.operators.binop.outermorphic.isomorphic.isomorphic import isomorphic

from libs.Sygal.imports.import_util2 import *

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


a1 = GB("a1",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
a2 = GB("a2",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
a3 = GB("a3",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
a4 = GB("a4",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
b1 = GB("b1",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
b2 = GB("b2",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
b3 = GB("b3",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
b4 = GB("b4",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
c1 = GB("c1",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
c2 = GB("c2",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
c3 = GB("c3",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
c4 = GB("c4",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
d1 = GB("d1",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
d2 = GB("d2",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
d3 = GB("d3",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
d4 = GB("d4",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1)})
rx = GExpr._rx
oo = GExpr._oo

na1 = GB("na1",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1),'self':S(0)})
na2 = GB("na2",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1),'self':S(0)})
na3 = GB("na3",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1),'self':S(0)})
nb1 = GB("nb1",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1),'self':S(0)})
nb2 = GB("nb2",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1),'self':S(0)})
nb3 = GB("nb3",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1),'self':S(0)})
nc1 = GB("nc1",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1),'self':S(0)})
nc2 = GB("nc2",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1),'self':S(0)})
nc3 = GB("nc3",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1),'self':S(0)})
nd1 = GB("nd1",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1),'self':S(0)})
nd2 = GB("nd2",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1),'self':S(0)})
nd3 = GB("nd3",1,pSC=lambda:GB.I41,dotdict={GB._oo:S(-1),'self':S(0)})

