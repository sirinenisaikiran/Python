#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the plusMinus function below.
def plusMinus(arr):
    positive_num_count = 0
    negative_num_count = 0
    zero_count = 0
    for i in arr:
        if i > 0:
            positive_num_count += 1
        elif i < 0:
            negative_num_count += 1
        elif i ==0:
            zero_count +=1
    print(round(positive_num_count / n,6))
    print(round(negative_num_count / n,6))
    print(round(zero_count / n,6))

if __name__ == '__main__':
    n = int(input())

    arr = list(map(int, input().rstrip().split()))

    plusMinus(arr)
    
