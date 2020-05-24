# Exercise Question 2: Display “My Name Is James” as “My**Name**Is**James” using output formatting of a print() function

# Expected Output:

# Use print() statement formatting to display ** separator between each word.

# For example: print('My', 'Name', 'Is', 'James') will display MyNameIsJames

# So use one of the formatting argument of print() to turn the output into My**Name**Is**James


#******************* One possibility *********************************************
# String = "My Name Is James"
# Str_List = String.split(' ')
# Str_output = ''
# for st in Str_List:
    # Str_output += st
    # Str_output += "**"
# print(Str_output)

# F:\Python\Practice\pynative.com\Python Input and Output Exercise>python 02PrintFormatedOutput.py
# My**Name**Is**James**
#*********************************************************************************

print(f'My{"*"*2}Name{"*"*2}Is{"*"*2}James')

print('My', 'Name', 'Is', 'James', sep='**')


# F:\Python\Practice\pynative.com\Python Input and Output Exercise>python 02PrintFormatedOutput.py
# My**Name**Is**James
# My**Name**Is**James
