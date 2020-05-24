# Question 5: Given a list of numbers, return True if first and last number of a list is same

# Expected Output:

# Given list is  [10, 20, 30, 40, 10]
# result is True
# Given list is  [10, 20, 30, 40, 50]
# result is False

input("""***********************
Enter number "," seperated
Exampple: 
Enter list: 1,2,3,4,5
***********************\n""")
STRTING = input("Enter list: ")
list = STRTING.split(',')
print("Given list is  ",list)
if list[0] == list [-1]:
    print("result is True")
else:
    print("result is False")
    
    

# F:\Python\Practice>python 05ListOfNumber.py
# ***********************
# Enter number "," seperated
# Exampple:
# Enter list: 1,2,3,4,5
# ***********************

# Enter list: 1,2,3,4,1
# Given list is   ['1', '2', '3', '4', '1']
# result is True

# F:\Python\Practice>python 05ListOfNumber.py
# ***********************
# Enter number "," seperated
# Exampple:
# Enter list: 1,2,3,4,5
# ***********************

# Enter list: 1,2,3,4,5
# Given list is   ['1', '2', '3', '4', '5']
# result is False