import sys


from typing import Tuple, TypeVar, Callable, Dict, Sequence, List, Optional, Union
print(sys.path)

from sympy import (
    diff, Rational, Symbol, S, Mul, Add, Expr,
    expand, simplify, eye, trigsimp,
    symbols, sqrt, Matrix,srepr,cos
)


(a1,b1,c1,d1,e1,f1) = symbols('a_1 b_1 c_1 d_1 e_1 f_1', real=True)
(a2,b2,c2,d2,e2,f2) = symbols('a_2 b_2 c_2 d_2 e_2 f_2', real=True)
(a3,b3,c3,d3,e3,f3) = symbols('a_3 b_3 c_3 d_3 e_3 f_3', real=True)



print((a1*a2).args)
print((a1*a2).func)

print((a1^a2).args)
print((a1^a2).func)

print((a1|a2).args)
print((a1|a2).func)

print(srepr(a1*a2))
print(srepr(a1^a2))

print(srepr((a2*a1*a3*(b1+b2))))

print(srepr(a1|a2))

# temp = cos(a1)
# temp = a3^a2
temp = a1
print(temp)

# <bound method Printable.__str__ of a_1>