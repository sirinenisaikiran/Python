# Challenge: https://www.hackerrank.com/contests/projecteuler/challenges/euler254/problem?h_r=profile
#!/bin/python3

import math
import os
import random
import re
import sys
#from itertools import combinations

# Complete the divisibleSumPairs function below.

def Fun_f_of_n(n):
    #print("Fun_f_of_n with n={}".format(n))
    sum_of_factorials = 0
    for k in list(map(int, str(n))):
        sum_of_factorials += math.factorial(k)
    return sum_of_factorials
        
#   
def Fun_g_of_i(i):
    #print("Fun_g_of_i with i = {}".format(i))
    #print("n :{}" .format(n))
    Sum_of_f_of_n = 0
    for j in Dict.keys():
        if Dict[j][1] == i:
            return j
    if len(Dict) > 0:
        n = max(Dict.keys()) + 1
    else:
        n = 1
    while [ True ]:
        f_of_n = Fun_f_of_n(n)
        Sum_of_f_of_n = sum(list(map(int, str(f_of_n))))
        Dict[n] = [f_of_n,Sum_of_f_of_n]
        if Sum_of_f_of_n == i:
            break
        n += 1
    #print("count: {}" .format(count))
    return n
    
def Fun_sum_of_g_of_i(i):
    #print("Fun_sum_of_g_of_i with i = {}".format(i))
    #print("n :{}" .format(n))
    g_of_i = Fun_g_of_i(i)
    #print("g_of_i: {}".format(g_of_i))
    Sum_of_g_of_i = sum(list(map(int, str(g_of_i))))
    return Sum_of_g_of_i

    
        
if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')
    Dict = {}

    q = int(input().strip())
    
    for _ in range(q):
        pq = input().rstrip().split()
        p = int(pq[0])
        q = int(pq[1]) # 
    
    # result = Summammation from 1 to n ( s g(i))
        result = 0
        for i in range(1, p+1):
            result += Fun_sum_of_g_of_i(i)
            #print("result = {}".format(result))
            print(Dict)
    
    
        #result = SumsofDigitFactorials(n, m)
        print(result)
    #fptr.write(str(result) + '\n')

    #fptr.close()
