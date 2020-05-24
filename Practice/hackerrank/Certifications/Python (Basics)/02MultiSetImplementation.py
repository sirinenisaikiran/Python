# import math
# import os
# import random
# import re
# import sys


class Multiset:
    List = []
    def add(self, val):
        # adds one occurrence of val from the multiset, if any
        List.append(val)

    def remove(self, val):
        # removes one occurrence of val from the multiset, if any
        if List.count(val) != 0: List.remove(val)

    def __contains__(self, val):
        # returns True when val is in the multiset, else returns False
        if List.count(val) != 0: return True           
        else: return False
    
    def __len__(self):
        # returns the number of elements in the multiset
        return len(List)

List = []
MS = Multiset()
number_of_inputs = int(input())
for i in range(0,number_of_inputs):
    #print(MS.List)

    q_List = input().split(' ')
    if q_List[0] == 'size':
        print(MS.__len__())
    elif q_List[0] == 'query':
        print(MS.__contains__(q_List[1]))
    elif q_List[0] == 'add':
        MS.add(q_List[1])
    elif q_List[0] == 'remove':
        MS.remove(q_List[1])
    #print(MS.List)

