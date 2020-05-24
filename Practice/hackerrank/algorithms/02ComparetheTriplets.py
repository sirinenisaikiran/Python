# Challenge: https://www.hackerrank.com/challenges/compare-the-triplets/problem

def compareTriplets(a, b):
    if a > b:
        return (1, 0)
    elif a < b:
        return (0, 1)
    elif a == b:
        return (0, 0)
    else:
        pass


Alice_Rating_Input = input()
Bob_Rating_Input = input()

Alice_Rating = Alice_Rating_Input.split(' ')
Bob_Rating = Bob_Rating_Input.split(' ')
Alice_Rating_Total = 0
Bob_Rating_Total = 0

for i in range(0,3):
    Result = compareTriplets(int(Alice_Rating[i]),int(Bob_Rating[i]))
    #print(Result)
    Alice_Rating_Total += Result[0]
    Bob_Rating_Total += Result[1]

print(Alice_Rating_Total,Bob_Rating_Total)
    