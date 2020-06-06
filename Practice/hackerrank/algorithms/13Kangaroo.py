# Challenge: https://www.hackerrank.com/challenges/kangaroo/problem
#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the kangaroo function below.
def kangaroo(x1, v1, x2, v2):
    count = 1
    kangaroo1_Distannce_Travelled = x1
    kangaroo2_Distannce_Travelled = x2
    while count <= 10000:
        kangaroo1_Distannce_Travelled += v1
        kangaroo2_Distannce_Travelled += v2
        if kangaroo1_Distannce_Travelled == kangaroo2_Distannce_Travelled:
            return "YES"
        count += 1
    if count > 100:
        return "NO"

if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    x1V1X2V2 = input().split()

    x1 = int(x1V1X2V2[0])

    v1 = int(x1V1X2V2[1])

    x2 = int(x1V1X2V2[2])

    v2 = int(x1V1X2V2[3])

    result = kangaroo(x1, v1, x2, v2)

    #fptr.write(result + '\n')

    #fptr.close()
    print(result)
