# This program is to generate ring for alphabets
N=26; Ring_Zn=[]; Ring_Alphabet=[]
#plain_text="ATTACK"
plain_text="hi this is SK and we are need to grow weed"
cipher_text=""
key=17
# create ring of alphabets
# a = 97 and z = 122
Ring_Alphabet = [chr(alpha) for alpha in range(97, 123)]
#print("Aplhabets: ",Ring_Alphabet)
# create ring of mod26
Ring_Zn = [i for i in range(0,N)]
#print("Ring: ",Ring_Zn)

#for i in range(0,N+1): print("{} - {}".format(Ring_Zn[i],Ring_Alphabet[i]))

# list(plain_text)
# plain_text.lower()

# Encoding
for char in list(plain_text.lower()):
    if char != " ":
        #print(char)
        i = Ring_Alphabet.index(char)
        cipher_text = cipher_text + Ring_Alphabet[(i + key) % N]
    else:
        cipher_text = cipher_text + " "
print("plain_text: ", plain_text)
print("cipher_text: ",cipher_text)
    
