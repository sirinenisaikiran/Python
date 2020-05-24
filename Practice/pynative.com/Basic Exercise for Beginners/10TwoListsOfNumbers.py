# Question 10: Given a two list of numbers create a new list such that new list should contain only odd numbers from the first list and even numbers from the second list

# Expected Output:

# First List  [10, 20, 23, 11, 17]
# Second List  [13, 43, 24, 36, 12]
# result List is [23, 11, 17, 24, 36, 12]

Fist_List = [10, 20, 23, 11, 17]
Second_List = [13, 43, 24, 36, 12]
Result_List = []

for i in Fist_List:
    if i % 2 != 0:
        Result_List.append(i)

for i in Second_List:
    if i % 2 == 0:
        Result_List.append(i)
print("First List ",Fist_List)
print("Second List ",Second_List)
print("result List is ",Result_List)

# F:\Python\Practice>python 10TwoListsOfNumbers.py
# First List  [10, 20, 23, 11, 17]
# Second List  [13, 43, 24, 36, 12]
# result List is  [23, 11, 17, 24, 36, 12]
