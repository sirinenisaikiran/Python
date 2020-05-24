# Question 3: Accept string from a user and display only those characters which are present at an even index number.

# For example str = "pynative" so you should display ‘p’, ‘n’, ‘t’, ‘v’.

# Expected Output:

# Enter String  pynative
# Orginal String is  pynative
# Printing only even index chars
# index[ 0 ] p
# index[ 2 ] n
# index[ 4 ] t
# index[ 6 ] v

STRING = input("Enter String: ")
print("Orginal String is  ",STRING)
print("Printing only even index chars")
for i in range(0,len(STRING)):
    if i % 2 == 0:
        print("index[",i,"] ",STRING[i])


# F:\Python\Practice>python 03PrintEvevnIndexChar.py
# Enter String: sirineni shireesha saikiran
# Orginal String is   sirineni shireesha saikiran
# Printing only even index chars
# index[ 0 ]  s
# index[ 2 ]  r
# index[ 4 ]  n
# index[ 6 ]  n
# index[ 8 ]
# index[ 10 ]  h
# index[ 12 ]  r
# index[ 14 ]  e
# index[ 16 ]  h
# index[ 18 ]
# index[ 20 ]  a
# index[ 22 ]  k
# index[ 24 ]  r
# index[ 26 ]  n