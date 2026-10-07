from Sygal.initial import *

"""
((a1^a2..a_r)<((b1..br)^(c1..cm)))^((a1..a_r)<((b1..br)^(d1..dn))) == (a1^a2..a_r)|((b1..br)*
(a1^a2..a_r)<((b1..br)^(c1..cm)^(d1..dn))
Will be done after implementing dot product and multiplication.
"""
coeff = (a1^a2^a3)<(b1^b2^b3)
exp_coeff = sclrprdct.gexpand1(coeff)

t1 = ((a1^a2^a3)<(b1^b2^b3^c1^c2))^((a1^a2^a3)<(b1^b2^b3^d1^d2))^((a1^a2^a3)<(b1^b2^b3^b4^c4))
t1_1 = (coeff*coeff)*((a1^a2^a3)<(b1^b2^b3^c1^c2^d1^d2^b4^c4))



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
t_sub = [ele.mv*ele.coeff.expand() for ele in sub.mv.args]
print(gadd(*t_sub)) 
print("\033[1;31;40mSUB")

# t3_1 = [ele for ele in t1_2.mv.args if ele.mv==t3.mv]
# t3_2 = [ele for ele in t1_3.mv.args if ele.mv==t3.mv]

# print(t3_1[0])
# print("\033[1;31;40mt3_1[0]")
# print(t3_2[0])
# print("\033[1;31;40mt3_2[0]")

# t4 = sclrprdct.gexpand1(((d1^d2^d3)|(c1^c2^c3)))
