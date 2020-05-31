#!/bin/python3
# Challenge: https://www.hackerrank.com/contests/hack-the-interview-iv-apac/challenges/maximum-or-1

import math
import os
import random
import re
import sys

#
# Complete the 'getNumberOfIntegers' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. STRING L
#  2. STRING R
#  3. INTEGER K
#

def getNumberOfIntegers(L, R, K):
    num_list = []
    for num in range(int(L)+1,int(R)+1):
        num_str = str(num)
        num_str_len = len(num_str)
        if num_str.count('0') == num_str_len - K:
            num_list.append(num_str)
            #print(num_str, end=' ')
    
    return len(num_list)
        
        
    # Write your code here

if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    L = input()

    R = input()

    K = int(input().strip())

    ans = getNumberOfIntegers(L, R, K)

    #fptr.write(str(ans) + '\n')

    #fptr.close()
    print(ans)
