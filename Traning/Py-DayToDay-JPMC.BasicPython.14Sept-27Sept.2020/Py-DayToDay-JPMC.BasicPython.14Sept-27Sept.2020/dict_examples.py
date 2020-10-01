s = "Hello World Hello Earth Hello Everyone"
# Find the frequency of each chars

#Create an empty dict(d)
d = {}
#Take each char(ch) from s 
for ch in s.split(" "):
    #If ch does not exist in empty dict 
    if ch not in d:
        #create a key, ch and value as 1 
        d[ch] = 1
    else:
        #increment ch( ie key) 's value 
        d[ch] = d[ch] + 1

print(d)