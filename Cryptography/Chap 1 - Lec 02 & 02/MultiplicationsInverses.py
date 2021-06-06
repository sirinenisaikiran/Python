# create ring of mod26
import math
N=26
Ring_Zn=[]
for i in range(0,N):
    Ring_Zn.append(i)
print("Ring: ",Ring_Zn)

for i in Ring_Zn:
    #print(i)
    for j in Ring_Zn:
        if i==j:
            pass
        else:
            # GCD of i*j, N shoud be 1 and (i*j)mod26 should be 1. Then we call i & j satissfy multiplicative inverse.
            if math.gcd(i*j,N) == 1 and (i*j)%N == 1:
                print("Inverse for {} is {}".format(i,j))

