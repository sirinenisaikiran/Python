# Challenge: https://www.hackerrank.com/challenges/polar-coordinates/problem
import cmath

complex_str = input()

if complex_str.count('+') == 1 or (complex_str.count('-') == 1 and complex_str.index('-') == 0):
    x = complex_str.split('+')[0]
    y = complex_str.split('+')[1].replace('j','')
    x, y = int(x), int(y)
elif complex_str.count('-') == 1 and complex_str.index('-') != 0:
    x = complex_str.split('-')[0]
    y = complex_str.split('-')[1].replace('j','')  
    x, y = int(x) , int(y) * -1
elif complex_str.count('-') == 2:
    x = complex_str.split('-')[1]
    y = complex_str.split('-')[2].replace('j','')  
    x, y = int(x) * -1, int(y) * -1



#print(complex(x,y))
print(abs(complex(x,y)))
print(cmath.phase(complex(x,y)))
