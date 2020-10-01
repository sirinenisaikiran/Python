Contents 
Module - pexpect for linux for py3.x or p2.7
ftplib Module - windows, linux , py2.x, py3.x 
Telnetlib - py3.x, py2.x, 
paramiko module - (2.6+, 3.3+) implementation of the SSHv2 protocol , provides server and client
Python Logging 
Python Argument Parsing 
Os and os.path module 
Module -subprocess - replaces os.system and os.spawn
Fabric 
------------------------
###*** Module - pexpect for linux for py3.x or p2.7
$ pip install pexpect

#for windows-There are some ports with PyWin32 
#for Py2.7, wexpect (downloaded win-pexpect/) cd and start py prompt

#Windows SSH client and server
#http://www.mls-software.com/opensshd.html
#with older SSH server 
#ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 ftpuser@127.0.0.1

#example -cygwin


#start ssh service , from services.msc for service 'CYGWIN sshd'


#for linux/cygwin
#main methods are 

class pexpect.spawn(command, args=[], timeout=30, maxread=2000, searchwindowsize=None, 
            logfile=None, cwd=None, env=None, ignore_sighup=False, echo=True, preexec_fn=None, 
            encoding=None, codec_errors='strict', dimensions=None)
    #check https://pexpect.readthedocs.io/en/stable/api/pexpect.html
    #Examples
    child = pexpect.spawn('/usr/bin/ftp')
    child = pexpect.spawn('/usr/bin/ssh user@example.com')
    child = pexpect.spawn('ls -latr /tmp')
    #OR
    child = pexpect.spawn('/usr/bin/ftp', [])
    child = pexpect.spawn('/usr/bin/ssh', ['user@example.com'])
    child = pexpect.spawn('ls', ['-latr', '/tmp'])
    After this the child application will be created and will be ready to talk to. 
    For normal use, use expect() and send() and sendline().

    Pexpect does NOT interpret shell meta characters such 
    as redirect, pipe, or wild cards , hence, use shell
    child = pexpect.spawn('/bin/bash -c "ls -l | grep LOG > logs.txt"')
    child.expect(pexpect.EOF)
    #OR
    shell_cmd = 'ls -l | grep LOG > logs.txt'
    child = pexpect.spawn('/bin/bash', ['-c', shell_cmd])
    child.expect(pexpect.EOF)

    The maxread attribute sets the read buffer size. 
    This is maximum number of bytes that Pexpect will try to read from a TTY at one time. 
    Setting the maxread size to 1 will turn off buffering

    When the keyword argument timeout is specified as a number, (default: 30), 
    then TIMEOUT will be raised after the value specified has elapsed, in seconds, 
    When None, TIMEOUT will not be raised, and expect() may block indefinitely until match.

    'searchwindowsiz'e is None (default), 
    the full buffer is searched for pattern at each iteration of receiving incoming  data

    'logfile' member turns on or off logging. 
    All input and output will be copied to the given file object. 
    Set logfile to None to stop logging. This is the default. 
    Set logfile to sys.stdout to echo everything to standard output. 
    The logfile is flushed after each write.
    #Example 
    child = pexpect.spawn('some_command')
    fout = open('mylog.txt','wb')
    child.logfile = fout
    # In Python 2:
    child = pexpect.spawn('some_command')
    child.logfile = sys.stdout
    # In Python 3, spawnu should be used to give str to stdout:
    child = pexpect.spawnu('some_command')
    child.logfile = sys.stdout    
    #Changed in version 4.0: spawn provides both the bytes and unicode interfaces. 
    #In Pexpect 3.x, the unicode interface was provided by a separate spawnu class.
    #Example 
    def execute(host, password, command, prompt):
        child = pexpect.spawnu('/usr/bin/ssh', [host, command])  
        child.logfile = sys.stdout
        child.expect ('Password: ')
        child.sendline (password)
        child.expect (prompt)
        child.sendline ('exit')
        child.close()
        
    The logfile_read and logfile_send members can be used to separately log the input 
    from the child and output sent to the child. 
    #You only want to log what the child sends back. for Py3.x , pass an encoding to spawn 
    child = pexpect.spawn('some_command')
    child.logfile_read = sys.stdout
    To separately log output sent to the child use logfile_send:
    child.logfile_send = fout

    If ignore_sighup is True, the child process will ignore SIGHUP signals. 
    The default is False from Pexpect 4.0, meaning that SIGHUP will be handled normally by the child.

    'delaybeforesend' uses a delay before sending ,  use 0.05 if some delay is required 

    To get the exit status of the child , call child.close()
    and then check child.exitstatus or child.signalstatus

    'echo' attribute may be set to False to disable echoing of input
    
    ##Methods of the class  
    expect(pattern, timeout=-1, searchwindowsize=-1, async=False)
        pattern can be a string(re pattern), pexpect.EOF, pexpect.TIMEOUT, a compiled re, 
        or a list of any of those types for any match 
        This returns the index into the pattern list or 0 if only one pattern given 
        This may raise exceptions for pexpect.EOF or pexpect.TIMEOUT. 
        To avoid the EOF or TIMEOUT exceptions add EOF or TIMEOUT to the pattern list

        When a match is found for the given pattern, 
        'match' becomes an re.MatchObject result or exception
        'before' and 'after' are before and after match   
            #example
            child.expect('password:')
            child.sendline(my_secret_password)
            # We expect any of these three patterns...
            i = child.expect (['Permission denied', 'Terminal type', '[#\$] '])
            if i==0:
                print('Permission denied on host. Can\'t login')
                child.kill(0)
            elif i==1:
                print('Login OK... need to send terminal type.')
                child.sendline('vt100')
                child.expect('[#\$] ')
            elif i==2:
                print('Login OK.')
                print('Shell command prompt', child.after)
        On Python3.4, , passing async=True will make this return an asyncio coroutine, 
            index = yield from p.expect(patterns, async=True)   
        A list entry may be EOF or TIMEOUT instead of a string. 
        This will catch these exceptions and return the index of the list entry instead of raising the exception. 
        The attribute 'after' will be set to the exception type. 
        The attribute 'match' will be None. 
        #Example 
        index = p.expect(['good', 'bad', pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            do_something()
        elif index == 1:
            do_something_else()
        elif index == 2:
            do_some_other_thing()
        elif index == 3:
            do_something_completely_different()

        You can also just expect the EOF if you are waiting for all output of a child to finish. 
        #Example 
        p = pexpect.spawn('/bin/ls')
        p.expect(pexpect.EOF)
        print p.before
        
    expect_exact(pattern_list, timeout=-1, searchwindowsize=-1, async=False) 
        The 'pattern_list' may be a string; a list or other sequence of strings; or TIMEOUT and EOF.
    expect_list(pattern_list, timeout=-1, searchwindowsize=-1, async_=False, **kw)
        This takes a list of compiled regular expressions and returns the index into the pattern_list 
        that matched the child output. 
        The list may also contain EOF or TIMEOUT(which are not compiled regular expressions).    
    compile_pattern_list(patterns)
        This compiles a pattern-string or a list of pattern-strings. 
        Patterns must be a StringType, EOF, TIMEOUT, SRE_Pattern, or a list of those. 
        Patterns may also be None which results in an empty list 
        Thus expect() is nothing more than:
            cpl = self.compile_pattern_list(pl)
            return self.expect_list(cpl, timeout)
    send(s)
        Sends string s to the child process, returning the number of bytes written. 
        If a logfile is specified, a copy is written to that log.
        As this is buffered, there is a limited size of such buffer.
        On Linux systems, this is 4096 (defined by N_TTY_BUF_SIZE). 
        All other systems honor the POSIX.1 definition PC_MAX_CANON – 1024 on OSX, 256 on OpenSolaris, and 1920 on FreeBSD.
    sendline(s='')
        Wraps send(), sending string s to child process, with os.linesep automatically appended. 
        Returns number of bytes written.
    writelines(sequence)
        This calls write() for each element in the sequence. 
        The sequence can be any iterable object producing strings, typically a list of strings. 
        This does not add line separators. 
    write(s)
        This is similar to send() except that there is no return value.
    sendcontrol(char) 
        Helper method that wraps send() with mnemonic access for sending control character to the child 
        child.sendcontrol('g')
    sendeof() 
        This sends an EOF to the child
    sendintr()
        This sends a SIGINT to the child. 
    readline(size=-1)
        This reads and returns one entire line. 
        The newline at the end of line is returned as part of the string, unless the file ends without a newline. 
        An empty string is returned if EOF is encountered immediately.
    read(size=-1) 
        This reads at most "size" bytes from the file 
    eof()
        This returns True if the EOF exception was ever raised.
    interact(escape_character='\x1d', input_filter=None, output_filter=None)
        This gives control of the child process to the interactive user 
        (the human at the keyboard).
        Keystrokes are sent to the child process, and the stdout and stderr output of the child process is printed. This simply echos the child stdout and child stderr to the real stdout and it echos the real stdin to the child stdin
    read_nonblocking(size=1, timeout=-1)[source]
        This reads at most size characters from the child application. 
        It includes a timeout.
        If the read does not complete within the timeout period then a TIMEOUT exception is raised
        If timeout is None then the read may block indefinitely. 
        If timeout is -1 then the self.timeout value is used. 
        If timeout is 0 then the child is polled and if there is no data immediately ready then this will raise a TIMEOUT exception.
    eof()
        This returns True if the EOF exception was ever raised.
    #Controlling the child process from spawn
    kill(sig)
    terminate(force=False)
    isalive()
    wait()
    close()

    
    
pexpect.run(command, timeout=30, withexitstatus=False, events=None, extra_args=None, logfile=None, cwd=None, env=None, **kwargs)[source] 
    This function runs the given command; waits for it to finish; 
    then returns all output as a string. STDERR is included in output. 
    If the full path to the command is not given then the path is searched.
    #Examples 
    from pexpect import *
    child = spawn('scp foo user@example.com:.')
    child.expect('(?i)password')
    child.sendline(mypassword)
    #or 
    run("ssh username@machine.example.com 'ls -l'",  events={'(?i)password':'secret\n'})
    #Run a command and capture exit status:
    from pexpect import *
    (command_output, exitstatus) = run('ls -l /bin', withexitstatus=1)
    #The following will run SSH and execute 'ls -l' on the remote machine. 
    #The password ‘secret’ will be sent if the '(?i)password' pattern is ever seen:
    run("ssh username@machine.example.com 'ls -l'",  events={'(?i)password':'secret\n'})

    
    
###Tips - Find the end of line – CR/LF conventions
#The $ pattern for end of line match is useless, Use below
child.expect('\r\n')  
child.expect('\w+\r\n')

#Pexpect compiles all regular expressions with the re.DOTALL flag. 
#With the DOTALL flag, a "." will match a newline
#+ and * at the end of patterns - in pexpect, always non greedy

#match  one character
child.expect ('.+')
#match no characters
child.expect ('.*')

##Debugging
#use str(child) where child = spawn(..)


##Pexpect on Windows
#As of version 4.0, Pexpect can be used on Windows and POSIX systems. 
#pexpect.spawn and pexpect.run() are not available on Windows, 
#Use below for cross platform code 

class pexpect.popen_spawn.PopenSpawn(cmd, timeout=30, maxread=2000, searchwindowsize=None, 
                logfile=None, cwd=None, env=None, encoding=None, codec_errors='strict', preexec_fn=None)
    expect()
    expect_exact()
    expect_list()
    send(s)
        Send data to the subprocess’ stdin.
        Returns the number of bytes written.
    sendline(s='')
        Wraps send(), sending string s to child process, with os.linesep automatically appended. 
        Returns number of bytes written.
    write(s)
        This is similar to send() except that there is no return value.
    writelines(sequence)
        This calls write() for each element in the sequence.
        The sequence can be any iterable object producing strings, typically a list of strings. 
        This does not add line separators. There is no return value.
    kill(sig)
        Sends a Unix signal to the subprocess.
        Use constants from the signal module to specify which signal.
    sendeof()
        Closes the stdin pipe from the writing end.
    wait()
        Wait for the subprocess to finish.
        Returns the exit code.







###Example
#in linux/cygwin

import pexpect

pexpect.run('ls -l') # in py3.x , use .decode("ascii"), each line ends with '\r\n'

#using spawn  , use spawnu for Py3.x as unicode version 

child = pexpect.spawn('scp var.txt ftpuser@localhost:.') #moves var.txt to ssh hosts ftpuser 
child.expect ('password: ')
child.sendline ('ftpuser')


child = pexpect.spawn("ssh ftpuser@localhost 'ls -l'")
child.expect ('password: ')
child.sendline ('ftpuser')
for line in child:
	print(">>" + line.decode("utf-8").strip())
	#print ">>" + line.strip() 
	


    
    
    
###*** ftplib Module - windows, linux , py2.x, py3.x 
#start the server from computer management
#IIS
#%windir%\system32\compmgmt.msc
#check ipconfig and change binding for correct ip



import ftplib
import os
filename = ".bashrc"
ftp = ftplib.FTP("192.168.1.106")
ftp.login("ftpuser", "ftpuser")
os.chdir(r'/home/das')    #from windows c:/cygwin64/home/das'
ftp.retrlines('LIST')   # list directory contents
ftp.nlst()  			#['.bashrc', 'class-ex.py', 'one.txt']

ftp.cwd("dump")
ftp.storbinary("STOR " + filename , open(filename, 'rb'))    # for uploading binary file, 
ftp.storlines("STOR " + filename + ".t" , open(filename, 'rb'))    # for uploading text file, always 'b' 
ftp.retrbinary('RETR ' + filename, open(filename + ".bak" , 'wb').write) #for downloading binary file
ftp.retrlines('RETR ' + filename, open(filename + ".bak2" , 'w').write) #for downloding text file

data = []
ftp.dir(data.append)
print("\n".join(data))
ftp.quit()


###*** Telnetlib - py3.x, py2.x, 
#for example start Telnet service from services.msc
#Py3.x - Always  interaction using bytes, hence encode/decode with 'ascii' or use b' '
#ending line by '\r\n'

Telnet.read_until(expected, timeout=None)
Read until a given byte string, expected, is encountered or until timeout seconds have passed.

Telnet.read_all()
Read all data until EOF as bytes; block until connection closed.

Telnet.read_some()
Read at least one byte of cooked data(ie IAC processed) unless EOF is hit. Return b'' if EOF is hit. 

Telnet.read_very_eager()
Read everything that can be without blocking in I/O (eager).

Telnet.read_eager()
Read readily available data.

Telnet.read_lazy()
Process and return data already in the queues (lazy).

Telnet.read_very_lazy()
Return any data available in the cooked queue (very lazy).

Telnet.read_sb_data()
Return the data collected between a SB/SE pair (suboption begin/end).

Telnet.write(buffer)
Write a byte string to the socket, doubling any IAC characters. 

(index_of_match, matchObject, data_till_match) = Telnet.expect(list, timeout=None)
Read until one from a list of a regular expressions matches ie compiled or byte string
If a regular expression ends with a greedy match (such as .*) or if more than one expression can match the same input, 
the results are non-deterministic
When nothing matches, return (-1, None, data)


#details of Telnet 
'''
telnet mode, as described in RFC854
Lines are expected to end with either '\r\n' or '\r\0', or '\n'  and ASCII 255 is used for telnet control codes
IAC in data is doubled , inserts \0 after \r  

Raw mode - basically raw tcpip socket , acts as a transparent bridge, transmitting all bytes across the socket unmodified
lines end with the ASCII NUL character \0, and no control codes are present. IAC in data is not doubled , no insertion of \0 after \r
'''

#Explains nicely options :  https://support.microsoft.com/en-us/kb/231866
  
#Options : http://www.iana.org/assignments/telnet-options/telnet-options.xhtml
'''
Senders wants to do an option  IAC WILL opt   
		receiver responds IAC DO opt or IAC DONT opt
sender asks receiver to do an options IAC DO opt    
		receiver responds IAC WILL opt or IAC WONT opt
'''

#Telnetlib has constants for options (check telnetlib.py)
'''
telnetlib.IAC  
telnetlib.DONT 
telnetlib.DO   
telnetlib.WONT 
telnetlib.WILL 
telnetlib.ECHO    #echoing data characters it receives over the   TELNET connection back to the sender of the data characters
telnetlib.SGA     #Supress GA  for full duplex operation.  by default 
'''
#setting debug level 
Telnet.set_debuglevel(debuglevel)
Set the debug level. >= 1 to get debug output  (on sys.stdout).

#installing callback for options 
Telnet.set_option_negotiation_callback(callback)
Each time a telnet option is read on the input flow, this callback (if set) is called with the following parameters: 
callback(telnet_socket, command (DO/DONT/WILL/WONT), option). 


# Example : How to disable telnet echo in python telnetlib
'''
telnetlib.py automatically responds to IAC commands . (See telnetlib.process_rawq()) if callback is not set 
If telnetlib gets WILL, sends DONT and if gets DO, sends WONT for the same option automatically 
(t.set_debuglevel(1) to get many outputs) 

Hence , telnetlib sends IAC DONT ECHO whenever gets IAC WILL ECHO
However, it might not be enough to turn off echo .
The solution most commonly used is  to say that reciever will do the echoing, which stops other end  doing echoing:
telnetlib.IAC + telnetlib.WILL + telnetlib.ECHO
But in this case, you need to echo back whatever you receive
'''

# set call back
t.set_option_negotiation_callback(callback)

#callback 
def callabck(sock, cmd, opt):
	if cmd == telnetlib.WILL and opt == telnetlib.ECHO:        #Senders  WILL ECHO
		sock.sendall(telnetlib.IAC + telnetlib.DONT + telnetlib.ECHO)
		sock.sendall(telnetlib.IAC + telnetlib.WILL + telnetlib.ECHO) 
	elif opt == telnetlib.ECHO and 	cmd == telnetlib.DO :   # server would respond back with DO for ECHO, ignore that 
		sock.sendall(telnetlib.IAC + telnetlib.WILL + telnetlib.ECHO) 
	else:
		#default handling 
		if cmd in (telnetlib.DO, telnetlib.DONT):
			sock.sendall(telnetlib.IAC + telnetlib.WONT + opt)
		elif cmd in (telnetlib.WILL, telnetlib.WONT):
			sock.sendall(telnetlib.IAC + telnetlib.DONT + opt)


#Write raw sequence
#write - Write a string to the socket, doubling any IAC characters.
#to write raw sequence , get inner socket 

def write_raw_sequence(tn, seq):
	sock = tn.get_socket()
	if sock is not None:
		sock.sendall(seq)

write_raw_sequence(tn, telnetlib.IAC + telnetlib.WILL + telnetlib.ECHO)


#example
import sys
import telnetlib
user = "ftpuser"
passw = "ftpuser"

#For example, you can create a dict , {opt : {cmd : response ...}  }
handlers = { telnetlib.SGA : {telnetlib.DO : telnetlib.WILL, telnetlib.WILL: telnetlib.DO}, telnetlib.ECHO : { telnetlib.WILL: telnetlib.DO }, telnetlib.BINARY: {telnetlib.DO : telnetlib.WILL, telnetlib.WILL: telnetlib.DO} }
text_handlers = {telnetlib.DO : "DO", telnetlib.WILL: "WILL", telnetlib.WONT : "WONT", telnetlib.DONT: "DONT"}


#callback 
def callback(sock, cmd, opt):
	if opt in handlers and cmd in handlers[opt]:
			sock.sendall(telnetlib.IAC + handlers[opt][cmd] + opt)
			print("Handled << IAC %s %d" % (text_handlers[handlers[opt][cmd]], ord(opt)))
	else:
		#default handling from telnetlib 
		if cmd in (telnetlib.DO, telnetlib.DONT):
			sock.sendall(telnetlib.IAC + telnetlib.WONT + opt)
			print("<< IAC %s %d" % (text_handlers[telnetlib.WONT ], ord(opt)))
		elif cmd in (telnetlib.WILL, telnetlib.WONT):
			sock.sendall(telnetlib.IAC + telnetlib.DONT + opt)
			print("<< IAC %s %d" % (text_handlers[telnetlib.DONT], ord(opt)))
			

tn = telnetlib.Telnet();
tn.set_debuglevel(1)
# set call back
tn.set_option_negotiation_callback(callback)
tn.open("localhost", 23)
print(tn.read_until(b"login: "))
tn.write(user.encode('ascii') + b"\r\n")

print(tn.read_until(b"password: "))
tn.write(passw.encode('ascii') + b"\r\n")
print(tn.read_until(b"ftpuser>"))
tn.write(b"dir\r\n")

print(tn.read_until(b"ftpuser>").decode("ascii"))
tn.write(b"exit\r\n")
tn.close()

#debug info 

#Telnet(localhost,23): IAC DO 37   IAC WONT ATHENTICAT
#Telnet(localhost,23): IAC WILL 1  IAC DONT ECHO
#Telnet(localhost,23): IAC WILL 3  IAC DONT SGA 
#Telnet(localhost,23): IAC DO 39   IAC WONT ENVIRON
#Telnet(localhost,23): IAC DO 31   IAC WONT WINDOWSIZE
#Telnet(localhost,23): IAC DO 0    IAC WONT BINARY
#Telnet(localhost,23): IAC WILL 0  IAC DONT BINARY







###*** Python Logging 

#Logging from multiple threads requires no special effort as logging is threadsafe 
#logging from multiple process to same file not supported, use SocketHandler(host, port) 
#or DatagramHandler(host, port)or HTTPHandler(host, url, method='GET') 
#to send to server and let server handle as it sees fit 
#or use advanced multiprocessing module with Lock as locking mechanism


#you can pass contextual information to be output along with logging event information- use the LoggerAdapter class
#you can use filtering mechanisms using using a user-defined Filter


##Logger hierarchy 
#Child loggers propagate messages up to the handlers associated with their ancestor loggers(till root looger)
#For example, given a logger with a name of foo, loggers with names of foo.bar, foo.bar.baz, and foo.bam are all descendants of foo

#Root level Logger - any configuration on this would be used if child logger is not configured 
#default level is WARNING 
rootLogger = logging.getLogger()

#child logger - eg Module level logger 
logger = logging.getLogger(__name__)





##Logging 
Logger.info(msg, *args, **kwargs)
    Logs a message with level INFO on this logger. The arguments are interpreted as for debug().
Logger.warning(msg, *args, **kwargs)
    Logs a message with level WARNING on this logger. The arguments are interpreted as for debug().
Logger.error(msg, *args, **kwargs)
    Logs a message with level ERROR on this logger. The arguments are interpreted as for debug().
Logger.critical(msg, *args, **kwargs)
    Logs a message with level CRITICAL on this logger. The arguments are interpreted as for debug().
Logger.log(lvl, msg, *args, **kwargs)
    Logs a message with integer level lvl on this logger. The other arguments are interpreted as for debug().
Logger.setLevel(level)
    Sets the threshold for this logger to level.

    
    
##basic usages 

import logging

# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')

##OR with config file 

import logging
import logging.config

#disable any existing loggers 
logging.config.fileConfig('logging.conf', disable_existing_loggers=True)

# create logger
logger = logging.getLogger('simpleExample')

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')


#logging.conf file:
[loggers]
keys=root,simpleExample

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_simpleExample]
level=DEBUG
handlers=consoleHandler
qualname=simpleExample
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=






##Multiple logging destinations 
#-D.Ds  for formatting info for string 
#'-' The converted value is left adjusted
#first D, Minimum field width , second D= precision 
#check https://pyformat.info/
import logging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

#Then usage 
rootLogger.warning('%s before you %s', 'Look', 'leap!')

#Prints to the format of:
2012-12-05 16:58:26,618 [MainThread  ] [INFO ]  my message



##Meaning of special syntax 
%(name)s 
    Name of the logger used to log the call. 
%(pathname)s 
    Full pathname of the source file where the logging call was issued (if available). 
%(process)d 
    Process ID (if available). 
%(processName)s 
    Process name 
%(thread)d 
    Thread ID (if available). 
%(threadName)s 
    Thread name (if available). 
%(asctime)s
    Human-readable time when the LogRecord was created. By default this is of the form ‘2003-07-08 16:49:45,896’ (the numbers after the comma are millisecond portion of the time). 
%(filename)s 
    Filename portion of pathname. 
%(funcName)s 
    Name of function containing the logging call. 
%(levelname)s 
    Text logging level for the message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'). 
%(levelno)s 
    Numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL). 
%(lineno)d 
    Source line number where the logging call was issued (if available). 
%(module)s 
    Module (name portion of filename). 
%(msecs)d 
    Millisecond portion of the time when the LogRecord was created. 
%(message)s 
    The logged message, computed as msg % args. 
    
##Handler Support
#Support is included in the package for writing log messages to files, 
#HTTP GET/POST locations, email via SMTP, generic sockets, 
#or OS-specific logging mechanisms such as syslog or the Windows NT event log

#https://docs.python.org/2/library/logging.handlers.html#module-logging.handlers
#under module logging.handlers for all except StreamHandler, FileHandler, NullHandler(under logging)
1.logging.StreamHandler(stream=None) (default stream is sys.stderr) 
    instances send messages to streams (file-like objects).
2.logging.FileHandler(filename, mode='a', encoding=None, delay=False) 
    instances send messages to disk files.
    By default, the file grows indefinitely.
3.BaseRotatingHandler 
    is the base class for handlers that rotate log files at a certain point. It is not meant to be instantiated directly. Instead, use RotatingFileHandler or TimedRotatingFileHandler.
4.logging.handlers.RotatingFileHandler(filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0) 
    instances send messages to disk files, with support for maximum log file sizes and log file rotation.
5.logging.handlers.TimedRotatingFileHandler(filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False) 
    instances send messages to disk files, rotating the log file at certain timed intervals.
6.logging.handlers.SocketHandler(host, port) 
    instances send messages to TCP/IP sockets.
    don't bother with a formatter, since a socket handler sends the event as an unformatted pickle
7.logging.handlers.DatagramHandler(host, port) 
    instances send messages to UDP sockets.
8.logging.handlers.SMTPHandler(mailhost, fromaddr, toaddrs, subject, credentials=None, secure=None) 
    instances send messages to a designated email address.
9.logging.handlers.SysLogHandler(address=('localhost', SYSLOG_UDP_PORT), facility=LOG_USER, socktype=socket.SOCK_DGRAM) 
    instances send messages to a Unix syslog daemon, possibly on a remote machine.
10.logging.handlers.NTEventLogHandler(appname, dllname=None, logtype='Application') 
    instances send messages to a Windows NT/2000/XP event log.
11.logging.handlers.MemoryHandler(capacity, flushLevel=ERROR, target=None)¶ 
    instances send messages to a buffer in memory, which is flushed 
    whenever specific criteria are met.
12.logging.handlers.HTTPHandler(host, url, method='GET') 
    instances send messages to an HTTP server using either GET or POST semantics.
    host is host:port
    Note it sends data as URL key for GET and application/x-www-form-urlencoded for POST 
13.logging.handlers.WatchedFileHandler(filename[, mode[, encoding[, delay]]]) 
    instances watch the file they are logging to. 
    If the file changes, it is closed and reopened using the file name. 
    This handler is only useful on Unix-like systems; Windows does not support the underlying mechanism used.
14.logging.NullHandler 
    instances do nothing with error messages. They are used by library developers who want to use logging, but want to avoid the ‘No handlers could be found for logger XXX’ message which can be displayed if the library user has not configured logging. See Configuring Logging for a Library for more information.

##Quick SocketHandler
#https://docs.python.org/2/howto/logging-cookbook.html#sending-and-receiving-logging-events-across-a-network



##Quick HTTPHandler Pattern using Flask 
#server.py:
#request.args is dict for URL KEY for GET 
#for POST and application/x-www-form-urlencoded, use request.form as dict 
#for post and 'application/json'  , use request.json or request.get_json() which json coverted to py obj 
#for post and 'text/plain', use request.data

from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    for key, value in request.args.items():
        print(key,value)
    return 'GET log' # it has to return something
    
    
@app.route('/json-post', methods = ['POST'])
def json_log():
    if request.headers['Content-Type'] == 'application/json':
        print(json.dumps(request.json))
    return "JSON log"
        
if __name__ == "__main__":
    app.run(debug=True)


#Usage: send_log.py:

import logging
import logging.handlers

logger = logging.getLogger(__name__)

server = '127.0.0.1:5000'
path = '/'
method = 'GET'

sh = logging.handlers.HTTPHandler(server, path, method=method)

logger.addHandler(sh)
logger.setLevel(logging.DEBUG)

logger.debug("Test message.")


##Custom Handler and Formatter eg to send json data to Flask server handling Json 
import requests, json 
class RequestsHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        return requests.post('http://localhost:8080/json-post',log_entry, headers={"Content-type": "application/json"}).content

class JsonFormatter(logging.Formatter):
    def __init__(self, task_name=None):
        self.task_name = task_name
        super(LogstashFormatter, self).__init__()
    def format(self, record):  #LogRecord attributes : https://docs.python.org/2/library/logging.html#logrecord-attributes
        res = super(JsonFormatter, self).format(record)
        data = {'message': res,
                'timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')}
        if self.task_name:
            data['task_name'] = self.task_name
        return json.dumps(data)
#Usage 
class SomeClass:
    def __init__(self, llogging_level,ogger_name="SomeModule.SomeClass"):
        self.logger = logging.getLogger(logger_name.upper())
        self.logger.setLevel(logging_level)
        handler = RequestsHandler()
        formatter = JsonFormatter(logger_name.upper())
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
##Usage of passing extra info in each call to logging 
#Option-1:LoggerAdapter

import logging
extra = {'app_name':'Super App'}

logger = logging.getLogger(__name__)
syslog = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(app_name)s : %(message)s')
syslog.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(syslog)
logger = logging.LoggerAdapter(logger, extra)


logger.info('The sky is so blue')

#Output 
2013-07-09 17:39:33,596 Super App : The sky is so blue


#Option-2: using Filters 
import logging

class AppFilter(logging.Filter):
    def filter(self, record):
        record.app_name = 'Super App'
        return True

logger = logging.getLogger(__name__)
logger.addFilter(AppFilter())
syslog = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(app_name)s : %(message)s')
syslog.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(syslog)

logger.info('The sky is so blue')



    

###*** Python Argument Parsing 

#Example 
import argparse

parser = argparse.ArgumentParser(description='sha_install')
parser.add_argument('-t', dest="INST_METHOD", action="store", help='<<give help text here>>')

args = parser.parse_args()
INST_METHOD = args.INST_METHOD.strip().upper()
print(args)


#Example 
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

#nargs = how many positional args to consume , + means atleast one and consume all 
#metavar would display in help 
#intergers would be destination by default 
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
                    
#'store_const' - store 'const' in 'dest' ie accumulate 
#by default(if no --sum provided) 'accumulate' would 'default' ie max      
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))


$ python prog.py -h
usage: prog.py [-h] [--sum] N [N ...]

Process some integers.

positional arguments:
 N           an integer for the accumulator

optional arguments:
 -h, --help  show this help message and exit
 --sum       sum the integers (default: find the max)


$ python prog.py 1 2 3 4
4

$ python prog.py 1 2 3 4 --sum
10


##Reference 
ArgumentParser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])

name or flags
    an optional argument, like -f or --foo, 
        >> parser.add_argument('-f', '--foo')
    while a positional argument c
        >>> parser.add_argument('bar')
    When parse_args() is called
        >>> parser.parse_args(['BAR'])
        Namespace(bar='BAR', foo=None)
        >>> parser.parse_args(['BAR', '--foo', 'FOO'])
        Namespace(bar='BAR', foo='FOO')
        >>> parser.parse_args(['--foo', 'FOO'])
        usage: PROG [-h] [-f FOO] bar
        PROG: error: the following arguments are required: bar
action
    'store' - This just stores the argument’s value. This is the default action. For example:
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--foo')
        >>> parser.parse_args('--foo 1'.split())
        Namespace(foo='1')
    'store_const' - This stores the value specified by the const keyword argument. 
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--foo', action='store_const', const=42)
        >>> parser.parse_args(['--foo'])
        Namespace(foo=42)
    'store_true' and 'store_false' -for storing the values True and False respectively. 
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--foo', action='store_true')
        >>> parser.add_argument('--bar', action='store_false')
        >>> parser.add_argument('--baz', action='store_false')
        >>> parser.parse_args('--foo --bar'.split())
        Namespace(foo=True, bar=False, baz=True)
    'append' - This stores a list, and appends each argument value to the list. 
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--foo', action='append')
        >>> parser.parse_args('--foo 1 --foo 2'.split())
        Namespace(foo=['1', '2'])
    'append_const' - This stores a list, and appends the value specified by the const keyword argument to the list. 
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--str', dest='types', action='append_const', const=str)
        >>> parser.add_argument('--int', dest='types', action='append_const', const=int)
        >>> parser.parse_args('--str --int'.split())
        Namespace(types=[<class 'str'>, <class 'int'>])
    'count' - This counts the number of times a keyword argument occurs. 
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--verbose', '-v', action='count')
        >>> parser.parse_args(['-vvv'])
        Namespace(verbose=3)
    'help' - This prints a complete help message for all the options in the current parser and then exits.
    'version' - This expects a version= keyword argument in the add_argument() call, 
        and prints version information and exits when invoked:
        >>> import argparse
        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument('--version', action='version', version='%(prog)s 2.0')
        >>> parser.parse_args(['--version'])
        PROG 2.0
nargs
    N (an integer). N arguments from the command line will be gathered together into a list. 
    Note that nargs=1 produces a list of one item
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--foo', nargs=2)
        >>> parser.add_argument('bar', nargs=1)
        >>> parser.parse_args('c --foo a b'.split())
        Namespace(bar=['c'], foo=['a', 'b'])
    '?'. One argument will be consumed from the command line if possible, and produced as a single item. 
    One of the more common uses of nargs='?' is to allow optional input and output files:
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                            default=sys.stdin)
        >>> parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                            default=sys.stdout)
        >>> parser.parse_args(['input.txt', 'output.txt'])
        Namespace(infile=<_io.TextIOWrapper name='input.txt' encoding='UTF-8'>,
                  outfile=<_io.TextIOWrapper name='output.txt' encoding='UTF-8'>)
        >>> parser.parse_args([])
        Namespace(infile=<_io.TextIOWrapper name='<stdin>' encoding='UTF-8'>,
                  outfile=<_io.TextIOWrapper name='<stdout>' encoding='UTF-8'>)
    '*'. All command-line arguments present are gathered into a list. 
    Note that it generally doesn’t make much sense to have more than one positional argument with nargs='*', 
    but multiple optional arguments with nargs='*' is possible. For example:
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--foo', nargs='*')
        >>> parser.add_argument('--bar', nargs='*')
        >>> parser.add_argument('baz', nargs='*')
        >>> parser.parse_args('a b --foo x y --bar 1 2'.split())
        Namespace(bar=['1', '2'], baz=['a', 'b'], foo=['x', 'y'])
    '+'. Just like '*', all command-line args present are gathered into a list.
        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument('foo', nargs='+')
        >>> parser.parse_args(['a', 'b'])
        Namespace(foo=['a', 'b'])
        >>> parser.parse_args([])
        usage: PROG [-h] foo [foo ...]
        PROG: error: the following arguments are required: foo
    argparse.REMAINDER. All the remaining command-line arguments are gathered into a list. 
        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument('--foo')
        >>> parser.add_argument('command')
        >>> parser.add_argument('args', nargs=argparse.REMAINDER)
        >>> print(parser.parse_args('--foo B cmd --arg1 XX ZZ'.split()))
        Namespace(args=['--arg1', 'XX', 'ZZ'], command='cmd', foo='B')
const
    The const argument of add_argument() is used to hold constant values 
    that are not read from the command line 
default
    All optional arguments and some positional arguments may be omitted at the command line. 
    The default keyword argument of add_argument(), whose value defaults to None, 
    specifies what value should be used if the command-line argument is not present. 
    Providing default=argparse.SUPPRESS causes no attribute to be added 
    if the command-line argument was not present:
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--foo', default=argparse.SUPPRESS)
        >>> parser.parse_args([])
        Namespace()
        >>> parser.parse_args(['--foo', '1'])
        Namespace(foo='1')
type
    By default, ArgumentParser objects read command-line arguments in as simple strings.
    type= can take any callable that takes a single string argument and returns the converted value
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('foo', type=int)
        >>> parser.add_argument('bar', type=open)
        >>> parser.parse_args('2 temp.txt'.split())
        Namespace(bar=<_io.TextIOWrapper name='temp.txt' encoding='UTF-8'>, foo=2)
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('bar', type=argparse.FileType('w'))
        >>> parser.parse_args(['out.txt'])
        Namespace(bar=<_io.TextIOWrapper name='out.txt' encoding='UTF-8'>)

choices
    Some command-line arguments should be selected from a restricted set of values.
        >>> parser = argparse.ArgumentParser(prog='game.py')
        >>> parser.add_argument('move', choices=['rock', 'paper', 'scissors'])
        >>> parser.parse_args(['rock'])
        Namespace(move='rock')
        >>> parser.parse_args(['fire'])
        usage: game.py [-h] {rock,paper,scissors}
        game.py: error: argument move: invalid choice: 'fire' (choose from 'rock','paper', 'scissors')
required
    In general, the argparse module assumes that flags like -f and --bar indicate optional arguments, 
    which can always be omitted at the command line. 
    To make an option required, True can be specified for the required= keyword argument
help
    The help value is a string containing a brief description of the argument.
metavar
    When ArgumentParser generates help messages, it needs some way to refer to each expected argument. 
    By default, ArgumentParser objects use the dest value as the “name” of each object. 
    By default, for positional argument actions, the dest value is used directly, 
    and for optional argument actions, the dest value is uppercased. 
    So, a single positional argument with dest='bar' will be referred to as bar. 
    A single optional argument --foo that should be followed by a single command-line argument 
    will be referred to as FOO.
    An alternative name can be specified with metavar:
dest
    Most ArgumentParser actions add some value as an attribute of the object returned by parse_args(). 
    The name of this attribute is determined by the dest keyword argument of add_argument(). 
    For positional argument actions, dest is normally supplied as the first argument to add_argument():



###*** Os and os.path module 

1. Create below env vars containing below 
HOST        hostname 
DT          todays date using pattern "%m%d%y%H%M%S" 
SCRIPT      this script name only (without extension)
SCRIPT_PID  this script pid 
OUTDIR      C:/tmp/adm
LOGFIL      $OUTDIR/$SCRIPT.$DT.log (in unix expansion of variable 
2. Then dump in parent and in child these values 
3. write mslog with takes any message and dumps that message to LOGFIL and console 
   with format , message may contain any env var and that should be expanded 
   HOST:DT:message 


#Code 
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

            
            
            
            
###*** Module -subprocess - replaces os.system and os.spawn

import subprocess

#Arguments meaning
stdin, stdout and stderr 
    specify the executed program's standard input, 
    standard output and standard error file handles, 
    values are PIPE, DEVNULL, an existing file descriptor (a positive integer), 
    an existing file object, and None    
    stderr can be STDOUT    
universal_newlines 
    if it is False the file objects stdin, stdout and stderr will be opened as binary streams,
    and no line ending conversion is done
shell 
    If shell is True, the specified command will be executed through the shell
    accesses to shell pipes, filename wildcards, environment variable expansion
    On POSIX with shell=True, the shell defaults to /bin/sh. 
    Popen(['/bin/sh', '-c', args[0], args[1], ...])
    On windows shell=True to execute is built into the shell (e.g. dir or copy)


#Main Interface -Py3.5
subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, 
        capture_output=False, shell=False, cwd=None, timeout=None, check=False, 
        encoding=None, errors=None, text=None, env=None)
    The Main High level interface 
    Run the command described by args. 
    Wait for command to complete, then return a CompletedProcess instance.
    If capture_output is true, stdout and stderr will be captured
    The input argument is passed to Popen.communicate() and thus to the subprocess’s stdin
    CompletedProcess has below methods 
    args
        The arguments used to launch the process. This may be a list or a string.
    returncode
        Exit status of the child process. 
        Typically, an exit status of 0 indicates that it ran successfully.
        A negative value -N indicates that the child was terminated by signal N (POSIX only).
    stdout
        Captured stdout from the child process. 
        A bytes sequence, or a string if run() was called with an encoding, errors, or text=True. 
        None if stdout was not captured.
        If you ran the process with stderr=subprocess.STDOUT, 
        stdout and stderr will be combined in this attribute, and stderr will be None.
    stderr
        Captured stderr from the child process. 
        A bytes sequence, or a string if run() was called with an encoding, errors, or text=True. 
        None if stderr was not captured.
    check_returncode()
        If returncode is non-zero, raise a CalledProcessError.
        
#Example 
>>> subprocess.run(["ls", "-l"])  # doesn't capture output
CompletedProcess(args=['ls', '-l'], returncode=0)

>>> subprocess.run("exit 1", shell=True, check=True)
Traceback (most recent call last):
  ...
subprocess.CalledProcessError: Command 'exit 1' returned non-zero exit status 1

>>> subprocess.run(["ls", "-l", "/dev/null"], capture_output=True)
CompletedProcess(args=['ls', '-l', '/dev/null'], returncode=0,
stdout=b'crw-rw-rw- 1 root root 1, 3 Jan 23 16:23 /dev/null\n', stderr=b'')

   
#Low level API 
class subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, 
            preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=False, 
            startupinfo=None, creationflags=0, restore_signals=True, start_new_session=False, 
            pass_fds=(), *, encoding=None, errors=None, text=None)    
    args should be a sequence of program arguments(RECOMENDED) or else a single string
    buffsize
        0 means unbuffered (read and write are one system call and can return short)
        1 means line buffered (only usable if universal_newlines=True i.e., in a text mode)
        any other positive value means use a buffer of approximately that size
        negative bufsize (the default) means the system default of io.DEFAULT_BUFFER_SIZE will be used.
    here Popen is instance as returned by above call 
    Popen.poll()
        Check if child process has terminated. Set and return returncode attribute.
    Popen.wait(timeout=None)
        Wait for child process to terminate. Set and return returncode attribute.
    Popen.send_signal(signal)
        Sends the signal signal to the child.
    Popen.terminate()
        Stop the child. 
    Popen.kill()
        Kills the child
    Popen.args
    Popen.stdin  
        if stdin argument was PIPE, it is file object, use write()
    Popen.stdout 
        If the stdout argument was PIPE, it is file object, use read()
        Use communicate() rather than .stdin.write, .stdout.read or .stderr.read to avoid deadlocks 
    Popen.stderr
    Popen.pid
        The process ID of the child process.
    Popen.returncode
    (stdoutdata, stderrdata) = Popen.communicate(input=None, timeout=None) 
        Send data to stdin. Read data from stdout and stderr, until end-of-file is reached
        Can only be used if stdin, stdout, stderr are PIPE 
        The data read is buffered in memory, so do not use this method 
        if the data size is large or unlimited.

#Examples 
proc = subprocess.Popen(...)
try:
    outs, errs = proc.communicate(timeout=15)
except TimeoutExpired:
    proc.kill()
    outs, errs = proc.communicate()

#works with with
import subprocess as S
with S.Popen(["ipconfig"], stdout=S.PIPE, universal_newlines =True) as proc:  #ifconfig in unix 
    output = proc.stdout.read() 

	
	
#shlex.split() can be useful when determining the correct tokenization for args, 
#especially in complex cases
import shlex

>>> command_line = input()
/bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"

>>> args = shlex.split(command_line)
>>> print(args)
['/bin/vikings', '-input', 'eggs.txt', '-output', 'spam spam.txt', '-cmd', "echo '$MONEY'"]



##Subprocess Pattern 

#Replacing /bin/sh shell backquote
output=`mycmd myarg`
# becomes
output = subprocess.run(["mycmd", "myarg"], capture_output=True).stdout

# Replacing shell pipeline
#cat regex.py | grep def

p1 = subprocess.Popen(["cat", "regex.py"], stdout=subprocess.PIPE)
p2 = subprocess.Popen(["grep", "def"], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()  ## Allow p1 to receive a SIGPIPE if p2 exits
output_str = p2.communicate()[0]  # or p2.stdout.read().decode("utf-8") or universal_newlines=True
print(output_str.decode("utf-8"))

#OR
output=`dmesg | grep hda`
# becomes
output = subprocess.run("dmesg | grep hda", shell=True, capture_output=True).stdout

#Replacing os.system()
sts = os.system("mycmd" + " myarg")
# becomes
sts = subprocess.run("mycmd" + " myarg", shell=True).returncode

#or 
try:
    retcode = subprocess.run("mycmd" + " myarg", shell=True).returncode
    if retcode < 0:
        print("Child was terminated by signal", -retcode, file=sys.stderr)
    else:
        print("Child returned", retcode, file=sys.stderr)
except OSError as e:
    print("Execution failed:", e, file=sys.stderr)



#Replacing the os.spawn family
#P_NOWAIT example:
pid = os.spawnlp(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg")
#becomes
pid = subprocess.Popen(["/bin/mycmd", "myarg"]).pid


#P_WAIT example:
retcode = os.spawnlp(os.P_WAIT, "/bin/mycmd", "mycmd", "myarg")
#becomes
retcode = subprocess.run(["/bin/mycmd", "myarg"]).returncode

#Environment example:
os.spawnlpe(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg", env)
#becomes
subprocess.Popen(["/bin/mycmd", "myarg"], env={"PATH": "/usr/bin"})


#Replacing os.popen(), os.popen2(), os.popen3()
(child_stdin, child_stdout) = os.popen2(cmd, mode, bufsize)
#becomes
p = subprocess.Popen(cmd, shell=True, bufsize=bufsize,
          stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
(child_stdin, child_stdout) = (p.stdin, p.stdout)

#OR 
(child_stdin,
 child_stdout,
 child_stderr) = os.popen3(cmd, mode, bufsize)
#becomes
p = Popen(cmd, shell=True, bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
(child_stdin,
 child_stdout,
 child_stderr) = (p.stdin, p.stdout, p.stderr)

#OR 
(child_stdin, child_stdout_and_stderr) = os.popen4(cmd, mode, bufsize)
#becomes
p = Popen(cmd, shell=True, bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
(child_stdin, child_stdout_and_stderr) = (p.stdin, p.stdout)


##few windows commands 
'''
tracert www.google.com
netstat -an
ipconfig /all
powercfg /lastwake
#file compare 
fc /l "C:\Program Files (x86)\example1.doc" "C:\Program Files (x86)\example2.doc"
driverquery -v
nslookup www.google.com 
tasklist -m
'''


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
 
 
 

##Example of timeout 
#py3.5 
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
    try:
        outs, errs = proc.communicate(timeout=TIMEOUT)
    except S.TimeoutExpired:
        #timeout 
        if test_d(proc.pid):
            proc.terminate()
            time.sleep(KILL_TMOUT)
        if test_d(proc.pid):
            proc.kill()
            time.sleep(KILL_TMOUT)
        outs, errs = proc.communicate()
        if test_d(proc.pid):
            #could not kill 
            pass
        return (9, outs, errs)
    return (proc.returncode, outs, errs)



#Py2.7 
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
    
    
    
## TroubleShooting 
#If subprocess method is hanging  unpredictably
#the problem might be , stdout=PIPE and/or stderr=PIPE and data volumn is large > 64KB 
#in this case, create Popen with bufsize = BIG number and then use Popen.communicate 
#OR, open one tempfile and then use stdout=fileObject 
import tempfile
temp_stdout = tempfile.NamedTemporaryFile(mode="w+t") #open for read, write and text mode 
proc = subprocess.Popen(command, universal_newlines =True, stdout=temp_stdout.file, stderr=subprocess.STDOUT, shell=True)
proc.wait()
#then read the file 
temp_stdout.flush()
temp_stdout.seek(0)
outs = temp_stdout.read()
temp_stdout.close()

    
###*** paramiko module -
# (2.6+, 3.3+) implementation of the SSHv2 protocol , provides server and client

$ pip install paramiko


# for example start cygwin ssh from services.msc


#python3

import paramiko
#paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)
ssh    = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("127.0.0.1", username="ftpuser", password="ftpuser")
i, o, e = ssh.exec_command("ls -l")
i.flush()
print(" ".join(o.readlines()))
ssh.close()

#for file transfer
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy())
ssh.connect("localhost", username="ftpuser", password="ftpuser")
ftp = ssh.open_sftp()
ftp.put('var.txt', 'remotefile.py')  #put to server 
ftp.close()
ftp = ssh.open_sftp() 
ftp.get('remotefile.py', 'localfile.py') #get from server 
ftp.close() 

#or open remote file 

sftp_client = ssh_client.open_sftp()
sftp_file = sftp_client.open('/var/log/messages')
for i, line in enumerate(sftp_file):
    print("%d: %s" % (i, line[:15]))
    if i >= 9:
        break
sftp_file.close()
sftp_client.close()
ssh.close()






###paramiko which uses configurations  ~/.ssh/config
options = {'hostname': ..., 'username':...}

client = paramiko.SSHClient()

#Connect automatically calls this 
client.load_system_host_keys()  #load all paramiko saved keys 
#other setup 
client._policy = paramiko.WarningPolicy()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #automatically add to paramiko keys 

ssh_config = paramiko.SSHConfig()
user_config_file = os.path.expanduser("~/.ssh/config")
if os.path.exists(user_config_file):
    with open(user_config_file) as f:
        ssh_config.parse(f)

#this would be further updated 
cfg = {'hostname': options['hostname'], 'username': options["username"]}

user_config = ssh_config.lookup(cfg['hostname'])
for k in ('hostname', 'username', 'port'):
    if k in user_config:
        cfg[k] = user_config[k]

if 'proxycommand' in user_config:
    cfg['sock'] = paramiko.ProxyCommand(user_config['proxycommand'])

client.connect(**cfg)

#Now connected , execute any command 
i, o, e = ssh.exec_command("ls -l")  #stdin, stdout, stderr 
i.flush()
print(" ".join(o.readlines()))
ssh.close()

#or do sftp 
scp = SCPClient(client.get_transport())
scp.get(src, dest)
ftp.put(src, dest)
scp.close()


##For example executing rest and getting XML 
from xml.etree import ElementTree as ET

stdin, stdout, stderr = client.exec_command('curl http://www.thomas-bayer.com/sqlrest/CUSTOMER/3/')
xml = stdout.read()
xml = ET.fromstring(xml)
assert xml.find('.//FIRSTNAME').text == 'Michael'




##EXample of SFTP and OOP  
import errno
import os.path

import paramiko


class SFTPHelper(object):

    def connect(self, hostname, **ssh_kwargs):
        """Create a ssh client and a sftp client

        **ssh_kwargs are passed directly to paramiko.SSHClient.connect()
        """
        self.sshclient = paramiko.SSHClient()
        self.sshclient.load_system_host_keys()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(hostname, **ssh_kwargs)
        self.sftpclient = self.sshclient.open_sftp()

    def remove_directory(self, path):
        """Remove remote directory that may contain files.
        It does not support directories that contain subdirectories
        """
        if self.exists(path):
            for filename in self.sftpclient.listdir(path):
                filepath = os.path.join(path, filename)
                self.sftpclient.remove(filepath)
            self.sftpclient.rmdir(path)

    def put_directory(self, localdir, remotedir):
        """Put a directory of files on the remote server
        Create the remote directory if it does not exist
        Does not support directories that contain subdirectories
        Return the number of files transferred
        """
        if not self.exists(remotedir):
            self.sftpclient.mkdir(remotedir)
        count = 0
        for filename in os.listdir(localdir):
            self.sftpclient.put(
                os.path.join(localdir, filename),
                os.path.join(remotedir, filename))
            count += 1
        return count

    def exists(self, path):
        """Return True if the remote path exists
        """
        try:
            self.sftpclient.stat(path)
        except IOError, e:
            if e.errno == errno.ENOENT:
                return False
            raise
        else:
            return True
            
            
### Creating an SSH key on Windows

#Check if existing keys are available 
$ cd %userprofile%/.ssh
$ dir id_*

#id_* is private key , id_*.pub is public key 
#~/.ssh/authorized_keys  contains all public keys which are authorized to access this machine via SSH 


#Generate a new SSH key- admin command prompt 
#Use PuTTYgen ,  from PuTTY .msi package installation, https://www.ssh.com/ssh/putty/download
#OR install GIT for windows , https://git-scm.com/downloads, contains ssh-keygen 

$ ssh-keygen -t rsa -C "your_email@example.com"

#A passphrase is an optional addition. 
#If you enter one, you will have to provide it every time you use this key 
#if you do not want to set a passphrase,  press ENTER to bypass this prompt.
Your identification has been saved in /home/username/.ssh/id_rsa.
Your public key has been saved in /home/username/.ssh/id_rsa.pub.
The key fingerprint is:
a9:49:2e:2a:5e:33:3e:a9:de:4e:77:11:58:b6:90:26 username@remote_host
The key's randomart image is:
+--[ RSA 2048]----+
|     ..o         |
|   E o= .        |
|    o. o         |
|        ..       |
|      ..S        |
|     o o.        |
|   =o.+.         |
|. =++..          |
|o=++.            |
+-----------------+

#Public key looks like 
$ cat ~/.ssh/id_rsa.pub

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDNqqi1mHLnryb1FdbePrSZQdmXRZxGZbo0gTfglysq6KMNUNY2VhzmYN9JYW39yNtjhVxqfW6ewc

#Then add this authorized_keys in remote machine where this machine would connect to 
$ cat ~/.ssh/id_rsa.pub | ssh username@remote_host "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"


###Configuration of .ssh/config 

System-wide OpenSSH config file client configuration
    /etc/ssh/ssh_config 
    This files set the default configuration for all users of OpenSSH clients 
    on that desktop/laptop and it must be readable by all users on the system.
User-specific OpenSSH file client configuration
    ~/.ssh/config or $HOME/.ssh/config 
    This is user’s own configuration file which, overrides the settings 
    in the global client configuration file, /etc/ssh/ssh_config.

#format 
config value
config1 value1 value2
#OR
config=value
config1=value1 value2
#All empty lines are ignored.
#All lines starting with the hash (#) are ignored.
#All values are case-sensitive, but parameter names are not.

#Config .ssh/config example 
#check https://www.cyberciti.biz/faq/create-ssh-config-file-on-linux-unix/
### default for all ##
Host *
     ForwardAgent no
     ForwardX11 no
     ForwardX11Trusted yes
     User nixcraft
     Port 22
     Protocol 2
     ServerAliveInterval 60
     ServerAliveCountMax 30
 
## override as per host ##
Host server1
     HostName server1.cyberciti.biz
     User nixcraft
     Port 4242
     IdentityFile /nfs/shared/users/nixcraft/keys/server1/id_rsa
 
## Home nas server ##
Host nas01
     HostName 192.168.1.100
     User root
     IdentityFile ~/.ssh/nas01.key
 
## Login AWS Cloud ##
Host aws.apache
     HostName 1.2.3.4
     User wwwdata
     IdentityFile ~/.ssh/aws.apache.key
 
## Login to internal lan server at 192.168.0.251 via our public uk office ssh based gateway using ##
## $ ssh uk.gw.lan ##
Host uk.gw.lan uk.lan
     HostName 192.168.0.251
     User nixcraft
     ProxyCommand  ssh nixcraft@gateway.uk.cyberciti.biz nc %h %p 2> /dev/null
 
## Our Us Proxy Server ##
## Forward all local port 3128 traffic to port 3128 on the remote vps1.cyberciti.biz server ## 
## $ ssh -f -N  proxyus ##
Host proxyus
    HostName vps1.cyberciti.biz
    User breakfree
    IdentityFile ~/.ssh/vps1.cyberciti.biz.key
    LocalForward 3128 127.0.0.1:3128

    
    
    
    
    
    
    
    
    
    
###*** Fabric 
#Used for automation of running remote commands using paramiko 
#It uses paramiko and it's configuration files 
$ pip install fabric




##Single commands on individual hosts:
from fabric import Connection
#Connection(host='web1', user='deploy', port=2202)
#Connection('deploy@web1:2202')
result = Connection('web1.example.com').run('uname -s', hide=True)
>>> result
<Result cmd='uname -s' exited=0>

msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
>>> print(msg.format(result))
Ran 'uname -s' on web1.example.com, got stdout:
Linux

#also supports 'with' 
with Connection('host') as c:
    c.run('command')
    c.put('file')


##details of Result 
from fabric import Connection
c = Connection('web1')
>>> result = c.run('uname -s')
Linux
>>> result.stdout.strip() == 'Linux'
True
>>> result.exited
0
>>> result.ok
True
>>> result.command
'uname -s'
>>> result.connection
<Connection host=web1>
>>> result.connection.host
'web1'



##Single commands across multiple hosts 
class fabric.group.SerialGroup(*hosts, **kwargs)
    Subclass of Group which executes in simple, serial fashion.
class fabric.group.ThreadingGroup(*hosts, **kwargs)
    Subclass of Group which uses threading to execute concurrently

#Example 
from fabric import SerialGroup
>>> result = SerialGroup('web1', 'web2').run('hostname')
web1
web2
# GroupResult is a dict of all connection:result 
>>> sorted(result.items())
[(<Connection host=web1>, <Result cmd='hostname' exited=0>), ...]

#GroupResult also contains succeeded and failed attributes containing sub-dicts 
#limited to just those key/value pairs that succeeded or encountered exceptions, respectively

from fabric import Connection
for host in ('web1', 'web2', 'web3'):
    c = Connection(host)
    if c.run('test -f /opt/mydata/myfile', warn=True).failed:
        c.put('myfiles.tgz', '/opt/mydata')
        c.run('tar -C /opt/mydata -xzvf /opt/mydata/myfiles.tgz')

#OR 
from fabric import SerialGroup as Group

def upload_and_unpack(c):
    if c.run('test -f /opt/mydata/myfile', warn=True).failed:
        c.put('myfiles.tgz', '/opt/mydata')
        c.run('tar -C /opt/mydata -xzvf /opt/mydata/myfiles.tgz')

for connection in Group('web1', 'web2', 'web3'):
    upload_and_unpack(connection)
    
    

##Python code blocks (functions/methods) targeted at individual connections:
def disk_free(c):
    uname = c.run('uname -s', hide=True)
    if 'Linux' in uname.stdout:
        command = "df -h / | tail -n1 | awk '{print $5}'"
        return c.run(command, hide=True).stdout.strip()
    err = "No idea how to get disk space on {}!".format(uname)
    raise Exit(err)

>>> print(disk_free(Connection('web1')))
33%


#Python code blocks on multiple hosts:
for cxn in SerialGroup('web1', 'web2', 'db1'):
    print("{}: {}".format(cxn, disk_free(cxn)))
#Output 
<Connection host=web1>: 33%
<Connection host=web2>: 17%
<Connection host=db1>: 2%




###The sudo helper

import getpass
from fabric import Connection, Config

>>> sudo_pass = getpass.getpass("What's your sudo password?")
What's your sudo password?

>>> config = Config(overrides={'sudo': {'password': sudo_pass}})
>>> c = Connection('db1', config=config)
>>> c.sudo('whoami', hide='stderr')
root
<Result cmd="...whoami" exited=0>
>>> c.sudo('useradd mydbuser')
<Result cmd="...useradd mydbuser" exited=0>
>>> c.run('id -u mydbuser')
1001
<Result cmd='id -u mydbuser' exited=0>

##Transfer files
#Connection.put and Connection.get exist to fill this need

from fabric import Connection
result = Connection('web1').put('myfiles.tgz', remote='/opt/mydata/')
>>> print("Uploaded {0.local} to {0.remote}".format(result))
Uploaded /local/myfiles.tgz to /opt/mydata/



###the fab command-line tool - 'fab' 

#fabfile.py

from fabric import task

@task
def upload_and_unpack(c):
    if c.run('test -f /opt/mydata/myfile', warn=True).failed:
        c.put('myfiles.tgz', '/opt/mydata')
        c.run('tar -C /opt/mydata -xzvf /opt/mydata/myfiles.tgz')


$ fab --list
Available tasks:
  upload_and_unpack


# To run the task once on a single server:
$ fab -H web1 upload_and_unpack

#or on multiple hosts 
$ fab -H web1,web2,web3 upload_and_unpack



###Reference 
#http://docs.fabfile.org/en/2.4/api/connection.html

class fabric.connection.Connection(host, user=None, port=None, config=None, 
            gateway=None, forward_agent=None, connect_timeout=None, 
            connect_kwargs=None, inline_ssh_env=None)
    A connection to an SSH daemon, with methods for commands and file transfer.
    Fabric uses Paramiko’s SSH config file machinery to load 
    and parse ssh_config-format files 
    # ~/.fabric.yaml:
    user: foo
    #Absent any other configuration, Connection('myhost') connects as the foo user.

    #OR  ~/.ssh/config:
    Host *
        User bar
    #then Connection('myhost') connects as bar (the SSH config wins over the Fabric config.)

    #OR below will connect as biz.
    Connection('myhost', user='biz') 
    #Methods 
    forward_local(*args, **kwds)
        Open a tunnel connecting local_port to the server’s environment.
        Parameters:
            •local_port (int) – The local port number on which to listen.
            •remote_port (int) – The remote port number. Defaults to the same value as local_port.
            •local_host (str) – The local hostname/interface on which to listen. Default: localhost.
            •remote_host (str) – The remote hostname serving the forwarded remote port. Default: localhost (i.e., the host this Connection is connected to.)
        For example, say you want to connect to a remote PostgreSQL database 
        which is locked down and only accessible via the system it’s running on. 
        You have SSH access to this server, so you can temporarily make port 5432 
        on your local system act like port 5432 on the server:
        #Exmaple 
        import psycopg2
        from fabric import Connection

        with Connection('my-db-server').forward_local(5432):
            db = psycopg2.connect(
                host='localhost', port=5432, database='mydb'
            )
            # Do things with 'db' here


    forward_remote(*args, **kwds)
        Open a tunnel connecting remote_port to the local environment.
        Parameters:
            •remote_port (int) – The remote port number on which to listen.
            •local_port (int) – The local port number. Defaults to the same value as remote_port.
            •local_host (str) – The local hostname/interface the forwarded connection talks to. Default: localhost.
            •remote_host (str) – The remote interface address to listen on when forwarding connections. Default: 127.0.0.1 (i.e. only listen on the remote localhost).
        For example, say you’re running a daemon in development mode on your workstation at port 8080, 
        and want to funnel traffic to it from a production or staging environment.
        In most situations this isn’t possible as your office/home network probably blocks inbound traffic. 
        But you have SSH access to this server, so you can temporarily make port 8080 on that server 
        act like port 8080 on your workstation:
        #Example 
        from fabric import Connection

        c = Connection('my-remote-server')
        with c.forward_remote(8080):
            c.run("remote-data-writer --port 8080")
            # Assuming remote-data-writer runs until interrupted, this will
            # stay open until you Ctrl-C...

    get(*args, **kwargs)
        Get a remote file to the local filesystem or file-like object.

    is_connected
        Whether or not this connection is actually open.

    local(*args, **kwargs)
        Execute a shell command on the local system.

    open()
        Initiate an SSH connection to the host/port this object is bound to.

    open_gateway()
        Obtain a socket-like object from gateway.
        Returns:
            A direct-tcpip paramiko.channel.Channel, if gateway was a Connection; 
            or a ProxyCommand, if gateway was a string. 
            
    put(*args, **kwargs)
        Put a remote file (or file-like object) to the remote filesystem.

    run(command, **kwargs)
        Execute a shell command on the remote end of this connection.

    sftp()
        Return a SFTPClient object.

    sudo(command, **kwargs)
        Execute a shell command, via sudo, on the remote end.








