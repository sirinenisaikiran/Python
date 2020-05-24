# Challenge: https://www.hackerrank.com/contests/hack-the-interview-global/challenges/high-security-strings

password = input()
weight_a = int(input())
atoz_dict = {}

weight_of_password = 0
for i in range(97,123):
    atoz_dict[chr(i)] = weight_a
    weight_a += 1
    if weight_a == 26:
        weight_a = 0
#print(atoz_dict)

for p in password:
    weight_of_password += atoz_dict[p]
print(weight_of_password)
    
