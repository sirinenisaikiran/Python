# Python code to demonstrate the working of gcd()
# importing "math" for mathematical operations
import math
  
# # prints 12
a=11
m=26
print("The gcd of {} and {} is : ".format(a,m), end="")
print(math.gcd(a, m))

# Alternate logic
# def hcf(a, b):
    # if(b == 0):
        # return a
    # else:
        # return hcf(b, a % b)
  
# a = 13
# m = 26
  
# # prints 12
# print("The gcd of {} and {} is : ".format(a,m), end="")
# print(hcf(a, m))