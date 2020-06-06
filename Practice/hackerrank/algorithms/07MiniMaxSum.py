# Challenge: https://www.hackerrank.com/challenges/mini-max-sum/problem
#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the miniMaxSum function below.
def miniMaxSum(arr):
    arr_new = arr
    arr_new.sort()
    Min = sum(arr_new[0:4])
    Max = sum(arr_new[1:5])
    print('{} {}'.format(Min,Max))

if __name__ == '__main__':
    arr = list(map(int, input().rstrip().split()))

    miniMaxSum(arr)