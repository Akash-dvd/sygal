from lib import *

# Circle

p1 = o1 + g1*x1+h1*y1+(g1*g1+h1*h1)*oo1/2
p2 = p1 + r2*(cos(th2)*x1+sin(th2)*y1)
p2 = p2*oo1*p2/-2
p3 = p1 + r3*(cos(th3)*x1+sin(th3)*y1)
p3 = p3*oo1*p3/-2

Ac1 = o1 + g1*x1+h1*y1+r1*en1+ (g1*g1+h1*h1-r1*r1)*oo1/2
IAc1 = -(inversion(I4,Ac1))
Sc1 = projection(I4,Ac1)

Ac2 = p1 + r*(cos(th2)*x1+sin(th2)*y1) + r2*en1
Ac2 = Ac2*oo1*Ac2/-2
IAc2 = -(inversion(I4,Ac2))
Sc2 = projection(I4,Ac2)

# Lines

Al1 = cos(th1)*x1+sin(th1)*y1+en1+d1*oo1
Sl1 = projection(I4,Al1)
IAl1 = -(inversion(I4,Al1))

Al2 = cos(th2)*x1+sin(th2)*y1+en1+d2*oo1
Sl2 = projection(I4,Al2)
IAl2 = -(inversion(I4,Al2))

Al3 = cos(th3)*x1+sin(th3)*y1+en1+d3*oo1
Sl3 = projection(I4,Al3)
IAl3 = -(inversion(I4,Al3))