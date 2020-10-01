# if name is "XYZ" and age is below 40, 
# print "suitable" else if age is greater
# than 50, print "old", else print "OK"
# For all other names, print "not known" 

#name = "ABC"
#name = input("Give Name:")
#age_1 = input("Give Age:")
#age = int(input("Give Age:"))
#Execute as below 
#python second.py ABC 40 
import sys 
name = sys.argv[1]  if len(sys.argv) > 1 else "XYZ"  #1st arg 
# if len(sys.argv) > 2:
#     age = int(sys.argv[2]) # 2nd Arg 
# else:
#     age = 40 
age = int(sys.argv[2])  if len(sys.argv) > 2 else 40
#print(sys.argv) #['second.py', 'ABC', '40']
if name == "XYZ":
    if age < 40:
        print("suitable")
    elif age > 50:
        print("old")
    else:
        print("OK")
else:
    print("not known")
print("END")   
