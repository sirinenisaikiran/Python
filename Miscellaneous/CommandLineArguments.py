import sys 
  
# total arguments 
n = len(sys.argv) 
print("Total arguments passed:", n) 
  
# Arguments passed 
print("\nName of Python script:", sys.argv[0]) 
  
print("\nArguments passed:", end = " ") 
for i in range(1, n): 
    print(sys.argv[i], end = " ") 
    
    
# F:\Programming\Python\Miscellaneous>Python CommandLineArguments.py A B C
# Total arguments passed: 4

# Name of Python script: CommandLineArguments.py

# Arguments passed: A B C