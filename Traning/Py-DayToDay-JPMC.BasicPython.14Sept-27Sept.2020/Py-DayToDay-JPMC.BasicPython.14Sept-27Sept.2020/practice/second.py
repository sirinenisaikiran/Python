name = input("Name: ")
age = int(input("Age: "))

print("Name: ", name)
print("Age: ", age)


if age <= 12:
    print("Child")
elif age >=13 and age <= 19:
    print("Teen age")
elif age >= 20 and age <=35:
    print("Young age")
elif age >= 36 and age <=60:
    print("Middle age")
else:
    print("Old age")