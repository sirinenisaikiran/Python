#!/bin/python3

import math
import os
import random
import re
import sys
from itertools import combinations

# Complete the divisibleSumPairs function below.
def divisibleSumPairs(n, k, ar):
    Divisible_Sum_Pairs_Count = 0
    for p in combinations(ar,2):
        #print(p)
        if sum(p) % k == 0:
            Divisible_Sum_Pairs_Count += 1
    return Divisible_Sum_Pairs_Count

if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    nk = input().split()

    n = int(nk[0])

    k = int(nk[1])

    ar = list(map(int, input().rstrip().split()))

    result = divisibleSumPairs(n, k, ar)
    print(result)
    #fptr.write(str(result) + '\n')

    #fptr.close()
