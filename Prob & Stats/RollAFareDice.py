import random
number_of_trials = 10 ** 6
one_count=0 
two_count=0
three_count=0 
four_count=0
five_count=0 
six_count=0
coutcome=0
count=0
while count < number_of_trials:
    # head - 0 ; tail - 1
    outome = random.randint(1, 6)
    count += 1
    if outome == 1: one_count += 1
    if outome == 2: two_count += 1
    if outome == 3: three_count += 1
    if outome == 4: four_count += 1
    if outome == 5: five_count += 1
    if outome == 6: six_count += 1
print("one_count: {}, percentage {}".format(one_count,(one_count/number_of_trials)*100))
print("two_count: {}, percentage {}".format(two_count,(two_count/number_of_trials)*100))
print("three_count: {}, percentage {}".format(three_count,(three_count/number_of_trials)*100))
print("four_count: {}, percentage {}".format(four_count,(four_count/number_of_trials)*100))
print("five_count: {}, percentage {}".format(five_count,(five_count/number_of_trials)*100))
print("six_count: {}, percentage {}".format(six_count,(six_count/number_of_trials)*100))



# F:\Programming\Python\Prob & Stats>python RollAFailDice.py
# one_count: 16667045, percentage 16.667044999999998
# two_count: 16668182, percentage 16.668182
# three_count: 16671245, percentage 16.671245000000003
# four_count: 16665032, percentage 16.665032
# five_count: 16667642, percentage 16.667642
# six_count: 16660854, percentage 16.660854
        