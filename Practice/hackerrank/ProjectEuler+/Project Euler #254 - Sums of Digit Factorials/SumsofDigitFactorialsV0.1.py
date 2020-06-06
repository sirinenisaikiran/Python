# Challenge: https://www.hackerrank.com/contests/projecteuler/challenges/euler254/problem?h_r=profile
#!/bin/python3

import math
import os
import random
import re
import sys
#from itertools import combinations

# Complete the divisibleSumPairs function below.

def Fun_f_of_i(c):
    sum_of_factorials = 0
    for k in list(map(int, str(c))):
        sum_of_factorials += math.factorial(k)
    return sum_of_factorials
        
#   
def Fun_g_of_i(n):
    #print("n :{}" .format(n))
    Sum_of_f_of_i = 0
    count = 1
    while [ True ]:
        f_of_i = Fun_f_of_i(count)
        Sum_of_f_of_i = sum(list(map(int, str(f_of_i))))
        if Sum_of_f_of_i == n:
            break
        count += 1
    #print("count: {}" .format(count))
    return count
    
def Fun_sum_of_g_of_i(n):
    #print("n :{}" .format(n))
    g_of_i = Fun_g_of_i(n)
    #print("g_of_i: {}".format(g_of_i))
    Sum_of_g_of_i = sum(list(map(int, str(g_of_i))))
    return Sum_of_g_of_i

    
        
if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input().strip())
    
    for i in range(q):
        nm = input().rstrip().split()
        n = int(nm[0])
        m = int(nm[1])
    
    # result = Summammation from 1 to n ( s g(i))
    result = 0
    for j in range(1, n+1):
        result += Fun_sum_of_g_of_i(j)
    
    
        #result = SumsofDigitFactorials(n, m)
    print(result)
    #fptr.write(str(result) + '\n')

    #fptr.close()
