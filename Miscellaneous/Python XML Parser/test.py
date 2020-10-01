def split(n):
    Lst = []
    if len(str(n)) == 2:
        return((str(n)[0],str(n)[1]))
    if len(str(n)) > 2:
        Lst.append(str(n))
        Lst.append((str(n)[0], str(n)[1:]))
        Lst.append((str(n)[0], split(int(str(n)[1:]))))
        Lst.append((str(n)[0:-1], str(n)[-1]))
        Lst.append((split(int(str(n)[0:-1])), str(n)[-1]))
        #return((l),('1', str(l - 1)),('1', split(l - 1)),(str(l - 1), '1'),(split(l - 1), '1'))
        return Lst

num = 6724
print(split(num))

for x in split(num):
    print("{} - {}".format(x,type(x)))