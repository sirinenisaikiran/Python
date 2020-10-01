#mex.py is module file 

def square(x):
    """ first function
    returns square of number"""
    z = x*x
    return z 

#import mex 
#lst = [1,2,3]
#print(mex.mean(lst)) #2
def mean(lst):
    """Sum of lst/length of lst"""
    return sum(lst)/len(lst)

import math 
def sd(lst):
    """sqrt of( SUM of square of 
    ( each elemnt - mean)  / length of lst  )"""
    m = mean(lst)
    output = []
    for e in lst:
        output.append( square(e-m))
    return math.sqrt(sum(output)/len(output))
    
import glob 
import os.path 
def getMaxFileName(path):
    """
    1. Given path, find out all files and dirs 
        import glob
        glob.glob(path+"/*")
    2. Based on os.path.isfile
       get all files 
    3. Create a dict of filename and size as value using os.path.getsize 
    4. sort that dict based on value ie size 
    5. return the last elemnt of that sorted data     
    """
    dictfiles = {}
    lstFull = glob.glob(path + "\*")
    for e in lstFull:
        if os.path.isfile(e):
            dictfiles[e] = os.path.getsize(e)
    #Now Step 4 and 5 
    sorted_data = sorted(dictfiles, key =lambda e: dictfiles[e])
    return sorted_data[-1]
    
    
    
    
    
    
    




