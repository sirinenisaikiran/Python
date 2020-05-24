# How to execue the script
# Command: python ReadJSON.py <number of days> <pattern>
# Example: python ReadJSON.py 10000 cc-r-2018-06-13-06-56-24-31

import json
import sys 
from datetime import datetime, timedelta, date


# Read arguments
n = len(sys.argv) 
# print("Total arguments passed:", n) 
n -= 1
if n == 0 :
    print("No arguments are passed")
    exit(1)
elif n != 2:
    print("Two arguments should be passed")
    exit(1)
else:
    number_of_days = int(sys.argv[1])
    pattern = sys.argv[2]
    if not number_of_days >= 0:
        print("number_of_days is not greater than equal to zero")
        exit(1)

# exit()
datelimit = datetime.today() - timedelta(days=number_of_days)

#number_of_days = input("Enter number of days: ")
#match_pattern = input("Enter pattern: ")
f = open("F:/Sridhar/metadata.json",'r')
data = json.load(f)
size = len(data)

# print(data[0]["creationTimestamp"])
# print(len(data))

for num in range(0,size):
    i=data[num]["creationTimestamp"][0:19]
    j = datetime.strptime(i,"%Y-%m-%dT%H:%M:%S")
    if j > datelimit:
        #print (j.strftime('%Y-%m-%dT%H:%M:%S'))
        #print(data[num])
        if pattern in data[num]["name"]:
            print(data[num])

