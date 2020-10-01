import random

def split_combinations(n):
    l = [int(i) for i in str(n)]
    comb = []
    for r in range(len(l)):
        random.shuffle(l)
        if l in comb:
            pass
        else:
            comb.append(l)
    return comb

print(split_combinations(41))