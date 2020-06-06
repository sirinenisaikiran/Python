# Challenge: https://www.hackerrank.com/challenges/birthday-cake-candles/problem
#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the birthdayCakeCandles function below.
def birthdayCakeCandles(ar):
    candle_heights = ar
    return candle_heights.count(max(candle_heights))

if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    ar_count = int(input())

    ar = list(map(int, input().rstrip().split()))

    result = birthdayCakeCandles(ar)

    #fptr.write(str(result) + '\n')

    #fptr.close()
    print(result)
