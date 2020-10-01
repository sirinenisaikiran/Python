#Contents 
Numpy - Quick Intro 
Pandas - Quick Intro 
*pandas- CSV 
*EXCEl: xlrd is required for pandas.read_excel 
#***************************************


###Numpy - Quick Intro 


# A numpy array(homogeneous)(numpy.ndarray) is created from python list or List of List for higher dimension
#indexed by a tuple of nonnegative integers.

#Stored as colum major way 

#dimensions are called axes. The number of axes(plural of axis) is rank. 
#axis starts from zero , axis=0 means 1st dimension(x) , axis=1 means 2nd dimension(y)...
#OR axis=-1 means last dimension, axis=-2 means 2nd last dimension 

#shape  is a tuple of integers giving the size of the array along each dimension.
#a 1D array can be .reshape(tuple_of_dims) if total elements are same 

#Note many function take 'axis' argument, means the dimension on which function operates
#For 2D , axis=0 means 1st dimension=Row , axis=1 means 2nd dimension=Column
#eg insert, delete etc 

#For certain methods (eg sum, prod etc) axis=0 means, operation along the 1st dimension
#ie 1st dimension  
#ie for 2D,  Row varying which is equivalent to ColumnWise 

#Hence Understand meaning of axis per function from reference documents 

#For  example, np.sum(axis=n),  dimension n is collapsed and deleted, 
#For example, if b has shape (5,6,7,8), and c = b.sum(axis=2), 
#then axis 2 (dimension with size 7) is collapsed, and the result has shape (5,6,8). 
#c[x,y,z] is equal to the sum of all elements c[x,y,:,z]



#Example 

import numpy as np

a = np.array([1, 2, 3])  # Create a rank 1 array
print type(a)            # Prints "<type 'numpy.ndarray'>"
print a.shape            # Prints "(3,)"
print a.ndim 			 # 1
print a[0], a[1], a[2]   # Prints "1 2 3"
a[0] = 5                 # Change an element of the array
print a                  # Prints "[5, 2, 3]"

b = np.array([[1,2,3],[4,5,6]])   # Create a rank 2 array
print b.shape                     # Prints "(2, 3)"
print b[0, 0], b[0, 1], b[1, 0]   # Prints "1 2 4"
b[0,]	#or b[0,:]   			  # array([1, 2, 3])  
b[:,0]                            #array([1, 4])



#Note the difference of below, one is vector and another is 1x3
>>> x = np.array([[1,2,3]])        
>>> x.shape                         #rank 2 as two dimension 
(1, 3)

>>> x = np.array([1,2,3])           # rank 1, generally called vector 
>>> x.shape
(3,)



##Creation of array - these methods take (m,n,...) dimensions 
# similar methods (zeros/ones/full)_like(another_array) which creates based on another_array.shape
import numpy as np

a = np.zeros((2,2))  # Create an array of all zeros 

    
b = np.ones((1,2))   # Create an array of all ones

c = np.full((2,2), 7) # Create a constant array
print c               # Prints "[[ 7.  7.]
                      #          [ 7.  7.]]"

d = np.eye(2)        # Create a 2x2 identity matrix

#random 
e = np.random.random((2,2)) # Create an array filled with random values
print e                     # Might print "[[ 0.91940167  0.08143941]
                            #               [ 0.68744134  0.87236687]]"
#array range 
>>> np.arange(10).reshape(2,5)
array([[0, 1, 2, 3, 4],
       [5, 6, 7, 8, 9]])
       
>>> np.arange(10)[:8].reshape(2,2,2)
array([[[0, 1],
        [2, 3]],

       [[4, 5],
        [6, 7]]])
        
##Array indexing - Slice Indexing (can be mutated)
#index can be single number, or start:stop:step (stop exclusive)
#or :(means all elements of that dimension) or array of indexes
#or boolean array(where True indexes are selected)
import numpy as np

# Create the following rank 2 array with shape (3, 4)
a = np.array([[1,2, 3, 4], 
              [5,6, 7, 8], 
              [9,10,11,12]])

# index 0 to 1 and columns 1 and 2; 
#b is the following array of shape (2, 2):
# [[2 3]
#  [6 7]]
b = a[:2, 1:3]

# A slice of an array is a view into the same data, so modifying it
# will modify the original array.
print a[0, 1]   # Prints "2"
b[0, 0] = 77    # b[0, 0] is the same piece of data as a[0, 1]
print a[0, 1]   # Prints "77"


#Mixing integer indexing with slice indexing.
#yields an array of lower rank than the original array. 

row_r1 = a[1, :]    # Rank 1 view of the second row of a  
row_r2 = a[1:2, :]  # Rank 2 view of the second row of a
print row_r1, row_r1.shape  # Prints "[5 6 7 8] (4,)"
print row_r2, row_r2.shape  # Prints "[[5 6 7 8]] (1, 4)"

# We can make the same distinction when accessing columns of an array:
col_r1 = a[:, 1]
col_r2 = a[:, 1:2]
print col_r1, col_r1.shape  # Prints "[ 2  6 10] (3,)"
print col_r2, col_r2.shape  # Prints "[[ 2]
                            #          [ 6]
                            #          [10]] (3, 1)"

##Array indexing - Integer array indexing to create subarray , use [ [],[] ]

import numpy as np

a = np.array([[1,2], [3, 4], [5, 6]])


# The returned array will have shape (3,) 
print a[ [0, 1, 2], [0, 1, 0] ]  # Prints "[1 4 5]"   #takes element from (first_array_index1, second_array_index1)  and so on..

# Same as 
print np.array([a[0, 0], a[1, 1], a[2, 0]])  # Prints "[1 4 5]"



##Boolean array indexing

import numpy as np

a = np.array([[1,2], [3, 4], [5, 6]])

bool_idx = (a > 2)  
            
print bool_idx      # Prints "[[False False]
                    #          [ True  True]
                    #          [ True  True]]"

print a[bool_idx]  # Prints "[3 4 5 6]"

# We can do all of the above in a single concise statement:
print a[a > 2]     # Prints "[3 4 5 6]"

>>> a[ (a > 2) & (a<5)]    #Use &, | and ~ for boolean operation , ==, !=, > >= etc for comparison
array([3, 4])
>>> a[ (a > 2) | (a<5)]
array([1, 2, 3, 4, 5, 6])
>>> a[ ~(a > 2) ]
array([1, 2])

>>> a[ a == 2]
array([2])
>>> a[ a != 2]
array([1, 3, 4, 5, 6])


##Array math and all np.methods - operates elementwise on array 
#check by 
dir(np)

#Basic mathematical functions operate elementwise on arrays, 
#and are available both as operator overloads and as functions in the numpy module

import numpy as np

x = np.array([[1,2],[3,4]], dtype=np.float64)
y = np.array([[5,6],[7,8]], dtype=np.float64)

# Elementwise sum; both produce the array
# [[ 6.0  8.0]
#  [10.0 12.0]]
print x + y                 
print np.add(x, y)

# Elementwise
print x - y    #print np.subtract(x, y)
print x * y    #print np.multiply(x, y)
print x / y    #print np.divide(x, y)
print np.sqrt(x)  #other math methods eg np.sin(), np.log() ....

##Use .dot  for inner product of vector or matrix multiplication 
v = np.array([9,10])
w = np.array([11, 12])

# Inner product of vectors; both produce 219
print v.dot(w)
print np.dot(v, w)

# Matrix / vector product; both produce the rank 1 array [29 67]
print x.dot(v)
print np.dot(x, v)

# Matrix / matrix product; both produce the rank 2 array
# [[19 22]
#  [43 50]]
print x.dot(y)
print np.dot(x, y)


##Sum -  for performing computations on arrays 

# For , np.sum(axis=n),  then dimension n is collapsed and deleted, 
#For example, if b has shape (5,6,7,8), and c = b.sum(axis=2), 
#then axis 2 (dimension with size 7) is collapsed, and the result has shape (5,6,8). 
#c[x,y,z] is equal to the sum of all elements c[x,y,:,z].

import numpy as np

x = np.array([[1,2],[3,4]])

print np.sum(x)  # Compute sum of all elements; prints "10"
print np.sum(x, axis=0)  # Compute sum of each column; prints "[4 6]"
print np.sum(x, axis=1)  # Compute sum of each row; prints "[3 7]"


##Transposing  an array 

import numpy as np

x = np.array([[1,2], [3,4]])
print x    # Prints "[[1 2]
           #          [3 4]]"
print x.T  # Prints "[[1 3]
           #          [2 4]]"

# Note that taking the transpose of a rank 1 array does nothing:
v = np.array([1,2,3])
print v    # Prints "[1 2 3]"
print v.T  # Prints "[1 2 3]"

##r_ , c_ , stack etc 

#np.r_  : By default: create a array(1D) from comma seperated many slices start:stop:step (stop exclusive)
#or comman seperated numbers (along the first axis ie row)
#it has many other functionalities - check Reference 

#np.c_ : create a array(2D) from comma seperated many 1D arrays or start:stop:step (stop exclusive)
# but  along the second axis(ie column) -> Column stack 
#

#note used with []   not ()

>>> np.c_[np.array([1,2,3]), np.array([4,5,6])]
array([[1, 4],
       [2, 5],
       [3, 6]])
>>> np.c_[np.array([[1,2,3]]), 0, 0, np.array([[4,5,6]])]
array([[1, 2, 3, 0, 0, 4, 5, 6]])


>>> x = np.r_[-2:3, 0,0, 3:9]
>>> x
array([-2, -1,  0,  1,  2,  0,  0,  3,  4,  5,  6,  7,  8]

##Difference between .r_[], .c_[] etc 
#columnwise append : .c_, column_stack, stack(axis=1), concatenate(axis=1) for tuple of 2Ds
#rowwise append  : .r_ , hstack, concatenate
#vertically stacking array : vstack, stack(axis=0), concatenate(axis=0) for tuple of 2Ds
#Repeat array to N,nxn times : tile(array, number N or tuple of m,n)

#.c_: columnwise append 
>>> np.c_[1:3,1:3]  
array([[1, 1],
       [2, 2]])
#.r_ : rowwise append 
>>> np.r_[1:3,1:3]
array([1, 2, 1, 2])
#column_stack : columnwise append 
>>> np.column_stack( [[1,2], [1,2]]) #[array1,array2,..] , only 1 positional arg 
array([[1, 1],
       [2, 2]])
#hstack: rowwise append       
>>> np.hstack([[1,2],[1,2]]) #[array1,array2,..] , only 1 positional arg 
array([1, 2, 1, 2])
#vstack: vertically stacking array*
>>> np.vstack([[1,2],[1,2]]) #[array1,array2,..] , only 1 positional arg 
array([[1, 2],
       [1, 2]])
#vertically stacking array*
>>> np.stack([[1,2],[10,11]])
array([[ 1,  2],
       [10, 11]])
#columnwise append 
>>> np.stack([[1,2],[10,11]], axis=1)
array([[ 1, 10],
       [ 2, 11]])    
#rowwise append    
>>> np.concatenate( [[1,2],[3,4]])
array([1, 2, 3, 4])
#vertically stacking array - note each is 2D ie arg is tuple of 2Ds
>>> np.concatenate(( [[1,2],[3,4]] , [[5,6]]  ), axis=0)
array([[1, 2],
       [3, 4],
       [5, 6]])
#2nd array appended columnwise - note each is 2D 
>>> np.concatenate(( [[1,2],[3,4]] , [[5],[6]]  ), axis=1)
array([[1, 2, 5],
       [3, 4, 6]])
#Repeat array to N times       
>>> np.tile([1,2],3)
array([1, 2, 1, 2, 1, 2])
#repeat array to MxN times 
>>> np.tile([1,2],(3,3))
array([[1, 2, 1, 2, 1, 2],
       [1, 2, 1, 2, 1, 2],
       [1, 2, 1, 2, 1, 2]])
#broadcasting 
>>> np.broadcast_to([1,2],(2,2)) #original shape=(2,) => (2,n)
array([[1, 2],
       [1, 2]])
>>> np.broadcast_to([[1,2]],(5,2)) #original shape=(1,2) => (n,2) 
array([[1, 2],
       [1, 2],
       [1, 2],
       [1, 2],
       [1, 2]])
>>> np.broadcast_to([10],(3,3))#original shape=(1,) => (m,n,k,..) 
array([[10, 10, 10],
       [10, 10, 10],
       [10, 10, 10]])
>>> np.broadcast_to(10,(3,3))#original shape=scaler => (m,n,k,..) 
array([[10, 10, 10],
       [10, 10, 10],
       [10, 10, 10]])       

       
       
##numpy.select(condlist, choicelist, default=0)
#if x > 3, then 0, if x>=0 , then x+2 else default =0 
>>> np.select([x > 3, x >= 0], [0, x+2])
array([0, 0, 2, 3, 4, 2, 2, 5, 0, 0, 0, 0, 0])

##numpy.where(condition[, x, y])
#condition : array_like, bool, When True, yield x, otherwise yield y.
#x, y : array_like, optional
#out : ndarray or tuple of ndarrays
#If both x and y are specified, the output array contains elements of x 
#where condition is True, and elements from y elsewhere.
#If only condition is given, return the tuple of indices where condition is True.
 
>>> x = np.arange(9.).reshape(3, 3)
>>> x
array([[ 0.,  1.,  2.],
       [ 3.,  4.,  5.],
       [ 6.,  7.,  8.]])
>>> np.where( x > 5 )
(array([2, 2, 2]), array([0, 1, 2]))     # indices [2,0], [2,1], [2,2] are true
>>> x[np.where( x > 3.0 )]               # Note: result is 1D.
array([ 4.,  5.,  6.,  7.,  8.])
>>> np.where(x < 5, x, -1)               # Note: broadcasting.
array([[ 0.,  1.,  2.],
       [ 3.,  4., -1.],
       [-1., -1., -1.]])

##Array creation routines - Numerical ranges
arange([start,] stop[, step,][, dtype]) 			Return evenly spaced values within a given interval.
linspace(start, stop[, num, endpoint, ...]) 		Return evenly spaced numbers over a specified interval.
logspace(start, stop[, num, endpoint, base, ...]) 	Return numbers spaced evenly on a log scale.
meshgrid(*xi, **kwargs) 							Return coordinate matrices from coordinate vectors.
mgrid 												nd_grid instance which returns a dense multi-dimensional 'meshgrid'.
ogrid 												nd_grid instance which returns an open multi-dimensional 'meshgrid'.


#numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)
>>> np.linspace(2.0, 3.0, num=5)
array([ 2.  ,  2.25,  2.5 ,  2.75,  3.  ])
#numpy.arange([start, ]stop, [step, ]dtype=None)
>>> np.arange(3.0)
array([ 0.,  1.,  2.])
#numpy.logspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None)
#base ** start is the starting value of the sequence.
>>> np.logspace(2.0, 3.0, num=4)
array([  100.        ,   215.443469  ,   464.15888336,  1000.        ])


#meshgrid- It is used to vectorise functions of two variables, so that you can write
x = np.array([1, 2, 3])
y = np.array([10, 20, 30]) 
XX, YY = np.meshgrid(x, y)  #XX is row stack of x, YY is column stack of y 
XX                          #
=> array([[1, 2, 3],
       [1, 2, 3],
       [1, 2, 3]])
YY
=> array([[10, 10, 10],
       [20, 20, 20],
       [30, 30, 30]])


ZZ = XX + YY    #all the combinations of x and y put into the function
ZZ => array([[11, 12, 13],
             [21, 22, 23],
             [31, 32, 33]])



#mgrid and ogrid are helper classes which use index notation 
#without having to use 'linspace'. 
#Note The order in which the output are generated is reversed.
YY, XX = np.mgrid[10:40:10, 1:4]
XX
array([[1, 2, 3],
       [1, 2, 3],
       [1, 2, 3]])
YY
array([[10, 10, 10],
       [20, 20, 20],
       [30, 30, 30]])
ZZ = XX + YY # These are equivalent to the output of meshgrid

YY, XX = numpy.ogrid[10:40:10, 1:4]
XX  #array([[1, 2, 3]])
YY 
array([[10],
       [20],
       [30]])
ZZ = XX + YY # 


##*3D plots 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')  #requires Axes3D
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
ax.set_zlim(-1.01, 1.01)
# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=10)
plt.show()


##*Plot an interpolant to the sine function:
#interp(x, xp, fp[, left, right, period]) 	One-dimensional linear interpolation

x = np.linspace(0, 2*np.pi, 10)
y = np.sin(x)
xvals = np.linspace(0, 2*np.pi, 50)
yinterp = np.interp(xvals, x, y)
import matplotlib.pyplot as plt
plt.plot(x, y, 'o',xvals, yinterp, '-x')
plt.show()


##*numpy.polyfit(x, y, deg, rcond=None, full=False, w=None, cov=False)
#Least squares polynomial fit.
#Fit a polynomial p(x) = p[0] * x**deg + ... + p[deg] of degree deg to points (x, y). 
#Returns a vector of coefficients p that minimises the squared error.


x = np.array([0.0, 1.0, 2.0, 3.0,  4.0,  5.0])
y = np.array([0.0, 0.8, 0.9, 0.1, -0.8, -1.0])
z = np.polyfit(x, y, 3)  #Polynomial coefficients, highest power first,0th index 
>>> z
array([ 0.08703704, -0.81349206,  1.69312169, -0.03968254])
>>> p = np.poly1d(z) #highest power first,0th index 
>>> print(p)
         3          2
0.08704 x - 0.8135 x + 1.693 x - 0.03968
>>> p(0.5)   #evaluate 
0.6143849206349179
>>> p.r #roots
array([6.24151464, 3.08128307, 0.02370685])
#+,-,*,**,/ are overloaded , np.methods() can be called 
>> p**2
poly1d([ 7.57544582e-03, -1.41607878e-01,  9.56497928e-01, -2.76158982e+00,
       2.93122393e+00, -1.34374738e-01,  1.57470396e-03])
>> np.sin(p)
array([ 0.08692719, -0.72669053,  0.99252758, -0.03967213])


#High-order polynomials may oscillate wildly:
p30 = np.poly1d(np.polyfit(x, y, 30))
>>> p30(4)
-0.80000000000000204

#plot 
import matplotlib.pyplot as plt
xp = np.linspace(-2, 6, 100)
_ = plt.plot(x, y, '.', xp, p(xp), '-', xp, p30(xp), '--')
plt.ylim(-2,2)
plt.show()


###Pandas - Quick Intro 

import numpy as np
import pandas as pd


##DF is composed of list of Series with one column is designated as Index 
#Creation 
df1 = pd.DataFrame(np.random.randn(6,4),index=list('abcdef'),columns=list('ABCD'))
#datetime based = 'M', 'D', 'Y','YS','Q','W','H','T'(min),'S'(sec),'ms','us'
dft = pd.DataFrame(np.random.randn(100000,1),
            columns=['A'],index=pd.date_range('20130101',periods=100000,freq='T')) #T=mins
ts = pd.Series(np.random.randn(100000), index=pd.date_range('20130101',periods=100000,freq='T'))
#to convert a string or a Index of string to datetime.datetime object 
#use pd.to_datetime('13000101', format='%Y%m%d')
#special index based access only for DatetimeIndex 
>>> dft.head()
                            A
2013-01-01 00:00:00  2.375359
2013-01-01 00:01:00  0.663875
2013-01-01 00:02:00 -0.534566
2013-01-01 00:03:00  0.172524
2013-01-01 00:04:00  0.502204

from datetime import datetime
#For specific exact datetimeindex for only DF , use df.loc 
dft['2013-01-01 00:00:00'] #ERROR 
dft[datetime(2013, 1, 1)] #equivalent to exact  #ERROR 
#use below 
dft.loc['2013-01-01 00:00:00']
dft.loc[datetime(2013, 1, 1)] 
#note for Series, below works 
ts['2013-01-01 00:00:00']
ts[datetime(2013, 1, 1)]
ts.loc[datetime(2013, 1, 1)]
#for both DF and Series- any partial date string or slice of exact index works 
dft['2013-01-01 00:00:00':'2013-01-01 00:04:00']
dft['2013-1-1']                     #from 2013-01-01 00:00:00 till upto 2013-01-01 23:59:00
dft['2013']                         #Year based , from 2013-01-01 00:00:00 till upto 2013-03-11 10:39:00
dft['2013-1':'2013-2']              #slice, end inclusive 
dft['2013-1':'2013-2-28']           # stop time that includes all of the times on the last day
dft['2013-1':'2013-2-28 00:00:00']  #exact stop time     
dft[datetime(2013, 1, 1):datetime(2013,2,28)] #exact start and stop time 
dft[datetime(2013, 1, 1, 10, 12, 0):datetime(2013, 2, 28, 10, 12, 0)] #exact start and stop time 
#Note the difference, first one is Series, 2nd one is DF 
>>> dft.loc[datetime(2013, 1, 1)]
A    2.375359
Name: 2013-01-01 00:00:00, dtype: float64
>>> dft.loc[[datetime(2013, 1, 1)]]
                   A
2013-01-01  2.375359

#Note 
ts[0]       #first item , scalar 
#but 
dft[0]      #error as for DF, [] includes column label 
dft['A']    #OK 
#but for slicing , works as it is row slicing 
ts[0:5]
dft[0:5]


##If a column is of strings , check string methods 
s = pd.Series(['A', 'B', 'C', 'Aaba', 'Baca', np.nan, 'CABA', 'dog', 'cat'])
dir(s.str)
s.str.lower()

##if column is of datetime , check datetime methods 
s1 = pd.Series(pd.date_range('20130101 09:10:12', periods=4))
dir(s1.dt)
s1.dt.hour

##if column is of type categorical, check category method 
s = pd.Series(["a","b","c","a"], dtype="category")
dir(s.cat)
s.cat.categories
s.cat.rename_categories([1,2,3])

##Column can be plotted 
s1 = pd.Series(pd.date_range('20130101 09:10:12', periods=4))
dir(s1.plot)
s1.plot.line()

##check column(ie Series) methods 
s = pd.Series(pd.RangeIndex(stop=10))#start,stop,step
dir(s)
#for example conversion 
s.astype(str)
s.sum()
#np.methods() can be applied 
np.log(s)
#or arithmatic 
s * 2 
#or logical 
s == 2 



##Check DF methods 
dir(dft)
dft.describe()

##Accessing 
df[column]
    column can be 
        Single column label eg ['City']
        Array of column lables eg ['City', 'City']
        A boolean eg df[df.City == 'Chicago']
        A callable, fn(df):returns_any_from_above eg. df[lambda d: d.City == 'Chicago']
    Can be used for create or update dfi['C'] = dfi['A']
df.column_name
    Only for accessing or update 
    Not for creation of new column, use df['column_name'] style 
    For index column, access always like df.index 
df[row_slice]
    row_slice can be 
        start:stop:step, stop exclusive 
        where start,stop are row index 
    there is no way to get row based on index label
    But for DatetimeIndex, it's possible to access based on datetime index 
df.loc[row,column] 
    label based(both row and column)
    row,column takes 
        A single label, e.g. 5 or 'a', 
        A list or array of labels ['a', 'b', 'c']
        A slice object with labels 'a':'f' (end inclusive)
        A boolean array eg df.A > 0 
        :  means all 
        A Callable fn(df):returns_any_from_above eg. lambda d: d.A > 0 
        For DatetimeIndex, row can be as given in above example 
    Can be used for update eg dfi.loc[:,'C'] = dfi.loc[:,'A']
df.loc[row]
    equivalent to df.loc[row,:]
df.iloc[row,column] 
    index based(both row, column)
    row,column takes 
        An integer e.g. 5
        A list or array of integers [4, 3, 0]
        A slice object with ints 1:7:1 , end exclusive 
        A boolean array*** NOT Implemented *** 
        :  means all 
        A Callable fn(df):returns_any_from_above eg. lambda d: d.A > 0 
    Can be used for update eg dfi.loc[:,'C'] = dfi.loc[:,'A']    
df.iloc[row]
    equivalent to df.iloc[row,:]
df.ix[row,column] 
    For each of row,column ,at first tries label based like df.loc[] 
    if Fails, then tries index based like df.iloc[]
    If the index or column does not have label,then behaves like df.iloc[] always 
    For DatetimeIndex, row can be as given in above example 
df.ix[row]
    equivalent to df.ix[row,:]
    For DatetimeIndex, row can be as given in above example

    
###*pandas- CSV 
pandas.read_csv(filepath_or_buffer, sep=', ', delimiter=None, header='infer', names=None, index_col=None, usecols=None, squeeze=False, prefix=None, mangle_dupe_cols=True, dtype=None, engine=None, converters=None, true_values=None, false_values=None, skipinitialspace=False, skiprows=None, nrows=None, na_values=None, keep_default_na=True, na_filter=True, verbose=False, skip_blank_lines=True, parse_dates=False, infer_datetime_format=False, keep_date_col=False, date_parser=None, dayfirst=False, iterator=False, chunksize=None, compression='infer', thousands=None, decimal=b'.', lineterminator=None, quotechar='"', quoting=0, escapechar=None, comment=None, encoding=None, dialect=None, tupleize_cols=None, error_bad_lines=True, warn_bad_lines=True, skipfooter=0, skip_footer=0, doublequote=True, delim_whitespace=False, as_recarray=None, compact_ints=None, use_unsigned=None, low_memory=True, buffer_lines=None, memory_map=False, float_precision=None)
DataFrame.to_csv(path_or_buf=None, sep=', ', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, mode='w', encoding=None, compression=None, quoting=None, quotechar='"', line_terminator='\n', chunksize=None, tupleize_cols=None, date_format=None, doublequote=True, escapechar=None, decimal='.')

#Example 
iris = pd.read_csv('data/iris.csv')
>>> iris.head()
SepalLength  SepalWidth  PetalLength  PetalWidth         Name
0          5.1         3.5          1.4         0.2  Iris-setosa
1          4.9         3.0          1.4         0.2  Iris-setosa
2          4.7         3.2          1.3         0.2  Iris-setosa
3          4.6         3.1          1.5         0.2  Iris-setosa
4          5.0         3.6          1.4         0.2  Iris-setosa
#Return new DF 
>>> (iris.assign(sepal_ratio = iris['SepalWidth'] / iris['SepalLength']).head())
SepalLength  SepalWidth  PetalLength  PetalWidth         Name  sepal_ratio
0          5.1         3.5          1.4         0.2  Iris-setosa       0.6863
1          4.9         3.0          1.4         0.2  Iris-setosa       0.6122
2          4.7         3.2          1.3         0.2  Iris-setosa       0.6809
3          4.6         3.1          1.5         0.2  Iris-setosa       0.6739
4          5.0         3.6          1.4         0.2  Iris-setosa       0.7200


#Or use function of one argument which is the  DF
>>> iris.assign(sepal_ratio = lambda df: (df['SepalWidth'] /df['SepalLength'])).head()
SepalLength  SepalWidth  PetalLength  PetalWidth         Name  sepal_ratio
0          5.1         3.5          1.4         0.2  Iris-setosa       0.6863
1          4.9         3.0          1.4         0.2  Iris-setosa       0.6122
2          4.7         3.2          1.3         0.2  Iris-setosa       0.6809
3          4.6         3.1          1.5         0.2  Iris-setosa       0.6739
4          5.0         3.6          1.4         0.2  Iris-setosa       0.7200



#Example - limit the DataFrame with a Sepal Length greater than 5, calculate the ratio, and plot:

(iris.query('SepalLength > 5').assign( SepalRatio = lambda df: df.SepalWidth / df.SepalLength,            
                     PetalRatio = lambda df: df.PetalWidth / df.PetalLength)   
                .plot(kind='scatter', x='SepalRatio', y='PetalRatio'))
plt.show()

#Clearly two clusters 
iris_m = iris.assign( SepalRatio = lambda df: df.SepalWidth / df.SepalLength, PetalRatio = lambda df: df.PetalWidth / df.PetalLength) 
iris_m.plot(kind='scatter', x='SepalRatio', y='PetalRatio')

#K-Means - Find those two clusters 
from sklearn.cluster import KMeans
numpy_features = iris_m[ ['SepalRatio','PetalRatio' ]].values
kmeans = KMeans(n_clusters=2, random_state=0).fit(numpy_features)
>>> kmeans.cluster_centers_
array([[0.68569927, 0.16512688],
       [0.46103872, 0.33785156]])
>>> kmeans.labels_  #each point's cluster index 
array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
       0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
       
#Assignment       
iris['sepalRatio'] = iris.SepalWidth / iris.SepalLength
iris.columns
       
#Get the names of the columns
>>> iris.columns
Index(['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth', 'Name','sepalRatio'],
      dtype='object')
      
#Any np.methods() can be used 
>>> np.unique(iris.Name)
array(['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'], dtype=object)      

>>> un = iris.Name.unique()
array(['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'], dtype=object)

#access string column by .str 
dir(iris.Name.str)
iris.Name.str.lower()

>>> np.unique(iris.Name.apply(lambda x: un.tolist().index(x)))
array([0, 1, 2], dtype=int64)
#apply for Series, fn takes each element, for DF, fn takes each col if axis=0 else takes each row if axis=1
iris["target"] = iris.Name.apply(lambda x: un.tolist().index(x))

#Get the first five rows of a column by name
iris['SepalLength'][:5]                     #Series
iris[ [ 'SepalLength', 'SepalWidth'] ][:5]  #DF 


#Create categorical ranges for numerical data. 14 is number of bins
sl_bin = pd.cut(iris['SepalLength'], 14)
sl_bin[:5]

#Look at the frequencies in the ranges created above
pd.value_counts(sl_bin)
sl_bin.value_counts()

#Access through .cat 
iris["category"] = sl_bin
iris.category.cat.categories
#to get index of each bin 
iris.category.cat.rename_categories(range(14))

#first six columns of the first row
#ix like .loc[row,column] , ie label based at first if not then iloc[row,column], index based
iris.ix[0,0:6]

#Order the data by specified column
iris['SepalLength'].sort_values()[:5]

#Sort by a column and that obtain a cross-section of that data , multiple can be given
sorteddata = iris.sort_values(by=['SepalLength', 'PetalLength'])  #DF
sorteddata.ix[:,0:6].head(3)  

#Obtain the first three rows and first three columns of the sorted data
sorteddata.iloc[0:3,0:3]

#Obtain value counts of specific column
iris['PetalLength'].value_counts()

#to obtain the datatype 
iris.dtypes

#Get the unique values for a column by name.
iris['Name'].unique()

#Get a count of the unique values of a column
len(iris['Name'].unique())

#Index into a column and get the first four rows
iris.ix[0:3,'Name']

#Obtain True/False  values which could be used inside iloc, loc etc 
iris.ix[:,'Name'] == 'Iris-setosa'
#Can get any columns , use  | , &, ~ for boolean conjunction, disjunction and inverse 
iris.loc[iris['Name'] == 'Iris-setosa', 'SepalLength']  #Series
iris.ix[iris['Name'] == 'Iris-setosa', 0] #note .iloc with boolean not available 
iris.loc[iris['Name'] == 'Iris-setosa', ['SepalLength','PetalLength']] #DF

#Query the data
qry1 = iris.query('Name == "Iris-setosa"')  #returns DF of original only where cond is valid 
qry1.head(10)

#Check a boolean condition
(iris.ix[:,'SepalLength'] > 4.3).any()


#Return descriptive statistics of the dataset- mean, std etc is calculated for each colu mn
>>> iris.describe()
       SepalLength
count   150.000000
mean      5.843333
std       0.828066
min       4.300000
25%       5.100000
50%       5.800000
75%       6.400000
max       7.900000
>>> iris.Name.describe()
count                 150
unique                  3
top       Iris-versicolor
freq                   50
Name: Name, dtype: object

#Crosstab(frequency) of the data by specified columns (of one column vs another)
pd.crosstab(iris['category'],iris['target']) #DF, multiindex 


#Group data and obtain the mean,
#group by col1 and then col2 and find mean of all other columns
grouped1 = iris.groupby('SepalLength') #single column based
grouped1 = iris.groupby(['SepalLength','PetalLength']) #pandas.core.groupby.DataFrameGroupBy
dir(grouped1)
grouped1.mean()  #DF
grouped1.agg(np.mean) #DF 
grouped1.mean().index #MultiIndex 
grouped1.agg({'SepalWidth':'count', 'PetalWidth':'mean'}) #DF 




##Visualization

#Plot counts of a specified column using Pand as
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns  #install it, pip install seaborn

iris.Name.value_counts().plot(kind='bar')
plt.show()
#with x and y 
iris.plot(x=None, y='SepalWidth', kind='line')
plt.show()
#full DF 
iris.plot( kind='line')
plt.show()
#for sub DF 
iris.iloc[:,0:4].plot(kind='line')
plt.show()
#with groupby 
iris.groupby('Name').plot(kind='line')
plt.show()
#as subplots 
iris.groupby('Name').plot(kind='line', subplots=True)
plt.show()
#for partial DF 
iris.iloc[:,0:5].groupby('Name')['SepalLength'].plot(kind='line', subplots=True)
plt.show()

#Reference of plot 
iris.plot(x=None, y='SepalWidth', kind='line', 
    ax=None, subplots=False, sharex=None, sharey=False, layout=None, 
    figsize=None, use_index=True, title=None, grid=None, legend=True, 
    style=None, logx=False, logy=False, loglog=False, xticks=None, yticks=None, 
    xlim=None, ylim=None, rot=None, fontsize=None, colormap=None, table=False, 
    yerr=None, xerr=None, secondary_y=False, sort_columns=False, **kwds)
#x : label string or position, default None means index 
#y : label string or position, default None, means each column 
#kind:
#line : line plot (default)
#'bar' : iristical bar plot
#'barh' : horizontal bar plot
#'hist' : histogram
#'box' : boxplot
#'kde' : Kernel Density Estimation plot
#'density' : same as 'kde'
#'area' : area plot
#'pie' : pie plot
#'scatter' : scatter plot
#'hexbin' : hexbin plot

#note 
iris.plot(kind='line') 
#is equivalent to 
iris.plot.line()
#and similarly for others 

#with subplots 
#multiple in one plot 
iris.plot(kind='line', y=['SepalLength','PetalLength'] )
#with subplots 
iris.plot(kind='line', y=['SepalLength','PetalLength'], subplots=True )

#Bar plot of median values
iris.groupby('Name')['SepalLength'].agg(np.mean).plot(kind = 'bar')
plt.show()

#Scatter_matrix or sns.pairplot
#hue is categorical data and for each hue, scatter_matrix is done
sns.pairplot(iris.iloc[:,0:5], hue='Name', size=2.5)
plt.show()

from pandas.plotting import scatter_matrix
scatter_matrix(iris.iloc[:,0:4], alpha=0.2, figsize=(6, 6), diagonal='kde')
plt.show()
#for only one Name 
scatter_matrix(iris.ix[iris.Name=='Iris-virginica',0:4], alpha=0.2, figsize=(6, 6), diagonal='kde')
plt.show()
#only density plot 
iris.SepalLength.plot.kde()
plt.show()
#or 
sns.kdeplot(iris.SepalLength)
sns.kdeplot(iris.SepalWidth)
plt.show()
#or
sns.distplot(iris.SepalLength)
plt.show()
#for bivariate kernel density estimate
sns.kdeplot(iris.iloc[:,0:4]) #bivariate kernel density estimate
plt.show()
#joint distribution of x,y and the marginal distributions (joit distribution with one const)
#For this plot, we'll set the style to a white background
#pearsonr = correlation coefficient  , -1 to 1, 0= not correlated, H0:not correlated 
#kind : { “scatter” | “reg” | “resid” | “kde” | “hex” }, optional
with sns.axes_style('white'):
    sns.jointplot(x="SepalLength", y="PetalLength", data=iris.iloc[:,0:4], kind='kde');

plt.show()

#Box plot - x= x axis categorical data, y= box plot variable  , hue=categorical data, for each, x vs y box plot is done 
#box plot - box-25%,median, 75%(third quartiles), min-max data - some convention of min and max - https://en.wikipedia.org/wiki/Box_plot, outliers
#seaborn.factorplot(x=None, y=None, hue=None, data=None, row=None, col=None, col_wrap=None, estimator=<function mean>, ci=95, n_boot=1000, units=None, order=None, hue_order=None, row_order=None, col_order=None, kind='point', size=4, aspect=1, orient=None, color=None, palette=None, legend=True, legend_out=True, sharex=True, sharey=True, margin_titles=False, facet_kws=None, **kwargs)
#kind : {point, bar, count, box, violin, strip}
#check pallet- https://seaborn.pydata.org/tutorial/color_palettes.html
import seaborn as sns
g = sns.factorplot(x="Name", y="PetalLength", hue="Name" ,data=iris.iloc[:,0:5], kind="box", palette="PRGn",aspect=2.25)
g.set(ylim=(0, 10))
plt.show()

#Barplot 
g = sns.factorplot(x="Name", data=iris.iloc[:,0:5], aspect=2,  kind="count", color='steelblue')




       
       
       
       
 




###*EXCEl: xlrd is required for pandas.read_excel 
pandas.read_excel(io, sheet_name=0, header=0, skiprows=None, skip_footer=0, index_col=None, names=None, usecols=None, parse_dates=False, date_parser=None, na_values=None, thousands=None, conirist_float=True, coniristers=None, dtype=None, true_values=None, false_values=None, engine=None, squeeze=False, **kwds)
    df = pd.read_excel("file_name", 'Sheet1') #needs xlrd
    #for example setting correct index from one column, if datetime, use to_datetime
    df.index = pd.to_datetime(df.Date)
DataFrame.to_excel(excel_writer, sheet_name='Sheet1', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, startrow=0, startcol=0, engine=None, merge_cells=True, encoding=None, inf_rep='inf', irisbose=True, freeze_panes=None)
pandas.to_datetime(arg, errors='raise', dayfirst=False, yearfirst=False, utc=None, box=True, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix')[source]
    Convert argument to datetime.
    arg : integer, float, string, datetime, list, tuple, 1-d array, Series
    #common format 
    %w  Weekday as a decimal number, where 0 is Sunday and 6 is Saturday. 0, 1, …, 6   
    %d  Day of the month as a zero-padded decimal number. 01, 02, …, 31 
    %b  Month as locale's abbreviated name. Jan, Feb, …, Dec (en_US);
    %B  Month as locale's full name. January, February, …, December (en_US);
    %m  Month as a zero-padded decimal number. 01, 02, …, 12   
    %y  Year without century as a zero-padded decimal number. 00, 01, …, 99   
    %Y  Year with century as a decimal number. 1970, 1988, 2001, 2013   
    %H  Hour (24-hour clock) as a zero-padded decimal number. 00, 01, …, 23   
    %I  Hour (12-hour clock) as a zero-padded decimal number. 01, 02, …, 12   
    %p  Locale's equivalent of either AM or PM. AM, PM (en_US);
    %M  Minute as a zero-padded decimal number. 00, 01, …, 59   
    %S  Second as a zero-padded decimal number. 00, 01, …, 59 
    %f  Microsecond as a decimal number, zero-padded on the left. 000000, 000001, …, 999999 
    %z  UTC offset in the form +HHMM or -HHMM (empty string if the the object is naive). (empty), +0000, -0400, +1030 
    %Z  Time zone name (empty string if the object is naive). (empty), UTC, EST, CST   
    %j  Day of the year as a zero-padded decimal number. 001, 002, …, 366   
    %U  Week number of the year (Sunday as the first day of the week) as a zero padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0. 00, 01, …, 53 
    %W  Week number of the year (Monday as the first day of the week) as a decimal number. All days in a new year preceding the first Monday are considered to be in week 0. 00, 01, …, 53 

#Example  
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import statsmodels.api as sm 

dft = pd.read_excel(r"data\Nifty-17_Years_Data-V1.xlsx", parseDates=True, index_col=0, header=0, date_parser=lambda x: pd.to_datetime(x, format="%d-%b-%y"))
dft.index
>> df.head()

from pandas.tseries.offsets import *
dft.index.freq = Day() #set freq as D 

import datetime
#For specific exact index for DF , use .loc 
dft['2000-06-01'] #ERROR 
dft[datetime.date(2000, 6, 1)] #equivalent to exact  #ERROR #datetime.date(year, month, day)
#use below 
dft.loc['2000-06-01']
dft.iloc[0]
dft.loc[datetime.date(2000, 6, 1)] 
#for both DF and Series- any partial date string or slice of exact index works 
dft['2000-06-01']             #from 2013-01-01 00:00:00 till upto 2013-01-01 23:59:00
dft['2013']                 #Year based , from 2013-01-01 00:00:00 till upto 2013-03-11 10:39:00
dft['2013-1':'2013-2']      #slice, end inclusive 
dft['2013-1':'2013-2-28']   # stop time that includes all of the times on the last day
dft['2013-1':'2013-2-28 00:00:00'] #exact stop time     
dft[datetime.date(2013, 1, 1):datetime.date(2013,2,28)] #exact start and stop time 
dft[datetime.datetime(2013, 1, 1, 10, 12, 0):datetime.datetime(2013, 2, 28, 10, 12, 0)] #exact start and stop time 
#Note the difference, first one is Series, 2nd one is DF 
>>> dft.loc[datetime.date(2013, 1, 1)]
A    2.375359
Name: 2013-01-01 00:00:00, dtype: float64
>>> dft.loc[[datetime.date(2013, 1, 1)]]
                   A
2013-01-01  2.375359

#Note 
ts[0] #first item , scalar 
#but 
dft[0] #error as for DF, [] includes column label 
dft['Open'] #OK 
#but for slicing , works as it is row slicing 
ts[0:5]
dft[0:5]


#plot 
dft.plot(kind='line', subplots=True)
plt.show()
dft.Close.plot(kind='line')
plt.show()


#complex plot 
#4x4 gridspecs, specification for 0,0 cell , row spanning 3 rows, column spanning 4 columns 
top = plt.subplot2grid((4,4), (0, 0), rowspan=3, colspan=4)
top.plot(dft.index, dft["Close"])
plt.title('Nifty close from 2000 - 2018')

#4x4 gridspecs, specification for 3,0 cell , row spanning 1 rows, column spanning 4 columns 
bottom = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4)
bottom.bar(dft.index, dft['Day Wise Variation ( points) '])
plt.title('Nifty Day wise variations ')

plt.show()

#(for Time series, equivalent to aggregation)
#Calculate moving airisages
#window : int,Size of the moving window. 
#This is the number of observations used for calculating the statistic.
dft_r = dft.rolling(30)  #rolling 30 samples 
dir(dft_r)
#plot rolling average 
dft_r.mean()['Open'] #DF 
dft_r.mean().dropna().plot(kind='line') #DF
plt.show()
#
dft_s = dft.ewm(com=0.5)#Returns Exponentially-weighted moving window(EWM) class ,com=decay in terms of center of mass
#
dft_s = dft.expanding(2) #Expanding window, Minimum number of observations in window required to have a value         (otherwise result is NA)
#or downsampling at month 
dft_s = dft.resample('M')
dir(dft_s)
#month value would be mean()
dft_s.mean() #DF 
dft_s['Open'].mean() #Series
dft_s['Open'].agg([np.sum, np.mean, np.std])
dft_s.agg({'Open':'mean', 'Close':'std'})
dft_s.agg({'Open':['mean',np.std], 'Close':['std','sum']})

#KDE plot
dft_s.Close.plot(kind='kde')

#lagplot -Lag plots are used to check if a data set or time series is random. 
#Random data should not exhibit any structure in the lag plot. 
#Non-random structure implies that the underlying data are not random.
from pandas.plotting import lag_plot
lag_plot(df.Close)
plt.show()


##Autocorrelation plots are often used for checking randomness in time series
#If time series is random, such autocorrelations should be near zero for  all time-lag separations(other than lag=0)
from pandas.plotting import autocorrelation_plot
autocorrelation_plot(df.Close)

##Time Series analysis - statsmodel 
import statsmodels.api as sm
import statsmodels.tsa.api as smt
##Checking stationary 
#constant mean
#constant variance
#an autocovariance that does not depend on time
#run plot 
ts = dft.Close 

#clearly shows overall increasing trend 
ts.plot(kind='line')
plt.show()

#further checking of stationary 
#rolling statistics plots - ever increasing 
#and  Dickey-Fuller test - adfuller
#H0: TS is non-stationary


def test_stationarity(timeseries):    
    #Determing rolling statistics
    rolmean = timeseries.rolling(window=12, center=False).mean()
    rolstd = timeseries.rolling(window=12, center=False).std()
    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)
    #Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = smt.adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)
    

>>> test_stationarity(ts)  
#variation in standard deviation is small, mean is clearly increasing with time 
#p-value>0.05, hence accept H0(=TS is non-stationary)
Results of Dickey-Fuller Test:
Test Statistic                    0.411488
p-value                           0.981920
#Lags Used                       14.000000
Number of Observations Used    4370.000000
Critical Value (10%)             -2.567122
Critical Value (5%)              -2.862202
Critical Value (1%)              -3.431847
dtype: float64


##How to make a Time Series Stationary?
#Reasons for nonstionary 
#1. Trend – varying mean over time. 
#    In this case, average mean increasing over time 
#2. Seasonality – variations at specific time-frames. 
#    eg people might have a tendency to buy cars in a particular month 
#    because of pay increment or festivals.

#First option for reducing increasing trend  - Tranformation 
#eg log, sqrt or cube root to dampen the trend 
#for decreasing trend, exp, square, cube etc 
ts_log = np.log(ts)
plt.plot(ts_log)
plt.show()


##Eliminating Trend and Seasonality
#Differencing – taking the differece with a particular time lag
#Decomposition – modeling both trend and seasonality and removing them from the model.

##Eliminating both Trend and Seasonality - Differencing
ts_log_diff = ts_log - ts_log.shift(1)
#or 
ts_log_diff = ts_log.diff(periods=1) #Periods to shift for forming difference

ts_log_diff.dropna(inplace=True)
>>> test_stationarity(ts_log_diff)
Results of Dickey-Fuller Test:
Test Statistic                -1.445462e+01
p-value                        7.006666e-27
#Lags Used                     1.900000e+01
Number of Observations Used    4.364000e+03
Critical Value (10%)          -2.567123e+00
Critical Value (5%)           -2.862203e+00
Critical Value (1%)           -3.431849e+00
dtype: float64

#Note 2nd differencing is extremly rare , DOn't use 
ts_log_diff2 = ts_log_diff - ts_log_diff.shift(1)
#or 
ts_log_diff2 = ts_log_diff.diff(1) #Note, it is not ts_log.diff(periods=2), which is diff with every 2nd period 

ts_log_diff2.dropna(inplace=True)
>>> test_stationarity(ts_log_diff2)
Results of Dickey-Fuller Test:
Test Statistic                -8.196629e+00
p-value                        7.419305e-13
#Lags Used                     1.300000e+01
Number of Observations Used    1.280000e+02
Critical Value (1%)           -3.482501e+00
Critical Value (10%)          -2.578960e+00
Critical Value (5%)           -2.884398e+00
dtype: float64


##Eliminating both Trend and Seasonality - Decomposing
#In this approach, both trend and seasonality are modeled separately 
#and the remaining part of the series is returned
'''
Arg freq : int, optional
        Frequency of the series. Must be used if x is not a pandas object. 
        Overrides default periodicity of x 
        if x is a pandas object with a timeseries index.
            #freqstr      Seasonal period    # of datapoints for aggregation
            A              1                 aggregate yearly 
            Q              4                 aggregate yearly 
            M              12                aggregate yearly
            W              52                aggregate yearly
            D              7                 aggregate weekly 
            B              5                 aggregate weekly 
            H              24                aggregate daily 
'''

from statsmodels.tsa.seasonal import seasonal_decompose

decomposition = seasonal_decompose(ts_log, freq=7) 
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid  #we need to work with this series further 
decomposition.plot()
plt.show()

#Get stats 
ts_log_decompose = residual
ts_log_decompose.dropna(inplace=True)
>>> test_stationarity(ts_log_decompose)
Test Statistic                  -18.851623
p-value                           0.000000
#Lags Used                       30.000000
Number of Observations Used    4348.000000
Critical Value (10%)             -2.567124
Critical Value (5%)              -2.862205
Critical Value (1%)              -3.431855
dtype: float64

##Forecasting a Time Series
#Use differencingfor making stationary 

#ACF and PACF plots:
#p – The lag value where the PACF chart crosses the upper confidence interval for the first time. 
#     If you notice closely, in this case p=1.
#q – The lag value where the ACF chart crosses the upper confidence interval for the first time. 
#     If you notice closely, in this case q=1.


#below line must, must not contain NaN 
ts_log_diff.dropna(inplace=True)

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
sm.graphics.tsa.plot_acf(ts_log_diff, lags=40, ax=ax1,alpha=0.05) #confidence level 95%
ax2 = fig.add_subplot(212)
sm.graphics.tsa.plot_pacf(ts_log_diff, lags=40, ax=ax2,alpha=0.05)
plt.show()

#or 
#x13 - 
import pandas as pd
df = pd.DataFrame(ts_log, index=dft.index)
#Requires x13as.exe in PATH , Only monthly and quarterly periods are supported
#download from https://www.census.gov/srd/www/winx13/winx13_down.html
import statsmodels
res = statsmodels.tsa.x13.x13_arima_select_order(df.resample('M').mean())
>>> res.order
(0, 1, 1)

#or 
ts_log_diff.dropna(inplace=True) #note if input contains nan, Error would happen 
res = sm.tsa.arma_order_select_ic(ts_log_diff, ic=['aic', 'bic'], trend='nc') #nc - no constant term
res.aic_min_order #(p,q) = (3, 2)
res.bic_min_order #(0, 1)
>>> res
{'bic_min_order': (0, 1), 'bic':               0             1             2
0           NaN -24712.161789 -24711.432984
1 -24709.468202 -24709.834026 -24703.079027
2 -24711.557674 -24703.279453 -24696.956015
3 -24703.333590 -24696.489131 -24696.783230
4 -24695.555535 -24687.204379           NaN, 'aic':               0
1             2
0           NaN -24724.933223 -24730.590135
1 -24722.239636 -24728.991176 -24728.621895
2 -24730.714824 -24728.822320 -24728.884599
3 -24728.876458 -24728.417715 -24735.097531
4 -24727.484119 -24725.518680           NaN, 'aic_min_order': (3, 2)}


#Fit now 
#since 1st order differntiation is done, hence d= 1
from statsmodels.tsa.arima_model import ARIMA

fig = plt.figure(figsize=(12,8))
#AR Model
model = ARIMA(ts_log, order=(1, 1, 0))  
results_AR = model.fit(disp=-1)   #disp:If True, convergence information is output.
ax1 = fig.add_subplot(311)
ax1.plot(ts_log_diff)
ax1.plot(results_AR.fittedvalues, color='red')
ax1.set_title('RSS: %.4f'% sum((results_AR.fittedvalues-ts_log_diff)**2))

#MA Model
model = ARIMA(ts_log, order=(0, 1, 1))  
results_MA = model.fit(disp=-1)  
ax2 = fig.add_subplot(312)
ax2.plot(ts_log_diff)
ax2.plot(results_MA.fittedvalues, color='red')
ax2.set_title('RSS: %.4f'% sum((results_MA.fittedvalues-ts_log_diff)**2), x=0.4)

#ARIMA 
model = ARIMA(ts_log, order=(1, 1, 1))  
results_ARIMA = model.fit(disp=-1)  
ax3 = fig.add_subplot(313)
ax3.plot(ts_log_diff)
ax3.plot(results_ARIMA.fittedvalues, color='red') #fittedvalues  is after differencing, d=1
ax3.set_title('RSS: %.4f'% sum((results_ARIMA.fittedvalues-ts_log_diff)**2), x=0.4)

plt.show()

#Note - all below are after differencing d=1
>>> ts_log_diff[1:5]  #with d=1 
Date
2000-06-02    0.029400
2000-06-05    0.010989
2000-06-06    0.012136
2000-06-07    0.006031
Name: Close, dtype: float64
>>> results_ARIMA.fittedvalues[0:4]  #with d=1 
Date
2000-06-02    0.000470
2000-06-05    0.002797
2000-06-06    0.000337
2000-06-07    0.001505
dtype: float64
>>> results_ARIMA.predict(start=1,end=4)  #in place , with d=1 
Date
2000-06-02    0.000470
2000-06-05    0.002797
2000-06-06    0.000337
2000-06-07    0.001505
dtype: float64
#out of sample prediction 
>>> results_ARIMA.predict(start=len(ts_log)-1, end=len(ts_log)+5)
4384    0.001018
4385    0.000623
4386    0.000416
4387    0.000488
4388    0.000463
4389    0.000472
4390    0.000469
dtype: float64

>>> results_ARIMA.forecast(steps=5)[0] #without d=1 , returns forecast,stderr, confInterval
array([9.26534234, 9.26575853, 9.26624702, 9.2667102 , 9.26718224])
>>> ts_log[-1]
9.2647196498149

#get summary 
results_ARIMA.summary()
#predict , next 20 values 
steps=20
predict_arima = results_ARIMA.forecast(steps=steps) #without d=1 , returns forecast,stderr, confInterval




##Taking it back to original scale
index = pd.date_range(ts.index[-1], periods=steps+1)[-steps:]
predictions_ARIMA_log = pd.Series(predict_arima[0], copy=True, index=index)
predictions_ARIMA_diff_orig = pd.Series(results_ARIMA.fittedvalues, copy=True)


#we took a lag by 1  for differencing 
#To undo, first determine the cumulative sum at index 
#add it to first value 
predictions_ARIMA_log_orig = predictions_ARIMA_diff_orig.cumsum() + ts_log.ix[0]


#and then anti-log 
predictions_ARIMA = np.exp(predictions_ARIMA_log)
predicted = np.exp(predictions_ARIMA_log_orig.append(predictions_ARIMA_log) ) 

plt.plot(ts)
plt.plot(predicted)
#use ts[1:] because predictions_ARIMA_log_orig does not initial d samples 
plt.title('RMSE: %.4f'% np.sqrt(sum((np.exp(predictions_ARIMA_log_orig)-ts[1:])**2)/len(ts[1:])))
plt.show()


