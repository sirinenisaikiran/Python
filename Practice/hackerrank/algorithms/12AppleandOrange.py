# Challange: https://www.hackerrank.com/challenges/apple-and-orange/problem
#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the countApplesAndOranges function below.
def countApplesAndOranges(s, t, a, b, apples, oranges):
    num_apples = 0
    num_oranges = 0
    for i in apples:
        if (a + i) >= s and (a + i) <= t:
            num_apples += 1
            #print("{} {}".format(a,i))
    for j in oranges:
        if (b + j) <= t and (b + j) >= s:
            num_oranges += 1
            #print("{} {}".format(b,j))
    
    print(num_apples)
    print(num_oranges)
            


if __name__ == '__main__':
    st = input().split()

    s = int(st[0])

    t = int(st[1])

    ab = input().split()

    a = int(ab[0])

    b = int(ab[1])

    mn = input().split()

    m = int(mn[0])

    n = int(mn[1])

    apples = list(map(int, input().rstrip().split()))

    oranges = list(map(int, input().rstrip().split()))

    countApplesAndOranges(s, t, a, b, apples, oranges)
