# Question 1: Accept two integer numbers from a user and return their product and  if the product is greater than 1000, then return their sum

# Expected Output:
# ------------------
# Enter first number 10
# Enter second number 20
# The result is 200

a,b = input("Enter first number: "), input("Enter second number: ")
a,b = int(a), int(b)
# print(a)
# print(b)
print("product of a & b is", a * b)
if a * b > 1000:
    print("sum of a & b is", a + b)
