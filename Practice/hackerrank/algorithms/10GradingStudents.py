# Challenge: https://www.hackerrank.com/challenges/grading/problem
#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'gradingStudents' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts INTEGER_ARRAY grades as parameter.
#

def gradingStudents(grades):
    Grades = grades
    Grades_Roundedoff = []
    for gr in Grades:
        if gr < 38:
            Grades_Roundedoff.append(gr)
        else:
            next_multiple_of_5 = math.ceil(gr/5) * 5
            if next_multiple_of_5 - gr < 3:
                Grades_Roundedoff.append(next_multiple_of_5)
            else:
                Grades_Roundedoff.append(gr)
    return Grades_Roundedoff
    # Write your code here

if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    grades_count = int(input().strip())

    grades = []

    for _ in range(grades_count):
        grades_item = int(input().strip())
        grades.append(grades_item)

    result = gradingStudents(grades)
    
    for res in result:
        print(res)

    #fptr.write('\n'.join(map(str, result)))
    #fptr.write('\n')

    #fptr.close()
