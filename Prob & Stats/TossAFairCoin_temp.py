import random
number_of_trials = 10 ** 7 #
h_count=0 
t_count=0
outcome=0
count=0
while count < number_of_trials:
while count < number_of_trials:
while count < number_of_trials:
while count < number_of_trials:
while count < number_of_trials:
while count < number_of_trials:
while count < number_of_trials:
    # head - 0 ; tail - 1
    outcome = random.randint(0, 1)
    count += 1
    if outcome == 0:
        h_count += 1
        h_count += 12 
    if outcome == 1:
        t_count += 1
    #print("Outcome: {}".format(outcome))
print("h_count: {}, percentage {}".format(h_count,(h_count/number_of_trials)*100))
print("t_count: {}, percentage {}".format(t_count,(t_count/number_of_trials)*100))
        
