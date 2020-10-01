lst = [ 3, 5, 2, 7]
output = [ 9, 25, 49]

#Create an empty list 
output = []
#Take each element(e) from lst 
for e in lst:
    #Square e if e is odd and append to empty list 
    if e % 2 == 1:
        output.append(e * e)

print(output)


s1 #{1, 2, 3, 4}
s1[0] #Error
s1.append(30) #Error 
s1.add(50)
s1  #{1, 2, 3, 4, 50}
dir(set)  # Check all methods 
s1 = {1,2,3,4}
s2 = {4,5,6}
s1 & s2 #{4}
s1 | s2 #{1, 2, 3, 4, 5, 6}
s1 - s2 #{1, 2, 3}
s1 ^ s2 #{1, 2, 3, 5, 6} #XOR 
# above and below are same things - Symmetric difference 
(s1-s2) | (s2-s1) #{1, 2, 3, 5, 6}

#Tuple 
t = (1,2,3)
et = ()
type(et) #<class 'tuple'>
len(t)
2 in t
t == (3,2,1) #False
for e in t:
    print(e)

#indexing 
t[0]
t[0] = 20 # Error 
t2 = t + (5,6) #OK 
t.append(30) #Error 
dir(tuple)
dir(list)
set(dir(list)) - set(dir(set))

#Mutability might be a TRAP 
lst = [1,2,3]
l2 = [ lst, lst, lst]#[[1, 2, 3], [1, 2, 3], [1, 2, 3]]
l2[-1][1] = 20
l2 #[[1, 20, 3], [1, 20, 3], [1, 20, 3]]
lst #[1, 20, 3]
l22 = [ lst.copy(), lst[:], lst.copy()]
l22 #[[1, 20, 3], [1, 20, 3], [1, 20, 3]]
l22[-1][1] = 200
l22 #[[1, 20, 3], [1, 20, 3], [1, 200, 3]]
lst #[1, 200, 3]
lst.append(lst)
lst #[1, 200, 3, [...]]
lst[-1] #[1, 200, 3, [...]]
lst[-1][-1] #[1, 200, 3, [...]]
lst[-1][-1][-1][-1][-1][0] = 20
lst #[20, 200, 3, [...]]









































