# Question 7: Return the total count of string “Emma” appears in the given string

# Given string is “Emma is good developer. Emma is a writer”

# Expected Output:

# Emma appeared 2 times

String = input("Enter a sentance: ")
Word = input("Enter a word: ")

List = String.split(' ')
count = 0
for st in List:
    if st.upper() == Word.upper():
        count += 1
print (Word," appeared ",count,"times")



# F:\Python\Practice>python 07WordAppearsInTheGivenString.py
# Enter a sentance: Apple i a fruite and apple is a company as well
# Enter a word: apple
# apple  appeared  2 times