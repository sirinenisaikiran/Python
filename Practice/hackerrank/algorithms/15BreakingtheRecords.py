# Challenge: https://www.hackerrank.com/challenges/breaking-best-and-worst-records/problem
#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the breakingRecords function below.
def breakingRecords(scores):
    min_score = scores[0]
    max_score = scores[0]
    min_rec = 0
    max_rec = 0
    for sc in scores[1:]:
        if sc > max_score:
            max_score = sc
            max_rec += 1
        if sc < min_score:
            min_score = sc
            min_rec += 1
    return [max_rec, min_rec]

if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input())

    scores = list(map(int, input().rstrip().split()))

    result = breakingRecords(scores)

    print(' '.join(map(str, result)))
    #fptr.write(' '.join(map(str, result)))
    #fptr.write('\n')

    #fptr.close()
