# This program is to generate ring for alphabets
N=25
Ring_Zn=[]
Ring_Alphabet=[]
# create ring of alphabets
# a = 97 and z = 122
for alpha in range(97, 123):
    Ring_Alphabet.append(chr(alpha))
print("Aplhabets: ",Ring_Alphabet)

# create ring of mod26
for i in range(0,N+1):
    Ring_Zn.append(i)
print("Ring: ",Ring_Zn)

for i in range(0,N+1):
    print("{} - {}".format(Ring_Zn[i],Ring_Alphabet[i]))