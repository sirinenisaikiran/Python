Q0: Nested If 
if name is "XYZ" 
and age is below 40, 
print "suitable" 
else if age is greater
than 50, print "old", 
else print "OK"
For all other names, 
print "not known" 

name = "XYZ"
age = 40 
if name == "XYZ":
    if age < 40:
        print("suitable")
    elif age > 50:
        print("old")
    else:
        print("OK")
else:
    print("not known")










Q0.1: Print prime numbers between 0 to 10

check = int(sys.argv[1])

print("2 is prime")
for nu in range(3,check,2):
    #Check when you divide nu by 2...nu-1 
    #the reminder should not be zero 
    #if so, it is prime 
    prime = True 
    for x in range(2,nu-1,1):
        if nu % x == 0:
            #print this is not prime 
            prime = False 
            break 
    if prime:
        print(nu , "is prime")


#OR 

check = int(sys.argv[1])

print("2 is prime")
for nu in range(3,check,2):
    #Check when you divide nu by 2...nu-1 
    #the reminder should not be zero 
    #if so, it is prime 
    #prime = True 
    for x in range(2,nu-1,1):
        if nu % x == 0:
            #print this is not prime 
            #prime = False 
            break 
    else:#if prime:
        print(nu , "is prime")

    















Q0.2: Print Pythogorus number  below 100
ie (x,y,z) which satisfy z*z == x*x +y*y 


for x in range(1,100):
    for y in range(x,100):
        for z in range(y,100):
            if z*z == x*x + y*y:
                print(x,y,z)










Q0.3:
Given:D1 = {'ok': 1, 'nok': 2}
D2 = {'ok': 2, 'new':3 }
Create below:
# union of keys, #value does not matter
D_UNION = { 'ok': 1, 'nok': 2 , 'new':3  } 
# intersection of keys, #value does not matter
D_INTERSECTION = {'ok': 1}
D1- D2 = {'nok': 2 }
#values are added for same keys
D_MERGE = { 'ok': 3, 'nok': 2 , 'new':3  }


#Merge solution 
m_dict = {}    
for k1 in in1:
	m_dict[k1] = in1[k1]			   #Initial values
	if k1 in in2:
		m_dict[k1] = in1[k1] + in2[k1] # merge		
for k2 in in2:							# remaining elements
	if k2 not in in1:
		m_dict[k2] = in2[k2]

		
print(m_dict)














Q1:
input_str = "Hello world 
print frequency of each alphabets 
H-1
e-1
l-3
and so on for other alphabets  


s = "Hello World"

for ch in s:
    # initialize counter 
    counter = 0
    # Take each char(ch1) from  s #for 
    for ch1 in s:
        # if ch and ch1 are same #if 
        if ch == ch1:
            # increment counter 
            counter = counter + 1
    # print ch and counter  # print 
    print(ch, '-', counter)












Q2:Find out the flaw in above program 
How can you solve that ?(Hint: use correct data structure )
Solve ..   
    
s = "Hello World"

for ch in set(s):
    # initialize counter 
    counter = 0
    # Take each char(ch1) from  s #for 
    for ch1 in s:
        # if ch and ch1 are same #if 
        if ch == ch1:
            # increment counter 
            counter = counter + 1
    # print ch and counter  # print 
    print(ch, '-', counter)
    
    
    
    
    
    
    
    
    
    
Q3: Actually, above data structure is dict, don't you think so?
So, formally solve with dict where key is aplhabet and value it's count 

s = "Hello World"

#create empty dict 
d = {}
#Take each char(ch) from s 
for ch in s:
    #if ch key does not exit in empty dict 
    if ch not in d:
        #create new key, ch and initialize
        d[ch] = 1
    else: 
        #increment ch'key value 
        d[ch] = d[ch] + 1
        
print(d) 




Q3.1 
input = "aaabbbbaaac"
output = "abc"

output = ""
#Take each char(ch) from input  #for 
for ch in input:
    #if ch does not exist in output  #not in 
    if ch not in output:
        output = output + ch 
    print(output, ch)
print(output)










Q4: Given input, find output 
input = [1,2,3,4]
output = [1,9]



res = []
for e in input:
    if e % 2 == 1 :
        res.append(e*e)












      
Q5: Given input, find output 
input = '[1,2,3,4]'
output = [1,2,3,4]

    
    
    
res = []
for e in input.strip('[]').split(","):
    res.append(int(e))   
    
    
    
    
    
    
    
    
    
    
    
    
Q5.1: Can you implement above with slice 


res = []
for e in list(input)[1:-1:2]:
    res.append(int(e))   
    

    
    
    
    
    
    
    
    
    
    
    
    
Q6: Given input, find output 
input = 'Name:ABC,age=20|Name:XYZ,age=30'
output = 'Name:Abc,age=20|Name:Xyz,age=30'



















#split input with "|" and store to s2
s2 = input.split("|')
#create empty list 
res = []
#Take each element(e) from s2 
for e in s2:
#    split that with ',', take first part 
    e2 = e.split(",")[0].split(":")[1]
#    then split with ':', take 2nd part 
#    title() it ,
#    then replace e , old = original, new= title 
    res.append(e.replace(e2, e2.title()))
#    append to empty list 
#join that empty list with "|"
"|".join(res0








Q7: Find checksum 
input="ABCDEF1234567890"

Take two two character(one byte) from above (which are in hex digit )
Convert to int  (Hint: use int function with base)
Sum all and then find mod with 255, that is your checksum 

out = [int("".join(e),16) for e in zip(input[::2],input[1::2])]
sum(out) % 255 



Q8: Sub process and Regex  hands on 
Execute below command and extract some info 

tracert www.google.com
netstat -an
ipconfig /all
powercfg /lastwake
driverquery -v
nslookup www.google.com 
tasklist -m

##4 patterns 
nslookup www.google.com
echo %errorlevel%
nslookup www.google.com > out.txt
type out.txt | findstr /c:"Server"
"""
Server:\t\t192.168.43.1\nAddress:\t192.168.43.1#53\n\nNon-authoritative answer:
\nName:\twww.google.com\nAddress: 172.217.26.228\n\n'
"""
'''
class subprocess.Popen(args, bufsize=0, 
stdin=None, stdout=None, stderr=None, shell=False, 
universal_newlines=False)
'''
#1
import subprocess as S
command = "nslookup www.google.com"
proc = S.Popen(command, shell=True, 
    stdout=S.PIPE, stderr=S.PIPE, universal_newlines=True)
outs, oute = proc.communicate()
print(outs)
import re 
res = re.findall(r"Address: (.+?)\n\n"  , outs)
res =re.findall (r"Addresses:\s+((.+)\n\t\s*(.+)\n\n)",s)

com1 = r"c:\windows\system32\ping %s" % res[0][-1]
proc = S.Popen(com1, shell=True, 
    stdout=S.PIPE, stderr=S.STDOUT, universal_newlines=True)
outs, oute = proc.communicate()
print(outs)

#2
command = "nslookup www.google.com"
proc = S.Popen(command, shell=True, 
    stdout=S.PIPE, stderr=S.PIPE, universal_newlines=True)
outs, oute = proc.communicate()
print(proc.returncode)

#3 nslookup www.google.com > out.txt
with open("out.txt", "wt") as f :
    command = "nslookup www.google.com"
    proc = S.Popen(command, shell=True, 
        stdout=f, stderr=S.STDOUT, universal_newlines=True)
    proc.wait()

proc2 = S.Popen("type out.txt", shell=True, 
    stdout=S.PIPE, stderr=S.PIPE, universal_newlines=True)
outs, oute = proc2.communicate()
print(outs)    
    
#4 type out.txt | findstr /c:"Server"
command = "type out.txt"
com2 = 'findstr /c:"Server"'
proc = S.Popen(command, shell=True, 
    stdout=S.PIPE, stderr=S.STDOUT, universal_newlines=True)
proc2 = S.Popen(com2, shell=True, 
    stdin= proc.stdout, 
    stdout=S.PIPE, stderr=S.STDOUT, universal_newlines=True)
proc.stdout.close()
outs, oute = proc2.communicate()
#
proc = S.Popen(command + "| "+com2, shell=True, 
    stdout=S.PIPE, stderr=S.STDOUT, universal_newlines=True)
outs, oute = proc2.communicate()    
    



Q8.1:  escapiing the pipe by ^, /v means lines other than matching , /c:"" - matching, /r - regex 
#To strip out the top 2 lines pipe the output to findstr /v "Active Proto".
for /f "tokens=2,5" %i  in ('netstat -n -o ^| findstr /v "Active Proto"') do @echo Local Address = %i, PID = %j
#OR 
for /f "tokens=2,5" %i  in ('netstat -n -o ^| findstr /C:"ESTABLISHED"') do @echo Local Address = %i, PID = %j
1. Execute above with big bufsize and get Unique port 
2. get detail of each PID by command: tasklist /fi "pid eq PID" /nh


Q8.2: Get return code of executing: taskkill -im iexplore.exe
      while redirecting both stdout and stderr to devnull 

Q8.2 : Execute via pipe ,  
dir /B | findstr /r /c:"[mp]"

Q8.3: Redirect 
tasklist /fi "imagename eq iexplore.exe"' > test.txt
and then display the content via type test.txt 



##Example - escapiing the pipe by ^, /v means lines other than matching , /c:"" - matching, /r - regex 
#To strip out the top 2 lines pipe the output to findstr /v "Active Proto".
for /f "tokens=2,5" %i  in ('netstat -n -o ^| findstr /v "Active Proto"') do @echo Local Address = %i, PID = %j
#OR 
for /f "tokens=2,5" %i  in ('netstat -n -o ^| findstr /C:"ESTABLISHED"') do @echo Local Address = %i, PID = %j




command = """for /f "tokens=2,5" %i  in ('netstat -n -o ^| findstr /C:"ESTABLISHED"') do @echo Local Address = %i, PID = %j"""
import subprocess as S
bufsize = 2**20
p = S.Popen(command, bufsize =bufsize, shell=True, stdout=S.PIPE, stderr=S.PIPE, universal_newlines=True)
(out,err) = p.communicate()

#Unique Port 
import re 
sp = r":(\d+),"
res = re.findall(sp, out)
unique = {int(e) for e in res }

#details of process 
sp = r"PID = (\d+)\n"
unique = {int(e) for e in re.findall(sp, out) }

command = r"""tasklist /fi "pid eq %d" /nh"""
stat = {}
for pid in unique:
    p = S.Popen(command % pid , shell=True, stdout=S.PIPE, stderr=S.STDOUT, universal_newlines=True)
    stat[pid] = p.communicate()[0]
    

#no header- nh 
D:\Desktop\PPT>tasklist /fi "pid eq 6340"

Image Name                     PID Session Name        Session#    Mem Usage
========================= ======== ================ =========== ============
iexplore.exe                  6340 Console                    7   1,33,468 K
    
    
##Example of only return code 
command = """taskkill -im iexplore.exe"""
#echo %errorlevel% or echo $? , note 0 means success 
import subprocess as S, os , sys 
#Py3.5, S.DEVNULL 
with open(os.devnull, 'w') as DEVNULL:
    exit = S.Popen(command, shell=True, stdout=DEVNULL, stderr=DEVNULL).returncode
#then exit 
sys.exit(exit)
 
 
##Example of pipe 
#dir /B | findstr /r /c:"[mp]"

import subprocess as S, os , sys 
command = 'dir /B | findstr /r /c:"[mp]"'
output = S.check_output(command, shell=True, stderr=S.STDOUT, universal_newlines=True)

#OR 
command1 = 'dir /B' 
command2 = 'findstr /r /c:"[mp]"'
#Py3.5, S.DEVNULL 
with open(os.devnull, 'w') as DEVNULL:
    p1 = S.Popen(command1, shell=True, stdout=S.PIPE, stderr=DEVNULL)
    p2 = S.Popen(command2, shell=True, stdin=p1.stdout, stdout= S.PIPE, stderr=DEVNULL)
    p1.stdout.close()  ## Allow p1 to receive a SIGPIPE if p2 exits
    (out, err) = p2.communicate() 
    


##Example of Redirect 
command = 'tasklist /fi "imagename eq iexplore.exe"' #> test.txt
file = "test.txt"
with open(file , "wt") as f :
    proc = S.Popen(command, shell=True, stdout=f, stderr=S.STDOUT)
    proc.wait()

command = "type %s"
contents = S.Popen(command % file, shell=True, stdout=S.PIPE, stderr=S.STDOUT).stdout.read() 
 
 






Q9 : Os hands on 
1. Create below env vars containing below 
HOST        hostname 
DT          todays date using pattern "%m%d%y%H%M%S" 
SCRIPT      this script name only (without extension)
SCRIPT_PID  this script pid 
OUTDIR      C:/tmp/adm
LOGFIL      $OUTDIR/$SCRIPT.$DT.log (in unix expansion of variable 
2. Then dump in parent and in child these values (Use Subprocess)
3. create a diction of filename and it's size only in given dir(without recursively going into subdirs)
4. Rename any files, *.txt in a given dir to *.txt.bak 
4. Print cwd in python and go to parent dir and again print 
5. Walk each dir & subdirs and create .done file containing today's date and no of file found , file names and each file size 
6. walk each dir and remove .done file 


1.
import os, os.path, sys, subprocess as S, time, datetime as D, shlex
direct_environ = dict(HOST=os.uname()[1], #platform.uname().node
                      DT=D.datetime.today().strftime("%m%d%y%H%M%S"),
                      SCRIPT=os.path.splitext(os.path.basename(sys.argv[0]))[0],
                      SCRIPT_PID=str(os.getpid()),
                      OUTDIR=r"/var/adm/aaas",
                      ) 
    

#Update, could have called os.environ.update(direct_environ), ensure all are string 
for k,v in direct_environ.items():
    os.environ[str(k)] = str(v) 
    
    
#Add all environs which are dependent on other environs , must after above 
indirect_environ = dict(LOGFILE=os.path.expandvars(r"$OUTDIR/$SCRIPT.$DT.log"))

for k,v in indirect_environ.items():
    os.environ[str(k)] = str(v)    
  
  

2.
for k,v in os.environ.items():
    if k in direct_environ or k in indirect_environ:
        print(k,'=',v)        


print("Print in subprocess")
#both in windows and shell 
proc = S.Popen("printenv", shell=True, stdout=S.PIPE, stderr=S.STDOUT, universal_newlines=True)
outs, errs = proc.communicate(timeout=10)
final_keys = direct_environ.keys() | indirect_environ.keys()
for line in outs.split():
    k,*v = line.split("=")
    if k in final_keys:
        print("\t",line)



3. create a dict of filename and it's size only in given dir(without recursively going into subdirs)
g_dir = "."
d = {}
for f in glob.glob(g_dir+"/*"):
    if os.path.isfile(f):
        d[f] = os.path.getsize(f) 



4. Rename any files, *.txt in a given dir to *.txt.bak 
g_dir = "."
d = {}
for f in glob.glob(g_dir+"/*"):
    if os.path.isfile(f):
        new_f = f + ".bak"
        with  open(f,"rt") as inf:
            with open(new_f, "wt") as outf:
                outf.writelines(inf.readlines())
                
4. Print cwd in python and go to parent dir and again print 
os.path.abspath(os.curdir)
os.chdir("..")
os.path.abspath(os.curdir)

5. Walk each dir & subdirs and create .done file containing today's date and no of file found , file names and each file size 
#os.walk(top, topdown=True, onerror=None, followlinks=False)
#For each directory ,, yields a 3-tuple (dirpath, dirnames, filenames).
import os, os.path,datetime 
for root, dirs, files in os.walk('.'):
    #print(root, dirs, files)
    res = [str(datetime.datetime.now())+"\n"] 
    res.append( "No of Files:%d\n" % len(files))
    for f in files:
        file = os.path.join(root, f)
        s = os.path.getsize(file)
        created = datetime.datetime.fromtimestamp(os.path.getctime(file))
        res.append("%s,%d,%s\n" %(file, s, created))
    with open(os.path.join(root, ".done"), "wt") as f :
        f.writelines(res)
        

6. walk each dir and remove .done file 
import os, os.path,datetime 
for root, dirs, files in os.walk('.'):
    file = os.path.join(root, ".done")
    if os.path.exists(file):
        os.remove(file)
        
    








Q-FUNC:Write functions of below , lst = list of numerics


Mean(lst) =         Sum of lst/length of lst 
Median(lst) =       sort and midddle value or average of two middle  if length is even
sd(lst) =           sqrt of( SUM of square of ( each elemnt - mean)  / length of lst  )

freq(lst) =         returns dict with key as element and value is count 
Mode(lst) =         sort with frequency, highest frequency

merge(in1,in2)      
    in1, in2 are dict, values are added for same keys
    Given:
    D1 = {'ok': 1, 'nok': 2}
    D2 = {'ok': 2, 'new':3 }
    returns  { 'ok': 3, 'nok': 2 , 'new':3  }

checksum(string)  
    Using regex 
    Take two two character(one byte) from above (which are in hex digit )
    Convert to int  (Hint: use int function with base)
    Sum all and then find mod with 255, that is your checksum 
    Test with input="ABCDEF1234567890"
                    
sliding(lst, windowSize, step)
    Take elements from lst with windowSize 
    and step with 'step' 
    eg given lst = [2,4,6,3,5,7]
    and sliding(lst, 2, 1) returns 
    [[2, 4], [4, 6], [6, 3], [3, 5], [5, 7]]
    
grouped(lst, n) 
    create each n elements of lst 
    eg given lst = [2,4,6,3,5,7]
    and grouped(lst, 2) returns 
    [[2, 4], [6, 3], [5, 7]]
    
group_by(lst, key)
    returns a dict of key(element) and values are list of those element of lst which satisfy's key function 
    key is function which takes each element 
    eg given lst = [2,4,6,3,5,7]
    and group_by(lst, lambda e : e%2)
    returns { 1:[3,5,7], 0:[2,4,6]}
    
     
take(lst, n, start=0)
    Takes n element from start 

drop(lst, n, start=0)
    takes all element after droping n from start 
    
agg(in_d, agg_d)
    Aggregation where agg_d is dict of column name and fn(lst), lst is values of in_d for each key  
    eg 
    in_d = { 1:[3,5,7], 0:[2,4,6]}
    agg_d = {'max': max, 'mean': lambda lst: sum(lst)/len(lst) , 'sum': sum }
    returns {0: {'max': 6, 'mean': 4.0, 'sum': 12}, 1: {'max': 7, 'mean': 5.0, 'sum': 15}}
    

    
    
    
read_csv(fileName)
    Return list of rows where each element is converted to int, then float, then str whichever succeeds 
read_csv(filename, dates_index= None, datetime_format=None)
    Extend that with datetime parseing for those indexes given in dates_index 
    if datettime_format is none, use dateutils.parser.parse function to autodetect the format  
write_csv(fileName, lst, headers)
        write headers and then lst to fileName

    
    
execute_and_watchdog(command, TIMEOUT=15, WAIT_FOR_KILL=60, **kwargs)
    Execute the command and keep on polling to check command is completed within TIMEOUT 
    If not, manually kill that and then sleep for WAIT_FOR_KILL

    
OS hands ON 
1.Create below env vars containing below 
HOST        hostname 
DT          todays date using pattern "%m%d%y%H%M%S" 
SCRIPT      this script name only (without extension)
SCRIPT_PID  this script pid 
OUTDIR      C:/tmp/adm
LOGFIL      $OUTDIR/$SCRIPT.$DT.log (in unix expansion of variable 
2. Then write functions to dump environs in parent and in child these values 
3. write mslog with takes any message and dumps that message to LOGFIL and console 
   with below format , message may contain any env var and that should be expanded 
   HOST:DT:message 
4. Given a filename and no of breaks, generate that many files with chunks from original file names 
5. Concatenate many .txt file into one file 
6. Recurively go below a dir and based on filter, dump those files in to  single file 




##
#Mean(lst) =         Sum of lst/length of lst 
@trace 
@mea                # mean = mea(mean)
def mean(lst):
    time.sleep(5)
    return sum(lst)/len(lst)
    

#Median(lst) =       sort and midddle value or average of two middle  if length is even

def median(lst):
    a = sorted(lst)
    b = len(a)
    if b % 2 == 0:
        c = a[b//2] + a[b//2-1]
        return c/2 
    else:
        return a[b//2]

#sd(lst) =           sqrt of( SUM of square of ( each elemnt - mean)  / length of lst  )
def sd(lst):
    import math 
    m = mean(lst)
    #res = []
    #for e in lst:
    #    res.append(  (e-m)*(e-m) )
    res = [ (e-m)*(e-m) for e in lst]
    return math.sqrt(sum(res)/len(lst))



def merge(in1,in2, op=lambda x,y:x+y):
    """    
    in1, in2 are dict, values are added for same keys
    Given:
    D1 = {'ok': 1, 'nok': 2}
    D2 = {'ok': 2, 'new':3 }
    returns  { 'ok': 3, 'nok': 2 , 'new':3  }
    """
    D = in1.copy()
    for k,v in in2.items():
        if k in D:
            D[k] = op(D[k] ,v)
        else:
            D[k] = v 
    return D

def checksum(string):    
    '''
    Take two two character(one byte) from above (which are in hex digit )
    Convert to int  (Hint: use int function with base)
    Sum all and then find mod with 255, that is your checksum 
    Test with input="ABCDEF1234567890"
    '''
    import re 
    data = [ int(x, 16) for x in re.findall(r"\w\w", string) ]
    return sum(data) % 256
   

def read_csv(filename, dates= None, datetime_format=None):
    def convert(x, fn):
        try:
            res = fn(x)
        except Exception:
            res = None 
        return res 
    def one_by_one(x, *fn):
        for f in fn:
            res = convert(x,f)
            if res != None:
                return res 
        return x
    from csv import reader
    with open(filename, "rt") as f :
        rd = reader(f)
        rows = list(rd)
    tryFn = [int, float, str]
    first =  [ [ one_by_one(e.strip(), *tryFn) for e in row]   for row in rows if len(row) > 0 ]
    #convert dates 
    from dateutil.parser import parse  
    from datetime import datetime    
    if datetime_format and type(datetime_format) is str:
        date_parse = lambda e: datetime.strptime(e, datetime_format)
    elif datetime_format and type(datetime_format) is function :
        date_parse = datetime_format
    else:
        date_parse = parse
    def convert_date(row, which):
        res = []        
        if type(which) is int:
            cols = [which]
        else:
            cols = which 
        #print(date_parse,cols)
        for i, e in enumerate(row) :
            if i in cols:
                #print("converting", i)
                try:
                    res.append(date_parse(e))
                except Exception:
                    res.append(e)
            else:
                res.append(e)
        return res        
    if dates != None:
        second = [convert_date(row,dates)  for row in first]     
    else:
        second = first 
    return second     

    
def write_csv(filename, lst, headers ):
    from csv import writer
    with open(filename, "wt", newline='') as f :
        wr = writer(f)
        wr.writerows([headers] + lst)
        

    
    
    
def sliding(lst, w, s):
    res = [] 
    n = ((len(lst)-w)/s)+1
    for i in range(0, int(n)):
        start = i*s 
        end = w + s*i 
        res.append(lst[start:end])
    #last segment 
    if  lst[end:]:
            res.append(lst[end:])
    return res     
    
def sliding2(lst, w, s):    
    assert s <= w
    res = list(zip(*[lst[i::s] for i in range(w)]))
    #last segment
    end = w + s*((len(lst)-w)//s)
    if  lst[end:]:
        res.append(tuple(lst[end:]))
    return res     

def grouped(lst, n):
    return sliding(lst, n, n)  

def group_by(lst, key):
    d = {}
    for e in lst:
        k = key(e)
        if k in d:
            d[k].append(e)
        else:
            d[k] = [e]
    return d 

def take(lst, n, start=0):
    return list(lst)[start:n]

def drop(lst, n, start=0):
    return list(lst)[start+n:]

def agg(in_d, agg_d):
    out_d = {}
    for key, lst in in_d.items():
        out_d[key] = agg_d.copy()
        for col, fn in agg_d.items():
            out_d[key][col] = fn(lst)
    return out_d     

def execute_and_watchdog(command, TIMEOUT=15, KILL_TMOUT=60, **kwargs): 
    import errno
    def test_d(pid):
        try:
            os.kill(pid, 0)
        except OSError as err:
            if err.errno == errno.ESRCH:
                return False
        return True         
    args = shlex.split(command)    
    proc = S.Popen(args, **kwargs)
    timeout = TIMEOUT + 1 
    while proc.poll() is None and timeout > 0 :
        time.sleep(1)
        timeout -= 1         
    if timeout == 0:
        print("INFO:Time out period reached. Killing process %d." % (proc.pid,))
        if test_d(proc.pid):
            proc.terminate()
            time.sleep(KILL_TMOUT)
        if test_d(proc.pid):
            proc.kill()
            time.sleep(KILL_TMOUT)
        outs, errs = proc.communicate()
        if test_d(proc.pid):
            print("INFO:Process %d cound not be kiilled. Please verify manually" % (proc.pid,))
        return (9, outs, errs)
    outs, errs = proc.communicate()
    return (proc.returncode, outs, errs)
      
   
   
   
   
#Os hands on 
import os, os.path, sys, subprocess as S, time, datetime as D, shlex
direct_environ = dict(HOST=os.uname()[1], 
                      DT=D.datetime.today().strftime("%m%d%y%H%M%S"),
                      SCRIPT=os.path.splitext(os.path.basename(sys.argv[0]))[0],
                      SCRIPT_PID=str(os.getpid()),
                      OUTDIR=r"/var/adm/aaas",
                      ) 
    

#Update, could have called os.environ.update(direct_environ), ensure all are string 
for k,v in direct_environ.items():
    os.environ[str(k)] = str(v) 
    
    
#Add all environs which are dependent on other environs , must after above 
indirect_environ = dict(LOGFILE=os.path.expandvars(r"$OUTDIR/$SCRIPT.$DT.log"))

for k,v in indirect_environ.items():
    os.environ[str(k)] = str(v)    
  
  

##Dumps all environ variable 
def print_parent_env():
    for k,v in os.environ.items():
        if k in direct_environ or k in indirect_environ:
            print(k,'=',v)        

def print_child_env():
    print("Print in subprocess")
    #both in windows and shell 
    proc = S.Popen("printenv", shell=True, stdout=S.PIPE, stderr=S.STDOUT, universal_newlines=True)
    outs, errs = proc.communicate(timeout=10)
    final_keys = direct_environ.keys() | indirect_environ.keys()
    for line in outs.split():
        k,*v = line.split("=")
        if k in final_keys:
            print("\t",line)


def msglog(text, file=True):
    import os 
    LOGFILE = os.environ["LOGFILE"]
    HOST = os.environ["HOST"]
    DT = os.environ["DT"]
    line = "%s:%s:%s" % (HOST, DT, os.path.expanduser(os.path.expandvars(text)))
    if file :
        with open(LOGFILE, "at") as f :
            f.writelines([line+"\n"])
    print(line)   
   
5. Given a filename and no of breaks, generate that many files with chunks from original file names 
def breakFiles(file, n, ext_length = 3):
    import os.path
    def write(fileName, lst):
        with open(fileName, "wt") as f:
            f.writelines(lst) 
        #print(fileName, "written", len(lst))
    def sliding(lst, w, s):
        res = [] 
        n = ((len(lst)-w)/s)+1
        for i in range(0, int(n)):
            start = i*s 
            end = w + s*i 
            res.append(lst[start:end])
        #last segment 
        if  lst[end:]:
                res.append(lst[end:])
        return res     
    def grouped(lst, n):
        return sliding(lst, n, n)        
    onlyFileName, ext = file[0: len(file)-ext_length-1], file[len(file)-ext_length:]
    with open(file, "rt") as f:
        lines = f.readlines()
    howmany = len(lines) // n 
    gr = grouped(lines, howmany)
    if len(gr) > n : #extra last part      
        gr[-2] += gr[-1]
        del gr[-1]         
    #now len(gr) == n 
    names = [ onlyFileName+str(i)+"."+ext     for i in range(1,len(gr)+1)]
    #print(names, n, len(gr))
    for lst, n in zip(gr, names):
        write(n,lst)
    
breakFiles("../data/WindowsUpdate.log", 3)


5. Concatenate many .txt file into one file 
def concatenate(*files, out):
    import os.path 
    def read(fileName):
        if os.path.exists(fileName):
            with open(fileName, "rt") as f:
                lines = f.readlines()
            return lines 
    with open(out, "wt") as fout:
        for f in files:
            if os.path.exists(f):
                fout.writelines(read(f))
    #done  
            
        


6. Recurively go below a dir and based on filter, dump those files in to  single file 
def print_files(g_dir, out_file, filter_path=r"\.py$"):
    import re , os, os.path 
    def read(fileName):
        if os.path.exists(fileName):
            with open(fileName, "rt") as f:
                lines = f.readlines()
            return lines 
    def write(fileName, inf_f, msg=None):
        header = ("\n\n##->file:%s\n" %(inf_f,)) if not msg else msg 
        with open(fileName, "at") as f:
            f.writelines([header])
            f.writelines(read(inf_f))
        #done 
    if not os.path.exists(g_dir):
        return 1
    if os.path.exists(out_file):
        os.remove(out_file)
    for root, dirs, files in os.walk(g_dir):
        in_files = [os.path.join(root, f) for f in files if re.search(filter_path,f)]
        for f in in_files:
            write(out_file, f)
    return 0 
        
print_files(".", "total.py")
    
   
     
#Recursion 
flatten(lst)        Flattens the list 
                    ie input = [1,2,3, [1,2,3,[3,4],2]]
                    output = [1,2,3,1,2,3,3,4,2]
                    
convert(x)          Converts like below 
                    input = [[[ '(0,1,2)' , '(3,4,5)'], ['(5,6,7)' , '(9,4,2)']]]
                    output = [[[[0,1,2],[3,4,5]],[[5,6,7],[9,4,2]]]]
                    
                    
checksum(string)    Implement checksum with recursion 

quicksort(lst)      Implement quicksort 
                    1. Take pivot as middle value 
                    2. Take left list which is smaller tha pivot 
                    3. Take right list which is higher than pivot 
                    4. return list which is append of quicksort of left, pivot and quicksort of right 
                    
binsearch(value, items, low=0, high=None) 
                    Items are sorted 
                    1. Get high either given or len of list 
                       Get middle pos 
                    2. if items's pos is value, return pos 
                    3. if pos is length of items or high is same as low or pos is low, return not found 
                    4. if items's pos is less than value call binsearch with low=pos+1 and high 
                    5. else call binsearch with low and high=pos 
                    


def flatten(lst):
    """
    Flattens the list 
    ie input = [1,2,3, [1,2,3,[3,4],2]]
    output = [1,2,3,1,2,3,3,4,2]
    
    """
    #Create empty list 
    #take each element from lst 
    #    Check the type of element , if list 
    #        call flatten(element) and append to empty list 
    #    if not 
    #        append that element to empty list 
    #return that empty list 
    res = []
    for e in lst:
        if type(e) is list :
            res += flatten(e)
        else:
            res.append(e)
    return res 
    
    
def convert(x):
    if isinstance(x, list):
        return [convert(y) for y in x]
    else:
        return [int(y) for y in x.strip('()').split(',')]
		
o = convert(l)    

    
def checksum(string):    
    '''
    Take two two character(one byte) from above (which are in hex digit )
    Convert to int  (Hint: use int function with base)
    Sum all and then find mod with 255, that is your checksum 
    Test with input="ABCDEF1234567890, answer:15"
    '''
    def hexsum(s):
        return 0 if not s else int(s[0:2], base=16) + hexsum(s[2:])
    res = hexsum(string)
    return res % 255 


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[int(len(arr) / 2)]         #or // in Py3.x or in Py2.x if from __future import division
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
    
print quicksort([3,6,8,10,1,2,1])
# Prints "[1, 1, 2, 3, 6, 8, 10]"


def binary_search(value, items, low=0, high=None):  #items are sorted		
    high = len(items) if not high  else high
    pos = (high + low) // 2
    #print(low, pos, high)
    if items[pos] == value:
        return pos
    elif pos == len(items) or high == low or pos == low:
        return False
    elif items[pos] < value:
        return binary_search(value, items, pos + 1, high)
    else:		
        return binary_search(value, items, low, pos)




























###DataStructure 

#ELement description:longitude,latitude,housing_median_age,total_rooms,total_bedrooms,population,households,median_income,median_house_value,ocean_proximity
lst = [ "-122.23,37.88,41.0,880.0,129.0,322.0,126.0,8.3252,452600.0,NEAR BAY",
"-122.22,37.86,21.0,7099.0,1106.0,2401.0,1138.0,8.3014,358500.0,NEAR BAY",
"-122.24,37.85,52.0,1467.0,190.0,496.0,177.0,7.2574,352100.0,NEAR BAY",
"-122.25,37.85,52.0,1274.0,235.0,558.0,219.0,5.6431,341300.0,NEAR BAY",
"-122.25,37.85,52.0,1627.0,280.0,565.0,259.0,3.8462,342200.0,NEAR BAY",
"-122.25,37.85,52.0,919.0,213.0,413.0,193.0,4.0368,269700.0,NEAR BAY",
"-122.25,37.84,52.0,2535.0,489.0,1094.0,514.0,3.6591,299200.0,NEAR BAY",
"-122.25,37.84,52.0,3104.0,687.0,1157.0,647.0,3.12,241400.0,NEAR BAY",
"-122.26,37.84,42.0,2555.0,665.0,1206.0,595.0,2.0804,226700.0,NEAR BAY",
"-122.25,37.84,52.0,3549.0,707.0,1551.0,714.0,3.6912,261100.0,NEAR BAY",
"-122.26,37.85,52.0,2202.0,434.0,910.0,402.0,3.2031,281500.0,NEAR BAY",
"-118.46,34.16,16.0,4590.0,1200.0,2195.0,1139.0,3.8273,334900.0,<1H OCEAN",
"-118.47,34.15,7.0,6306.0,1473.0,2381.0,1299.0,4.642,457300.0,<1H OCEAN",
"-118.47,34.16,30.0,3823.0,740.0,1449.0,612.0,4.6,392500.0,<1H OCEAN",
"-118.47,34.15,43.0,804.0,117.0,267.0,110.0,8.2269,500001.0,<1H OCEAN",
"-118.48,34.15,31.0,2536.0,429.0,990.0,424.0,5.4591,495500.0,<1H OCEAN",
"-118.48,34.16,30.0,3507.0,536.0,1427.0,525.0,6.7082,500001.0,<1H OCEAN",
"-118.48,34.14,31.0,9320.0,1143.0,2980.0,1109.0,10.3599,500001.0,<1H OCEAN",
"-118.46,34.14,34.0,5264.0,771.0,1738.0,753.0,8.8115,500001.0,<1H OCEAN",
"-118.47,34.14,36.0,2873.0,420.0,850.0,379.0,8.153,500001.0,<1H OCEAN",
"-118.47,34.14,34.0,3646.0,610.0,1390.0,607.0,7.629,500001.0,<1H OCEAN",
"-118.43,34.14,44.0,1693.0,239.0,498.0,216.0,10.9237,500001.0,<1H OCEAN",
"-118.43,34.13,37.0,4400.0,695.0,1521.0,666.0,8.2954,500001.0,<1H OCEAN",
"-118.45,34.14,33.0,1741.0,274.0,588.0,267.0,7.9625,490800.0,<1H OCEAN",
"-118.35,34.15,52.0,1680.0,238.0,493.0,211.0,9.042,500001.0,<1H OCEAN",
"-118.36,34.15,41.0,3545.0,698.0,1221.0,651.0,4.3,500001.0,<1H OCEAN",
"-118.36,34.15,34.0,3659.0,921.0,1338.0,835.0,3.6202,366100.0,<1H OCEAN",
"-118.37,34.15,23.0,4604.0,1319.0,2391.0,1227.0,3.1373,263100.0,<1H OCEAN",
"-117.21,32.85,15.0,2593.0,521.0,901.0,456.0,4.2065,277800.0,NEAR OCEAN",
"-117.21,32.85,26.0,2012.0,315.0,872.0,335.0,5.4067,277500.0,NEAR OCEAN",
"-117.24,32.83,18.0,3109.0,501.0,949.0,368.0,7.4351,445700.0,NEAR OCEAN",
"-117.25,32.82,19.0,5255.0,762.0,1773.0,725.0,7.8013,474000.0,NEAR OCEAN",
"-117.25,32.82,23.0,6139.0,826.0,2036.0,807.0,9.5245,500001.0,NEAR OCEAN",
"-117.26,32.83,24.0,1663.0,199.0,578.0,187.0,10.7721,500001.0,NEAR OCEAN",
"-117.26,32.82,34.0,5846.0,785.0,1817.0,747.0,8.496,500001.0,NEAR OCEAN",
"-117.27,32.83,35.0,1420.0,193.0,469.0,177.0,8.0639,500001.0,NEAR OCEAN",
"-117.29,32.92,25.0,2355.0,381.0,823.0,358.0,6.8322,500001.0,NEAR OCEAN",
"-117.25,32.86,30.0,1670.0,219.0,606.0,202.0,12.4429,500001.0,NEAR OCEAN",
"-117.25,32.86,25.0,2911.0,533.0,1137.0,499.0,5.1023,500001.0,NEAR OCEAN",
"-117.25,32.86,27.0,2530.0,469.0,594.0,326.0,7.2821,500001.0,NEAR OCEAN",
"-120.69,37.59,27.0,1170.0,227.0,660.0,222.0,2.3906,81800.0,INLAND",
"-120.76,37.61,30.0,816.0,159.0,531.0,147.0,3.2604,87900.0,INLAND",
"-120.8,37.61,30.0,918.0,154.0,469.0,139.0,3.9688,175000.0,INLAND",
"-120.76,37.58,35.0,1395.0,264.0,756.0,253.0,3.6181,178600.0,INLAND",
"-120.83,37.58,30.0,1527.0,256.0,757.0,240.0,3.6629,171400.0,INLAND",
"-120.85,37.57,27.0,819.0,157.0,451.0,150.0,3.4934,193800.0,INLAND",
"-120.88,37.57,22.0,1440.0,267.0,774.0,249.0,3.9821,204300.0,INLAND",
"-120.87,37.62,30.0,455.0,70.0,220.0,69.0,4.8958,142500.0,INLAND",
"-120.87,37.6,32.0,4579.0,914.0,2742.0,856.0,2.6619,86200.0,INLAND",
"-120.86,37.6,25.0,1178.0,206.0,709.0,214.0,4.5625,133600.0,INLAND"]

Q1: Find unique value for 'ocean_proximity'
Hint: split each element with , to get list
Take the last value of above split and collect into list 
then convert to ? data structure ( can you identify the data structure?)

#Note: ..  means similar structure or values from above list 

res = []
for e in lst:
    res.append(e.split(",")[-1])

>>> set(res)
{'<1H OCEAN', 'NEAR BAY', 'NEAR OCEAN', 'INLAND'}



Q2: Create a list of dict with each dict as below 
{'housing_median_age': .. , 'total_bedrooms' :.., 
'median_income':.. ,'median_house_value':..,'ocean_proximity':.. }

required = { 'housing_median_age' :float,'total_bedrooms':float ,
'median_income' :float,'median_house_value':float,'ocean_proximity':str}
h = "longitude,latitude,housing_median_age,total_rooms,total_bedrooms,population,households,median_income,median_house_value,ocean_proximity"
headers = {}
for k,v in enumerate(h.split(',')):
    headers[v] = k


output = []
for e in lst:
    d = {}
    for re,fn in required.items():
        d[re] = fn(e.split(',')[headers[re]])
    output.append(d)

#OR 
required = { 'housing_median_age' :float,'total_bedrooms':float ,
'median_income' :float,'median_house_value':float,'ocean_proximity':str}

h = "longitude,latitude,housing_median_age,total_rooms,total_bedrooms,population,households,median_income,median_house_value,ocean_proximity"
headers = {v:k for k,v in enumerate(h.split(','))}
output = [{re: fn(e.split(',')[headers[re]]) for re,fn in required.items()}  for e in lst]



Q3: Create a dict where values are list of each column ie 
{'housing_median_age':[..,..,...] , 'total_bedrooms' :[..,..,...], 
'median_income':[..,..,...] ,'median_house_value':[..,..,...],'ocean_proximity':[..,..,...] }

#output=list of dict or each row,  from above 
q3output = {'median_house_value': [], 'median_income': [], 'total_bedrooms': [], 'housing_median_age': [], 'ocean_proximity': []}
for e in output:
    for k,v in e.items():
            q3output[k].append(v)

            
#OR      
#output from above       
q3output = {}
for e in output:
    for k,v in e.items():
        if k not in q3output:
            q3output[k] = [v]
        else:
            q3output[k].append(v) 
            

            
            
Q4: Create dict with key as unique value of 'ocean_proximity' as below 
{'INLAND' :{'housing_median_age':[..,..,...] , 'total_bedrooms' :[..,..,...], 'median_income':[..,..,...] ,'median_house_value':[..,..,...]} ,
 '<1H OCEAN':{..} , 'NEAR OCEAN':{..}, 'NEAR BAY':{..}}

#output=list of dict or each row,  from above  , don't use q3output  
q4output = {}
for e in output:
    key = e['ocean_proximity']
    if key not in q4output:
        q4output[key] = {}    
    for k,v in e.items():
        if k != 'ocean_proximity':
            if k not in q4output[key]:
                q4output[key][k] = [v]
            else:
                q4output[key][k].append(v) 
 
 
 
 
 
Q5: Create a dict of 
{'INLAND' :{'max':{'housing_median_age':maxvalue , 'total_bedrooms' :maxvalue},
            'sum':{'housing_median_age':sumvalue , 'total_bedrooms' :sumvalue}}
'<1H OCEAN':{..} , 
'NEAR OCEAN':{..}, 
'NEAR BAY':{..}}

#q4output=dict of ocean_proximity and value is dict of housing_median_age,...  from above 
q5output = {}
for ocean, another_dict in q4output.items():
    if ocean not in q5output:
        q5output[ocean] = {'max':{}, 'sum':{}}    
    for k,v in another_dict.items():
        q5output[ocean]['max'][k] = max(v)
        q5output[ocean]['sum'][k] = sum(v)



{'<1H OCEAN': {'max': {'housing_median_age': 52.0,
                       'median_house_value': 500001.0,
                       'median_income': 10.9237,
                       'total_bedrooms': 1473.0},
               'sum': {'housing_median_age': 556.0,
                       'median_house_value': 7800210.0,
                       'median_income': 115.698,
                       'total_bedrooms': 11823.0}},
 'INLAND': {'max': {'housing_median_age': 35.0,
                    'median_house_value': 204300.0,
                    'median_income': 4.8958,
                    'total_bedrooms': 914.0},
            'sum': {'housing_median_age': 288.0,
                    'median_house_value': 1455100.0,
                    'median_income': 36.4965,
                    'total_bedrooms': 2674.0}},
 'NEAR BAY': {'max': {'housing_median_age': 52.0,
                      'median_house_value': 452600.0,
                      'median_income': 8.3252,
                      'total_bedrooms': 1106.0},
              'sum': {'housing_median_age': 520.0,
                      'median_house_value': 3426300.0,
                      'median_income': 53.1639,
                      'total_bedrooms': 5135.0}},
 'NEAR OCEAN': {'max': {'housing_median_age': 35.0,
                        'median_house_value': 500001.0,
                        'median_income': 12.4429,
                        'total_bedrooms': 826.0},
                'sum': {'housing_median_age': 301.0,
                        'median_house_value': 5475008.0,
                        'median_income': 93.3656,
                        'total_bedrooms': 5704.0}}}

                        
#
actual = {'<1H OCEAN': {'max': {'housing_median_age': 52.0,
                       'total_bedrooms': 1473.0},
               'sum': {'housing_median_age': 556.0,
                       'total_bedrooms': 11823.0}},
 'INLAND': {'max': {'housing_median_age': 35.0,
                    'total_bedrooms': 914.0},
            'sum': {'housing_median_age': 288.0,
                    'total_bedrooms': 2674.0}},
 'NEAR BAY': {'max': {'housing_median_age': 52.0,
                      'total_bedrooms': 1106.0},
              'sum': {'housing_median_age': 520.0,
                      'total_bedrooms': 5135.0}},
 'NEAR OCEAN': {'max': {'housing_median_age': 35.0,
                        'total_bedrooms': 826.0},
                'sum': {'housing_median_age': 301.0,
                        'total_bedrooms': 5704.0}}}                       
                        
{'<1H OCEAN': {'max': {'housing_median_age': 52.0, 'total_bedrooms': 1473.0},
               'sum': {'housing_median_age': 556.0, 'total_bedrooms': 11823.0}},

 'INLAND': {'max': {'housing_median_age': 35.0, 'total_bedrooms': 914.0},
            'sum': {'housing_median_age': 288.0, 'total_bedrooms': 2674.0}},
 'NEAR BAY': {'max': {'housing_median_age': 52.0, 'total_bedrooms': 1106.0},
              'sum': {'housing_median_age': 520.0, 'total_bedrooms': 5135.0}},
 'NEAR OCEAN': {'max': {'housing_median_age': 35.0, 'total_bedrooms': 826.0},
                'sum': {'housing_median_age': 301.0, 'total_bedrooms': 5704.0}}}


###Class examples 

#File(dir) class with getMaxSizeFile()

import datetime,re
class File:
    def __init__(self, dir, pattern=r".", dynamic=False):
        self.dir = dir 
        self.file_dict = None 
        self.refresh = dynamic
        self.pattern = pattern
    def _isToBeRead(self):
        return not self.file_dict or self.refresh        
    def getAllFiles(self):
        def recurse(root, acc={} ):
            import os.path, glob
            lst = [os.path.normpath(f) for f in glob.glob(os.path.join(root, "*"))]
            acc.update( { f:{'size':os.path.getsize(f), 
                             'mtime': datetime.date.fromtimestamp(os.path.getmtime(f)),
                             'ctime': datetime.date.fromtimestamp(os.path.getctime(f))}   for f in lst if os.path.isfile(f) and re.search(self.pattern,f) } )
            [recurse(f, acc) for f in lst if os.path.isdir(f)]	
            return acc
        if self._isToBeRead():
            self.file_dict = recurse(self.dir)
    def getMaxSizeFile(self, howmany=1):
        self.getAllFiles()
        maxnames = sorted(self.file_dict.keys(), key = lambda n: self.file_dict[n]['size'], reverse=True )
        return ( [(maxnames[i],self.file_dict[maxnames[i]]['size'])  for i in range(howmany)] )
    def getLatestFiles(self, after=datetime.date.today()-datetime.timedelta(days=7)):
        """ after : datetime.date(year, month, day)"""
        self.getAllFiles()
        return [ f  for f in  self.file_dict if self.file_dict[f]['mtime'] >= after or self.file_dict[f]['ctime'] >= after ]
        
        

#Poly 
import re
class Poly:
	def __init__(self, *args):		# an, an-1, ...., a0		
		self.a = { "a" + str(arg[0]) : arg[1]  for arg in list(enumerate(args[::-1])) } #degree = max n , #of elements = degree + 1
		self.degree = len(args)-1
	def to_array(self):
		#print(self.a)
		res = [ self.a.setdefault("a" + str(count), 0) for count in range(0, self.degree+1)]
		res.reverse()		
		return res
	def __str__(self):
		arr = self.to_array();
		#print(arr)		
		res = "".join( [ ("-" if v[1] < 0 else "+" ) + str(abs(v[1])) + "x^" + str(v[0]) for v in list(enumerate(arr[::-1]))[::-1] ]) 
		#print(res)
		#re.sub(pattern, repl, string)
		res = res[0:-3]  		  #chop last  x^0
		res = re.sub('(\+|\-)0x\^\d', '', res)   # +0x^2
		res = re.sub('(\+|\-)1(\.0)*x\^', 'x^', res)    # +1x
		res = re.sub('x\^1', 'x', res)      #^1
		res = re.sub('^\+', '', res)         #beginning +
		res = re.sub('(\+|\-)0(\.0)*$', '', res)         #last +0
		return res
	def  expand(self, newdeg):           #in place op
		if newdeg <= self.degree:
			return
		curdeg = self.degree + 1
		for i in range(curdeg, newdeg+1):
			self.a["a" + str(i)] = 0
		self.degree = newdeg	
	def __add__ (self, other):
		in1 = self.to_array()   #an is 0th element
		#if constant
		if type(other) is int :
			in1[0] += other
		elif type(other) is float:
			in1[0] += other
		else:
			other.expand( self.degree ) if self.degree > other.degree else self.expand(other.degree)
			o = other.to_array()
			in1 = self.to_array()
			for i in range(0, self.degree + 1):
				in1[i] += o[i]  #an is 0th element  
		return Poly(*in1)
	def __sub__ (self, other):
		in1 = self.to_array()   #an is 0th element
		#if constant
		if type(other) is int :
			in1[0] -= other
		elif type(other) is float:
			in1[0] -= other
		else:
			other.expand( self.degree ) if self.degree > other.degree else self.expand(other.degree)
			o = other.to_array()
			in1 = self.to_array()
			for i in range(0, self.degree + 1):
				in1[i] -= o[i]  #an is 0th element  
		return Poly(*in1)
	def evaluate(self, x):
		result = 0
		for ele in self.to_array():
			result = result * x + ele
		return result
	def derivative(self):		
		in1 = self.to_array()		
		in1.pop()
		if len(in1) == 0:
			return Poly(0)	
		deg = self.degree		
		in2 = []
		for i in range(0, deg):
			in2.append(in1[i] * deg )  #an is 0th element
			deg -= 1
		return Poly(*in2)
	def __mul__(self, other):  
		in1 = self.to_array()   #an is 0th element
		#if constant
		if type(other) is int :
			in1 = [ ele * other for ele in in1]
		elif type(other) is float:
			in1 = [ ele * other for ele in in1]
		else:
			res = [ 0 for i in range(0, self.degree + other.degree +1) ]
			in1 = self.to_array()
			o = other.to_array()
			for i in range(0, self.degree + 1):
				for j in range(0, other.degree+1):
					res[i+j] += in1[i] * o[j]
			in1 = res.copy()
		return Poly(*in1)
	def __truediv__(self, other):
		in1 = self.to_array()   #an is 0th element
		#if constant
		if type(other) is int :
			in1 = [ ele / other for ele in in1]
			return Poly(*in1)
		elif type(other) is float:
			in1 = [ ele / other for ele in in1]
			return Poly(*in1)
		else:
			n = self.to_array()	
			rd = other.to_array()
			gd = len(rd)
			q = []
			#print(q, n)
			if  len(n) >= gd  :   
				while  len(n) >= gd  :
					piv = n[0]/rd[0]
					q.append(piv)
					for i in range(0, min(len(n), gd)):
						n[i] -= rd[i] * piv						 
					n = n[1:]
				#print(Poly(*q), Poly(*n), piv)
				return [ Poly(*q), Poly(*n) ]
			return [ Poly(0), Poly(*n) ];

			

px = Poly( 2, 1,1)
print(px)
qx = Poly( 3, 1,-1)
print(qx)
cx = px + qx
print(cx)
cx = qx - px
print(cx)
print(px.evaluate(1))
print(px.derivative())

px = Poly( 1,1)
qx = Poly(  1,-1)
cx = px * qx
print(cx)
px = Poly( 1,1)
qx = Poly(1,0,-1)
print(qx)
print(px)
cx = qx / px
print("Q= %s R=%s" % (cx[0],cx[1]))

Design a mixin class LoggingMixin to be used as 

class MyClass(LoggingMixin):
    def somefunction.......
        self.log(msg, *args, **kwargs)


class LoggingMixin:
    def log(self, msg, *args, **kwargs):
        logs to a file and console together 
        get all configuration from calling below methods 
            loggerName = getLoggerName
            isFileLevelLoggingOn
            fileName = getLogFileName 
            fileLogLevel = getFileLogLevel
            fileFormatter = getFileFormatter 
            isConsoleLevelLoggingOn 
            consoleLogLevel = getConsoleLogLevel
            consoleFormatter = getConsoleFormatter 
        these methods can be overridden by derived class 
        if not overriddern, then use resonable default 

#Ans 
import logging 
class LoggingMixin(object):
        logger = None 
        curLevel = None 
        def setCurrentLoggingLevel(self, lvl=None):
            self.curLevel = lvl
        def getCurrentLoggingLevel(self):
            return logging.WARNING if self.curLevel is None else self.curLevel        
        def isFileLevelLoggingRequired(self):
            return True 
        def isConsoleLevelLoggingRequired(self):
            return True 
        def getLogFileName(self):
            return self.__class__.__name__ + ".log"
        def getFileLogLevel(self):
            return logging.WARNING
        def getFileFormatter(self):
            logFormatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")
            return logFormatter
        def getConsoleLogLevel(self):
            return self.getFileLogLevel()            
        def getConsoleFormatter(self):
            return self.getFileFormatter()
        def forceRoot(self):
            return False 
        def getLoggerName(self):
            if self.forceRoot():
                return None 
            return self.__class__.__name__
        def _config(self):
            fOn = self.isFileLevelLoggingRequired()
            cOn = self.isConsoleLevelLoggingRequired()
            fn = self.getLogFileName()
            fl = self.getFileLogLevel()
            ff = self.getFileFormatter()
            cl = self.getConsoleLogLevel()    
            cf = self.getConsoleFormatter()
            ln = self.getLoggerName()
            _logger = logging.getLogger(ln)
            #check whether we need to update class varible or not
            if LoggingMixin.logger is None:
                LoggingMixin.logger = _logger 
            elif LoggingMixin.logger is not _logger:
                self.logger = _logger 
            else:
                return 
            #file
            if fOn:
                self.fileHandler = logging.FileHandler(fn)
                self.fileHandler.setFormatter(ff)
                self.fileHandler.setLevel(fl)
                self.logger.addHandler(self.fileHandler)
            #console
            if cOn:
                self.consoleHandler = logging.StreamHandler()
                self.consoleHandler.setFormatter(cf)
                self.consoleHandler.setLevel(cl)
                self.logger.addHandler(self.consoleHandler)
            #done 
        def log(self, msg, *args, **kwargs):
            lvl = self.getCurrentLoggingLevel()
            self._config()
            res = self.logger.log(lvl, msg, *args, **kwargs)
            return res 
        

class SomeClass(LoggingMixin):
    def test(self):
        self.log('%s before you %s', 'Look', 'leap!')
 
     
##Create a Subprocess Class which have following methods 

a = Subprocess(command)
a.exitcode(timeout=None)
a.stdout(timeout=None)
a.stderr(timeout=None)
a.pipeTo(rhs_command) -> returns a new Subprocess of the result 
a.redirectTo(fileName, timeout=None)
a.get_pattern(pattern, timeout=None, isout=True) -> gets pattern from stdout if isout=True 
else from stderr 
Note there must be internal method 
_execute(timeout=None) which does the actual work
and sets a internal flag executed=True
all other methods calls execute(..) based on this flag and then returns required value 

import subprocess as S
class Subprocess(object):
    def __init__(self, command, wait_after_kill=60):
        self.command = command 
        self.executed = False 
        self.proc = None 
        self.wait_after_kill = wait_after_kill
    def _execute(self, timeout=None, stdin=None, stdout=S.PIPE, stderr=S.PIPE, bufsize=-1, pipeFlag=False):
        import time 
        if self.executed:
            return "Already executed, Create again" 
        self.proc = S.Popen(self.command, bufsize=bufsize, shell=True, stdin=stdin,
            stdout=stdout, stderr=stderr, universal_newlines=True)
        if pipeFlag:
            return None #other process must drain stdout 
        tmout = timeout if timeout is not None else 9999 #very big number 
        while tmout > 0 and self.proc.poll() is None:
            time.sleep(1)
            tmout -= 1 
        if tmout == 0: #timeout case
            self.proc.terminate()
            time.sleep(self.wait_after_kill)
            if self.proc.poll() is None:
                self.proc.kill()
                time.sleep(self.wait_after_kill)
            self._exitcode = -9
        else:
            self.executed = True 
            self._exitcode = self.proc.returncode 
        self._out, self._err = self.proc.communicate()        
        return None 
    def exitcode(self, timeout=None):
        self._execute(timeout)
        return self._exitcode
    def stdout(self, timeout=None):
        self._execute(timeout)
        return self._out
    def stderr(self, timeout=None):
        self._execute(timeout)
        return self._err
    def redirectTo(self, fileName, timeout=None):
        with open(fileName, "wt") as f:
            self._execute(timeout, stdout=f, stderr=S.STDOUT)
        return self._exitcode
    def pipeTo(self, rhs_command, timeout=None):
        self._execute(timeout, stdout=S.PIPE, stderr=S.STDOUT, pipeFlag=True)
        proc2 = Subprocess(rhs_command)
        proc2._execute(timeout, stdin=self.proc.stdout)
        self.proc.stdout.close()
        return proc2 
    def get_pattern(self, pattern, timeout=None, isout=True):
        import re 
        self._execute(timeout)
        if isout:
            res = re.findall(pattern, self._out)
        else:
            res = re.findall(pattern, self._err)
        return res 

#Testing 
command = "nslookup www.google.com"
file= "out.txt" 
pattern = r"Address: (.+?)\n\n" 
pattern2 = r"Addresses:\s+((.+)\n\t\s*(.+)\n\n)"
command1 = "type out.txt"
command2 = 'findstr /c:"Server"'

a = Subprocess(command)
a.exitcode()
a.stdout()
a.stderr()
#timeout case 
a = Subprocess(command)
a.exitcode(1)
a.stdout(1)
a.stderr(1)
#others 
a = Subprocess(command)
a.redirectTo(file)
#others 
a = Subprocess(command1)
b = a.pipeTo(command2)
b.exitcode()
b.stdout()
b.stderr()
#others 
a = Subprocess(command)
a.get_pattern(pattern)


##Asynchronous Subprocess 
import asyncio, sys
import asyncio.subprocess

class AsyncSubprocess(object):
    def __init__(self, **commands):
        self.procs = {}
        for k, v in commands.items():
            self.procs[k] = {'command':v }
        #Create loop, on windows , subproces is supported only in ProactorEventLoop
        if sys.platform == "win32":
            self.loop = asyncio.ProactorEventLoop()
            #asyncio.set_event_loop(self.loop)
        else:
            self.loop = asyncio.get_event_loop()
    async def run(self, key):        
        proc = await asyncio.create_subprocess_shell(
            self.procs[key]['command'],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE, loop=self.loop)
        stdout, stderr = await proc.communicate()
        self.procs[key]['exitcode'] = proc.returncode
        self.procs[key]['stdout'] = stdout.decode()
        self.procs[key]['stderr'] = stderr.decode()
        return key  
    def get_all_results(self):
        result = self.loop.run_until_complete(asyncio.gather(*[self.run(key) for key in self.procs], loop=self.loop))
        self.loop.close()
        return self.procs 
    def get_next_result(self):
        coros = [self.run(key) for key in self.procs]
        # get commands output concurrently
        for f in asyncio.as_completed(coros, loop=self.loop): # f is future
            key = self.loop.run_until_complete(f)
            yield {key: self.procs[key]}
        self.loop.close()
        
#Testing 
a = AsyncSubprocess(c1=command, c2=command, c3=command)
>>> a.get_all_results()
{'c1': {'exitcode': 0, 'command': 'nslookup www.google.com', 'stderr': '', 'stdout': 'Server:\t\t218.248.112.1\nAddress:\t218.248.112.1#53\n\nNon-authoritativeanswer:\nName:\twww.google.com\nAddress: 172.217.163.68\n\n'}, 'c3': {'exitcode': 0, 'command': 'nslookup www.google.com', 'stderr': '', 'stdout': 'Server:\t\t218.248.112.1\nAddress:\t218.248.112.1#53\n\nNon-authoritative answer:\nName:\twww.google.com\nAddress: 172.217.163.68\n\n'}, 'c2': {'exitcode': 0, 'command': 'nslookup www.google.com', 'stderr': '', 'stdout': 'Server:\t\t218.248.112.1\nAddress:\t218.248.112.1#53\n\nNon-authoritative answer:\nName:\twww.google.com\nAddress: 172.217.163.68\n\n'}}

a = AsyncSubprocess(c1=command, c2=command, c3=command)
i = iter(a.get_next_result())
>>> next(i)
{'c3': {'exitcode': 0, 'command': 'nslookup www.google.com', 'stderr': '', 'stdout': 'Server:\t\t218.248.112.1\nAddress:\t218.248.112.1#53\n\nNon-authoritativeanswer:\nName:\twww.google.com\nAddress: 172.217.163.68\n\n'}}
>>> next(i)
{'c1': {'exitcode': 0, 'command': 'nslookup www.google.com', 'stderr': '', 'stdout': 'Server:\t\t218.248.112.1\nAddress:\t218.248.112.1#53\n\nNon-authoritativeanswer:\nName:\twww.google.com\nAddress: 172.217.163.68\n\n'}}
>>> next(i)
{'c2': {'exitcode': 0, 'command': 'nslookup www.google.com', 'stderr': '', 'stdout': 'Server:\t\t218.248.112.1\nAddress:\t218.248.112.1#53\n\nNon-authoritativeanswer:\nName:\twww.google.com\nAddress: 172.217.163.68\n\n'}}
>>> next(i)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration


###Decorators hands ON 
import time 
from functools import wraps 
def mea(f):
    @wraps(f)
    def _inner(*args, **kargs):
        s = time.time()
        res = f(*args, **kargs)
        e = time.time()
        print("Time, taken by",f.__name__,  e-s )
        return res 
    return _inner
def trace(f):
    @wraps(f)
    def _inner(*args, **kargs):
        print("Entering", f.__name__)
        res = f(*args, **kargs)
        print("Exiting", f.__name__)
        return res 
    return _inner  



###Yield hands on 
#open WindowsUpdate.log, Send all  WARNING one by one 


def getWarning(filename):
    f = open(filename, "rt")
    sp=r"(\d\d\d\d-\d\d-\d\d)\s+.+?WARNING"
    for line in f :
        s = re.findall(sp, line)
        if not s:
            continue
        else:
            yield s[0]    
    f.close()    

#Usage 
g = getWarning(r"D:\PPT\python\initial-reference\data\WindowsUpdate.log")
i = iter(g)
print(next(i))
import itertools
print(list(itertools.islice(i,20)))


### DB 
import csv
with open(r"..\data\iris.csv", "rt") as f:
    rd = csv.reader(f)
    rows = list(rd)

rowsd = []
for sl, sw, pl, pw, n in rows[1:]:
    rowsd.append([float(sl), float(sw), float(pl), float(pw),n])

#manual group by 
unique = {row[-1] for row in rowsd}
d = { name:[row[0] for row in rowsd if row[-1] == name] for name in unique  }
{n:{'max':max(lst)}  for n,lst in d.items()}
    
#db group by 

from sqlite3 import connect
con = connect(r"iris.db")
cur = con.cursor()

cur.execute("create table iris (sl double, sw double, pl double, pw double, name string)")
for row in rowsd:
    s = cur.execute("insert into iris values (?,?,?,?,?)",row)

con.commit()
q = cur.execute("select name, max(sl) from iris group by name order by name")
result= list(q.fetchall())
result
#ris-virginica', 7.9), ('Iris-versicolor', 7.0), ('Iris-setosa', 5.8)]
con.close()




###Requests with beautifulSoup 
from bs4 import BeautifulSoup
import requests

r  = requests.get("http://www.yahoo.com")
data = r.text

soup = BeautifulSoup(data, 'html.parser')
soup.get_text()

for link in soup.find_all('a'):  # tag <a href=".."
		print(link.get('href'))	 # Attribute href


        
        
        
        
        
        
        
        
        
###Requests module to send json data and get json data - httpbin.org/get /post 

import json, requests 
data = {'username': 'xyz'}
headers = {'Content-Type': 'application/json'}
r = requests.post("http://httpbin.org/post", data=json.dumps(data), headers=headers)
r.json()
#GET 
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get("http://httpbin.org/get", params=payload)
print(r.url)  #http://httpbin.org/get?key2=value2&key1=value1
r.headers
r.text

#With proxies 
#ofr socks, check http://docs.python-requests.org/en/master/user/advanced/#socks
#update username, proxyaddress, port 
#password is taken from commandline 
proxies = {
  'http': 'http://username:%s@proxyAddress:port',
  'https': 'https://username:%s@proxyAddress:port',
}
#above is equivalent to 
#set http_proxy=http://username:password@proxyAddress:port
#set https_proxy=https://username:password@proxyAddress:port

import getpass
p = getpass.getpass() 
#update proxies 
proxies = {k: v % (p,) for k,v in proxies.items()}

requests.get('http://example.org', proxies=proxies)

##Verbose logging 
import requests
import logging

# for Python 3
from http.client import HTTPConnection
#for python 2
#from httplib import HTTPConnection

HTTPConnection.debuglevel = 1

logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

requests.get('https://httpbin.org/headers')

##FUrther 
r = requests.get('https://api.github.com', auth=('user', 'pass'))

#r is a response, with attributes 
r.request.allow_redirects  r.request.headers          r.request.response
r.request.auth             r.request.hooks            r.request.send
r.request.cert             r.request.method           r.request.sent
r.request.config           r.request.params           r.request.session
r.request.cookies          r.request.path_url         r.request.timeout
r.request.data             r.request.prefetch         r.request.url
r.request.deregister_hook  r.request.proxies          r.request.verify
r.request.files            r.request.redirect         
r.request.full_url         r.request.register_hook

#r.request.headers gives the headers:

{'Accept': '*/*',
 'Accept-Encoding': 'identity, deflate, compress, gzip',
 'Authorization': u'Basic dXNlcjpwYXNz',
 'User-Agent': 'python-requests/0.12.1'}

#Then r.request.data has the body as a mapping. 
#To convert this with urllib.urlencode if they prefer:

import urllib
b = r.request.data
encoded_body = urllib.urlencode(b)




###Introduction to function and Flask framework to send json output 

#rest.py 
from flask import Flask, request, jsonify
import json 

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html><body><h1>Hello there!!!</h1></body></html>    
    """

@app.route("/json", methods=["POST"])
def json1():
    with open(r"D:\PPT\python\initial-reference\data\example.json", "rt") as f :
        obj = json.load(f)
    resp = jsonify(obj)
    resp.status_code = 200 
    return resp


@app.route('/index', methods=['POST'])
def index():
    user = { 'username': 'Nobody'}
    if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
        user['username'] = request.json['username']
    resp = jsonify(user)
    resp.status_code = 200 
    return resp 



if __name__ == '__main__':
    app.run()
    
#with gevent as server 
from gevent.pywsgi import WSGIServer
from rest import app

http_server = WSGIServer(('127.0.0.1', 5000), app)
http_server.serve_forever()
    
    
#Usage 
$ curl -v -H "Content-Type:application/json" -X POST http://127.0.0.1:5000/index -d "{\"username\":\"Das\"}"

import requests
import json
user={'username': 'Das'}
headers= {'Content-Type':"application/json"}
r = requests.post("http://127.0.0.1:5000/index", data=json.dumps(user), headers=headers)
>>> r.json()
{'username': 'Das'}

>>> import subprocess
>>> import shlex
>>> args = shlex.split(r'curl -v -H "Content-Type:application/json" -X POST http://127.0.0.1:5000/index -d "{\"username\":\"Das\"}"')
>>> args
['curl', '-v', '-H', 'Content-Type:application/json', '-X', 'POST', 'http://127.0.0.1:5000/index', '-d', '{"username":"Das"}']
obj = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
>>> obj.stdout.read()
'{\n  "username": "Das"\n}\n'
>>> obj.stderr.read()



###Modules and doc test 

def square(x):
    """First function square 
    
    >>> square(10)
    100
    
    >>> square(0)
    0
    
    """
    z = x*x 
    return z 
if __name__ == '__main__':
    import doctest 
    doctest.testmod() 
    

###Pytest of MyInt with mocking 

#pytest.ini 
[pytest]
markers = 
    addl: Addl testcases 
    
#conftest.py 
from pkg.MyInt import MyInt 
import pytest 


@pytest.fixture(scope='module')
def one(request):
    a = MyInt(1)
    yield a 
    print("shutdown code")
    
'''
$ python -m pytest -v first_test.py 

#To see all builtin fixtures 

$ pytest --fixtures

#default fixture 
#cache, capsys,capfd,doctest_namespace,pytestconfig,record_xml_property,monkeypatch,recwarn,tmpdir_factory,tmpdir


#check default markers
pytest --markers   
         
#For running marker
pytest -v -m addl
pytest -v -m "not addl"

'''
#test_myint.py 
from pkg.MyInt import MyInt 
import pytest

class TestMyInt:
    def test_add(self):
        a = MyInt(2)
        b = MyInt(3)
        assert a+b == MyInt(5)
     
@pytest.mark.addl     
def test_sub(one):   
    assert one - one  == MyInt(0)
    
    
#table tests     
def process(a,op,b):
    if op == '+': return a+b 
    if op == '==': return a == b 
    if op == '-' : return a - b 
    
#pytest -v -k "sub" test_myint.py
#pytest -v -k "not sub" test_myint.py
#pytest -v -k "sub and Test" test_myint.py
#pytest -v -k "sub or add" test_myint.py
#pytest --collect-only  test_myint.py
#pytest -v test_myint.py::test_sub
@pytest.mark.parametrize("a,op,b,op2,result",[
    (MyInt(1) , '+' ,MyInt(2), '==', MyInt(3)),
    pytest.param(MyInt(2),'-',MyInt(1),'==',MyInt(1), marks=pytest.mark.addl),
    ],
    ids=["Testing add2", "Testing sub2"]
)
def testMany(a,op,b,op2,result):
    assert process(process(a,op,b),op2,result)
    
    
import pkg.MyInt 
def test_add_monkey(request, monkeypatch):
    def myint(a):
        print("Patching")
        return a 
    monkeypatch.setattr(pkg.MyInt, "MyInt", myint)
    assert pkg.MyInt.MyInt(2) + pkg.MyInt.MyInt(2) == pkg.MyInt.MyInt(4)

    
###Group_by with functions 

B. boston.csv 
    :Attribute Information (in order):
        - CRIM     per capita crime rate by town
        - ZN       proportion of residential land zoned for lots over 25,000 sq.ft.
        - INDUS    proportion of non-retail business acres per town
        - CHAS     Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
        - NOX      nitric oxides concentration (parts per 10 million)
        - RM       average number of rooms per dwelling
        - AGE      proportion of owner-occupied units built prior to 1940
        - DIS      weighted distances to five Boston employment centres
        - RAD      index of accessibility to radial highways
        - TAX      full-value property-tax rate per $10,000
        - PTRATIO  pupil-teacher ratio by town
        - B        1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
        - LSTAT    % lower status of the population
        - MEDV     Median value of owner-occupied homes in $1000s

"crim", "zn",   "indus", "chas", "nox",  "rm",  "age",  "dis",  "rad", "tax", "ptratio", "b",   "lstat","medv"
0.00632, 18,     2.31,    "0",    0.538,  6.575, 65.2,   4.09,  1,      296,   15.3,      396.9, 4.98,   24



1. read data in boston 
rows = read_csv(r"D:\Desktop\PPT\python\initial-reference\data\boston.csv") 


2. Create a new column crimxmedv = crim X medv 
headers = rows[0]
data = rows[1:]

def get_col(key, row, headers=[]):
    hs = {h:i for i,h in enumerate(headers)} 
    #print(key, row, headers)
    def get(k):
        #print(len(row), k, hs[k])
        if type(k) is int:
            return row[k]
        elif type(k) is str:
            return row[hs[k]]
        else:
            return None 
    g = get(key)
    if g != None :
        return g 
    elif type(key) is tuple or type(key) is list:
        return tuple([ get(i)  for i in key])



def withColumn(hs, data, colName, opp_fn , *cols):
    from copy import deepcopy  
    new_data = deepcopy(data)
    headers = deepcopy(hs)
    headers.append(colName)    
    for i,row in enumerate(data):
        value = opp_fn(*get_col(cols,row,hs))
        new_data[i].append(value)
    return (headers, new_data)

#test 
from functools import partial 
bcol = partial(get_col, headers=headers)
bcol(["crim", "medv"], data[0])

#ans
headers, data = withColumn(headers,data, "crimxdev", lambda a,b :a*b, "crim", "medv")




3. select columns crimxmedv , tax 
s_data = [get_col(["crimxdev","tax"], row, headers) for row in data]
   
   
   
4. what is the max value of crim 
crim_max = max([get_col("crim", row, headers) for row in data])


5. what is max value of medv 
medv_max = max([get_col("medv", row, headers) for row in data])


5. select rows of crim where medv is max 
crim_mdev = [get_col(["crim", "medv"], row, headers) for row in data]
[ r[0]  for r in crim_mdev if r[-1] == medv_max]


6. select rows of medv where crim is max 
[ r[-1]  for r in crim_mdev if r[0] == crim_max]

7. how many unique value in chas and rad 
un = {get_col("chas", row, headers) for row in data}
{get_col("rad", row, headers) for row in data}

8. what is max and min value of medv for each chas 
g_data = group_by(data, lambda row: get_col("chas", row, headers))
agg(g_data, dict(max=max,min=min))
#OR 
medv_chas = [get_col(["medv", "chas"], row, headers) for row in data]
g_data = group_by(medv_chas, lambda row: row[-1])
agg(g_data, dict(max=max,min=min))



9. put crimxmedv and tax in csv 
s_data = [get_col(["crimxdev","tax"], row, headers) for row in data]

write_csv("process.csv", s_data, ["crimxdev","tax"])


  
  
C. windows.csv 

1.read csv file 
2. extract each column  and then 'cast' to correct type with name eventTime,deviceId,signal
col1 - timestamp, column2 - string, column3-int 

rows = read_csv(r"D:\Desktop\PPT\python\initial-reference\data\window.csv",dates=0) 

  
4. group by deviceId and collect all signals into a list 'signals'
headers = rows[0]
data = rows[1:]
g_data = group_by(data, lambda row: row[1])
n_headers = ["deviceId", "signals"]
rows = [[k,[e[-1] for e in lst]] for k,lst in g_data.items()]

#another group by with deviceId and minute
g_data = group_by(data, lambda row: (row[1], row[0].minute))
{k:len(lst) for k,lst in g_data.items()}
n_headers = ["deviceId", "signals"]
rows = [[k,[e[-1] for e in lst]] for k,lst in g_data.items()]



4. select deviceId,signals, it's size and dump into csv file '
n_headers.append("size")
rows = [[d,s,len(s)] for d,s in rows]
write_csv("process1.csv", rows,n_headers)
 
 
5. Create 5 minutes tumbling window and create bins from min to max time 
   Assign each to correct window 
 
def time_window(mn, mx, size):
    res = [] 
    td = (mx - mn)/size 
    start = mn 
    while start < mx :
        res.append((start, start+size))
        start = start + size 
    #append last one 
    res.append((start, start+size))
    return res 

def find(dt, windows):
    for i, win in enumerate(windows):
        if dt >= win[0] and dt < win[1]:
            break
    return windows[i]

min_t = min([r[0] for r in data])
max_t = max([r[0] for r in data])
#timedelta([days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])
import datetime 
size = datetime.timedelta(minutes=5)

wns = time_window(min_t, max_t, size)

headers, data = withColumn(headers,data, "window", lambda w : find(w,wns), "eventTime")
g_data = group_by(data, lambda row: get_col(["deviceId","window"], row, headers))

g_data.keys()
{k:len(lst) for k,lst in g_data.items()}
{(k1, e-s):len(lst) for (k1,(s,e)),lst in g_data.items()}
 
rows = [[k,[e[-2] for e in lst]] for k,lst in g_data.items()]

n_headers = headers + ["size"]
rows = [[d,s,len(s)] for d,s in rows]
write_csv("process2.csv", rows,n_headers)
 
 
###SortyBy example 
#Given a dir, find out the file name which is of max file size recursively 

import functools
import os.path
import glob

def createdirlist(root, acc={} ):
	import os.path
	import glob
	lst = [os.path.normpath(f) for f in glob.glob(os.path.join(root, "*"))]
	acc.update( { f:os.path.getsize(f) for f in lst if os.path.isfile(f) } )
	[createdirlist(f, acc) for f in lst if os.path.isdir(f)]	
	return acc

d = createdirlist(".")
maxnames = sorted(d.keys(), key = lambda n: d[n], reverse=True )
print([maxnames[0], d[maxnames[0]]])



 
 
 
###Sortby example -population.csv 
#Country Name,Country Code,Year,Value,Country

rows = read_csv(r"D:\Desktop\PPT\python\initial-reference\data\population.csv") 
headers = rows[0]
data = rows[1:]

1. which country has the max population during 2008 
countries = [ (row[0], row[-2])    for row in data if row[-1] == "Yes" and row[-3]== 2008]
sorted(countries, key = lambda t: t[-1])[-1]


2. what is the total population of "World" during 2008 
world_2008 = [ (row[0], row[-2])    for row in data if row[0] == "World" and row[-3]== 2008]




3. which year is the max jump in "World" population 
worlds = [ (row[0], row[-2], row[-3])    for row in data if row[0] == "World"]
#get it sorted with year 
w_s = sorted(worlds, key=lambda t: t[-1])
    

w_s_d = [ (n1,v1,v2,y1,y2,v2-v1)    for (n1,v1,y1),(n2,v2,y2) in zip(w_s, w_s[1:])]
#first two 
sorted(w_s_d, key=lambda t: t[-1])[-1:-3:-1]


4. During 2008, which of "Low Income", "Middle Income" and "High Income" has max jump in population 
keys = ("Low income", "Middle income" , "High income")
years = (2007, 2008)


rows = [ (row[0], row[-2], row[-3])    for row in data if row[0] in keys and row[-3] in years]
#sort based year and country name 
sr = sorted(rows, key=lambda t: (t[0], t[-1]))

#
f_sr = [ (n1,n2,v1,v2,y1,y2,v2-v1)    for (n1,v1,y1),(n2,v2,y2) in  zip( sr[::2], sr[1::2]) ]
sorted(f_sr, key=lambda t : t[-1])[-1]


##More hands on 
#File Hands on 
def filecopy(src, dest):
    """Copy one file to another file 
    src,dest: file name as string
    returns None 
    """
    with open(src, "rb") as s:
        with open(dest, "wb") as d:
            d.write(s.read())
    #done 
    
def filecompare(file1,file2):
    """Given two files, compare file contents line by line 
    file1,file2 : file name as string 
    returns line number of 2nd file where first difference occurs
    """
    with open(file1, "rt") as f1:
        with open(file2, "rt") as f2:
            for index,(l2,l1) in enumerate(zip(f2,f1)):                
                if l2 != l1:
                    return index+1
    return -1 
    
def filemerge(one_dir, dest_file, file_filter):
    """Concatenate many files with file_file_filter under one dir into one file
    one_dir : given dir name as str 
    dest_file : file name where to copy 
    file_filter = string regex of files to merge 
    returns none """ 
    import os.path, re, glob 
    files = glob.glob(os.path.normpath(one_dir+"/*"))
    #print(files)
    only_files = [f for f in files if re.search(file_filter, f)]
    #print(only_files)
    def file_copy(file):
        with open(file, "rb") as s:
            with open(dest_file, "ab") as d: 
                    d.write(s.read())
    for f in only_files:
        file_copy(f)
    #done 
    

def execute_and_return_code(command):
    """Given command, returns it's exit code"""
    import subprocess as S , os 
    with open(os.devnull, "w") as DEVNULL:
        proc = S.Popen(command, shell=True, 
            stdout=DEVNULL, stderr=DEVNULL, universal_newlines=True)
        proc.wait()
    return proc.returncode
    
    
def execute_and_return_output(command):
    """Given command , returns it's stdout and stderr """
    import subprocess as S , os 
    proc = S.Popen(command, shell=True, 
        stdout=S.PIPE, stderr=S.STDOUT, universal_newlines=True)
    outs, oute = proc.communicate()
    return outs
    
    

def execute_and_redirect_to_file(command, filename):
    """Given command and file name, redirect stdout and stderr to file"""
    import subprocess as S , os 
    with open(filename, "wt") as f :    
        proc = S.Popen(command, shell=True, 
            stdout=f, stderr=S.STDOUT, universal_newlines=True)
        proc.wait()
    return None 

def execute_with_pipe(command1, command2):    
    """Given two commands, returns output of 2nd command after piping first command""" 
    import subprocess as S , os 
    proc = S.Popen(command1, shell=True, 
        stdout=S.PIPE, stderr=S.STDOUT, universal_newlines=True)
    proc2 = S.Popen(command2, shell=True, 
        stdin= proc.stdout, 
        stdout=S.PIPE, stderr=S.STDOUT, universal_newlines=True)
    proc.stdout.close()
    outs, oute = proc2.communicate()
    return outs 
        
    
    
def execute_and_return_pattern_match(command, pattern):
    """execute the command and the find the pattern in that stdout 
    and return result
    Use execute_and_return_output(command) function to implement this 
    """  
    import subprocess as S , os , re     
    outs = execute_and_return_output(command)
    res = re.findall(pattern, outs)
    return res 
    
    
    
def update_env_var(another_dict):
    """Given another dict of env vars , update to process env vars 
    Note env vars may contain reference to other environment vars in form of $VAR
    so should expand that before updating
    
    Test above function with with below env vars containing below 
    HOST        hostname 
    DT          todays date(use datetime.datetime) using pattern "%m%d%y%H%M%S" 
    SCRIPT      this script name only (without extension)
    SCRIPT_PID  this script pid 
    OUTDIR      C:/tmp/adm
    LOGFILE      $OUTDIR/$SCRIPT.$DT.log (in unix expansion of variable )
    """
    import os , os.path
    #find $VAR type 
    without_exp = {}
    with_exp = {}
    for k, v in another_dict.items():
        if '$' in v:
            with_exp[k] = v 
        else:
            without_exp[k] = v 
    #update first 
    os.environ.update(without_exp)
    #then 
    os.environ.update({k:os.path.expandvars(v) for k, v in with_exp.items()})
    #done 
    
    
import platform, os , sys, datetime as D 
d = dict(HOST=platform.uname().node, 
                      DT=D.datetime.today().strftime("%m%d%y%H%M%S"),
                      SCRIPT=os.path.splitext(os.path.basename(sys.argv[0]))[0],
                      SCRIPT_PID=str(os.getpid()),
                      OUTDIR=r"/var/adm/aaas",
                      LOGFILE="$OUTDIR/$SCRIPT.$DT.log")
  
    
    
    
def dump_env_var(only_keys):
    """returns dict of  env var of element found in 'only_keys'   
    """
    d = {}
    keys = [k.upper() for k in only_keys]
    for k,v in os.environ.items():
        if k.upper() in only_keys:
            d[k]=v 
    return d 
            
def dump_env_var_in_child(only_keys):
    """returns dict env var of element found in 'only_keys'
    in child process"""
    import sys, subprocess as S , os 
    command = "set" if sys.platform in ["win32"] else "printenv"
    proc = S.Popen(command, shell=True, stdout=S.PIPE, stderr=S.STDOUT, universal_newlines=True)
    outs, errs = proc.communicate()
    d = {}
    keys = [k.upper() for k in only_keys]
    for line in outs.splitlines():
        ss = line.split("=")
        if ss[0].upper() in only_keys:
            d[ss[0]]= ss[1] if ss[1:] else ""
    return d 

            
            
#recursion
def get_all_files(one_dir):
    """Given a directory one_dir , 
    returns dict of filenames and size including subdirs    
    """
    import os.path, glob 
    def createdirlist(root, acc):
        lst = glob.glob(os.path.normpath(root+"/*"))
        acc.update( { f:os.path.getsize(f) for f in lst if os.path.isfile(f) } )
        [createdirlist(f, acc) for f in lst if os.path.isdir(f)]	
        return acc
    return createdirlist(one_dir, {})
    
def get_all_files_after(one_dir, after_datetime):
    """Given a directory one_dir , 
    returns list of filenames which are modified or created after_datetime 
    recursively
    """
    import os.path, glob , datetime as D 
    def recurFile(root, acc):
        lst = glob.glob(os.path.normpath(root+"/*"))
        acc.update( { f:{'ctime': D.datetime.fromtimestamp(os.path.getctime(f)),
                          'mtime': D.datetime.fromtimestamp(os.path.getmtime(f))} 
                for f in lst if os.path.isfile(f) } )
        [recurFile(f, acc) for f in lst if os.path.isdir(f)]	
        return acc
    def after(d):
        dtime = D.datetime.strptime(after_datetime, "%Y-%m-%d")
        if d['mtime'] >= dtime or d['ctime'] >= dtime:
            return True 
        return False 
    all_files = [f for f, dt in recurFile(one_dir, {}).items() if after(dt)]
    return all_files
    
    
def create_hashes_of_all_files_under_one_dir(one_dir):
    """ Create a .hashes file inside each dir . this file contains 
    all file names of that dir and hash of each file"""
    import os.path, glob , os , sys 
    def md5(fname):
        import hashlib
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    def process_one_dir(root, files):
        with open(os.path.join(root,".hashes"), "wt") as f:
            for file in files:
                if os.path.exists(file):
                    f.writelines([os.path.basename(file)+"="+str(md5(file))+"\n"])
    lst = glob.glob(os.path.normpath(one_dir+"/*"))
    process_one_dir(one_dir, [f for f in lst if os.path.isfile(f) ] )
    [create_hashes_of_all_files_under_one_dir(f) for f in lst if os.path.isdir(f)]	
    return None
        
###Aynchronous quick  
import asyncio, sys
import threading, concurrent.futures  #in Py2, must do, pip install futures
import os.path 
import functools,time
import asyncio.subprocess


#Create loop, on windows , subproces is supported only in ProactorEventLoop
if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()

executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
loop.set_default_executor(executor)

'''
***** Asyncio primer *******

1. await can be used inside another async def/coroutine 
   result = await arg
   A Future, a coroutine or an awaitable, 'arg' is required
2. Inside main process use loop.run_until_complete(future_coroutine)

#Example 
import asyncio
import threading, concurrent.futures  #in Py2, must do, pip install futures
import os.path 
import functools,time



#Create loop, on windows , subproces is supported only in ProactorEventLoop
import sys
if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()


#simple coroutines 
async def m2(*args):
    print("m2")
    return args[0:1]


async def m1(arg1,arg2):
    #option 1
    r1 = await m2(arg1)  #blocks, m2 is executed now 
    await asyncio.sleep(1)
    #option 2 with Task(is a asyncio.Future with cancel())
    fut = asyncio.ensure_future(m2(arg2))
    fut.add_done_callback(lambda f: print(f.result())) #f= future of m2(arg2)
    #or 
    r2 = await fut     #r2 is direct result 
    await asyncio.sleep(1)
    #option-3 await with with timeout
    try:
        r3 = await asyncio.wait_for(m2(arg2), timeout=None) #any float , None means blocking
    except asyncio.TimeoutError:
        print('timeout!')
    #option-4: wait for many coroutines 
    r4 = await asyncio.gather(m2(2),m2(3))   #r4 is list of result 
    return [r1,r2,r3] 

#all the above obj in 'await obj' can be passed to  'run_until_complete'
#start the events loop 
r2 = loop.run_until_complete(m1(2,3))
#or a list of many coroutines 
r2 = loop.run_until_complete(asyncio.gather(m1(2,3), m1(2,3)))
    
#To run non coroutine based function  under asyncio 
#Option-1: with executor
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
loop.set_default_executor(executor)

def m3(*args):
    print("m3", threading.current_thread().getName())
    time.sleep(1)
    return len(args)

#r is asyncio.Future 
r = loop.run_in_executor(None, m3, 2,3 ) #executor=None , means default executor or provide custom axecutor 
result = loop.run_until_complete(r) #await r inside coroutine 

#Option-2: with delayed call , can not return result 
h1 = loop.call_soon(m3, 2,3)
h1 = loop.call_later(2, m3, 2,3) #after 2 secs, should not exceed one day.
h1 = loop.call_at(loop.time()+3, m3, 2,3) #after 3 sec, should not exceed one day.

async def dummy():
    await asyncio.sleep(10)

#some other thread function calling normal function under asyncio
def callback(loop):
    time.sleep(1)
    loop.call_soon_threadsafe(m3, 2,3)

t = threading.Thread(target=callback, args=(loop,))
t.start()
loop.run_until_complete(dummy())
    
    
#Synchronization primitives 
#also has 
asyncio.Lock
asyncio.Event
asyncio.Condition
asyncio.Semaphore
asyncio.BoundedSemaphore
#Usage 
count = 0 
async def proc(lck):
    global count 
    async with lck:
        print("Got it")
        lc = count 
        lc += 1 
        count = lc 


lock = asyncio.Lock() # asyncio.Semaphore(2) #asyncio.BoundedSemaphore(2)
loop.run_until_complete(asyncio.gather(*[proc(lock) for i in range(10)]))


#Usage Event 
async def waiter(event):
    print('waiting for it ...')
    await event.wait()
    print('... got it!')

async def main():
    # Create an Event object.
    event = asyncio.Event()
    # Spawn a Task to wait until 'event' is set.
    waiter_task = asyncio.ensure_future(waiter(event))
    # Sleep for 1 second and set the event.
    await asyncio.sleep(1)
    event.set()
    # Wait until the waiter task is finished.
    await waiter_task

loop.run_until_complete(main())
    
#Queue 
#infinte loop 
async def worker(name,queue):
    while True:
        item = await queue.get()  #blocks , get_nowait(): does not block, but raises QueueEmpty
        await asyncio.sleep(1)
        print("Got",name, item)
        queue.task_done()

async def main():
    queue = asyncio.Queue()  #maxsize=0 , means infinite 
    tasks = []
    [queue.put_nowait(i) for i in range(10)] #does not block raises QueueFull, put():no block 
    for i in range(3):
        task = asyncio.ensure_future(worker(str(i),queue))
        tasks.append(task)
    await queue.join()
    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()


loop.run_until_complete(main())    
    
#Subprocess 
async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    print(cmd, 'exited with ',proc.returncode)
    if stdout:
        print('[stdout]\n',stdout.decode())
    if stderr:
        print('[stderr]\n',stderr.decode())
    return stdout.decode()

async def main(urls):
    coros = [run("nslookup "+ url) for url in urls]
    #for f in asyncio.as_completed(coros): # print in the order they finish
    #    print(await f)
    #or 
    return await asyncio.gather(*coros)

urls = ["www.google.com", "www.yahoo.com", "www.wikipedia.org"]
result = loop.run_until_complete(main(urls))


    

#aiohttp
import aiohttp  #asyncio enabled http requests 

        
async def get(session, url, *args, **kwargs):  
    async with session.get(url, *args, **kwargs ) as resp:
        return (await resp.json())

async def post(session, url, *args, **kwargs):  
    async with session.post(url, *args, **kwargs ) as resp:
        return (await resp.json())

async def download_get(urls, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
            results = await asyncio.gather(*[get(session, url, *args, **kwargs) for url in urls])
    return results 

async def download_post(urls, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
            results = await asyncio.gather(*[post(session, url, *args, **kwargs) for url in urls])
    return results 

urls1 = ["http://httpbin.org/get" for i in range(10)]
urls2 = ["http://httpbin.org/post" for i in range(10)]
headers = {'Content-Type': 'application/json'}
params = { 'name': 'abc'}
data = {'name': 'xyz'}
import json 

rsults = loop.run_until_complete(download_get(urls1, params=params))        
rsults = loop.run_until_complete(download_post(urls2, data=json.dumps(params),headers=headers))        


loop.stop()

'''

@asyncio.coroutine
def get_date():
    code = 'import datetime; print(datetime.datetime.now())'  #python code 
    # Create the subprocess, redirect the standard output into a pipe
    create = asyncio.create_subprocess_exec(sys.executable, '-c', code,  stdout=asyncio.subprocess.PIPE)
    proc = yield from create
    # Read one line of output
    data = yield from proc.stdout.readline()
    line = data.decode('ascii').rstrip()
    # Wait for the subprocess exit
    yield from proc.wait()
    return line

#asyncio.subprocess.DEVNULL, asyncio.subprocess.STDOUT, asyncio.subprocess.PIPE
'''
If PIPE is passed to stdin argument, the Process.stdin attribute will point to a StreamWriter instance.
If PIPE is passed to stdout or stderr arguments, the Process.stdout and Process.stderr attributes will point to StreamReader instances.

class asyncio.StreamReader
    coroutine read(n=-1)
    coroutine readline()
    coroutine readexactly(n)
    coroutine readuntil(separator=b'\n')
    at_eof()
class asyncio.StreamWriter
    can_write_eof()
    write_eof()
    get_extra_info(name, default=None)
    write(data)
    writelines(data)
    coroutine drain()
        writer.write(data)
        await writer.drain()
    close()
    is_closing()
    coroutine wait_closed()
'''  

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    print(cmd, 'exited with ',proc.returncode)
    if stdout:
        print('[stdout]\n',stdout.decode())
    if stderr:
        print('[stderr]\n',stderr.decode())
    return stdout.decode()

#Another way 
async def get_lines(shell_command):
    p = await asyncio.create_subprocess_shell(shell_command,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
    return (await p.communicate())[0].splitlines()

async def main(urls):
    coros = [run("nslookup "+ url) for url in urls]
    # get commands output concurrently
    for f in asyncio.as_completed(coros): # print in the order they finish
        print("main\n",await f)


urls = ["www.google.com", "www.yahoo.com", "www.wikipedia.org"]
        

result = loop.run_until_complete(asyncio.gather(get_date(), main(urls), *[run("nslookup "+ url) for url in urls]))
print("Current date: %s" % result[0])
loop.close()


#_________________________________________________________________________


1. Write IMDB Ratings class 
Given a movie_id , search imdb  and get it's ratings 
Hint:
1. class name Imdb with movie_id as constructor parameter and one method  
    def ratings(source='Internet Movie Database')
      Source could be 'Internet Movie Database' or 'Metacritic'
2. Use Rest server http://omdbapi.com/
  eg http://omdbapi.com/?i=tt1270797&apikey=5cdc2256
3. Movie id is receieved from https://www.imdb.com
4. Advanced class structure can be seen from existing python module https://imdbpy.sourceforge.io/


class IMDB:
    def __init__(self, movie_id, api_key="5cdc2256"):
        self.movie_id = movie_id 
        self.json = None
        self.api_key = api_key         
    def _load(self):
        import requests
        if self.json is None:
            r = requests.get("http://omdbapi.com/?i=%s&apikey=%s" %(self.movie_id,self.api_key))
            self.json = r.json()
    def ratings(self, source='Internet Movie Database'):
        self._load()
        _tmp = [each['Value'] for each in self.json['Ratings'] if each['Source'] == source]
        return _tmp[0] if _tmp else "Not Found"
                






2. Pandas 
a. Read sales_transactions.xlsx 
b. What percentage of the total order value(ie ext price) does each order represent?"
Hint: Use dataframe.transform along with groupby of order 
OR use dataframe.Join on 'order' after groupby of order , Then get % 


df = pd.read_excel("./data/sales_transactions.xlsx")
df.groupby('order').mean()

>>> df.groupby('order')["ext price"].sum().rename("Order_Total").reset_index()
   order  Order_Total
0  10001       576.12
1  10005      8185.49
2  10006      3724.49

#how to combine this data back with the original dataframe. 
order_total = df.groupby('order')["ext price"].sum().rename("Order_Total").reset_index()
df_1 = df.merge(order_total, on='order')
>>> df_1.head(3)
   account      name  order       sku  quantity  unit price  ext price     Order_Total
0   383080  Will LLC  10001  B1-20000         7       33.69     235.83  0       576.12
1   383080  Will LLC  10001  S1-27722        11       21.12     232.32  1       576.12
2   383080  Will LLC  10001  B1-86481         3       35.99     107.97  2       576.12


df_1["Percent_of_Order"] = df_1["ext price"] / df_1["Order_Total"]


#Second Approach - Using Transform
>>> df.groupby('order')["ext price"].transform('sum')
0      576.12
1      576.12
2      576.12
3     8185.49
4     8185.49
5     8185.49
6     8185.49
7     8185.49
8     3724.49
9     3724.49
10    3724.49
11    3724.49
Name: ext price, dtype: float64

df["Order_Total"] = df.groupby('order')["ext price"].transform('sum')
df["Percent_of_Order"] = df["ext price"] / df["Order_Total"]

#other problem 
>>> df.groupby('order')["ext price"].mean().max()
1637.098
>>> df.groupby('order')["ext price"].mean().argmax()
__main__:1: FutureWarning: 'argmax' is deprecated. Use 'idxmax'
argmax' will be corrected to return the positional maximum in th
es.argmax' to get the position of the maximum now.
10005
>>> df.groupby('order')["ext price"].mean().values.argmax()
1
>>> df.groupby('order')["ext price"].mean().idxmax()
10005
>>> df.groupby('account')["ext price"].sum().idxmax()
412290
>>> df.groupby('account')["quantity"].sum().idxmax()
412290
>>> df.groupby('sku')["quantity"].sum().idxmax()



3. Write Django REST API server 
API: 
    http://localhost:8000/get_weather?location=mumbai
Result: In Json 
{ 'todays_date':{'text': .., 'high':..., 'low': ..}, 'tomorrow_date': {...} .. like five days data}

Use -  module weather-api 
https://pypi.org/project/weather-api/

3.2. Test using requests 
a. write one script get_weather.py to interact with REST server 
b. should take location via command line 
c. print json output using pprint.pprint 

#commands
$ django-admin startproject weathersite
$ python manage.py migrate
$ python manage.py runserver 8000

#Urls.py 
from django.contrib import admin
from django.urls import path, include
from .views import get_weather


urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_weather/', get_weather, name='get_weather21'), #for default 
    path('get_weather/<str:location>', get_weather, name='get_weather22'),
    path('get_weather', get_weather, name='get_weather'), #for handling ?GET_QUERY or POST QUERY , Note no end '/'
]



#views.py 
from weather import Weather, Unit
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json 

import logging
log = logging.getLogger(__name__)


@csrf_exempt
def get_weather(request, location='mumbai'):
    loc = None
    loc = request.GET.dict().get('location', None)
    log.info("GET " + str(loc))
    if loc is None and 'post' in request.method.lower() :
        #log.info("POST " + str(request.META))
        #note it is CONTENT_TYPE , not Content-Type 
        if 'CONTENT_TYPE' in request.META and 'application/json' in request.META['CONTENT_TYPE']: 
            loc = json.loads(request.body.decode()).get('location', None)
            log.info("JSON POST " + str(loc))
        else:
            loc = request.POST.dict().get('location', None)
            log.info("FORM POST " + str(loc))
    if loc is None:
        loc = location 
        log.info("REST GET " + str(loc))
    weather = Weather(unit=Unit.CELSIUS)
    data = {loc:{}}
    error = {loc: 'Not Found'}
    try:
        location = weather.lookup_by_location(loc)
    except Exception as ex:
        error[loc] = str(ex)
        return JsonResponse(error)  
    if location is None:
        return JsonResponse(error) 
    forecasts = location.forecast
    for forecast in forecasts:
        data[loc][forecast.date] = {}
        data[loc][forecast.date]['text'] = forecast.text
        data[loc][forecast.date]['high'] = forecast.high
        data[loc][forecast.date]['low'] = forecast.low
    return JsonResponse(data)          
    
##testing 
import requests 
import json , pprint

data = {'location':'hyderabad'}
headers = {'Content-Type': 'application/json'}
error = {'location':'xyz'}

test = {
    'test1' : {'url': "http://localhost:8000/get_weather", 'method': requests.get , 'data':{}},
    'test2' : {'url': "http://localhost:8000/get_weather", 'method': requests.get , 'data': dict(params=data)},
    'test3' : {'url': "http://localhost:8000/get_weather", 'method': requests.get , 'data': dict(params=error)},
    'test4' : {'url': "http://localhost:8000/get_weather", 'method': requests.post , 'data': dict(data=data)},
    'test5' : {'url': "http://localhost:8000/get_weather", 'method': requests.post , 'data': dict(data=json.dumps(data), headers=headers )},
    'test6' : {'url': "http://localhost:8000/get_weather/", 'method': requests.get , 'data': {}},
    'test7' : {'url': "http://localhost:8000/get_weather/delhi", 'method': requests.get , 'data': {}},
}

for name, p in test.items():
    r = p['method'](p['url'], **p['data'])
    print('for ', name)
    pprint.pprint(r.json())

    
    
###
#unit can be 
CELSIUS = 'c'
FAHRENHEIT = 'f'
    
 
unit = 'c'
URL = 'http://query.yahooapis.com/v1/public/yql'

#lookup(woeid), Lookup WOEID via http://weather.yahoo.com.
woeid = 560743
url = "%s?q=select * from weather.forecast where woeid = '%s' and u='%s' &format=json" % (URL, woeid, unit)

#lookup_by_location(location)
location = 'mumbai'
url = "%s?q=select* from weather.forecast " \
      "where woeid in (select woeid from geo.places(1) where text='%s') and u='%s' &format=json" % (URL, location, unit)
    
#lookup_by_latlng(lat, lng)
lat, lng = 53.3494,-6.2601
url = "%s?q=select* from weather.forecast " \
    "where woeid in (select woeid from geo.places(1) where text='(%s,%s)') and u='%s' &format=json" % (URL, lat, lng, unit)

import requests
r = requests.get(url)
r.json()
#for xml 
location = 'mumbai'
url = "%s?q=select* from weather.forecast " \
      "where woeid in (select woeid from geo.places(1) where text='%s') and u='%s' &format=xml" % (URL, location, unit)
r = requests.get(url)
r.content
import lxml.etree as etree
x = etree.fromstring(r.content) #takes byte string
print(etree.tostring(x, pretty_print=True).decode())

#Json 
{'query': {'count': 1,
           'created': '2018-11-20T01:19:24Z',
           'lang': 'en-US',
           'results': {'channel': {'astronomy': {'sunrise': '6:49 am',
                                                 'sunset': '5:59 pm'},
                                   'atmosphere': {'humidity': '90',
                                                  'pressure': '34202.54',
                                                  'rising': '0',
                                                  'visibility': '25.43'},
                                   'description': 'Yahoo! Weather for Mumbai, '
                                                  'MH, IN',
                                   'image': {'height': '18',
                                             'link': 'http://weather.yahoo.com',
                                             'title': 'Yahoo! Weather',
                                             'url': 'http://l.yimg.com/a/i/brand/purplelogo//uh/us/news-wea.gif',
                                             'width': '142'},
                                   'item': {'condition': {'code': '27',
                                                          'date': 'Tue, 20 Nov '
                                                                  '2018 05:30 '
                                                                  'AM IST',
                                                          'temp': '24',
                                                          'text': 'Mostly '
                                                                  'Cloudy'},
                                            'description': '<![CDATA[<img '
                                                           'src="http://l.yimg.com/a/i/us/we/52/27.gif"/>\n'
                                                           '<BR />\n'
                                                           '<b>Current '
                                                           'Conditions:</b>\n'
                                                           '<BR />Mostly '
                                                           'Cloudy\n'
                                                           '<BR />\n'
                                                           '<BR />\n'
                                                           '<b>Forecast:</b>\n'
                                                           '<BR /> Tue - '
                                                           'Partly Cloudy. '
                                                           'High: 32Low: 24\n'
                                                           '<BR /> Wed - '
                                                           'Partly Cloudy. '
                                                           'High: 32Low: 22\n'
                                                           '<BR /> Thu - '
                                                           'Partly Cloudy. '
                                                           'High: 34Low: 23\n'
                                                           '<BR /> Fri - '
                                                           'Partly Cloudy. '
                                                           'High: 36Low: 23\n'
                                                           '<BR /> Sat - '
                                                           'Sunny. High: '
                                                           '35Low: 22\n'
                                                           '<BR />\n'
                                                           '<BR />\n'
                                                           '<a '
                                                           'href="http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2295411/">Full '
                                                           'Forecast at Yahoo! '

                                                           'Weather</a>\n'
                                                           '<BR />\n'
                                                           '<BR />\n'
                                                           '<BR />\n'
                                                           ']]>',
                                            'forecast': [{'code': '30',
                                                          'date': '20 Nov 2018',

                                                          'day': 'Tue',
                                                          'high': '32',
                                                          'low': '24',
                                                          'text': 'Partly '
                                                                  'Cloudy'},
                                                         {'code': '30',
                                                          'date': '21 Nov 2018',

                                                          'day': 'Wed',
                                                          'high': '32',
                                                          'low': '22',
                                                          'text': 'Partly '
                                                                  'Cloudy'},
                                                         {'code': '30',
                                                          'date': '22 Nov 2018',

                                                          'day': 'Thu',
                                                          'high': '34',
                                                          'low': '23',
                                                          'text': 'Partly '
                                                                  'Cloudy'},
                                                         {'code': '30',
                                                          'date': '23 Nov 2018',

                                                          'day': 'Fri',
                                                          'high': '36',
                                                          'low': '23',
                                                          'text': 'Partly '
                                                                  'Cloudy'},
                                                         {'code': '32',
                                                          'date': '24 Nov 2018',

                                                          'day': 'Sat',
                                                          'high': '35',
                                                          'low': '22',
                                                          'text': 'Sunny'},
                                                         {'code': '30',
                                                          'date': '25 Nov 2018',

                                                          'day': 'Sun',
                                                          'high': '33',
                                                          'low': '20',
                                                          'text': 'Partly '
                                                                  'Cloudy'},
                                                         {'code': '28',
                                                          'date': '26 Nov 2018',

                                                          'day': 'Mon',
                                                          'high': '32',
                                                          'low': '20',
                                                          'text': 'Mostly '
                                                                  'Cloudy'},
                                                         {'code': '34',
                                                          'date': '27 Nov 2018',

                                                          'day': 'Tue',
                                                          'high': '33',
                                                          'low': '18',
                                                          'text': 'Mostly '
                                                                  'Sunny'},
                                                         {'code': '30',
                                                          'date': '28 Nov 2018',

                                                          'day': 'Wed',
                                                          'high': '32',
                                                          'low': '18',
                                                          'text': 'Partly '
                                                                  'Cloudy'},
                                                         {'code': '34',
                                                          'date': '29 Nov 2018',

                                                          'day': 'Thu',
                                                          'high': '32',
                                                          'low': '18',
                                                          'text': 'Mostly '
                                                                  'Sunny'}],
                                            'guid': {'isPermaLink': 'false'},
                                            'lat': '19.090281',
                                            'link': 'http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2295411/',
                                            'long': '72.871368',
                                            'pubDate': 'Tue, 20 Nov 2018 05:30 '

                                                       'AM IST',
                                            'title': 'Conditions for Mumbai, '
                                                     'MH, IN at 05:30 AM IST'},
                                   'language': 'en-us',
                                   'lastBuildDate': 'Tue, 20 Nov 2018 06:49 AM '

                                                    'IST',
                                   'link': 'http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2295411/',
                                   'location': {'city': 'Mumbai',
                                                'country': 'India',
                                                'region': ' MH'},
                                   'title': 'Yahoo! Weather - Mumbai, MH, IN',
                                   'ttl': '60',
                                   'units': {'distance': 'km',
                                             'pressure': 'mb',
                                             'speed': 'km/h',
                                             'temperature': 'C'},
                                   'wind': {'chill': '77',
                                            'direction': '45',
                                            'speed': '4.83'}}}}}

#XML 
<query xmlns:yahoo="http://www.yahooapis.com/v1/base.rng" yahoo:count="1" yahoo:created="2018-11-20T01:24:18Z" yahoo:lang="en-US">
  <results>
    <channel>
      <yweather:units xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" distance="km" pressure="mb" speed="km/h" temperature="C"/>
      <title>Yahoo! Weather - Mumbai, MH, IN</title>
      <link>http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2295411/</link>
      <description>Yahoo! Weather for Mumbai, MH, IN</description>
      <language>en-us</language>
      <lastBuildDate>Tue, 20 Nov 2018 06:54 AM IST</lastBuildDate>
      <ttl>60</ttl>
      <yweather:location xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" city="Mumbai" country="India" region=" MH"/>
      <yweather:wind xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" chill="77" direction="45" speed="4.83"/>
      <yweather:atmosphere xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" humidity="90" pressure="34202.54" rising="0" visibility="25.43"/>
      <yweather:astronomy xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" sunrise="6:49 am" sunset="5:59 pm"/>
      <image>
        <title>Yahoo! Weather</title>
        <width>142</width>
        <height>18</height>
        <link>http://weather.yahoo.com</link>
        <url>http://l.yimg.com/a/i/brand/purplelogo//uh/us/news-wea.gif</url>
      </image>
      <item>
        <title>Conditions for Mumbai, MH, IN at 05:30 AM IST</title>
        <geo:lat xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">19.090281</geo:lat>
        <geo:long xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">72.871368</geo:long>
        <link>http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2295411/</link>
        <pubDate>Tue, 20 Nov 2018 05:30 AM IST</pubDate>
        <yweather:condition xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" code="27" date="Tue, 20 Nov 2018 05:30 AM IST" temp="24" text="Mostly Cloudy"/>
        <yweather:forecast xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" code="30" date="20 Nov 2018" day="Tue" high="32" low="24" text="Partly Cloudy"/>
        <yweather:forecast xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" code="30" date="21 Nov 2018" day="Wed" high="32" low="22" text="Partly Cloudy"/>
        <yweather:forecast xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" code="30" date="22 Nov 2018" day="Thu" high="34" low="23" text="Partly Cloudy"/>
        <yweather:forecast xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" code="30" date="23 Nov 2018" day="Fri" high="36" low="23" text="Partly Cloudy"/>
        <yweather:forecast xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" code="32" date="24 Nov 2018" day="Sat" high="35" low="22" text="Sunny"/>
        <yweather:forecast xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" code="30" date="25 Nov 2018" day="Sun" high="33" low="20" text="Partly Cloudy"/>
        <yweather:forecast xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" code="28" date="26 Nov 2018" day="Mon" high="32" low="20" text="Mostly Cloudy"/>
        <yweather:forecast xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" code="34" date="27 Nov 2018" day="Tue" high="33" low="18" text="Mostly Sunny"/>
        <yweather:forecast xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" code="30" date="28 Nov 2018" day="Wed" high="32" low="18" text="Partly Cloudy"/>
        <yweather:forecast xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" code="34" date="29 Nov 2018" day="Thu" high="32" low="18" text="Mostly Sunny"/>
        <description>&lt;![CDATA[&lt;img src="http://l.yimg.com/a/i/us/we/52/27.gif"/&gt;
&lt;BR /&gt;
&lt;b&gt;Current Conditions:&lt;/b&gt;
&lt;BR /&gt;Mostly Cloudy
&lt;BR /&gt;
&lt;BR /&gt;
&lt;b&gt;Forecast:&lt;/b&gt;
&lt;BR /&gt; Tue - Partly Cloudy. High: 32Low: 24
&lt;BR /&gt; Wed - Partly Cloudy. High: 32Low: 22
&lt;BR /&gt; Thu - Partly Cloudy. High: 34Low: 23
&lt;BR /&gt; Fri - Partly Cloudy. High: 36Low: 23
&lt;BR /&gt; Sat - Sunny. High: 35Low: 22
&lt;BR /&gt;
&lt;BR /&gt;
&lt;a href="http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2295411/"&gt;Full Forecast at Yahoo! Weather&lt;/a&gt;
&lt;BR /&gt;
&lt;BR /&gt;
&lt;BR /&gt;
]]&gt;</description>
        <guid isPermaLink="false"/>
      </item>
    </channel>
  </results>
</query>


###Quick code 

##XML
import xml.etree.ElementTree as ET
tr = ET.parse(r"data\example.xml")
r = tr.getroot()
r.tag
r.attrib
r.text
nn = r.findall("./country/rank")
[n.text  for n in nn]

res = []
for n in nn:
    res.append(n.text)

[int(n.text)  for n in nn]

nn = r.findall("./country")
[n.attrib['name']  for n in nn]

res = []
for n in nn:
    res.append(n.attrib['name'])
    
    
    
##CSV 
import csv
with open(r"data/iris.csv", "rt") as f:
    rd = csv.reader(f)
    rows = list(rd)

rows[0:5]
headers = rows[0]
rows = rows[1:]

rowsd = []
for sl, sw, pl, pw, name in rows:
    rowsd.append([float(sl), float(sw), float(pl), float(pw), name])

rowsd[:5]

names = {row[-1] for row in rowsd }

{n : max([r[0] for r in rowsd if r[-1] == n]) for n in names }

##SQL 
from sqlite3 import connect
con = connect(r"iris.db")
cur = con.cursor()
cur.execute("""create table iris (sl double, sw double,
        pl double, pw double, name string)""")
for r in rowsd:
    cur.execute("""insert into iris values(?,?,?,?,?) """, r)

con.commit()
q = cur.execute("""select name, max(sl) from iris group by name""")
result = list(q.fetchall())
print(result)
cur.execute("""drop table if exists iris""")

con.close()

##JSON 
import json
with open(r"data/example.json", "rt") as f:
    obj = json.load(f)

[emp['empId']   for emp in obj]

res = []
for emp in obj:
    res.append(emp['empId'])

[emp['details']['firstName'] + emp['details']['lastName']   for emp in obj]

for emp in obj:
    res.append(emp['details']['firstName'] + emp['details']['lastName'])

##REST and JSON 
url = 'http://omdbapi.com/?i=tt1285016&apikey=5cdc2256'
import requests
r = requests.get(url)
r.json()
data = r.json()
[r['Value']     for r in data['Ratings']]

[r['Value']     for r in data['Ratings'] if r['Source']=='Metacritic']


##REST 
import json, requests 
data = {'username': 'xyz'}
headers = {'Content-Type': 'application/json'}
r = requests.post("http://httpbin.org/post", 
    data=json.dumps(data), 
    headers=headers)
r.json()
#GET 
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get("http://httpbin.org/get", params=payload)
print(r.url)  #http://httpbin.org/get?key2=value2&key1=value1
r.headers
r.text

##QUick JSON Server 
from flask import Flask,request, jsonify
import json 

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html><body><h1>Hello there!!!</h1></body></html>    
    """

@app.route("/json", methods=["POST"])
def json1():
    with open(r"data\example.json", "rt") as f :
        obj = json.load(f)
    resp = jsonify(obj)
    resp.status_code = 200 
    return resp


@app.route('/index', methods=['POST'])
def index():
    user = { 'username': 'Nobody'}
    if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
        user['username'] = request.json['username']
    resp = jsonify(user)
    resp.status_code = 200 
    return resp 

  

if __name__ == '__main__':
    app.run()
    


##HTML scrapping 
from bs4 import BeautifulSoup
import requests

r  = requests.get("http://www.yahoo.com")
data = r.text

soup = BeautifulSoup(data, 'html.parser')
soup.get_text()

for link in soup.find_all('a'):  # tag <a href=".."
		print(link.get('href'))	 # Attribute href

