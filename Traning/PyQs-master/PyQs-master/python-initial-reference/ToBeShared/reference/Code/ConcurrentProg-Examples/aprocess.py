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
async def m2(*args):
    print("m2")
    return args[0:1]


ARG1 = m2(2,3)

#OR in another coroutine 
async def m1(arg1,arg2):
    result = await m2(arg1)  #blocks, m2 is executed now 
    await asyncio.sleep(1)
    fut = asyncio.ensure_future(m2(arg2))
    fut.add_done_callback(lambda f: print(f.result())) #f= future of m2(arg2)
    print("m1")
    return (result,fut)

ARG_tuple = m1(2,3)    

#For using some function in thread 
#coroutines cannot be used with run_in_executor()
def m3(*args):
    print("m3")
    time.sleep(1)

result = loop.run_in_executor(executor, m3, 2,3 ) #*args, result => func return 

#or 
async def m4(loop,executor,func,*args):
    result = await loop.run_in_executor(executor, m3, *args)
    return result 

ARG3 = m4(loop,executor, m3, 2, 3)  #*args

#Execution 
r1 = loop.run_until_complete(ARG1)

#Or multiple 
ARG_all = asyncio.gather(ARG3,ARG_tuple)
r2 = loop.run_until_complete(ARG_all)


>>> r1
(2,)

>>> r2
[None, ((2,), <Task finished coro=<m2() done, defined at <stdin>:1> result=(3,)>)]
>>> type(r2[-1][-1])
<class 'asyncio.tasks.Task'>
>>> r2[-1][-1].result()
(3,)

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


