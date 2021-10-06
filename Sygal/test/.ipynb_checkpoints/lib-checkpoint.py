from sympy import symbols,exp,sin,cos,tan,cot,simplify,expand,factor,cosh,sinh,sqrt,Matrix ,MatrixSymbol,pi,solve,log,Eq,srepr
from galgebra.ga import Ga
from galgebra.printer import Format, Fmt
from IPython.display import Latex
Format()


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




Ga.dual_mode(mode='+I')

e3d = Ga('e_p e_1 e_2 e_3 e_n1 e_n2 en3',g=[1,1,1,1,-1,-1,-1])
(ep,x1,y1,z1,en1,en2,en3) = e3d.mv()

s31d = Ga('zeta_o1 zeta_eo1 zeta_x1 zeta_y1 zeta_z1 zeta_rx zeta_eoo1 zeta_oo1',g=[1,1,1,1,1,1,1,1])
(so1,so,sx1,sy1,sz1,srx1,soo,soo1) = s31d.mv()

s32d = Ga('zeta_o2 zeta_eo2 zeta_x2 zeta_y2 zeta_z2 zeta_rx zeta_eoo2 zeta_oo2',g=[1,1,1,1,1,1,1,1])
(so2,seo2,sx2,sy2,sz2,srx2,seoo2,soo2) = s32d.mv()

fac1 = (x1^y1*-ph/2).exp()*(x1^z1*-th/2).exp()*(x1^y1*-psi/2).exp()
fac2 = (x1^y1*psi/2).exp()*(x1^z1*th/2).exp()*(x1^y1*ph/2).exp()

z2 = fac1*(z1)*fac2
x2 = fac1*(x1)*fac2
y2 = fac1*(y1)*fac2




o  = (-ep+en3)/lam/2
oo = (ep+en3)*lam

o1  = (-z1+en3)/lam1/2
oo1 = (z1+en3)*lam1

o2  = (-z2+en3)/lam2/2
oo2 = (z2+en3)*lam2

I4 = o1^x1^y1^oo1
I5 = o1^x1^y1^en1^oo1


def inversion(sub,obj):
    temp = (sub.inv())*obj*sub
    return(temp)



def projection(sub,obj):
    temp = (obj<sub)<(sub.inv())
    return(temp)

def rejection(sub,obj):
    temp = (obj^sub)>(sub.inv())
    return(temp)

def conjugation(sub,obj):
    temp = sub^(sub<obj)
    return(temp)
    
def union(sub,obj):
    temp =  sub*obj*sub
    return(temp)
    
    
def pinversion(sub,obj):
    sub = sub^oo1
    temp = inversion(sub,obj)
    return(temp)

def p_pinversion(sub,obj):
    sub = (sub^oo1)*I4
    temp = inversion(sub,obj)
    return(temp)

# INVERSION NOT VALID
# RESULT IS USELESS
def linversion(sub,obj):
    opr = ((sub^oo1)*I4/2)
    temp = (opr)*obj*opr
    return(temp)
    
def _trans(sub,obj,opr):
    sub = ((sub^oo1)<<opr)/2
    sub = sub.exp()
    temp = inversion(sub,obj)
    return(temp)

def _itrans(sub,obj,opr):
    opr *= I4
    temp = _trans(sub,obj,opr)
    return(temp)
    
def rotate(sub,obj,opr=1):
#     TESTS : sub|001 != 0
    temp = _itrans(sub,obj,opr)
    return(temp)

def ptranslate(sub,obj,opr=1):
#     TESTS : sub|001 == 0
    temp = _itrans(sub,obj,opr)
    return(temp)

def translate(sub,obj,opr=1):
#     TESTS : sub|001 == 0   
    temp = _trans(sub,obj,opr)
    return(temp)

def dilate(sub,obj,opr=1):
#     TESTS : sub|001 != 0
    temp = _trans(sub,obj,opr)
    return(temp)

def dilate1(sub,obj,opr=1):
#     TESTS : sub|001 != 0
    sub = sub^oo1
    temp1 = (1+opr)/2 + sub*(1-opr)/2
    temp2 = (1+opr)/2 - sub*(1-opr)/2
    temp = temp2*obj*temp1
    return(temp)
    
# def show(a):
#     to    = -(a|oo).scalar()*so
#     too   = -(a|o).scalar()*soo
    
#     tx   = (a|x1).scalar()*sx1
#     ty   = (a|y1).scalar()*sy1
#     tz   = (a|z1).scalar()*sz1

#     temp = to + tx + ty + tz + too
#     return(temp)
def show(a):
    to    = -(a|oo).scalar()*so
    too   = -(a|o).scalar()*soo
    
    tx   = (a|x1).scalar()*sx1
    ty   = (a|y1).scalar()*sy1
    tz   = (a|z1).scalar()*sz1
    
    trx  = -(a|en1).scalar()*srx1

    temp = to + tx + ty + tz + trx + too
    return(temp)

def show1(a):
    to    = -(a|oo1).scalar()*so1
    too   = -(a|o1).scalar()*soo1
    
    tx   = (a|x1).scalar()*sx1
    ty   = (a|y1).scalar()*sy1
#     tz   = (a|z1).scalar()*sz1
    tr   = -(a|en1).scalar()*srx1

    temp = to + tx + ty + tr + too
    return(temp)

def show2(a):
    to    = -(a|oo2).scalar()*so2
    too   = -(a|o2).scalar()*soo2
    
    tx   = (a|x2).scalar()*sx2
    ty   = (a|y2).scalar()*sy2
    tr   = -(a|en1).scalar()*srx2

    temp = to + tx + ty + tr + too
    return(temp)

def fact(B,con = oo1+en1):
    temp = (B|B).scalar()
    sqrtT = sqrt(temp)
    B1 = B/sqrtT
    temp1 = ((con<B1)<B1)-(con<B1)
    temp2 = ((con<B1)<B1)+(con<B1)
    return([temp1,temp2])

def fact1(B,con = oo1):
    temp = fact(B,con = oo1)
    return(temp)

def fact2(B,con = x1):
    temp = fact(B,con = x1)
    return(temp)

def fact3(B,con = o1):
    B1 = B/((o1^oo1)<B)
    temp1 = (((con<B1)<B1)+(con<B1))/2
    temp2 = (((con<B1)<B1)-(con<B1))/2
    return([temp1,temp2])

def fact4(B,con = o1):
    B1 = B/((o1^en1)<B)
    temp1 = (((con<B1)<B1)+(con<B1))/2
    temp2 = (((con<B1)<B1)-(con<B1))/2
    return([temp1,temp2])
    
# def norm(M,b=o1):
#     temp = M/M.blade_coefs([o1])
#     return(temp)
    
def esinh(a):
    return(sinh(a).rewrite(exp))
def ecosh(a):
    return(cosh(a).rewrite(exp))

# .subs([(sin(th2/2)**2,(1-cos(th2))/2),(cos(th2/2)**2,(1+cos(th2))/2)])
# .subs([(sinh(r3/2),esinh(r3/2)),(cosh(r3/2),ecosh(r3/2))])/(o1-o1+r3).exp()