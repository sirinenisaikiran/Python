# Exercise Question 1: Accept two numbers from the user and calculate multiplication

num1 = input("Enter number one: ")
num1 = int(num1)
num2 = input("Enter number two: ")
num2 = int(num2)

def Multiplication(i,j):
    return i * j
    
print("Number one:",num1)
print("Number two:",num2)
print("Multiplication of",num1,"and",num2,"is ",Multiplication(num1,num2))

# F:\Python\Practice\pynative.com\Python Input and Output Exercise>python 01MultiplicationOfTwoNumbers.py
# Enter number one: 10
# Enter number two: 12
# Number one: 10
# Number two: 12
# Multiplication of 10 and 12 is  120

# F:\Python\Practice\pynative.com\Python Input and Output Exercise>python 01MultiplicationOfTwoNumbers.py
# Enter number one: 123456789
# Enter number two: 987654321
# Number one: 123456789
# Number two: 987654321
# Multiplication of 123456789 and 987654321 is  121932631112635269