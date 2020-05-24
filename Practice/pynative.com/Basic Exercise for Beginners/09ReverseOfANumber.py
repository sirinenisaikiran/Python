# Question 9: Reverse a given number and return true if it is the same as the original number

# Expected Output:

# original number 121
# The original and reverse number is the same: True
# original number 125
# The original and reverse number is the same: False
# True

number = input("Enter the number: ")
number = str(number)
rev_number = number[::-1]

print("original number ",number)
if number == rev_number:
    print("The original and reverse number is the same: True")
else:
    print("The original and reverse number is the same: False")


# F:\Python\Practice>python 09ReverseOfANumber.py
# Enter the number: 12321
# original number  12321
# The original and reverse number is the same: True

# F:\Python\Practice>python 09ReverseOfANumber.py
# Enter the number: 12345
# original number  12345
# The original and reverse number is the same: False
    