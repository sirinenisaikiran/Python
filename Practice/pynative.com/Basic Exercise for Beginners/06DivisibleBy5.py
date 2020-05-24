# Question 6: Given a list of numbers, Iterate it and print only those numbers which are divisible of 5

# Expected Output:

# Given list is  [10, 20, 33, 46, 55]
# Divisible of 5 in a list
# 10
# 20
# 55
print("""
List you enter should have number seperated by ",".
example:
Enter list: 1,2,3,4,5
""")
String = input("Enter list: ")
List = String.split(',')
print("Given list is  ",List)
print("Divisible of 5 in a list")
for num in List:
    if int(num) % 5 == 0:
        print(num)


# List you enter should have number seperated by ",".
# example:
# Enter list: 1,2,3,4,5

# Enter list: 10,20,33,46,55
# Given list is   ['10', '20', '33', '46', '55']
# Divisible of 5 in a list
# 10
# 20
# 55