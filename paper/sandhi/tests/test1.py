from Sygal.initial import *

# t1 = (d1<(a1^(d2<(b1^(d3<(c1^c2^c3))))))^(d1<(a3^(d2<(b3^(d3<(c1^c2^c3^c4))))))
# t1_1 = ((d1^d2^d3)|(c1^c2^c3))*(d1<(a1^a3^(d2<(b1^b3^(d3<(c1^c2^c3^c4))))))
# t3 = (a1^a3^b1^b3^c4)

t1 = (d1<(a1^a2^(d2<(b1^b2^(d3<(c1^c2^c3))))))^(d1<(a3^a4^(d2<(b3^b4^(d3<(c1^c2^c3^c4))))))

t1_1 = ((d1^d2^d3)|(c1^c2^c3))*(d1<(a1^a2^a3^a4^(d2<(b1^b2^b3^b4^(d3<(c1^c2^c3^c4))))))
t3 = (a1^a2^a3^a4^b1^b2^b3^b4^c4)
exp_coeff = sclrprdct.gexpand1((d1^d2^d3)|(c1^c2^c3))

print(t1)
print(t1_1)
print("\033[1;31;40mBREAK")
# t1_2 = expand_iter(glcntrct)(t1)
t1_2 = GExpr.gdistribute(expand_iter(glcntrct)(t1))
print(t1_2)
print("\033[1;31;40mt1_2")

t1_3 = GExpr.gdistribute(sclrprdct.gexpand1(expand_iter(glcntrct)(t1_1)))
# t1_3 = expand_iter(glcntrct)(t1_1)

print(t1_3)
print("\033[1;31;40mt1_3")
sub = (t1_2 - t1_3) 
expr = sub.mv*sub.coeff.expand() 
print(expr)
print("\033[1;31;40mSUB")

# t3_1 = [ele for ele in t1_2.mv.args if ele.mv==t3.mv]
# t3_2 = [ele for ele in t1_3.mv.args if ele.mv==t3.mv]

# print(t3_1[0])
# print("\033[1;31;40mt3_1[0]")
# print(t3_2[0])
# print("\033[1;31;40mt3_2[0]")

# t4 = sclrprdct.gexpand1(((d1^d2^d3)|(c1^c2^c3)))
