#!/bin/python3

# Challenge: https://www.hackerrank.com/challenges/diagonal-difference/problem

import math
import os
import random
import re
import sys

#
# Complete the 'diagonalDifference' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY arr as parameter.
#

def diagonalDifference(arr):
    arr_len = len(arr)
    primary_diagonal = 0
    secondary_diagonal = 0
    for i in range(0,arr_len):
        for j in range(0,arr_len):
            if j == i:
                #print("primary_diagonal : {}" .format(arr[i][j]))
                primary_diagonal += arr[i][j]
            if j == arr_len -1 - i:
                #print("secondary_diagonal : {}" .format(arr[i][j]))
                secondary_diagonal += arr[i][j]
    diff_diagonals = primary_diagonal - secondary_diagonal
    return abs(diff_diagonals)
    # Write your code here
    # return 10

if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    arr = []

    for _ in range(n):
        arr.append(list(map(int, input().rstrip().split())))

    result = diagonalDifference(arr)

    #fptr.write(str(result) + '\n')

    #fptr.close()
    print(result)
