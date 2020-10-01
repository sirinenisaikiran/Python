def split(n):
    Lst = []
    if len(str(n)) == 2:
        return str(n)[0],str(n)[1]
    if len(str(n)) > 2:
        # Lst.append(str(n))
        # Lst.append((str(n)[0], str(n)[1:]))
        # Lst.append((str(n)[0], split(int(str(n)[1:]))))
        # Lst.append((str(n)[0:-1], str(n)[-1]))
        # Lst.append((split(int(str(n)[0:-1])), str(n)[-1]))
        return str(n),(str(n)[0], str(n)[1:]),(str(n)[0], split(int(str(n)[1:]))),(str(n)[0:-1], str(n)[-1]),(split(int(str(n)[0:-1])), str(n)[-1])
        #return Lst
def get_comb(x):
    if x is str:
        return x
    elif x is tuple:
        for y in x:
            

num = 6724
print(split(num))

for x in split(num):
    print("{} - {}".format(x,type(x)))
    get_comb(x)