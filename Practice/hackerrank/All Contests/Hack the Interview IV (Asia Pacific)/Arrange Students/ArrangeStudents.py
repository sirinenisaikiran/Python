#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'arrangeStudents' function below.
#
# The function is expected to return a STRING.
# The function accepts following parameters:
#  1. INTEGER_ARRAY a
#  2. INTEGER_ARRAY b
#

def arrangeStudents(a, b):
    # Write your code here
    # print(a)
    # print(b)
    #b, g = []
    b, g = a, b
    # print(b)
    # print(g)
    b.sort()
    g.sort()
    # print(b)
    # print(g)
    orderd_group = []
    last_in_order = ''
    ast_in_order_height = 0
    Is_Arragne_Possible = "YES"
    

    for i in range(len(b)):
        if i == 0:
            if b[i] < g[i]:
                last_in_order_height = g[i]
                last_in_order = 'g'
                orderd_group.append(b[i])
                orderd_group.append(g[i])
            elif b[i] > g[i]:
                last_in_order_height = b[i]
                last_in_order = 'b'
                orderd_group.append(g[i])
                orderd_group.append(b[i])
            elif b[i] == g[i]:
                last_in_order_height = (b[i] + g[i])//2
                last_in_order = 'g or b'
                orderd_group.append(b[i])
                orderd_group.append(g[i])
        else:
            #print("last_in_order: {}".format(last_in_order))
            #print("last_in_order_height: {}".format(last_in_order_height))
            #print("boy height: {}".format(b[i]))
            #print("girl height: {}".format(g[i]))
            if last_in_order == 'g':
                if not b[i] > last_in_order_height:
                    Is_Arragne_Possible = "NO"
                    break
                else:
                    if not g[i] >= b[i]:
                        Is_Arragne_Possible = "NO"
                        break
                    else:
                        last_in_order == 'g'
                        last_in_order_height = g[i]
                        orderd_group.append(b[i])
                        orderd_group.append(g[i])
            elif last_in_order == 'b':
                if not g[i] > last_in_order_height:
                    Is_Arragne_Possible = "NO"
                    break
                else:
                    if not b[i] >= g[i]:
                        Is_Arragne_Possible = "NO"
                        break
                    else:
                        last_in_order == 'b'
                        last_in_order_height = b[i]
                        orderd_group.append(g[i])
                        orderd_group.append(b[i])
            elif last_in_order == 'g or b':
                if b[i] < g[i]:
                    last_in_order_height = g[i]
                    last_in_order = 'g'
                    orderd_group.append(b[i])
                    orderd_group.append(g[i])
                elif b[i] > g[i]:
                    last_in_order_height = b[i]
                    last_in_order = 'b'
                    orderd_group.append(g[i])
                    orderd_group.append(b[i])
                elif b[i] == g[i]:
                    last_in_order_height = b[i]
                    last_in_order = 'g or b'
                    orderd_group.append(b[i])
                    orderd_group.append(g[i])
    #print(orderd_group)
    return Is_Arragne_Possible
        
        
    

if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    t = int(input().strip())

    for t_itr in range(t):
        n = int(input().strip())

        a = list(map(int, input().rstrip().split()))

        b = list(map(int, input().rstrip().split()))
        # print(a)
        # print(b)

        result = arrangeStudents(a, b)

        #fptr.write(result + '\n')
        print(result)

    #fptr.close()