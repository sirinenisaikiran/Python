s = "Hello World"
#i = 0
#for element in s:
#    print("index:", i, "element:", element)
#    i = i + 1
#Take each char(ch1) from s 
for ch1 in set(s):
    #initialize counter 
    counter = 0
    #Take each char(ch2) from s 
    for ch2 in s:
        #if ch1 and ch2 are same 
        if ch1 == ch2:
            #increment counter
            counter = counter + 1
    #print ch1 and counter 
    print(ch1, "-", counter)
    
# s[0]
# s[0] = 'K'  # Immutable, so can not change 
# s2 = s + " OK"  #concatenation 
# "OK" * 4        #repeat 
# dir(str)        # see instance method 
# #Split usage 
# s1 = "A:B:C"
# s1.split(":")   #['A', 'B', 'C']
# #strip usage 
# s2 = "[OK, NOK]"
# s2.strip('[]')  #'OK, NOK'
# s3 = "    OK     "
# s3.strip(" ")   #'OK'
# #len is builtin method, never called like instance 
# len(s1)# THIS IS wrong calling - s1.len()
# 
#########Key points 
[]  list - Duplicates-P, Indexing - P, Insertion Order-P , Mutable
()      tuple - immutable, --- above ---
  
{}  set - Duplicates-NP, Indexing-NP, Insertion Order - NP , Mutable
      frozenset - Immutable , --- above --
  
---------------
{key: value} dict - Key and value pairs - Keys are like set , 
             Value can be anything
             Most Used usecase - Given Key, get Value ~ constant time



#Iris.csv 
filename = r"D:\handson\data\iris.csv"
with open(filename, "rt") as f:
    lines = f.readlines()

rows = lines[1:]
e = '5.1,3.5,1.4,0.2,Iris-setosa\n'
e.strip().split(",")
e.strip().split(",")[-1]
output = set()
for e in rows:
    output.add( e.strip().split(",")[-1] )

print(output)
#







    
    
    
