# Challenge: https://www.hackerrank.com/challenges/time-conversion/problem

#!/bin/python3

import os
import sys

#
# Complete the timeConversion function below.
#
def timeConversion(s):
    hr = s.split(':')[0]
    mn = s.split(':')[1]
    sc = s.split(':')[2][0:2]
    am_or_pm = s.split(':')[2][2:4]
    
    if am_or_pm == 'AM':
        if hr == "12":
            return "00" + ":" + mn + ":" + sc
        else:
            return hr + ":" + mn + ":" + sc
    elif am_or_pm == 'PM':
        if int(hr) == 12:
            return hr + ":" + mn + ":" + sc
        else:
            return str(int(hr) + 12) + ":" + mn + ":" + sc
    #
    # Write your code here.
    #

if __name__ == '__main__':
    #f = open(os.environ['OUTPUT_PATH'], 'w')

    s = input()

    result = timeConversion(s)

    #f.write(result + '\n')

    #f.close()
    print(result)
