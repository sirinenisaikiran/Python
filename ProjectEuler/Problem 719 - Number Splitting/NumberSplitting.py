# Challenge: https://projecteuler.net/problem=719
import math

def split_combinations(n):


        
        
        


def Is_n_a_S(n):
    split_combinations(n)

    
    
        
if __name__ == '__main__':
    N = int(input())
    Sum = 0
    #count = 0
    for n in range(4,N+1):
        sqrt_of_n = math.sqrt(n)
        if sqrt_of_n - math.floor(sqrt_of_n) == 0:
            #count += 1
            #print("{}:{} - {}".format(count,n,sqrt_of_n))
            if Is_n_a_S(n) == True:
                Sum += n
    print("count = {}" .format(count))
    print(Sum)
            