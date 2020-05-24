# Challenge: https://www.hackerrank.com/challenges/a-very-big-sum/problem

def aVeryBigSum(a):
    sum = 0
    Array = a
    for i in Array:
        sum += int(i)
    return sum

num = input()
numbers = input()
number_list = numbers.split(' ')
if len(number_list) != int(num):
    print("Not ",num," number of intergers enter")
sum_of_nums = aVeryBigSum(number_list)

print(sum_of_nums)