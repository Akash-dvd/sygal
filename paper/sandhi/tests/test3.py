from Sygal.initial import *

"""
((a1^a2..a_r)<((b1..br)^(c1..cm)))^((a1..a_r)<((b1..br)^(d1..dn))) == (a1^a2..a_r)|((b1..br)*
(a1^a2..a_r)<((b1..br)^(c1..cm)^(d1..dn))
Will be done after implementing dot product and multiplication.
"""
coeff1 = (a1^a2)<(b1^b2)
coeff2 = (a1^a2)<(d1^d2)


t1 = ((a1^a2)<(b1^b2^c1^c2))^((a1^a2)<(b1^b2^d1^d2))^((a1^a2)<(d1^d2^b4^c4))
t1_1 = (coeff1*coeff2)*((a1^a2)<(b1^b2^c1^c2^d1^d2^b4^c4))



print(t1)
print(t1_1)
print("\033[1;31;40mBREAK")
# t1_2 = expand_iter(glcntrct)(t1)
t1_2 = GExpr.gdistribute(sclrprdct.gexpand1(expand_iter(glcntrct)(t1)))
print(t1_2)
print("\033[1;31;40mt1_2")

t1_3 = GExpr.gdistribute(sclrprdct.gexpand1(expand_iter(glcntrct)(t1_1)))
# t1_3 = expand_iter(glcntrct)(t1_1)
print(t1_3)
print("\033[1;31;40mt1_3")
sub = (t1_2 - t1_3) 
print(sub)
# print("\033[1;31;40mSUB")

t2 = ((a1^a2)<(b1^b2^b3))^((a1)<((a2<(b1^b2))^b3))
t2_1 = ((a1^a2)<(b1^b2))*((a1)<(b3^(a2<(b1^b2^b3))))

print(t2)
print(t2_1)
print("\033[1;31;40mBREAK")
# t1_2 = expand_iter(glcntrct)(t1)
t2_2 = GExpr.gdistribute(sclrprdct.gexpand1(expand_iter(glcntrct)(t2)))
print(t2_2)
print("\033[1;31;40mt2_2")

t2_3 = GExpr.gdistribute(sclrprdct.gexpand1(expand_iter(glcntrct)(t2_1)))
# t1_3 = expand_iter(glcntrct)(t1_1)
print(t2_3)
print("\033[1;31;40mt2_3")
sub = (t2_2 - t2_3) 
print(sub)
print("\033[1;31;40mSUB")