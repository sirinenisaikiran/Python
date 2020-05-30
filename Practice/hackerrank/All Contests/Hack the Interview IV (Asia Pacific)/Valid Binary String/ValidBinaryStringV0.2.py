#!/bin/python3

import math
import os
import random
import re
import sys
import time

#
# Complete the 'minimumMoves' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. STRING s
#  2. INTEGER d
#

def minimumMoves(s, d):
    s_len = len(s)
    Num_Moves = 0
    sub_str = ''
    #sub_str_list=[]
    s_list = list(s)
    zero_sub_str = '0' * d
    while True:
        #print('Lis: {}'.format(s_list))
        Num_Moves_New = 0
        for i in range(s_len):
            fist_str = ''
            next_str = ''
            if i + d <= s_len:
                fist_str = ''.join(s_list[i:i+d])
            if i + d + 1 <= s_len:
                next_str = ''.join(s_list[i+1:i+1+d])
            
            # print('fist_str: {} next_str: {}'.format(fist_str,next_str))
            # print('Number of moves : {}' .format(Num_Moves))
            
            if fist_str == zero_sub_str and next_str != zero_sub_str:
                Num_Moves += 1
                Num_Moves_New += 1
                s_list[i] = '1'
                break
            elif fist_str == zero_sub_str and next_str == zero_sub_str:
                s_list[i+d-1] = '1'
                Num_Moves += 1
                Num_Moves_New += 1
                break
        if Num_Moves_New == 0:
            break
        #print('fist_str: {} next_str: {}'.format(fist_str,next_str))
        #print('Number of moves : {}' .format(Num_Moves))
        #print('updated list :{}' .format(s_list))
    #print('Final number of moves : {}' .format(Num_Moves))
        
    return Num_Moves
        



if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = input()
    # s = '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001'
    d = int(input().strip())
    # d = 2
    # starting time
    #start = time.time()

    result = minimumMoves(s, d)

   # fptr.write(str(result) + '\n')
    print(str(result))
    #fptr.close()\
    
    # end time
    #end = time.time()
    # total time taken
    #print(f"Runtime of the program is {end - start}")
