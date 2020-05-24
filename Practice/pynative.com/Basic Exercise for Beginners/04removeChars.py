# Question 4: Given a string and an integer number n, remove characters from a string starting from zero up to n and return a new string

# For example, removeChars("pynative", 4) so output must be tive. Note: n must be less than the length of the string.

string , num = input("Enter string :"), int(input("Enter number: "))
print(string[num:])

# F:\Python\Practice>python 04removeChars.py
# Enter string :pynative
# Enter number: 4
# tive

# F:\Python\Practice>python 04removeChars.py
# Enter string :saikiran
# Enter number: 3
# kiran