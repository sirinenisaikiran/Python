Asyncio
tornado 
openAPI/swagger 
connexion
Aiohttp
--------------------------------------
###Coroutine 
#Functions which exist together with main function in the same thread 
#primitive implementation 
##Coroutine style - single thread
def search_file(filename):
    print('Searching file %s' % (filename))
    my_file = open(filename, 'r')
    file_content = my_file.read()
    my_file.close()
    while True:
        search_result = 0
        search_text = (yield search_result)        
        search_result = file_content.count(search_text)
        print('Number of matches: %d' % (search_result))


        
search = search_file("recurseDown_a.py")
search = iter(search)
search=iter(search)  #go upto yield in coroutine 
search.send('import') #yield would return this 
search.close()  #close the coroutine 



###Asyncio - asynchronous io
#get a event loop and run it, all Tasks would be executed  
#has coroutine, task, future, transport proptocol and subprocess related functionality

import asyncio

##features
1.a pluggable event loop with various system-specific implementations;
2.transport and protocol abstractions (similar to those in Twisted);
3.concrete support for TCP, UDP, SSL, subprocess pipes, delayed calls, and others (some may be system-dependent);
4.a Future class that mimics the one in the concurrent.futures module, 
  but adapted for use with the event loop;
5.coroutines and tasks based on yield from , to help write concurrent code in a sequential fashion;
6.cancellation support for Futures and coroutines;
7.synchronization primitives for use between coroutines in a single thread, 
  mimicking those in the threading module;
8.an interface for passing work off to a threadpool, for times when you absolutely, positively have to use a library that makes blocking I/O calls.


##Most asyncio functions don’t accept keywords based arg passing 
#use functools.partial(). 
#For example, 
loop.call_soon(functools.partial(print, "Hello", flush=True)) 
#will call print("Hello", flush=True).


##Enabling the Debug 
1.Enable the asyncio debug mode globally by setting the environment 
  variable PYTHONASYNCIODEBUG to 1, or by calling AbstractEventLoop.set_debug().
2.Set the log level of the asyncio logger to logging.DEBUG. 
  For example, call 
  logging.basicConfig(level=logging.DEBUG) at startup.
  Default log level for the asyncio module is logging.INFO
  To change 
  logging.getLogger('asyncio').setLevel(logging.WARNING)
3.Configure the warnings module to display ResourceWarning warnings. 
  For example, use the -Wdefault command line option of Python to display them.

#Examples debug checks:
•Log coroutines defined but never “yielded from”
•call_soon() and call_at() methods raise an exception 
 if they are called from the wrong thread.
•Log the execution time of the selector
•Log callbacks taking more than 100 ms to be executed. 
 The AbstractEventLoop.slow_callback_duration attribute is the minimum duration in seconds of “slow” callbacks.
•ResourceWarning warnings are emitted 
 when transports and event loops are not closed explicitly.

 
 
 
##Available event loops
class asyncio.SelectorEventLoop #for Windows, Others 
    Event loop based on the selectors module
    Use the most efficient selector available on the platform.
    On Windows
        •SelectSelector is used which only supports sockets and is limited to 512 sockets.
        •add_reader() and add_writer() only accept file descriptors of sockets
        •Pipes are not supported (ex: connect_read_pipe(), connect_write_pipe())
        •Subprocesses are not supported (ex: subprocess_exec(), subprocess_shell())

class asyncio.ProactorEventLoop #for Windows
    Proactor event loop for Windows using “I/O Completion Ports” aka IOCP
    Supports Subprocesses and pipes
        •create_datagram_endpoint() (UDP) is not supported
        •add_reader() and add_writer() are not supported

import asyncio, sys
if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)

    
    


 




###Asyncio - Introduction 

##Asyncio - Execution - General Points 
#if a coro, coroutine is written
1. execute them in main process  
    1.Execute with loop.run_until_complete(coro(args...))
    2.or schedule with task = asyncio.ensure_future(coro(args...))
      Returns a Task object , get result by task.result()
      Execute all such by loop.run_forever()
      or loop.run_until_complete(task)
2.or in another coroutine as 
  result = await coro(args...)  , this blocks 
  result = await asyncio.ensure_future(coro(args..)) 
  , schedules this and return result, a future   
3.for sleep use, await asyncio.sleep(sleeptime)

##Asyncio - Execution - Various options 
#if thread execution is required 
executor = ThreadPoolExecutor(max_workers=4)
loop.set_default_executor(executor)

#Create coroutine 
async def m1(arg1,arg2):
    result = await m2(arg1)  #blocks, m2 is executed now 
    fut = asyncio.ensure_future(m2(arg2))
    fut.add_done_callback(lambda f: print(f.result())) #f= future of m2(arg2)
    print("m1")
    return (result,fut)

async def m2(arg1):
    print("m2")
    return arg1 

#Get a event loop
loop = asyncio.get_event_loop()

#Options for : run_until_complete's ARG 
#for single coroutine 
ARG = m2(2)         #result => m2 return 
#OR
ARG = asyncio.wait_for(ARG,timeout=0)
#OR here ARG(done) would be set of all returns from wait's ARG 
ARG, pending = asyncio.wait([ARG,ARG,ARG],timeout=0)

#For using some function in thread 
ARG = loop.run_in_executor(executor, func, *args) #result => func return 
#or 
async def m3(loop,executor,func,*args):
    result = await loop.run_in_executor(executor, func, *args)
    return result 
ARG = m3(loop,executor,func,*args)

#Note Above ARG can be packaged(scheduled) as (below all returns asyncio.Task)
#.result() to get result after executed by loop.run_until_complete(ARG) or loop.run_forever()
ARG = asyncio.ensure_future(ARG)
#OR 
ARG = asyncio.async(ARG)
#OR here ARG would be list of all returns from gather's ARG 
ARG = asyncio.gather(ARG,ARG,ARG)


#Run it in main process 
result = loop.run_until_complete(ARG)
loop.stop()

#run it in another coroutine 
result = await ARG 

#For a general function, fn it can be executed when  loop.run_forever()
#package it in (note here fn must not be coroutine)
handle = loop.call_soon(fn, *args)         
handle = loop.call_soon_threadsafe(fn, *args) #To schedule a callback from a different thread, thread must have access to 'loop'
handle = loop.call_later(delay, fn, *args) 
handle = loop.call_at(when, fn, *args) # 'when' (int/float) must be as per loop.time() 


##Asyncio - Hands on experiment 
import asyncio
fut = asyncio.Future()
loop = asyncio.get_event_loop()
fut.add_done_callback(lambda x: print(type(x)))
async def s(f):
    f.set_result(20)

>>> res = loop.run_until_complete(s(fut))
<class 'asyncio.futures.Future'>
>>> fut.result()
20

async def m1(arg1,arg2):
    result = await m2(arg1)  #blocks, m2 is executed now
    fut = asyncio.ensure_future(m2(arg2))
    fut.add_done_callback(lambda f: print(f.result())) #f= future of m2(arg2)
    print("m1")
    return (result,fut)

async def m2(arg1):
    print("m2")
    return arg1

ARG = m2(2)
>>> r = loop.run_until_complete(ARG)
m2
>>> r
2
>>> ARG = asyncio.gather(ARG,ARG,ARG)
>>> r = loop.run_until_complete(ARG)
RuntimeError: cannot reuse already awaited coroutine
>>> ARG = m2(2)
>>> ARG = asyncio.gather(ARG,ARG,ARG)
>>> r = loop.run_until_complete(ARG)
m2
>>> r
[2, 2, 2]
>>> ARG = m2(2)
>>> ARG = asyncio.gather(ARG,ARG,ARG)
>>> r = loop.run_until_complete(asyncio.wait_for(ARG,None))
m2
>>> r
[2, 2, 2]
>>> ARG = m2(2)
>>> ARG = asyncio.wait([ARG,ARG,ARG])
>>> r = loop.run_until_complete(ARG)
m2
>>> r
({<Task finished coro=<m2() done, defined at <stdin>:1> result=2>}, set())
>>> r[0]
{<Task finished coro=<m2() done, defined at <stdin>:1> result=2>}
>>> r[0].pop().result()
2
>>> ARG = m2(2)
>>> ARG2 = m2(2)
>>> ARG3 = asyncio.wait([ARG,ARG2])
>>> r = loop.run_until_complete(ARG3)
m2
m2
>>> r
({<Task finished coro=<m2() done, defined at <stdin>:1> result=2>, 
<Task finished coro=<m2() done, defined at <stdin>:1> result=2>}, set())

>>> r = loop.run_until_complete(m1(2,3))
m2
m1
m2
>>> r
(2, <Task finished coro=<m2() done, defined at <stdin>:1> result=3>)
>>> r = loop.run_until_complete(m1(20,30))
3
m2
m1
m2
>>> r
(20, <Task finished coro=<m2() done, defined at <stdin>:1> result=30>)
>>> r = loop.run_until_complete(m1(20,30))
30
m2
m1
m2
>>> cs = loop.call_soon(m1,200,300)
TypeError: coroutines cannot be used with call_soon()
>>>



##Asyncio - asyncio.Future and concurrent.futures.Future
#Note asyncio.Future and concurrent.futures.Future are different 
#and both are not compatible , but both have .result(), .add_done_callback(fn)

#from concurrent to asyncio conversion 
await/ensure_future(asyncio.wrap_future(concurrent_future))


##Asyncio - Run an event loop

loop.run_forever()
    Run all coroutines until stop() is called. 
    If stop() is called before run_forever() is called, 
    already scheduled callbacks would run if corresponding IO happened

loop.run_until_complete(future_or_coroutine_or_task)
    Run until the Future or coroutine
    Return the Future’s result, or raise its exception.


loop.is_running()
loop.stop()
loop.is_closed()
loop.close()

coroutine loop.shutdown_asyncgens()
    Schedule all currently open asynchronous generator objects to close with an aclose() call
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


##Asyncio - Calling a method/callback 
        
loop.call_soon(callback, *args) #args for positional arguments to callback 
    Arrange for a callback to be called as soon as possible(callback Q is FIFO)
    Returns asyncio.Handle (can be cancelled)
    Use functools.partial to pass keywords to the callback.
    loop.call_soon(functools.partial(print, "Hello", flush=True)) 
        
loop.call_soon_threadsafe(callback, *args) #args for positional arguments to callback 
    Like call_soon(), but thread safe.
    Returns asyncio.Handle (can be cancelled)
    Use functools.partial to pass keywords to the callback.
    loop.call_soon_threadsafe(functools.partial(print, "Hello", flush=True)) 

#helper class 
class asyncio.Handle
    cancel()
        Cancel the call
##Asyncio - Delayed calls
loop.call_later(delay, callback, *args) #args for positional arguments to callback 
    Arrange for the callback to be called after the given delay seconds (either an int or float).
    Returns asyncio.Handle (can be cancelled)
    Use functools.partial to pass keywords to the callback.#For example, 
    loop.call_later(60, functools.partial(print, "Hello", flush=True)) 

loop.call_at(when, callback, *args) #args for positional arguments to callback 
    'when' (int/float) must be as per loop.time() returns 
    Returns asyncio.Handle (can be cancelled)
    Use functools.partial to pass keywords to the callback.
    #For example, 
    loop.call_at(60,functools.partial(print, "Hello", flush=True)) 

loop.time()
    Return the current time, as a float value

coroutine asyncio.sleep(sleeptime)
    Sleeps that many int/float time



##Asyncio - UNIX signals(not supported on Windows)
#check signum from https://docs.python.org/3/library/signal.html#module-contents
loop.add_signal_handler(signum, callback, *args)  #args for positional arguments to callback
    Use functools.partial to pass keywords to the callback.
loop.remove_signal_handler(sig)
    Return True if a signal handler was removed, False if not.

    
##Asyncio - Executing external blocking function 
#Use external ThreadPoolExecutor(by default) or ProcessPoolExecutor
#or pass executor=None for default executor

#Note inside coroutine use  yield from <<below method>> or await <<below method>>
#but outside , call loop.run_until_complete(<<below_method>>) as yield from/await works only inside coroutine 


coroutine loop.run_in_executor(executor, func, *args)  #args for positional arguments to callback
    Use functools.partial to pass keywords to the *func
    It's a coroutine, hence use below to get result 
    result=await coroutine 
    #or 
    result=yield from coroutine
    
    
loop.set_default_executor(executor)
    Set the default executor used by run_in_executor()

##Asyncio - Error Handling API
loop.set_exception_handler(handler)  
    handler_function(loop, context)
loop.get_exception_handler()
    Return the exception handler, or None if the default one is in use
loop.default_exception_handler(context) 
    Default exception handler.
loop.call_exception_handler(context)  
    Call the current event loop exception handler

#context is a dict object containing the following keys 
    •'message': Error message;
    •'exception' (optional): Exception object;
    •'future' (optional): asyncio.Future instance;
    •'handle' (optional): asyncio.Handle instance;
    •'protocol' (optional): Protocol instance;
    •'transport' (optional): Transport instance;
    •'socket' (optional): socket.socket instance.

##Asyncio - Debug mode
loop.get_debug()
    Get the debug mode (bool) of the event loop.
loop.set_debug(enabled: bool)
    Set the debug mode of the event loop.


###Asyncio - Coroutine 
#Coroutines used with asyncio may be implemented using the async def (Py3.5)
#or by using generators(@asyncio.coroutine)

#Things a coroutine can do:
• result = await future or result = yield from future 
  suspends the coroutine until the future is done, 
  then returns the future's result, or raises an exception, which will be propagated. 
  (If the future is cancelled, it will raise a CancelledError exception.) 
  Note that tasks are futures, and everything said about futures also applies to tasks.
• result = await coroutine or result = yield from coroutine 
  wait for another coroutine to produce a result 
  (or raise an exception, which will be propagated). 
  The coroutine expression must be a call to another coroutine.
• return expression 
  produce a result to the coroutine that is waiting for this one using await or yield from.
• raise exception 
  raise an exception in the coroutine that is waiting for this one using await or yield from.

#Calling a coroutine does not start its code running 
#the coroutine object returned by the call doesn't do anything 
#until you schedule its execution, via asyncio.ensure_future(), then loop.run_forever()


###Asyncio - asyncio.Future 
#coroutine can return a result via Future and we can wait for this Future 
#Note we have another Future, concurrent.futures.Future (not suitable for eventloop)
# All Future mentioned here is asyncio.Future 

#This future is not threadsafe as eventloop occurs in only one thread 
#hence for cancelling this future from anothor thread, 
loop.call_soon_threadsafe(fut.cancel)
 
#asyncio.Future is used for result passing from coroutine
#which can be used for waiting in loop.run_until_complete(future)
#or result = await future or result = yield from future inside a coroutine 

future = loop.create_future()  #returns asyncio.Future 
#or
future = asyncio.Future()
#attach this future to a co-routine which does set_result() or raise exception
async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')
    
#schedules coroutine, to be executed when loop.run_forever() is called  
asyncio.ensure_future(slow_operation(future)) #returns Task , which can be cancelled etc
#OR Wait for future result
loop.run_until_complete(future)
print(future.result())
loop.close()

#or 
future.add_done_callback(got_result)
try:
    loop.run_forever()
finally:
    loop.close()
    
#Or inside a coroutine 
result = await future 
#Or
result = yield from future 

#reference
class asyncio.Future(*, loop=None)
    cancel()
        Cancel the future and schedule callbacks
    cancelled()
        Return True if the future was cancelled.
    done()
        Return True if the future is done.
        Done means either that a result / exception are available, 
        or that the future was cancelled.
    result()
        Return the result this future represents.
    exception()
        Return the exception that was set on this future
    add_done_callback(fn)
        Add a callback to be run when the future becomes done.
        Use functools.partial to pass parameters to the callback
    remove_done_callback(fn)
        Remove all instances of a callback from the “call when done” list.
    set_result(result)
        Mark the future done and set its result.
    set_exception(exception)
        Mark the future done and set an exception.


###Asyncio - Tasks
#A task is a subclass of Future
#A task(Future) is responsible for executing a coroutine object in an event loop
#ie schedules the future or coroutine when loop gets executed by loop.run_forever() etc 

#creation
#Note inside coroutine use  yield from <<below method>> or await <<below method>>
#but outside , call loop.run_until_complete(<<below method>>) as yield from/await works only inside coroutine 
asyncio.ensure_future(coro_or_future, *, loop=None)
    Return a Task object.(schedules coro_or_future for execution )

asyncio.async(coro_or_future, *, loop=None)
    A deprecated alias to ensure_future().

asyncio.wrap_future(future, *, loop=None)
    Wrap a concurrent.futures.Future object in a Future object.
    
asyncio.gather(*coros_or_futures, loop=None, return_exceptions=False)
    Return a future aggregating list of coroutine objects or futures
    Once completed, that result of future is list of results in original order

loop.create_task(coroutine) #Py3.4.2
    Wrap it in a future. Return a Task object.
    Use the asyncio.async(coroutine)  in older Python versions 
    
#Reference 
class asyncio.Task(coro, *, loop=None)
    Subclass of Future 
    Calling cancel() will throw a CancelledError to the wrapped coroutine. 
    cancelled() only returns True if the wrapped coroutine did not catch the CancelledError exception, 
    or raised a CancelledError exception.
    This class is not thread safe.
    #other methods 
    classmethod all_tasks(loop=None)#None means default loop
        Return a set of all tasks for an event loop.
    classmethod current_task(loop=None)
        Return the currently running task in an event loop or None.
    cancel()
        Request that this task cancel itself.
    get_stack(*, limit=None)
        Return the list of stack frames for this task's coroutine.
    print_stack(*, limit=None, file=None)
        Print the stack or traceback for this task's coroutine.



##Other Task/Future helper functions
#the optional loop argument allows explicitly setting the event loop object used by the underlying task or coroutine. 
#If it's not provided, the default event loop is used

asyncio.as_completed(list_futures_or_coroutines, *, loop=None, timeout=None)
    Return an iterator whose values, when waited for, are Future instances
    #Example, in a coroutine 
    for f in as_completed(fs):
        result = yield from f  # The 'yield from' may raise
        # Use result

coroutine asyncio.wait_for(single_future_or_coroutine, timeout, *, loop=None)
    Returns result of the Future or coroutine
    To avoid the task cancellation, wrap it in shield().
    result = yield from asyncio.wait_for(fut, 60.0)

    
coroutine asyncio.wait(list_of_futures_or_coroutines, *, loop=None, timeout=None, return_when=ALL_COMPLETED)
    return_when can be  FIRST_COMPLETED, FIRST_EXCEPTION, ALL_COMPLETED 
    Returns two sets of Future: (done, pending).
    #Example 
    done, pending = yield from asyncio.wait(fs)
    result = yield from asyncio.wait_for(fut, 60.0)


coroutine asyncio.sleep(delay, result=None, *, loop=None)
    Sleeps delay(seconds)
    Result is result from 'yield from'
    yield from asyncio.sleep(2.0)
    
asyncio.shield(coroute_future_task, arg, *, loop=None)  
    Wait for a future, shielding it from cancellation.
    res = yield from shield(something())
    #or handle exception 
    try:
        res = yield from shield(something())
    except CancelledError:
        res = None

    
asyncio.iscoroutine(obj)
    Return True if obj is a coroutine object, 
    which may be based on a generator or an async def coroutine.
    
asyncio.iscoroutinefunction(func)
    Return True if func is determined to be a coroutine function, 
    which may be a decorated generator function or an async def function.
    
asyncio.run_coroutine_threadsafe(coro, loop)
    Submit a coroutine object to a given event loop.
    Requires the loop argument to be passed explicitly.
    Return a concurrent.futures.Future to access the result.

    This function is meant to be called from a different thread 
    than the one where the event loop is running. 
    # Create a coroutine
    coro = asyncio.sleep(1, result=3)
    # Submit the coroutine to a given loop
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    # Wait for the result with an optional timeout argument
    assert future.result(timeout) == 3

    If an exception is raised in the coroutine, 
    the returned future will be notified.     
    It can also be used to cancel the task in the event loop:
    try:
        result = future.result(timeout)
    except asyncio.TimeoutError:
        print('The coroutine took too long, cancelling the task...')
        future.cancel()
    except Exception as exc:
        print('The coroutine raised an exception: {!r}'.format(exc))
    else:
        print('The coroutine returned: {!r}'.format(result))






###Asyncio - Example 

##with async lock 


import asyncio

async def coro(name, lock):
    print('coro {}: waiting for lock'.format(name))
    async with lock:
        print('coro {}: holding the lock'.format(name))
        await asyncio.sleep(1)
        print('coro {}: releasing the lock'.format(name))

loop = asyncio.get_event_loop()
lock = asyncio.Lock()
coros = asyncio.gather(coro(1, lock), coro(2, lock))
try:
    loop.run_until_complete(coros)
finally:
    loop.close()

    
    
##Basic 
import asyncio

async def hello_world():
    print("Hello World!")

loop = asyncio.get_event_loop()
# Blocking call which returns when the hello_world() coroutine is done
loop.run_until_complete(hello_world())
loop.close()


##Hello World with call_soon()

import asyncio

def hello_world(loop):
	print('Hello World')
	loop.stop()             #must

loop = asyncio.get_event_loop()

# Schedule a call to hello_world()
loop.call_soon(hello_world, loop)   #schedule a call , but actually runs when run_forever is called

# hangs forevere, , only can be interrupted by loop.stop() as inside hello_word
loop.run_forever()
loop.close()


##Coroutine displaying the current date every second during 5 seconds using the sleep() function:

import asyncio
import datetime

async def display_date(loop):
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()
# Blocking call which returns when the display_date() coroutine is done
loop.run_until_complete(display_date(loop))
loop.close()



##Display the current date with call_later()
import asyncio
import datetime

def display_date(end_time, loop):
    print(datetime.datetime.now())
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, display_date, end_time, loop)
    else:
        loop.stop()

loop = asyncio.get_event_loop()

# Schedule the first call to display_date()
end_time = loop.time() + 5.0
loop.call_soon(display_date, end_time, loop)

# Blocking call interrupted by loop.stop()
loop.run_forever()
loop.close()

##Chain coroutines

import asyncio

async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)
    return x + y
    
@asyncio.coroutine
def print_sum(x, y):
    result = yield from compute(x, y)
    print("%s + %s = %s" % (x, y, result))

loop = asyncio.get_event_loop()
loop.run_until_complete(print_sum(1, 2))
loop.close()

##Future with run_until_complete()
import asyncio

async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')

loop = asyncio.get_event_loop()
future = asyncio.Future()
asyncio.ensure_future(slow_operation(future))
loop.run_until_complete(future)
print(future.result())
loop.close()


##Future with run_forever()
import asyncio

async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')

def got_result(future):
    print(future.result())
    loop.stop()

loop = asyncio.get_event_loop()
future = asyncio.Future()
asyncio.ensure_future(slow_operation(future))
future.add_done_callback(got_result)
try:
    loop.run_forever()
finally:
    loop.close()

    
##Parallel execution of tasks
import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number+1):
        print("Task %s: Compute factorial(%s)..." % (name, i))
        await asyncio.sleep(1)
        f *= i
    print("Task %s: factorial(%s) = %s" % (name, number, f))

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    factorial("A", 2),
    factorial("B", 3),
    factorial("C", 4),
))
loop.close()


###Asyncio - Concurrency and multithreading

#An event loop runs in a thread 
#and executes all callbacks and tasks in the same thread
#While a task is running in the event loop, no other task is running in the same thread. 
#But when the task uses yield from, 
#the task is suspended and the event loop executes the next task

#To schedule a callback from a different thread,
loop.call_soon_threadsafe(callback, *args)

#Most asyncio objects are not thread safe. 
#You should only worry if you access objects outside the event loop
#for example to cancel future(asyncio.Future) in another thread
loop.call_soon_threadsafe(fut.cancel)

#To schedule a coroutine object from a different thread
#returns concurrent.futures.Future 
future = asyncio.run_coroutine_threadsafe(coro_func(), loop) 
result = future.result(timeout)  # Wait for the result with a timeout

#to execute a callback in different thread to not block the thread of the event loop.
executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
loop.run_in_executor(executor, func, *args) #a coroutine, hence to get result, use await or yield from 



##Handle blocking functions correctly
#Blocking functions should not be called directly

#For networking and subprocesses,use 
class asyncio.Protocol
    The base class for implementing streaming protocols 
    (for use with e.g. TCP and SSL transports).
class asyncio.DatagramProtocol
    The base class for implementing datagram protocols 
    (for use with e.g. UDP transports).
class asyncio.SubprocessProtocol
    The base class for implementing protocols communicating 
    with child processes (through a set of unidirectional pipes).


#Example 
class B(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.loop = None

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)

    def _add_task(self, future, coro):
        task = self.loop.create_task(coro)
        future.set_result(task)

    def add_task(self, coro):
        future = Future()
        p = functools.partial(self._add_task, future, coro)
        self.loop.call_soon_threadsafe(p)
        return future.result() #block until result is available

    def cancel(self, task):
        self.loop.call_soon_threadsafe(task.cancel)

#Using run_coroutine_threadsafe to submit a coroutine object from a thread 
#to an event loop. 
#It returns a concurrent.futures.Future to access the result or cancel the task.

@asyncio.coroutine
def test(loop):
    try:
        while True:
            print("Running")
            yield from asyncio.sleep(1, loop=loop)
    except asyncio.CancelledError:
        print("Cancelled")
        loop.stop()
        raise

loop = asyncio.new_event_loop()
thread = threading.Thread(target=loop.run_forever)
future = asyncio.run_coroutine_threadsafe(test(loop), loop)

thread.start()
time.sleep(5)
future.cancel()
thread.join()





###Problem - Detect coroutine objects never scheduled
#When a coroutine function is called and its result is not passed to ensure_future() 
#or to the loop.create_task() method, 
#the execution of the coroutine object will never be scheduled which is probably a bug


import asyncio

@asyncio.coroutine
def test():
    print("never scheduled")

test()

#Output in debug mode:
Coroutine test() at test.py:3 was never yielded from
Coroutine object created at (most recent call last):
  File "test.py", line 7, in <module>
    test()

    
    
##Detect exceptions never consumed
import asyncio

@asyncio.coroutine
def bug():
    raise Exception("not consumed")

loop = asyncio.get_event_loop()
asyncio.ensure_future(bug())
loop.run_forever()
loop.close()

#Output in debug mode:
Task exception was never retrieved
future: <Task finished coro=<bug() done, defined at test.py:3> exception=Exception('not consumed',) created at test.py:8>
source_traceback: Object created at (most recent call last):
  File "test.py", line 8, in <module>
    asyncio.ensure_future(bug())

#The first option is to chain the coroutine in another coroutine 
#and use classic try/except:
@asyncio.coroutine
def handle_exception():
    try:
        yield from bug()
    except Exception:
        print("exception consumed")

loop = asyncio.get_event_loop()
asyncio.ensure_future(handle_exception())
loop.run_forever()
loop.close()


#Another option is to use the loop.run_until_complete() function:
task = asyncio.ensure_future(bug())
try:
    loop.run_until_complete(task)
except Exception:
    print("exception consumed")

    
    
    
##Chain coroutines correctly
#When a coroutine function calls other coroutine functions and tasks, 
#they should be chained explicitly with yield from. 
#Otherwise, the execution is not guaranteed to be sequential.

import asyncio

@asyncio.coroutine
def create():
    yield from asyncio.sleep(3.0)
    print("(1) create file")

@asyncio.coroutine
def write():
    yield from asyncio.sleep(1.0)
    print("(2) write into file")

@asyncio.coroutine
def close():
    print("(3) close file")

@asyncio.coroutine
def test():
    asyncio.ensure_future(create())
    asyncio.ensure_future(write())
    asyncio.ensure_future(close())
    yield from asyncio.sleep(2.0)
    loop.stop()

loop = asyncio.get_event_loop()
asyncio.ensure_future(test())
loop.run_forever()
print("Pending tasks at exit: %s" % asyncio.Task.all_tasks(loop))
loop.close()


#Expected output:
(1) create file
(2) write into file
(3) close file
Pending tasks at exit: set()


#Actual output:
(3) close file
(2) write into file
Pending tasks at exit: {<Task pending create() at test.py:7 wait_for=<Future pending cb=[Task._wakeup()]>>}
Task was destroyed but it is pending!
task: <Task pending create() done at test.py:5 wait_for=<Future pending 

#To fix the example, tasks must be marked with yield from:
@asyncio.coroutine
def test():
    yield from asyncio.ensure_future(create())
    yield from asyncio.ensure_future(write())
    yield from asyncio.ensure_future(close())
    yield from asyncio.sleep(2.0)
    loop.stop()


#Or without asyncio.ensure_future():

@asyncio.coroutine
def test():
    yield from create()
    yield from write()
    yield from close()
    yield from asyncio.sleep(2.0)
    loop.stop()



##Pending task destroyed
#If a pending task is destroyed, 
#the execution of its wrapped coroutine did not complete. 
#It is probably a bug and so a warning is logged.

#Example of log:
Task was destroyed but it is pending!
task: <Task pending coro=<kill_me() done, defined at test.py:5> wait_for=<Future pending cb=[Task._wakeup()]>>


#Enable the debug mode of asyncio to get the traceback where the task was created.
Task was destroyed but it is pending!
source_traceback: Object created at (most recent call last):
  File "test.py", line 15, in <module>
    task = asyncio.ensure_future(coro, loop=loop)
task: <Task pending coro=<kill_me() done, defined at test.py:5> wait

##Close transports and event loops
#When a transport is no more needed, 
#call its close() method to release resources. 
#Event loops must also be closed explicitly.

#If a transport or an event loop is not closed explicitly, 
#a ResourceWarning warning will be emitted in its destructor in debug mode 



###Asyncio - Synchronization primitives
#Locks: 
asyncio.Lock(*, loop=None)
    locked()
        Return True if the underlying lock is acquired
    coroutine acquire()
            This method blocks until the lock is unlocked, then sets it to locked and returns True.
            Use with 'async with'
    release()
    
    
#Event 
class asyncio.Event(*, loop=None)
    clear()
        Reset the internal flag to false. 
        Subsequently, coroutines calling wait() will block until set() is called to set the internal flag to true again.
    is_set()
        Return True if and only if the internal flag is true.
    set()
        Set the internal flag to true. 
        All coroutines waiting for it to become true are awakened. 
        Coroutine that call wait() once the flag is true will not block at all.
    coroutine wait()
        Block until the internal flag is true.


#Condition
class asyncio.Condition(lock=None, *, loop=None)
    coroutine acquire()
        This method blocks until the lock is unlocked, then sets it to locked and returns True.
    notify(n=1)
    locked()
        Return True if the underlying lock is acquired
    notify_all()
    release()
    coroutine wait()
        Wait until notified.
    coroutine wait_for(predicate)
        Wait until a predicate becomes true.


#Semaphore
class asyncio.Semaphore(value=1, *, loop=None)
    coroutine acquire()
            This method blocks until the lock is unlocked, then sets it to locked and returns True.
    locked()
        Return True if the underlying lock is acquired
    release()


#BoundedSemaphore
class asyncio.BoundedSemaphore(value=1, *, loop=None)
    A bounded semaphore implementation. Inherit from Semaphore.
    This raises ValueError in release() if it would increase the value above the initial value.



#Usgae
lock = Lock()
...
yield from lock  #calls acquire() 
try:
    ...
finally:
    lock.release()


#Context manager usage:
lock = Lock()
...
with (yield from lock):
     ...


#Lock objects can be tested for locking state:
if not lock.locked():
   yield from lock
else:
   # lock is acquired
    ...
    
##Note asyncio is single threaded code, we don't require Lock generally
#But, it allows to protect a critical section, 
#without blocking other coroutines from running which don't need access to that critical section

#for example 

#note below, both parse_stuff and use_stuff would call get_stuff and update cache- which is waste  
@asyncio.coroutine
def get_stuff(url):
    if url in cache:
        return cache[url]
    stuff = yield from aiohttp.request('GET', url)
    cache[url] = stuff
    return stuff
    

    
def parse_stuff():
    stuff = yield from get_stuff()
    # do some parsing

def use_stuff():
    stuff = yield from get_stuff()
    # use stuff to do something interesting

def do_work():
     out = yield from aiohttp.request("www.awebsite.com")
     # do some work with out


tasks = [
     asyncio.async(parse_stuff()),
     asyncio.async(use_stuff()),
     asyncio.async(do_work()),
]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
    
#Here only one get_stuff would be executed and other would use cache value 
stuff_lock = asyncio.Lock()

def get_stuff(url):
    with (yield from stuff_lock):
        if url in cache:
            return cache[url]
        stuff = yield from aiohttp.request('GET', url)
        cache[url] = stuff
        return stuff


###Asyncio - Transports and protocols (callback based API) - Low level 

#Transports are classes to abstract various kinds of communication channels

#protocol_factory must be a callable returning a protocol instance.
coroutine loop.create_connection(protocol_factory, host=None, port=None, *, 
    ssl=None, family=0, proto=0, flags=0, sock=None, local_addr=None, 
    server_hostname=None)
    Returns a (transport, protocol) pair.

coroutine loop.create_server(protocol_factory, host=None, port=None, *, 
    family=socket.AF_UNSPEC, flags=socket.AI_PASSIVE, sock=None, backlog=100, 
    ssl=None, reuse_address=None, reuse_port=None)
    

coroutine loop.create_datagram_endpoint(protocol_factory, local_addr=None, 
    remote_addr=None, *, family=0, proto=0, flags=0, reuse_address=None, 
    reuse_port=None, allow_broadcast=None, sock=None)
    Returns a (transport, protocol) pair.

coroutine loop.connect_accepted_socket(protocol_factory, sock, *, ssl=None)
    Handle an accepted connection.
    This is used by servers that accept connections outside of asyncio 
    but that use asyncio to handle them.
    the coroutine returns a (transport, protocol) pair.

##Extrmely low level routine, Donot use these, Use Protocole or Stream based approach  
coroutine loop.sock_recv(sock, nbytes)
    Receive data from the socke
    With SelectorEventLoop event loop, the socket sock must be non-blocking
    With SelectorEventLoop event loop, the socket sock must be non-blocking
    
coroutine loop.sock_sendall(sock, data)
    Send data to the socket
    The socket must be connected to a remote socket 
    None is returned on success. On error, an exception is raised
    With SelectorEventLoop event loop, the socket sock must be non-blocking


coroutine loop.sock_connect(sock, address)
    Connect to a remote socket at address
    With SelectorEventLoop event loop, the socket sock must be non-blocking


coroutine loop.sock_accept(sock)
    Accept a connection
    The socket must be bound to an address and listening for connections.
    The return value is a pair (conn, address) 
    where conn is a new socket object usable to send and receive data on the connection, 
    and address is the address bound to the socket on the other end of the connection.
    The socket sock must be non-blocking.

coroutine loop.getaddrinfo(host, port, *, family=0, type=0, proto=0, flags=0)
    This method is a coroutine, similar to socket.getaddrinfo() function but non-blocking.

coroutine loop.getnameinfo(sockaddr, flags=0)
    This method is a coroutine, similar to socket.getnameinfo() function but non-blocking.

coroutine loop.connect_read_pipe(protocol_factory, pipe)
    Register read pipe in eventloop.
    protocol_factory should instantiate object with Protocol interface. 
    Return pair (transport, protocol), 
    where transport supports the ReadTransport interface.
    With SelectorEventLoop event loop, the pipe is set to non-blocking mode.
    On Windows Use ProactorEventLoop 
    
coroutine loop.connect_write_pipe(protocol_factory, pipe)
    Register write pipe in eventloop.
    protocol_factory should instantiate object with BaseProtocol interface. 
    Return pair (transport, protocol), 
    where transport supports the WriteTransport interface.
    With SelectorEventLoop event loop, the pipe is set to non-blocking mode.
    On Windows Use ProactorEventLoop 
    
##Protocols 
#asyncio provides base classes that you can subclass to implement your network protocols
#override certain methods

class asyncio.Protocol
    The base class for implementing streaming protocols 
    (for use with e.g. TCP and SSL transports).
class asyncio.DatagramProtocol
    The base class for implementing datagram protocols (for use with e.g. UDP transports).
class asyncio.SubprocessProtocol
    The base class for implementing protocols communicating with child processes 
    (through a set of unidirectional pipes).

##State machine:
start -> connection_made() [-> data_received() *] [-> eof_received() ?] 
            -> connection_lost() -> end

##Connection callbacks - Protocol, DatagramProtocol and SubprocessProtocol
BaseProtocol.connection_made(transport)
    Called when a connection is made.
BaseProtocol.connection_lost(exc)
    Called when the connection is lost or closed.

#SubprocessProtocol instances:
SubprocessProtocol.pipe_data_received(fd, data)
    Called when the child process writes data into its stdout or stderr pipe. 
    fd is the integer file descriptor of the pipe. 
    data is a non-empty bytes object containing the data.
SubprocessProtocol.pipe_connection_lost(fd, exc)
    Called when one of the pipes communicating with the child process is closed. 
    fd is the integer file descriptor that was closed.
SubprocessProtocol.process_exited()
    Called when the child process has exited.


##Streaming protocols - Protocol
Protocol.data_received(data)
    Called when some data is received. 
Protocol.eof_received()
    Called when the other end signals it won't send any more data 
    (for example by calling write_eof(), if the other end also uses asyncio).




##Datagram protocols - DatagramProtocol

DatagramProtocol.datagram_received(data, addr)
    Called when a datagram is received. 
    data is a bytes object containing the incoming data. 
    addr is the address of the peer sending the data; 
    the exact format depends on the transport.
DatagramProtocol.error_received(exc)
    Called when a previous send or receive operation raises an OSError. 
    exc is the OSError instance.



##Flow control callbacks - Protocol, DatagramProtocol and SubprocessProtocol
BaseProtocol.pause_writing()
    Called when the transport's buffer goes over the high-water mark.
BaseProtocol.resume_writing()
    Called when the transport's buffer drains below the low-water mark.
    pause_writing() and resume_writing() calls are paired 

##Transport 
class asyncio.BaseTransport
    Base class for transports.
    close()
        Close the transport. If the transport has a buffer for outgoing data, buffered data will be flushed asynchronously. No more data will be received. After all buffered data is flushed, the protocol’s connection_lost() method will be called with None as its argument.
    is_closing()
        Return True if the transport is closing or is closed.
    get_extra_info(name, default=None)
        Return optional transport information. name is a string representing the piece of transport-specific information to get, default is the value to return if the information doesn’t exist.
        This method allows transport implementations to easily expose channel-specific information.
            socket:
                'peername': the remote address to which the socket is connected, result of socket.socket.getpeername() (None on error)
                'socket': socket.socket instance
                'sockname': the socket’s own address, result of socket.socket.getsockname()
            SSL socket:
                'compression': the compression algorithm being used as a string, or None if the connection isn’t compressed; result of ssl.SSLSocket.compression()
                'cipher': a three-value tuple containing the name of the cipher being used, the version of the SSL protocol that defines its use, and the number of secret bits being used; result of ssl.SSLSocket.cipher()
                'peercert': peer certificate; result of ssl.SSLSocket.getpeercert()
                'sslcontext': ssl.SSLContext instance
                'ssl_object': ssl.SSLObject or ssl.SSLSocket instance
            pipe:
                'pipe': pipe object
            subprocess:
                'subprocess': subprocess.Popen instance
    set_protocol(protocol)
        Set a new protocol. Switching protocol should only be done when both protocols are documented to support the switch.
    get_protocol()
        Return the current protocol.

##ReadTransport
class asyncio.ReadTransport
    Interface for read-only transports.
    pause_reading()
        Pause the receiving end of the transport. No data will be passed to the protocol’s data_received() method until resume_reading() is called.
    resume_reading()
        Resume the receiving end. The protocol’s data_received() method will be called once again if some data is available for reading.
##WriteTransport
class asyncio.WriteTransport
    Interface for write-only transports.
    abort()
        Close the transport immediately, without waiting for pending operations to complete. Buffered data will be lost. No more data will be received. The protocol’s connection_lost() method will eventually be called with None as its argument.
    can_write_eof()
        Return True if the transport supports write_eof(), False if not.
    get_write_buffer_size()
        Return the current size of the output buffer used by the transport.
    get_write_buffer_limits()
        Get the high- and low-water limits for write flow control. Return a tuple (low, high) where low and high are positive number of bytes.
        Use set_write_buffer_limits() to set the limits.
        New in version 3.4.2.
    set_write_buffer_limits(high=None, low=None)
        Set the high- and low-water limits for write flow control.
        These two values (measured in number of bytes) control when the protocol’s pause_writing() and resume_writing() methods are called. If specified, the low-water limit must be less than or equal to the high-water limit. Neither high nor low can be negative.
        pause_writing() is called when the buffer size becomes greater than or equal to the high value. If writing has been paused, resume_writing() is called when the buffer size becomes less than or equal to the low value.
        The defaults are implementation-specific. If only the high-water limit is given, the low-water limit defaults to an implementation-specific value less than or equal to the high-water limit. Setting high to zero forces low to zero as well, and causes pause_writing() to be called whenever the buffer becomes non-empty. Setting low to zero causes resume_writing() to be called only once the buffer is empty. Use of zero for either limit is generally sub-optimal as it reduces opportunities for doing I/O and computation concurrently.
        Use get_write_buffer_limits() to get the limits.
    write(data)
        Write some data bytes to the transport.
        This method does not block; it buffers the data and arranges for it to be sent out asynchronously.
    writelines(list_of_data)
        Write a list (or any iterable) of data bytes to the transport. This is functionally equivalent to calling write() on each element yielded by the iterable, but may be implemented more efficiently.
    write_eof()
        Close the write end of the transport after flushing buffered data. Data may still be received.
        This method can raise NotImplementedError if the transport (e.g. SSL) doesn’t support half-closes.
##DatagramTransport
DatagramTransport.sendto(data, addr=None)
    Send the data bytes to the remote peer given by addr (a transport-dependent target address). If addr is None, the data is sent to the target address given on transport creation.
    This method does not block; it buffers the data and arranges for it to be sent out asynchronously.
DatagramTransport.abort()
    Close the transport immediately, without waiting for pending operations to complete. Buffered data will be lost. No more data will be received. The protocol’s connection_lost() method will eventually be called with None as its argument.
##BaseSubprocessTransport
class asyncio.BaseSubprocessTransport
    get_pid()
        Return the subprocess process id as an integer.
    get_pipe_transport(fd)
        Return the transport for the communication pipe corresponding to the integer file descriptor fd:
            0: readable streaming transport of the standard input (stdin), or None if the subprocess was not created with stdin=PIPE
            1: writable streaming transport of the standard output (stdout), or None if the subprocess was not created with stdout=PIPE
            2: writable streaming transport of the standard error (stderr), or None if the subprocess was not created with stderr=PIPE
            other fd: None
    get_returncode()
        Return the subprocess returncode as an integer or None if it hasn’t returned, similarly to the subprocess.Popen.returncode attribute.
    kill()
        Kill the subprocess, as in subprocess.Popen.kill().
        On POSIX systems, the function sends SIGKILL to the subprocess. On Windows, this method is an alias for terminate().
    send_signal(signal)
        Send the signal number to the subprocess, as in subprocess.Popen.send_signal().
    terminate()
        Ask the subprocess to stop, as in subprocess.Popen.terminate(). This method is an alias for the close() method.
        On POSIX systems, this method sends SIGTERM to the subprocess. On Windows, the Windows API function TerminateProcess() is called to stop the subprocess.
    close()
        Ask the subprocess to stop by calling the terminate() method if the subprocess hasn’t returned yet, and close transports of all pipes (stdin, stdout and stderr).
        
    
##TCP CLient and server 
#Use Stream based protocol (easier)

##UDP echo client protocol

import asyncio

class EchoClientProtocol:
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print('Send:', self.message)
        self.transport.sendto(self.message.encode())

    def datagram_received(self, data, addr):
        print("Received:", data.decode())

        print("Close the socket")
        self.transport.close()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Socket closed, stop the event loop")
        loop = asyncio.get_event_loop()
        loop.stop()

loop = asyncio.get_event_loop()
message = "Hello World!"
#Not Supported on ProactorEventLoop
connect = loop.create_datagram_endpoint(
    lambda: EchoClientProtocol(message, loop),
    remote_addr=('127.0.0.1', 9999))
transport, protocol = loop.run_until_complete(connect)
loop.run_forever()
transport.close()
loop.close()



##UDP echo server protocol

import asyncio

class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print('Received %r from %s' % (message, addr))
        print('Send %r to %s' % (message, addr))
        self.transport.sendto(data, addr)

loop = asyncio.get_event_loop()
print("Starting UDP server")
# One protocol instance will be created to serve all client requests
#Not Supported on ProactorEventLoop
listen = loop.create_datagram_endpoint(EchoServerProtocol, local_addr=('127.0.0.1', 9999))
transport, protocol = loop.run_until_complete(listen)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

transport.close()
loop.close()


    
    
    
    
    
    
###Asynio -Asynchronous Reader and Writer - Stream based(coroutine) - High level 

class asyncio.StreamReader(limit=None, loop=None)
    Not Thread safe 
        coroutine read(n=-1)
        coroutine readline()
        coroutine readexactly(n)
        coroutine readuntil(separator=b'\n')

        feed_eof()  #Acknowledge the EOF.
        at_eof() #Return True if the buffer is empty and feed_eof() was called.
        exception()
        feed_data(data)  #Feed data bytes in the internal buffer. Any operations waiting for the data will be resumed.
        set_exception(exc)
        set_transport(transport)



class asyncio.StreamWriter(transport, protocol, reader, loop)
    Not Thread safe 
        write(data)
        writelines(data)
        write_eof()

        can_write_eof()  #Return True if the transport supports write_eof(), False if not. 

        close()
        coroutine drain()   
            Let the write buffer of the underlying transport a chance to be flushed
            #use as 
            w.write(data)
            yield from w.drain()

##Wrapper function - High level
#calls internally low level create_connection and create_server)
coroutine asyncio.open_connection(host=None, port=None, *, loop=None, limit=None, **kwds)
    returning a (reader, writer) pair
    The reader returned is a StreamReader instance; the writer is a StreamWriter instance.
    
coroutine asyncio.start_server(client_connected_cb, host=None, port=None, *, loop=None, limit=None, **kwds)
    Start a socket server, with a callback for each client connected
    client_connected_cb parameter _function(client_reader, client_writer)
    client_reader is a StreamReader object, 
    while client_writer is a StreamWriter object

    
    
    
##Example -TCP echo client using streams

import asyncio

@asyncio.coroutine
def tcp_echo_client(message, loop):
    reader, writer = yield from asyncio.open_connection('127.0.0.1', 8888, loop=loop)

    print('Send: %r' % message)
    writer.write(message.encode())

    data = yield from reader.read(100)
    print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()

message = 'Hello World!'
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()


##Example - TCP echo server using streams

import asyncio

@asyncio.coroutine
def handle_echo(reader, writer):
    data = yield from reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))

    print("Send: %r" % message)
    writer.write(data)
    yield from writer.drain()  #must wait for writing to happen

    print("Close the client socket")
    writer.close()


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()





##Example - Get HTTP headers


import asyncio
import urllib.parse
import sys

@asyncio.coroutine
def print_http_headers(url):
    url = urllib.parse.urlsplit(url)
    if url.scheme == 'https':
        connect = asyncio.open_connection(url.hostname, 443, ssl=True)
    else:
        connect = asyncio.open_connection(url.hostname, 80)
	
    reader, writer = yield from connect
	
    query = ('HEAD {path} HTTP/1.0\r\n'
             'Host: {hostname}\r\n'
             '\r\n').format(path=url.path or '/', hostname=url.hostname)
    writer.write(query.encode('latin-1'))
    while True:
        line = yield from reader.readline()
        if not line:
            break
        line = line.decode('latin1').rstrip()
        if line:
            print('HTTP header> %s' % line)

    # Ignore the body, close the socket
    writer.close()

url = sys.argv[1]
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(print_http_headers(url))
loop.run_until_complete(task)
loop.close()

#Execution 
$ python example.py http://example.com/path/page.html





###Asyncio - Subprocess 


##In windows, use ProactorEventLoop to support subprocess
import asyncio, sys

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)




#Create a subprocess: high-level API using Process
coroutine asyncio.create_subprocess_exec(*args, stdin=None, stdout=None, 
        stderr=None, loop=None, limit=None, **kwds)
    Return a Process instance.
    
coroutine asyncio.create_subprocess_shell(cmd, stdin=None, stdout=None, 
            stderr=None, loop=None, limit=None, **kwds)
    Return a Process instance.
    shlex.quote() function can be used to properly escape whitespace and shell metacharacters in strings 
    import shlex 
    command = 'ls -l {}'.format(shlex.quote(filename))

asyncio.subprocess.PIPE
asyncio.subprocess.STDOUT
asyncio.subprocess.DEVNULL


    
class asyncio.subprocess.Process
    coroutine wait()
        Wait for child process to terminate. Set and return returncode attribute
    coroutine communicate(input=None)  
        Interact with process: Send data(arg input) to stdin. 
        Read data from stdout and stderr, until end-of-file is reached
        returns (stdout_data, stderr_data)
        to send data to the process's stdin, create the Process object with stdin=PIPE. 
        to get anything other than None in the result tuple, give stdout=PIPE and/or stderr=PIPE too.
    send_signal(signal)
        Sends the signal signal to the child process
        On Windows, SIGTERM is an alias for terminate().
    terminate()
        Stop the child
    kill()
        Kills the child
    stdin
        Standard input stream (StreamWriter), None if the process was created with stdin=None.
    stdout
        Standard output stream (StreamReader), None if the process was created with stdout=None.
    stderr
        Standard error stream (StreamReader), None if the process was created with stderr=None.
    pid
    returncode


##Example - Subprocess using stream 

import asyncio.subprocess
import sys

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

if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()

date = loop.run_until_complete(get_date())
print("Current date: %s" % date)
loop.close()


###Combining Coroutines with Threads and Processes

#A ThreadPoolExecutor starts its worker threads 
#and then calls each of the provided functions once in a thread. 

import asyncio
import concurrent.futures
import logging
import sys
import time


def blocks(n):
    log = logging.getLogger('blocks({})'.format(n))
    log.info('running')
    time.sleep(0.1)
    log.info('done')
    return n ** 2


async def run_blocking_tasks(executor):
    log = logging.getLogger('run_blocking_tasks')
    log.info('starting')

    log.info('creating executor tasks')
    loop = asyncio.get_event_loop()
    blocking_tasks = [
        loop.run_in_executor(executor, blocks, i)
        for i in range(6)
    ]
    log.info('waiting for executor tasks')
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info('results: {!r}'.format(results))

    log.info('exiting')


if __name__ == '__main__':
    # Configure logging to show the name of the thread
    # where the log message originates.
    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)10s %(name)18s: %(message)s',
        stream=sys.stderr,
    )

    # Create a limited thread pool.
    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=3,
    )

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            run_blocking_tasks(executor)
        )
    finally:
        event_loop.close()


##A ProcessPoolExecutor works in much the same way, 


# changes from asyncio_executor_thread.py

if __name__ == '__main__':
    # Configure logging to show the id of the process
    # where the log message originates.
    logging.basicConfig(
        level=logging.INFO,
        format='PID %(process)5s %(name)18s: %(message)s',
        stream=sys.stderr,
    )

    # Create a limited process pool.
    executor = concurrent.futures.ProcessPoolExecutor(
        max_workers=3,
    )

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            run_blocking_tasks(executor)
        )
    finally:
        event_loop.close()







    
### async-timeout
$ pip install async-timeout   
    
#The context manager is useful in cases 
#when you want to apply timeout logic around block of code  
#or in cases when asyncio.wait_for() is not suitable

async with timeout(1.5):
    await inner()

#1.If inner() is executed faster than in 1.5 seconds nothing happens.
#2.Otherwise inner() is cancelled internally by sending asyncio.CancelledError into but asyncio.TimeoutError is raised outside of context manager scope.

#Context manager has .expired property for check if timeout happens exactly in context manager:
async with timeout(1.5) as cm:
    await inner()
print(cm.expired)

 
    
    
    
    
###aiohttp 
$ pip install aiohttp

##Supports 
•Supports both Client and HTTP Server.
•Supports both Server WebSockets and Client WebSockets out-of-the-box.
•Web-server has Middlewares, Signals and pluggable routing.



#Example:Using aiohttp

import asyncio
import aiohttp
 
@asyncio.coroutine
def fetch_page(url):
    response = yield from aiohttp.request('GET', url)
    assert response.status == 200
    content = yield from response.read()  #response.read_and_close(decode=True)
    print('URL: {0}:  Content: {1}'.format(url, len(content)))
    return (url, len(content))
 



 
loop = asyncio.get_event_loop()
tasks = [
     asyncio.async(fetch_page('http://google.com')),
     asyncio.async(fetch_page('http://cnn.com')),
     asyncio.async(fetch_page('http://twitter.com'))]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
 
for task in tasks:
    print(task.result())



#Another examples

import asyncio
import aiohttp
import bs4

@asyncio.coroutine
def get(*args, **kwargs):  
    response = yield from aiohttp.request('GET', *args, **kwargs)
    return (yield from response.read())

	
def first_magnet(page):  
    soup = bs4.BeautifulSoup(page, "html.parser")
    a = soup.find('a', title='Download this torrent using magnet')
    return a['href']


@asyncio.coroutine
def print_magnet(query):  
    url = 'http://thepiratebay.se/search/{}/0/7/0'.format(query)
    page = yield from get(url, compress=True)
    magnet = first_magnet(page)
    print('{}: {}'.format(query, magnet))
	

	
distros = ['archlinux', 'ubuntu', 'debian']  
loop = asyncio.get_event_loop()  
f = asyncio.wait([print_magnet(d) for d in distros])  
loop.run_until_complete(f)  
loop.close()


##Py3.5 version 

import aiohttp
import asyncio
import async_timeout

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://python.org')
        print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())


#Server example:


from aiohttp import web

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/{name}', handle)

web.run_app(app)

##Make a Request
async with aiohttp.ClientSession() as session:
    async with session.get('https://api.github.com/events') as resp:
        print(resp.status)
        print(await resp.text())

#Other HTTP methods
session.post('http://httpbin.org/post', data=b'data')
session.put('http://httpbin.org/put', data=b'data')
session.delete('http://httpbin.org/delete')
session.head('http://httpbin.org/get')
session.options('http://httpbin.org/get')
session.patch('http://httpbin.org/patch', data=b'data'


##JSON Request
async with aiohttp.ClientSession() as session:
    async with session.post(json={'test': 'object})
    
##Passing Parameters In URLs
params = {'key1': 'value1', 'key2': 'value2'}
async with session.get('http://httpbin.org/get', params=params) as resp:
    assert str(resp.url) == 'http://httpbin.org/get?key2=value2&key1=value1'

params = [('key', 'value1'), ('key', 'value2')]
async with session.get('http://httpbin.org/get',
                       params=params) as r:
    assert str(r.url) == 'http://httpbin.org/get?key=value2&key=value1'


##Response Content   
#ClientResponse object contains request_info property
#contains request fields: url and headers.

async with session.get('https://api.github.com/events') as resp:
    print(await resp.text())

    
#aiohttp will automatically decode the content from the server. 
#or specify
await resp.text(encoding='windows-1251')

##Binary Response Content    
#The gzip and deflate transfer-encodings are automatically decoded 
print(await resp.read())

##JSON Response Content
async with session.get('https://api.github.com/events') as resp:
    print(await resp.json())

##Streaming Response Content
#It is not possible to use read(), json() and text() after explicit reading from content
with open(filename, 'wb') as fd:
    while True:
        chunk = await resp.content.read(chunk_size)
        if not chunk:
            break
        fd.write(chunk)

##Custom Headers
import json
url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}
headers = {'content-type': 'application/json'}

await session.post(url,
                   data=json.dumps(payload),
                   headers=headers)

##Custom Cookies
url = 'http://httpbin.org/cookies'
cookies = {'cookies_are': 'working'}
async with ClientSession(cookies=cookies) as session:
    async with session.get(url) as resp:
        assert await resp.json() == {
           "cookies": {"cookies_are": "working"}}

##to send some form-encoded data 
payload = {'key1': 'value1', 'key2': 'value2'}
async with session.post('http://httpbin.org/post',
                        data=payload) as resp:
    print(await resp.text())


import json
url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}

async with session.post(url, data=json.dumps(payload)) as resp:
    ...

##POST a Multipart-Encoded File

url = 'http://httpbin.org/post'
files = {'file': open('report.xls', 'rb')}
await session.post(url, data=files)

#set the filename, content_type explicitly:
url = 'http://httpbin.org/post'
data = FormData()
data.add_field('file',
               open('report.xls', 'rb'),
               filename='report.xls',
               content_type='application/vnd.ms-excel')

await session.post(url, data=data)


##Streaming uploads
##to send large files without reading them into memory.

with open('massive-body', 'rb') as f:
   await session.post('http://httpbin.org/post', data=f)


#Or  use aiohttp.streamer object:
@aiohttp.streamer
def file_sender(writer, file_name=None):
    with open(file_name, 'rb') as f:
        chunk = f.read(2**16)
        while chunk:
            yield from writer.write(chunk)
            chunk = f.read(2**16)

# Then you can use `file_sender` as a data provider:

async with session.post('http://httpbin.org/post',
                        data=file_sender(file_name='huge_file')) as resp:
    print(await resp.text())


#or use a StreamReader object
#to upload a file from another request and calculate the file SHA1 hash:
async def feed_stream(resp, stream):
    h = hashlib.sha256()

    while True:
        chunk = await resp.content.readany()
        if not chunk:
            break
        h.update(chunk)
        stream.feed_data(chunk)

    return h.hexdigest()

resp = session.get('http://httpbin.org/post')
stream = StreamReader()
loop.create_task(session.post('http://httpbin.org/post', data=stream))

file_hash = await feed_stream(resp, stream)

#And chain get and post requests together:
r = await session.get('http://python.org')
await session.post('http://httpbin.org/post',
                   data=r.content)



##Uploading pre-compressed data
#set  the value of the Content-Encoding header:
async def my_coroutine(session, headers, my_data):
    data = zlib.compress(my_data)
    headers = {'Content-Encoding': 'deflate'}
    async with session.post('http://httpbin.org/post',
                            data=data,
                            headers=headers)
        pass



##Keep-Alive, connection pooling and cookie sharing
#ClientSession may be used for sharing cookies between multiple requests:


async with aiohttp.ClientSession() as session:
    await session.get('http://httpbin.org/cookies/set?my_cookie=my_value')
    filtered = session.cookie_jar.filter_cookies('http://httpbin.org')
    assert filtered['my_cookie'].value == 'my_value'
    async with session.get('http://httpbin.org/cookies') as r:
        json_body = await r.json()
        assert json_body['cookies']['my_cookie'] == 'my_value'


#set default headers for all session requests:
async with aiohttp.ClientSession(
    headers={"Authorization": "Basic bG9naW46cGFzcw=="}) as session:
    async with session.get("http://httpbin.org/headers") as r:
        json_body = await r.json()
        assert json_body['headers']['Authorization'] == \
            'Basic bG9naW46cGFzcw=='


##Resolving using custom nameservers
#aiodns is required:
from aiohttp.resolver import AsyncResolver

resolver = AsyncResolver(nameservers=["8.8.8.8", "8.8.4.4"])
conn = aiohttp.TCPConnector(resolver=resolver)

##SSL control for TCP sockets
#TCPConnector constructor accepts mutually exclusive verify_ssl and ssl_context params.
#Certification checks can be relaxed by passing verify_ssl=False:
conn = aiohttp.TCPConnector(verify_ssl=False)
session = aiohttp.ClientSession(connector=conn)
r = await session.get('https://example.com')


#to setup custom ssl parameters (use own certification files for example) 
sslcontext = ssl.create_default_context(
   cafile='/path/to/ca-bundle.crt')
conn = aiohttp.TCPConnector(ssl_context=sslcontext)
session = aiohttp.ClientSession(connector=conn)
r = await session.get('https://example.com')


#to verify client-side certificates
sslcontext = ssl.create_default_context(
   cafile='/path/to/client-side-ca-bundle.crt')
sslcontext.load_cert_chain('/path/to/client/public/key.pem', '/path/to/client/private/key.pem')
conn = aiohttp.TCPConnector(ssl_context=sslcontext)
session = aiohttp.ClientSession(connector=conn)
r = await session.get('https://server-with-client-side-certificates-validaction.com')


#verify certificates via MD5, SHA1, or SHA256 fingerprint:
# Attempt to connect to https://www.python.org
# with a pin to a bogus certificate:
bad_md5 = b'\xa2\x06G\xad\xaa\xf5\xd8\\J\x99^by;\x06='
conn = aiohttp.TCPConnector(fingerprint=bad_md5)
session = aiohttp.ClientSession(connector=conn)
exc = None
try:
    r = yield from session.get('https://www.python.org')
except FingerprintMismatch as e:
    exc = e
assert exc is not None
assert exc.expected == bad_md5

# www.python.org cert's actual md5
assert exc.got == b'\xca;I\x9cuv\x8es\x138N$?\x15\xca\xcb'


#Note that this is the fingerprint of the DER-encoded certificate. 
#If you have the certificate in PEM format, you can convert it to DER with e.g. 
$ openssl x509 -in crt.pem -inform PEM -outform DER > crt.der.

#to convert from a hexadecimal digest to a binary byte-string, 
#you can use binascii.unhexlify:
md5_hex = 'ca3b499c75768e7313384e243f15cacb'
from binascii import unhexlify
assert unhexlify(md5_hex) == b'\xca;I\x9cuv\x8es\x138N$?\x15\xca\xcb'


##Proxy support
sync with aiohttp.ClientSession() as session:
    async with session.get("http://python.org",
                           proxy="http://some.proxy.com") as resp:
        print(resp.status)


#it won't read environment variables by default. 
#or set proxy_from_env to True
async with aiohttp.ClientSession() as session:
    async with session.get("http://python.org",
                           proxy_from_env=True) as resp:
        print(resp.status)


#It also supports proxy authorization:
async with aiohttp.ClientSession() as session:
    proxy_auth = aiohttp.BasicAuth('user', 'pass')
    async with session.get("http://python.org",
                           proxy="http://some.proxy.com",
                           proxy_auth=proxy_auth) as resp:
        print(resp.status)


#Authentication credentials can be passed in proxy URL:
session.get("http://python.org",
            proxy="http://user:pass@some.proxy.com")



##Response Status Codes
async with session.get('http://httpbin.org/get') as resp:
    assert resp.status == 200



##Response Headers

>>> resp.headers
{'ACCESS-CONTROL-ALLOW-ORIGIN': '*',
 'CONTENT-TYPE': 'application/json',
 'DATE': 'Tue, 15 Jul 2014 16:49:51 GMT',
 'SERVER': 'gunicorn/18.0',
 'CONTENT-LENGTH': '331',
 'CONNECTION': 'keep-alive'}


>>> resp.headers['Content-Type']
'application/json'

>>> resp.headers.get('content-type')
'application/json'

>>> resp.raw_headers
((b'SERVER', b'nginx'),
 (b'DATE', b'Sat, 09 Jan 2016 20:28:40 GMT'),
 (b'CONTENT-TYPE', b'text/html; charset=utf-8'),
 (b'CONTENT-LENGTH', b'12150'),
 (b'CONNECTION', b'keep-alive'))



##Response Cookies
url = 'http://example.com/some/cookie/setting/url'
async with session.get(url) as resp:
    print(resp.cookies['example_cookie_name'])

##Response History
#If a request was redirected
>>> resp = await session.get('http://example.com/some/redirect/')
>>> resp
<ClientResponse(http://example.com/some/other/url/) [200]>
>>> resp.history
(<ClientResponse(http://example.com/some/redirect/) [301]>,)

##Timeouts
#None or 0 disables timeout check.
async with session.get('https://github.com', timeout=60) as r:
    ...




#or use async_timeout.timeout() 
import async_timeout

with async_timeout.timeout(0.001, loop=session.loop):
    async with session.get('https://github.com') as r:
        await r.text()



###Recursive Asyncio 

import asyncio 

@asyncio.coroutine 
def fib(a=0,b=1):
    print(b)
    yield from fib(b,a+b)
    
loop = asyncio.get_event_loop()
loop.run_until_complete(fib())
#Crashes with stack overflow 

#version-1 
import asyncio 


async def fib(a=0,b=1):
    print(b)
    await asyncio.ensure_future(fib(b,a+b))  #schedules Task 

loop = asyncio.get_event_loop()
#
asyncio.ensure_future(fib())
loop.run_forever()
#else 
loop.run_until_complete(fib())



##Trampoline 
import asyncio

@asyncio.coroutine
def a(n):
    print("A: {}".format(n))
    if n > 1000: return n
    else: yield from b(n+1)

@asyncio.coroutine
def b(n):
    print("B: {}".format(n))
    yield from a(n+1)

loop = asyncio.get_event_loop()
loop.run_until_complete(a(0))
#crashes with stack overflow 

#To keep the stack from growing,use asyncio.async 

import asyncio

@asyncio.coroutine
def a(n):
    fut = asyncio.Future()  # We're going to return this right away to our caller
    def set_result(out):  # This gets called when the next recursive call completes
        fut.set_result(out.result()) # Pull the result from the inner call and return it up the stack.
    print("A: {}".format(n))
    if n > 1000: 
        return n
    else: 
        in_fut = asyncio.async(b(n+1))  # This returns an asyncio.Task
        in_fut.add_done_callback(set_result) # schedule set_result when the Task is done.
    return fut

@asyncio.coroutine
def b(n):
    fut = asyncio.Future()
    def set_result(out):
        fut.set_result(out.result())
    print("B: {}".format(n))
    in_fut = asyncio.async(a(n+1))
    in_fut.add_done_callback(set_result)
    return fut

loop = asyncio.get_event_loop()
print("Out is {}".format(loop.run_until_complete(a(0))))


Output:
A: 0
B: 1
A: 2
B: 3
A: 4
B: 5
...
A: 994
B: 995
A: 996
B: 997
A: 998
B: 999
A: 1000
B: 1001
A: 1002
Out is 1002

#Now, your example code doesn't actually return n all the way back up the stack, 
#so you could make something functionally equivalent that's a bit simpler:
import asyncio

@asyncio.coroutine
def a(n):
    print("A: {}".format(n))
    if n > 1000: loop.stop(); return n
    else: asyncio.async(b(n+1))

@asyncio.coroutine
def b(n):
    print("B: {}".format(n))
    asyncio.async(a(n+1))

loop = asyncio.get_event_loop()
asyncio.async(a(0))
loop.run_forever()

#Async, await: 
import asyncio

async def a(n):
    if n > 1000:
        return n
    else:
        ret = await asyncio.ensure_future(b(n + 1))
        return ret

async def b(n):
    ret = await asyncio.ensure_future(a(n + 1))
    return ret

import timeit
print(min(timeit.repeat("""
loop = asyncio.get_event_loop()
loop.run_until_complete(a(0))
""", "from __main__ import a, b, asyncio", number=10)))

Result:
% time  python stack.py
0.45157229300002655
python stack.py  1,42s user 0,02s system 99% cpu 1,451 total







    


###Tornado-Overriding RequestHandler methods
On every request, the following sequence of calls takes place:
 1. A new RequestHandler object is created on each request.
 2. initialize() is called with the initialization arguments from the Application configuration.
    initialize should typically just save the arguments passed into member variables; it may not produce any
    output or call methods like send_error .
 3. prepare() is called. This is most useful in a base class shared by all of your handler subclasses, as prepare
    is called no matter which HTTP method is used. prepare may produce output; 
    if it calls finish (or redirect, etc), processing stops here.
 4. One of the HTTP methods is called: get(), post(), put(), etc. If the URL regular expression contains
    capturing groups, they are passed as arguments to this method.
 5. When the request is finished, on_finish() is called. 
    This is generally after get() or another HTTP method returns.
    
https://www.tornadoweb.org/en/stable/web.html
Some of the most commonly overridden methods include:
     · write_error - outputs HTML for use on error pages.
     · on_connection_close - called when the client disconnects; applications may choose to detect this case
       and halt further processing. Note that there is no guarantee that a closed connection can be detected promptly.
     · get_current_user - see User authentication.
     · get_user_locale - returns Locale object to use for the current user.
     · set_default_headers - may be used to set additional headers on the response (such as a custom Server header).

     
     
#Example 
import tornado.options, tornado.ioloop, tornado.web, tornado.escape, tornado.iostream, tornado.gen
import logging
import os,  uuid, shutil
import mimetypes

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world and earth")
        
        
class MainHandler2(tornado.web.RequestHandler):
    def get(self):
        self.write('<a href="%s">link to story 1</a>' %
                   self.reverse_url("story", "1"))  #'story' comes from URL, name , become /story/1

class StoryHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self, story_id):
        self.write("this is story %s" % story_id)

        
#The main entry point for a handler subclass is a method named 
#after the HTTP method being handled: get(), post() ...
#render() loads a Template by name and renders it with the given arguments
#write() is used for non-template-based output; it accepts strings, bytes, and dictionaries 
#(dicts will be encoded as JSON).
class JsonHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.args = None 
        if self.request.headers.get('Content-Type',"Unknown") == 'application/json':
            self.args = tornado.escape.json_decode(self.request.body)
        # Access self.args directly instead of using self.get_argument.
    def get_name(self, name):
        #to search both query or body 
        # RequestHandler.get_argument(name: str, default: Union[None, str, RAISE] = RAISE, strip: bool = True) -> Optional[str]
        # RequestHandler.get_arguments(name: str, strip: bool = True) -> List[str]
        #to search query 
        # RequestHandler.get_query_argument(name: str, default: Union[None, str, RAISE] = RAISE, strip: bool = True) => Optional[str][source]
        # RequestHandler.get_query_arguments(name: str, strip: bool = True) => List[str]
        #to search body 
        # RequestHandler.get_body_argument(name: str, default: Union[None, str, RAISE] = RAISE, strip: bool = True) => Optional[str][source]
        # RequestHandler.get_body_arguments(name: str, strip: bool = True) => List[str]
        res = name 
        if not name:
            if self.args:
                res = self.args.get('name',"Jane Doe")
            elif self.get_query_argument('name', None):
                res = self.get_query_argument('name')
        return res or "Jane Doe"
        
    def get(self, name=None):
        obj = {'name': self.get_name(name), 'age': 200}
        self.set_status(200) 
        self.write(obj)
        
        
class XMLHandler(tornado.web.RequestHandler):
    def get(self, name):
        obj = "<data><name>%s</name><age>%d</age></data>" %(name, 20)
        self.add_header("Content-Type", "application/xml; charset=UTF-8")
        self.write(obj)

    
#In templates, followings are available
#    escape: alias for tornado.escape.xhtml_escape
#    xhtml_escape: alias for tornado.escape.xhtml_escape
#    url_escape: alias for tornado.escape.url_escape
#    json_encode: alias for tornado.escape.json_encode
#    squeeze: alias for tornado.escape.squeeze
#    linkify: alias for tornado.escape.linkify
#    datetime: the Python datetime module
#    handler: the current RequestHandler object
#    request: alias for handler.request
#    current_user: alias for handler.current_user
#    locale: alias for handler.locale
#    _: alias for handler.locale.translate
#    static_url: alias for handler.static_url
#    xsrf_form_html: alias for handler.xsrf_form_html
#    reverse_url: alias for Application.reverse_url
#    All entries from the ui_methods and ui_modules Application settings
#    Any keyword arguments passed to render or render_string
    
# Tornado templates support control statements and expressions. 
# Control statements are surrounded by {% and %}, e.g. {% if len(items) > 2 %}. 
# Expressions are surrounded by {{ and }}, e.g. {{ items[0] }}.

# Control statements more or less map exactly to Python statements. 
# We support if, for, while, and try, all of which are terminated with {% end %}. 
# We also support template inheritance using the extends and block statements

# Expressions can be any Python expression, including function calls. Te
    
class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        #RequestHandler.render_string(template_name: str, **kwargs) -> bytes
        #could have used self.write(html_string) but to support xsrf use below 
        self.render("env_get.html", url=self.reverse_url("myform"))
                   
    def post(self):
        #for list, use RequestHandler.get_body_arguments(name: str, strip: bool = True) -> List[str]
        envp = self.get_body_argument("envp","all").upper()
        env_dict = os.environ
        if os.environ.get(envp, "notfound") != "notfound":
            env_dict = { envp : os.environ.get(envp,"notfound") }        
        self.render("env.html", envs=env_dict)   
        
        
#Login 
#The currently authenticated user is available in every request handler 
#as self.current_user, and in every template as current_user. 
#By default, current_user is None.

#To implement user authentication in your application, 
#you need to override the get_current_user() method in your request handlers 
#to determine the current user based on, e.g., the value of a cookie. 

#Third party authentication
#https://www.tornadoweb.org/en/stable/guide/security.html#third-party-authentication

# RequestHandler.set_secure_cookie(name: str, value: Union[str, bytes], 
#     expires_days: int = 30, version: int = None, **kwargs) -> None
# RequestHandler.get_secure_cookie(name: str, value: str = None, 
#     max_age_days: int = 31, min_version: int = None) => Optional[bytes]

# Note that the expires_days parameter sets the lifetime of the cookie in the browser, 
# but is independent of the max_age_days parameter to get_secure_cookie.
 
# By default, Tornado’s secure cookies expire after 30 days. 
# To change this, use the expires_days keyword argument to set_secure_cookie 
# and the max_age_days argument to get_secure_cookie. 
# These two values are passed separately so that you may 
# e.g. have a cookie that is valid for 30 days for most purposes, 
# but for certain sensitive actions (such as changing billing information) 
# you use a smaller max_age_days when reading the cookie.

def check_auth(username, password):
    return username == 'admin' and password == 'secret'

class SecureBaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class LoginHandler(SecureBaseHandler):
    def get(self):
        self.render("login.html", url=self.application.settings['login_url'])

    def post(self):
        name = self.get_argument("name", None)
        password = self.get_argument("password", None)        
        if check_auth(name, password):
            self.set_secure_cookie("user", name)
            self.redirect(self.get_argument("next", None) or self.reverse_url("secure_site") )
        else:
             self.redirect(self.application.settings['login_url'])

        
# If a request goes to a method with tornado.web.authenticated decorator, 
# and the user is not logged in, they will be redirected to login_url

# If you decorate post() methods with the authenticated decorator, 
# and the user is not logged in, the server will send a 403 response. 
# The @authenticated decorator is simply shorthand for
# if not self.current_user: self.redirect()
# Note, it appends ?next=self.request.uri

class SecureMainHandler(SecureBaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)
        
"""
To use with requests 


import requests

URL = 'http://localhost:8888/login'

client = requests.session()

# Retrieve the CSRF token first
getr = client.get(URL)  # sets cookie
from bs4 import BeautifulSoup
soup = BeautifulSoup(getr.text, 'html.parser')

#if with cookies 
if 'csrftoken' in client.cookies:
    # Django 1.6 and up
    csrftoken = client.cookies['csrftoken']
else:
    # older versions
    csrftoken = client.cookies['csrf']
login_data = dict(username=EMAIL, password=PASSWORD, csrfmiddlewaretoken=csrftoken, next='/')

#if with page meta holds the CSRF token
csrf_token = soup.select_one('meta[name="csrf-token"]')['content']

#if with header 
csrf_token = getr.headers.get('X-Xsrf-Token',None) or getr.headers['X-CSRFToken']

#in our case 
csrftoken = soup.find('input', dict(name='_xsrf'))['value']
#or 
csrftoken = client.cookies['_xsrf']

login_data = dict(name='admin', password='secret', _xsrf=csrftoken )
r = client.post(URL, data=login_data, params=dict(next='/secure'), headers=dict(Referer=URL))

"""
        
##Upload and download 
class UploadPOSTHandler(tornado.web.RequestHandler):
    def initialize(self, upload_path):
        self.upload_path = upload_path
    def get(self):
        self.render("upload.html")
    def post(self):
        try:
            fileinfo = self.request.files['file'][0]
        except:
            self.redirect(self.reverse_url("upload_normal"))
            return
        try:
            with open(os.path.join(self.upload_path, fileinfo["filename"]), 'wb') as fh:
                fh.write(fileinfo['body'])
            logging.info("%s uploaded %s, saved as %s",
                         str(self.request.remote_ip),
                         str(fileinfo['filename']),
                         fileinfo["filename"])
        except IOError as e:
            logging.error("Failed to write file due to IOError %s", str(e))
        
        self.redirect(self.reverse_url("download", fileinfo['filename']))

        
#Download 
class DownloadHandler(tornado.web.RequestHandler):
    def initialize(self, upload_path):
        self.upload_path = upload_path
    async def get(self, filename):
        # chunk size to read
        chunk_size = 1024 * 1024 * 1 # 1 MiB
        mtype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        self.set_header("Content-Disposition", 'attachment; filename="%s"' %(filename,) )
        self.set_header("Content-Type", mtype )        
        with open(os.path.join(self.upload_path,filename), 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                try:
                    self.write(chunk) # write the cunk to response
                    await self.flush() # flush the current chunk to socket
                except tornado.iostream.StreamClosedError:
                    # this means the client has closed the connection
                    # so break the loop
                    break
                finally:
                    # deleting the chunk is very important because 
                    # if many clients are downloading files at the 
                    # same time, the chunks in memory will keep 
                    # increasing and will eat up the RAM
                    del chunk
                    # pause the coroutine so other handlers can run
                    await tornado.gen.sleep(0.000000001) # 1 nanosecond        
        
        
        
#for large file 
MAX_STREAMED_SIZE = 1024 * 1024 * 1024

# Tornado does not currently  support streaming multi-part uploads. 
# This means that uploads you wish to stream must be simple PUTs, 
# instead of a POST that mixes the uploaded data with other form fields like _xsrf. 
# To use XSRF protection in this scenario you must pass the XSRF token via an HTTP header 
# (X-Xsrf-Token/X-CSRFToken) instead of via a form field. 
# Unfortunately this is incompatible with non-javascript web form uploads; 
# you must have a client capable of setting arbitrary HTTP headers


@tornado.web.stream_request_body
class UploadLargePOSTHandler(tornado.web.RequestHandler):
    def initialize(self, upload_path):
        self.bytes_read = 0
        self.upload_path = upload_path
        self.temp_filename = uuid.uuid4().hex
        
    def prepare(self):
        self.request.connection.set_max_body_size(MAX_STREAMED_SIZE)        
        
    #The regular HTTP method (post, put, etc) will be called 
    #after the entire body has been read.    
    def data_received(self, chunk):
        self.bytes_read += len(chunk)
        #store in temp file 
        with open(os.path.join(self.upload_path, self.temp_filename), 'ab') as fw:
            fw.write(chunk)

    def post(self):
        try:
            fileinfo = self.request.files['file'][0]
        except:
            self.redirect(self.reverse_url("upload_large"))
            return
        try:
            #copy from temp file to correct file 
            import shutil
            with open(os.path.join(self.upload_path, filename), 'wb') as fw:
                with open(os.path.join(self.upload_path, self.temp_filename), 'rb') as fr:
                    shutil.copyfileobj(fr, fw) 
            #remove self.temp_filename
            os.rm(os.path.join(self.upload_path, self.temp_filename))
        except IOError as e:
            logging.error("Failed to write file due to IOError %s", str(e))
        
        self.write("OK")
    def get(self):
        self.render("notsupported.html")
        
#DB 
"""
#check for DB lib in aio-libs eg aiopg, aiomysql etc 
#many other libs in aio-libs
#or 
you can turn synchronous calls into asynchronous ones by wrapping 
them in run_in_executor. For example:

async def fetchall_async(conn, query):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, lambda: conn.cursor().execute(query).fetchall())
   
#OR using tornado

async def fetchall_async(conn, query):
    return await tornado.ioloop.IOLoop.current().run_in_executor(
        None, lambda conn, query: conn.cursor().execute(query).fetchall(), conn, query)
    
#Then using 
async def some_task():
    ...
    students = await fetchall_async(conn, "select * from students")
    
    
#For our case, we would use 
$ pip install aiosqlite

"""
import aiosqlite


class NoResult(Exception):
    pass
        
class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db
    def row_to_obj(self, row, cur):
        obj = tornado.util.ObjectDict()
        for val, desc in zip(row, cur.description):
            obj[desc[0]] = val #first one is name 
        return obj        
        
    async def query(self, stmt, *args):
        async with aiosqlite.connect(self.db) as db:
            db.row_factory = aiosqlite.Row 
            async with db.execute(stmt, args) as cur:
                #in python3.6, https://www.python.org/dev/peps/pep-0530/#implementation
                #return [self.row_to_obj(row, cur) async for row in cur.fetchall()]
                return [self.row_to_obj(row, cur) for row in await cur.fetchall()]
                
    async def queryone(self, stmt, *args):
        results = await self.query(stmt, *args)
        if len(results) >= 0 :
            return results[0] 
        else:
            raise NoResult("No result")
            
async def maybe_create_tables(dbpath):   
    async with aiosqlite.connect(dbpath) as db:
        try:
            async with db.execute("SELECT COUNT(*) FROM people LIMIT 1") as cursor:
                await cursor.fetchone()
        except :                
            await db.execute("""create table if not exists people (name string, age int)""")
            await db.execute("""insert into people values(?,?) """, ('xyz',20))
            await db.execute("""insert into people values(?,?) """, ('abc',20))
            await db.commit()

        
class DBHandler(BaseHandler):
    async def get(self, name=None):
        try:
            if not name:
                people = await self.query(
                    "SELECT * FROM people"
                )
                obj = {'all': people}
            else:
                entries = await self.queryone(
                    "SELECT * FROM people where name=?", name
                )
                #find age , each row is dict because of db.row_factory = aiosqlite.Row
                obj = {'name': name, 'age': entries['age']}
        except Exception as ex:
            obj={'message': str(ex)}
        self.write(obj) #only accepts bytes, unicode, and dict objects
        
"""
Urls 
http://localhost:8888/
http://localhost:8888/static/hello.html 
http://localhost:8888/some.txt
http://localhost:8888/main 
http://localhost:8888/story/2

http://localhost:8888/helloj/das
http://localhost:8888/helloj/ with json  "{\"name\": \"dasn\"}"
http://localhost:8888/helloj/
http://localhost:8888/helloj/?name=dasq

http://localhost:8888/hellox/das

http://localhost:8888/env

http://localhost:8888/secure
http://localhost:8888/login   with admin/secret

http://localhost:8888/upload
http://localhost:8888/upload_large
http://localhost:8888/download/data.jpg

http://localhost:8888/db/
http://localhost:8888/db/abc 

"""



def make_app(dbpath):
    settings = {
    #This setting will automatically make all requests that start with /static/ serve from that static directory
    #automatically serve /robots.txt and /favicon.ico from the static directory (even though they don’t start with the /static/ prefix)
    #To use /static/images/logo.png, use <img src="{{ static_url("images/logo.png") }}"/></div>,
    # It uses cacheing , to disable, use static_hash_cache=False
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": True,
    #templates 
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),
    #file upload 
    "upload_path": os.path.join(os.path.dirname(__file__), "uploads"),
    }
    return tornado.web.Application([
        (r"/", MainHandler),
        #static file can be served directly by below with url /some.txt , note below is regex group
        (r"/(some\.txt)", tornado.web.StaticFileHandler, dict(path=settings['static_path']) ),
        
        tornado.web.url(r"/main", MainHandler2),
        #db goes to StoryHandler.__init__ 
        #regex group goes to StoryHandler.get(story_id)
        tornado.web.url(r"/story/([0-9]+)", StoryHandler, dict(db=None), name="story"),
        
        #handlinh json
        (r"/helloj/(\w*)", JsonHandler),
        #XML
        (r"/hellox/(\w+)", XMLHandler),
        #form 
        tornado.web.url(r"/env", MyFormHandler, name="myform"),
        
        #login 
        (r"/login", LoginHandler),
        tornado.web.url(r"/secure", SecureMainHandler, name="secure_site"),
        
        #upload 
        tornado.web.url(r"/upload", UploadPOSTHandler, dict(upload_path=settings['upload_path']), name="upload_normal"),
        tornado.web.url(r"/upload_large", UploadLargePOSTHandler, dict(upload_path=settings['upload_path']), name="upload_large"),
        tornado.web.url(r"/download/(.+)", DownloadHandler, dict(upload_path=settings['upload_path']), name="download"),
        
        #db 
        tornado.web.url(r"/db/(.*)", DBHandler, dict(db=dbpath), name="db"),
        
    ],    **settings
    )
    
    
#for debug true , it has to be module 
#debug=True) #autoreload=True,compiled_template_cache=False:,static_hash_cache=False,serve_traceback=True:
#does not work as intended in windows 

if __name__ == "__main__":
    ## to enable logging , start with 'python basic.py --logging=info'
    # check other options eg log file prefix, rotation etc 
    #https://www.tornadoweb.org/en/stable/_modules/tornado/log.html#LogFormatter
    tornado.options.parse_command_line()
    dbpath = "tornado.db"
    application =  make_app(dbpath)
    application.listen(8888)
    
    # In Python, signals are always handled by the main thread. 
    # If the IOLoop is run from the main thread, it will block it when server is idle 
    # and waiting for IO. 
    # As a result, all signals will be pending on the thread to wake up. 
    # So, press  crtl+c and then refresh browser or install below callback 
    tornado.ioloop.PeriodicCallback( lambda:None, 1000 , jitter=0.1).start()   
    #add db creation in IOLoop
    tornado.ioloop.IOLoop.current().spawn_callback(maybe_create_tables, dbpath)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:  #for crtl+c 
        logging.getLogger("tornado.general").info("Exiting")
        tornado.ioloop.IOLoop.current().stop()

    
        
"""
#using asyncio (arguments are like requests)

aiohttp.ClientSession(cookies=None, headers=None, read_timeout=None, conn_timeout=None)
    request(method, url, *, params=None, data=None, json=None, cookies=None, 
            headers=None,proxy=None, proxy_auth=None, timeout=sentinel, 
            ssl=None, proxy_headers=None)
        cookies, headers are dict 
        params ,for query params 
        data , for form data 
        json , any python object (then dont use data)
        proxy  ,URL 
        proxy_auth ,aiohttp.BasicAuth(login, password='', encoding='latin1')
        ssl=False , dont use certificates verification 
        ssl=ssl_context, with certs, https://docs.python.org/3/library/ssl.html#ssl.SSLContext 
        timeout , If float is passed it is a total timeout or aiohttp.ClientTimeout(*, total=None, connect=None, sock_connect, sock_read=None)
Response 
    cookies
    headers
    status 
    content_type
    coroutine text()
    coroutine json()
    coroutine read()
    content aiohttp.StreamReader
    
    
#code 
import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        print(html)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(url="http://localhost:8888/"))



"""
#forms 


#->file:base.html:
<html>
<body>
<table border="1">
<tr><th>Key</th><th>Value</th></tr>
{% if envs.items() %}  
{% for key,value in envs.items() %}
{% block row %}
<tr>
<td>{{ key }}</td>
<td>{{ value }}</td>
</tr>
{% end %}
{% end %}
{% end %}
</table>
</body>
</html>



#->file:env.html:
{% extends "base.html" %}


{% block row %}
<tr style="background-color:lightgrey;">
<td style="color:red; font-style: bold;">{{ key }}</td>
<td>{{ value }}</td>
</tr>
{% end %}


#->file:env_get.html:
<html><body><form  action="{{url}}" method="POST">
{% module xsrf_form_html() %}
Put env variable:
<input type="text" name="envp" value="ALL">
<input type="submit" value="Submit">
</form></body></html>


#->file:login.html:
<html><body><form  action="{{url}}" method="POST">
{% module xsrf_form_html() %}
User Name: <input type="text" name="name"> <br/>
Password:<input type=password name="password">
<input type="submit" value="Sign in">
</form></body></html>


#->file:upload.html:
<!doctype html>
<title>Upload new File</title>
<body>
<h1>Upload new File</h1>
<form method="post" enctype="multipart/form-data">
{% module xsrf_form_html() %}
<input type=file name="file" />
<input type=submit value="Upload" />
</form>
</body></html>


###Tornado-*** Introduction 
Tornado is different from most Python web frameworks. It is not based on WSGI, 
and it is typically run with only one thread per process.

While some support of WSGI is available in the tornado.wsgi module, 
it is not a focus of development and most applications should be written 
to use Tornado's own interfaces (such as tornado.web) directly instead of using WSGI.

In general, Tornado code is not thread-safe. 
The only method in Tornado that is safe to call from other threads is IOLoop.add_callback
You can also use IOLoop.run_in_executor to asynchronously run a blocking
function on another thread, but note that the function passed to run_in_executor should avoid referencing any
Tornado objects. run_in_executor is the recommended way to interact with blocking code.

Tornado is integrated with the standard library asyncio module and shares the same event loop (by default since
Tornado 5.0). In general, libraries designed for use with asyncio can be mixed freely with Tornado.

On Windows, Tornado requires the WindowsSelectorEventLoop. This is the default in Python 3.7
and older, but Python 3.8 defaults to an event loop that is not compatible with Tornado. Applications
that use Tornado on Windows with Python 3.8 must call 
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) 
at the beginning of their main file/function.


###Tornado-*** Using Tornado


#Here is a sample synchronous function:

from tornado.httpclient import HTTPClient

def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body

#rewritten asynchronously as a native coroutine:

from tornado.httpclient import AsyncHTTPClient

async def asynchronous_fetch(url):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(url)
    return response.body

#Or for compatibility with older versions of Python, using the tornado.gen module:

from tornado.httpclient import AsyncHTTPClient
from tornado import gen

@gen.coroutine
def async_fetch_gen(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)

#Coroutines do internally is something like this:
from tornado.concurrent import Future

def async_fetch_manual(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    def on_fetch(f):
        my_future.set_result(f.result().body)
    fetch_future.add_done_callback(on_fetch)
    return my_future
    

##Native vs decorated coroutines


# Decorated:                                # Native:

# Normal function declaration
# with decorator                            # "async def" keywords
@gen.coroutine
def a():                                    async def a():
    # "yield" all async funcs                   # "await" all async funcs
    b = yield c()                               b = await c()
    # "return" and "yield"
    # cannot be mixed in
    # Python 2, so raise a
    # special exception.                         # Return normally
    raise gen.Return(b)                          return b

    
· Native coroutines:
  ­ are generally faster.
  ­ can use async for and async with statements which make some patterns much simpler.
  ­ do not run at all unless you await or yield them. 
    So use with await inside another coroutine or pass it in spawn_callback
    Decorated coroutines can start running "in the
    background" as soon as they are called. Note that for both kinds of coroutines it is important to use
    await or yield so that any exceptions have somewhere to go.
     
     
#How to call a coroutine


async def divide(x, y):
    return x / y

def bad_call():
    # This should raise a ZeroDivisionError, but it won't because
    # the coroutine is called incorrectly.
    divide(1, 0)

#In nearly all cases, any function that calls a coroutine must be a coroutine itself, 
#and use the await or yield keyword in the call. 

async def good_call():
    # await will unwrap the object returned by divide() and raise
    # the exception.
    await divide(1, 0)


##to "fire and forget" a coroutine without waiting for its result
tornado.ioloop.IOLoop.current().spawn_callback(divide, 1, 0)
#same as 
IOLoop.add_callback(callback: Callable, *args, **kwargs) -> None

##at the top level of a program, if the IOLoop is not yet running, 
#you can start the IOLoop, run the coroutine, and then stop the IOLoop with the IOLoop.run_sync method. 
#This is often used to start the main function of a batch-oriented program:

# run_sync() doesn't take arguments, so we must wrap the  call in a lambda.
tornado.ioloop.IOLoop.current().run_sync(lambda: divide(1, 0))


##Calling blocking functions
IOLoop.run_in_executor(executor: Optional[concurrent.futures._base.Executor], func: Callable[[...], _T], *args) -> Awaitable[_T]
    Runs a function in a concurrent.futures.Executor. If executor is None, the IO loop’s default executor will be used.
    Use functools.partial to pass keyword arguments to func.
IOLoop.set_default_executor(executor: concurrent.futures._base.Executor) -> None
    Sets the default executor to use with run_in_executor().

#IOLoop.run_in_executor , which returns Futures that are compatible with coroutines:

async def call_blocking(*args):
    await tornado.ioloop.IOLoop.current().run_in_executor(None, blocking_func, *args)

tornado.ioloop.IOLoop.current().spawn_callback(call_blocking, *args)


##Running many coroutines in Parallel
#The multi function(similar to asyncio.loop.gather) accepts lists and dicts whose values are Futures, 
#and waits for all of those Futures in parallel:

from tornado.gen import multi

async def parallel_fetch(url1, url2):
    resp1, resp2 = await multi([http_client.fetch(url1),
                                http_client.fetch(url2)])

async def parallel_fetch_many(urls):
    responses = await multi ([http_client.fetch(url) for url in urls])
    # responses is a list of HTTPResponses in the same order

async def parallel_fetch_dict(urls):
    responses = await multi({url: http_client.fetch(url)
                             for url in urls})
    # responses is a dict {url: HTTPResponse}

    
    
    
##Interleaving
#To save a Future instead of yielding it immediately, 
#so you can start another operation before waiting.

from tornado.gen import convert_yielded

async def get(self):
    # convert_yielded() starts the native coroutine in the background.
    # This is equivalent to asyncio.ensure_future() (both work in Tornado).
    fetch_future = convert_yielded(self.fetch_next_chunk())
    while True:
        chunk = await fetch_future
        if chunk is None: break
        self.write(chunk)
        fetch_future = convert_yielded(self.fetch_next_chunk())
        await self.flush()



##Looping
#In native coroutines, async for can be used. 

async with aiosqlite.connect(...) as db:
    async with db.execute('SELECT * FROM some_table') as cursor:
        async for row in cursor:
            print(row)


##Running in the background
#PeriodicCallback is not normally used within coroutines(but used with IOLoop)
#Instead, a coroutine can contain a while True:  and use tornado.gen.sleep:

async def minute_loop():
    while True:
        await do_something()
        await gen.sleep(60)

IOLoop.current().spawn_callback(minute_loop)

#the previous loop runs every 60+N seconds,
where N is the running time of do_something(). 
#To run exactly every 60 seconds, use the interleaving pattern 

async def minute_loop2():
    while True:
        nxt = gen.sleep(60)           # Start the clock.
        await do_something()          # Run while the clock is ticking.
        await nxt                     # Wait for the timer to run out.

        
##Schedule a function         
IOLoop.add_callback_from_signal(callback: Callable, *args, **kwargs) -> None
    Calls the given callback on the next I/O loop iteration.
    Safe for use from a Python signal handler; should not be used otherwise.
    
IOLoop.add_future(future: Union[tornado.concurrent.Future[_T], concurrent.futures.Future[_T]], callback: Callable[[Future[_T]], None]) -> None
    Schedules a callback on the IOLoop when the given Future is finished.
    The callback is invoked with one argument, the Future.(has .result())

IOLoop.add_timeout(deadline: Union[float, datetime.timedelta], callback: Callable[[...], None], *args, **kwargs) -> object
    Runs the callback at the time deadline from the I/O loop.
    Returns an opaque handle that may be passed to remove_timeout to cancel.
IOLoop.remove_timeout(timeout: object) -> None
    Cancels a pending timeout.

IOLoop.time() -> float
    Returns the current time according to the IOLoop’s clock.
    The return value is a floating-point number relative to an unspecified time in the past.
IOLoop.call_later(delay: float, callback: Callable[[...], None], *args, **kwargs) -> object
    Runs the callback after delay seconds have passed.
IOLoop.call_at(when: float, callback: Callable[[...], None], *args, **kwargs) -> object
    Runs the callback at the absolute time designated by when.
    when must be a number using the same reference point as IOLoop.time.
    Returns an opaque handle that may be passed to remove_timeout to cancel. 
    Note that unlike the asyncio method of the same name, the returned object does not have a cancel() method.

class tornado.ioloop.PeriodicCallback(callback: Callable[[], None], callback_time: float, jitter: float = 0)
    Schedules the given callback to be called periodically.
    The callback is called every callback_time milliseconds. 
    Note that the timeout is given in milliseconds, 
    while most other time-related functions in Tornado use seconds.
    If jitter is specified, each callback time will be randomly selected 
    within a window of jitter * callback_time milliseconds. 
    Jitter can be used to reduce alignment of events with similar periods. 
    A jitter of 0.1 means allowing a 10% variation in callback time. 
    start() -> None
        Starts the timer.
    stop() -> None
        Stops the timer.
    is_running() -> bool
        Returns True if this PeriodicCallback has been started.

#One example- webspider 
import time, sys 
from datetime import timedelta

from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag

from tornado import gen, httpclient, ioloop, queues

base_url = sys.argv[1] if len(sys.argv) >=2 else "http://www.tornadoweb.org/en/stable/"
concurrency = int(sys.argv[1]) if len(sys.argv) >=3 else 10

#Returned links have had the fragment after `#` removed,
def remove_fragment(url):
    pure_url, frag = urldefrag(url)
    return pure_url


def get_links(html):
    class URLSeeker(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.urls = []
        def handle_starttag(self, tag, attrs):
            href = dict(attrs).get("href")
            if href and tag == "a":
                self.urls.append(href)
    url_seeker = URLSeeker()
    url_seeker.feed(html)
    return url_seeker.urls
    
async def get_links_from_url(url):
    """Download the page at `url` and parse it for links
    """
    response = await httpclient.AsyncHTTPClient().fetch(url)
    print("fetched %s" % url)
    html = response.body.decode(errors="ignore")
    #url have been made  absolute
    return [urljoin(url, remove_fragment(new_url)) for new_url in get_links(html)]

async def main():
    q = queues.Queue()
    start = time.time()
    fetching, fetched, dead = set(), set(), set()

    async def fetch_url(current_url):
        if current_url in fetching:
            return
        print("fetching %s" % current_url)
        fetching.add(current_url)
        urls = await get_links_from_url(current_url)
        fetched.add(current_url)
        for new_url in urls:
            # Only follow links beneath the base URL
            if new_url.startswith(base_url):
                await q.put(new_url)

    async def worker():
        async for url in q:
            if url is None:
                return
            try:
                await fetch_url(url)
            except Exception as e:
                print("Exception: %s %s" % (e, url))
                dead.add(url)
            finally:
                q.task_done()

    await q.put(base_url)

    # Start workers, then wait for the work queue to be empty.
    workers = gen.multi([worker() for _ in range(concurrency)])
    await q.join(timeout=timedelta(seconds=300))
    assert fetching == (fetched | dead)
    print("Done in %d seconds, fetched %s URLs." % (time.time() - start, len(fetched)))
    print("Unable to fetch %s URLS." % len(dead))

    # Signal all the workers to exit.
    for _ in range(concurrency):
        await q.put(None)
    await workers


if __name__ == "__main__":
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)



###Tornado-Error Handling

The default error page includes a stack trace in debug mode 
and a one-line description of the error (e.g. "500: Internal Server Error") otherwise. 

To produce a custom error page, override RequestHandler.write_error(status_code: int, **kwargs) -> None. 
call write, render, set_header, etc to produce output as usual.
If this error was caused by an uncaught exception (including HTTPError), 
an exc_info triple will be available as kwargs["exc_info"]. 
Note that this exception may not be the 'current' exception for purposes of methods 
like sys.exc_info() or traceback.format_exc.

It is also possible to generate an error page from regular handler methods 
instead of write_error by calling set_status, writing a response, and returning. 
RequestHandler.set_status(status_code: int, reason: str = None) 
#Example 
if self.check_etag_header():
    self.set_status(304)
    return

The special exception tornado.web.Finish may be raised to terminate the handler 
without calling write_error in situations where simply returning is not convenient.
#Example 
if self.current_user is None:
    self.set_status(401)
    self.set_header('WWW-Authenticate', 'Basic realm="something"')
    raise Finish()


For 404 errors, use the default_handler_class Application setting . 
This handler should override prepare instead of a more specific method like get() 
so it works with any HTTP method. 
It should produce itserror page : either by raising a HTTPError(404) 
and overriding write_error, or calling self.set_status(404) 
and producing the response directly in prepare().


###Tornado-Permanent Redirection


app = tornado.web.Application([
    url(r"/app", tornado.web.RedirectHandler,
        dict(url="http://itunes.apple.com/my-app-id")),
    ])

RedirectHandler also supports regular expression substitutions. 
The following rule redirects all requests beginning with /pictures/ to the prefix /photos/ instead:

app = tornado.web.Application([
    url(r"/photos/(.*)", MyPhotoHandler),
    url(r"/pictures/(.*)", tornado.web.RedirectHandler,
        dict(url=r"/photos/{0}")),
    ])

Unlike RequestHandler.redirect, RedirectHandler uses permanent redirects by default. This is because
the routing table does not change at runtime and is presumed to be permanent, while redirects found in handlers are
likely to be the result of other logic that may change. 
To send a temporary redirect with a RedirectHandler , add permanent=False to the RedirectHandler initialization arguments.


###Tornado-Asynchronous handlers
Certain handler methods (including prepare() and the HTTP verb methods get()/post()/etc)
may be overridden as coroutines to make the handler asynchronous.

For example, here is a simple handler using a coroutine:

class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        response = await http.fetch("http://friendfeed-api.com/v2/feed/bret")
        json = tornado.escape.json_decode(response.body)
        self.write("Fetched " + str(len(json["entries"])) + " entries "
                   "from the FriendFeed API")


For a more advanced asynchronous example, take a look at the chat example application, 
which implements an AJAX chat room using long polling. 
Users of long polling may want to override on_connection_close() to clean up
after the client closes the connection 

###Tornado-Internationalization

If RequestHandler.get_user_locale returns None, we fall back on the Accept-Language header.

The tornado.locale module supports loading translations in two formats: 
the .mo format used by gettext and related tools, and a simple .csv format. 

An application will generally call either tornado.locale.load_translations 
or tornado.locale.load_gettext_translations once at startup; 

tornado.locale.load_translations(directory: str, encoding: str = None) -> None
    Loads translations from CSV files in a directory.
    Translations are strings with optional Python-style named placeholders 
    (e.g., My name is %(name)s) and their associated translations.
    The directory should have translation files of the form LOCALE.csv, e.g. es_GT.csv. 
    The CSV files should have two or three columns: string, translation,and an optional plural indicator. 
    Plural indicators should be one of 'plural' or 'singular'. 
    A given string can have both singular and plural forms. 
    There should be two rows in the CSV file for a string, 
    one with plural indicator 'singular', and one 'plural'. 
    For strings with no verbs that would change on translation, 
    simply use 'unknown' or the empty string (or don’t include the column at all).
    The file is read using the csv module in the default 'excel' dialect. 
    In this format there should not be spaces after the commas.
    If no encoding parameter is given, the encoding will be detected automatically 
    (among UTF-8 and UTF-16) if the file contains a byte-order marker (BOM), 
    defaulting to UTF-8 if no BOM is present.
    #file:es_LA.csv:
    "I love you","Te amo"
    "%(name)s liked this","A %(name)s les gustó esto","plural"
    "%(name)s liked this","A %(name)s le gustó esto","singular"
    
tornado.locale.load_gettext_translations(directory: str, domain: str) -> None
    https://www.gnu.org/software/gettext/manual/html_node/xgettext-Invocation.html
    Loads translations from gettext’s locale tree
    Locale tree is similar to system’s /usr/share/locale, like:
    {directory}/{lang}/LC_MESSAGES/{domain}.mo
    Three steps are required to have your app translated:
        Generate POT translation file:(--keyword means look for _ to pick for po file)
        Replace relevant strings in file1.py file2.html with _()
        eg 
            _("Translate this string")
            #singular/plural form 
            _("A person liked this", "%(num)d people liked this", len(people)) % {"num": len(people)}
        #then generate 
        xgettext --language=Python --keyword=_:1,2 -d mydomain file1.py file2.html 
        #or python equivalent 
        $ python  C:\Python35\Tools\i18n\pygettext.py --keyword=_:1,2 -d mydomain file1.py file2.html 
        Merge against existing POT file:
        msgmerge old.po mydomain.po > new.po
        Edit and compile new.po using Poedit.exe from https://poedit.net/ 
        OR Compile:
        msgfmt new.po -o {directory}/pt_BR/LC_MESSAGES/mydomain.mo
        #or
        $ python  C:\Python35\Tools\i18n\msgfmt.py new.po -o {directory}/pt_BR/LC_MESSAGES/mydomain.mo
        #check https://inventwithpython.com/blog/2014/12/20/translate-your-python-3-program-with-the-gettext-module/
        
        
tornado.locale.get_supported_locales() -> Iterable[str]
    Returns a list of all the supported locale codes.
    
class tornado.locale.Locale(code: str)
    Object representing a locale.
    After calling one of load_translations or load_gettext_translations, 
    call get or get_closest to get a Locale object.
    classmethod get_closest(*locale_codes) -> tornado.locale.Locale
        Returns the closest match for the given locale code.
    classmethod get(code: str) -> tornado.locale.Locale
        Returns the Locale for the given locale code.
        If it is not supported, we raise an exception.
    translate(message: str, plural_message: str = None, count: int = None) -> str
        Returns the translation for the given message for this locale.
        If plural_message is given, you must also provide count. 
        We return plural_message when count != 1, and we return the singular form 
        for the given message when count == 1.
    format_date(date: Union[int, float, datetime.datetime], gmt_offset: int = 0, relative: bool = True, shorter: bool = False, full_format: bool = False) -> str
        Formats the given date (which should be GMT).
        By default, we return a relative time (e.g., '2 minutes ago'). 
        You can return an absolute date string with relative=False.
        You can force a full format date ('July 10, 1980') with full_format=True.
        This method is primarily intended for dates in the past. 
        For dates in the future, we fall back to full format.
    format_day(date: datetime.datetime, gmt_offset: int = 0, dow: bool = True) -> bool
        Formats the given date as a day of week.
        Example: 'Monday, January 22'. You can remove the day of week with dow=False.
    list(parts: Any) -> str
        Returns a comma-separated list for the given list of parts.
        The format is, e.g., 'A, B and C', 'A and B' or just 'A' for lists of size 1.
    friendly_number(value: int) -> str
        Returns a comma-separated number for the given integer.

You can get the list of supported locales in your application with tornado.locale.get_supported_locales(). 
The user's locale is chosen to be the closest match based on the supported locales. 
For example, if the user's locale is es_GT, and the es locale is supported, s
elf.locale will be es for that request. 
We fall back on en_US if no close match can be found.

The locale of the current user (whether they are logged in or not) is always available as self.locale in the request
handler and as locale in templates. The name of the locale (e.g., en_US) is available as locale.name, and
you can translate strings with the Locale.translate method. 
user_locale = tornado.locale.get("es_LA")
print(user_locale.translate("Sign out"))

The most common pattern for translations is to use Python named placeholders 
for variables (the %(num)d in the example above) since placeholders can move around on translation.

<html>
   <head>
      <title>FriendFeed - {{ _("Sign in") }}</title>
   </head>
   <body>
     <form action="{{ request.path }}" method="post">
       <div>{{ _("Username") }} <input type="text" name="username"/></div>
       <div>{{ _("Password") }} <input type="password" name="password"/></div>
       <div><input type="submit" value="{{ _("Sign in") }}"/></div>
       {% module xsrf_form_html() %}
     </form>
   </body>
 </html>

By default, we detect the user locale using the Accept-Language header sent by the user's browser. 
We choose en_US if we can't find an appropriate Accept-Language value. 
If you let user's set their locale as a preference,you can override this default locale 
selection by overriding RequestHandler.get_user_locale:

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.backend.get_user_by_id(user_id)

     def get_user_locale(self):
         if "locale" not in self.current_user.prefs:
             # Use the Accept-Language header
             return None
         return self.current_user.prefs["locale"]




###Tornado-UI modules
Tornado supports UI modules to make it easy to support standard, 
reusable UI widgets across your application. 
UI modules are like special function calls to render components of your page, 
and they can come packaged with their own CSS and JavaScript.

For example, if you are implementing a blog, 
and you want to have blog entries appear on both the blog home page and on each blog entry page, 
you can make an Entry module to render them on both pages. 

First, create a Python module for your UI modules, 
#uimodules.py:
#Modules can include custom CSS and JavaScript functions by overriding  
#the   embedded_css, embedded_javascript, javascript_files, or css_files methods:

class Entry(tornado.web.UIModule):
    def embedded_css(self):
        return ".entry { margin-bottom: 1em; }"

     def render(self, entry, show_comments=False):
         return self.render_string(
             "module-entry.html", show_comments=show_comments)

#Tell Tornado to use uimodules.py 
#using the ui_modules setting in your application:
#convert(entry) converts to entry object with .id, .published, .html, .slug, .title 
from . import uimodules

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        entries = list(self.db.execute("SELECT * FROM entries ORDER BY date DESC").fetchall())
        self.render("home.html", entries=[convert(entry) for entry in entries])

class EntryHandler(tornado.web.RequestHandler):
    def get(self, entry_id):
        entry = self.db.execute("SELECT * FROM entries WHERE id = %s", entry_id).fetchone()
        if not entry: raise tornado.web.HTTPError(404)
        self.render("entry.html", entry=convert(entry))

settings = {
    "ui_modules": uimodules,
}
application = tornado.web.Application([
    (r"/", HomeHandler),
    (r"/entry/([0-9]+)", EntryHandler),
], **settings)

#Within a template, you can call a module with the {% module %} statement. 
#home.html:

{% for entry in entries %}
  {% module Entry(entry) %}
{% end %}

#entry.html:
{% module Entry(entry, show_comments=True) %}

#Then module-entry.html
<div class="entry">
  <h1><a href="/entry/{{ entry.slug }}">{{ entry.title }}</a></h1>
  <div class="date">{{ locale.format_date(entry.published, full_format=True, shorter=True) }}</div>
  <div class="body">{% raw entry.html %}</div>
  {% if current_user %}
    <div class="admin"><a href="/compose?id={{ entry.id }}">{{ _("Edit this post") }}</a></div>
  {% end %}
</div>


##Details 
Module CSS and JavaScript will be included once no matter 
how many times a module is used on a page. 
CSS is always included in the <head> of the page, 
and JavaScript is always included just before the </body> tag at the endof the page.

When additional Python code is not required, a template file itself may be used as a module. 
For example, the preceding example could be rewritten to put the following in module-entry.html:

{{ set_resources(embedded_css=".entry { margin-bottom: 1em; }") }}
<!-- more template html... -->

This revised template module would be invoked with:
{% module Template("module-entry.html", show_comments=True) %}

The set_resources function is only available in templates invoked via 
{% module Template(...) %}. 
Unlike the {% include ... %} directive, template modules have a distinct namespace from their containing
template - they can only see the global template namespace and their own keyword arguments.


###Tornado-Third party authentication
The tornado.auth module implements the authentication and authorization protocols 
for a number of the most popular sites on the web, including Google/Gmail, Facebook, Twitter, and FriendFeed. 

The module includes methods to log users in via these sites 
and, where applicable, methods to authorize access to the service so you can, e.g.,
download a user's address book or publish a Twitter message on their behalf.

Here is an example handler that uses Google for authentication, 
saving the Google credentials in a cookie for later access:

class GoogleOAuth2LoginHandler(tornado.web.RequestHandler,
                               tornado.auth.GoogleOAuth2Mixin):
    async def get(self):
        if self.get_argument('code', False):
            user = await self.get_authenticated_user(
                redirect_uri='http://your.site.com/auth/google',
                code=self.get_argument('code'))
            # Save the user with e.g. set_secure_cookie
        else:
            await self.authorize_redirect(
                redirect_uri='http://your.site.com/auth/google',
                client_id=self.settings['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})



###Tornado-Cross-site request forgery protection

settings = {
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": True,
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
], **settings)

If xsrf_cookies is set, the Tornado web application will set the _xsrf cookie 
for all users and reject all POST, PUT, and DELETE requests 
that do not contain a correct _xsrf value. 

<form action="/new_message" method="post">
  {% module xsrf_form_html() %}
  <input type="text" name="message"/>
  <input type="submit" value="Post"/>
</form>

If you submit AJAX POST requests, you will also need to instrument 
your JavaScript to include the _xsrf value with each request.
This is the jQuery function we use at FriendFeed for AJAX POST requests 
that automatically adds the _xsrf value to all requests:

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

jQuery.postJSON = function(url, args, callback) {
    args._xsrf = getCookie("_xsrf");
    $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
         success: function(response) {
         callback(eval("(" + response + ")"));
    }});
};

For PUT and DELETE requests (as well as POST requests that do not use form-encoded arguments), the XSRF
token may also be passed via an HTTP header named X-XSRFToken. 
The XSRF cookie is normally set when xsrf_form_html is used, 
but in a pure-Javascript application that does not use any regular forms 
you may need to access self.xsrf_token manually 
(just reading the property is enough to set the cookie as a side effect).

If you need to customize XSRF behavior on a per-handler basis, 
you can override RequestHandler.check_xsrf_cookie(). 
For example, if you have an API whose authentication does not use cookies, 
you may want to disable XSRF protection by making check_xsrf_cookie() do nothing. 
However, if you support both cookie and non-cookie-based authentication, 
it is important that XSRF protection be used whenever the current request is authenticated with a cookie.


###Tornado-DNS Rebinding
DNS rebinding is an attack that can bypass the same-origin policy 
and allow external sites to access resources on private networks. 
This attack involves a DNS name (with a short TTL) that alternates between returning an IP address
controlled by the attacker and one controlled by the victim 
(often a guessable private IP address such as 127.0.0.1 or 192.168.1.1).

Applications that use TLS are not vulnerable to this attack (because the browser will display certificate mismatch
warnings that block automated access to the target site).

Applications that cannot use TLS and rely on network-level access controls (for example, assuming that a server
on 127.0.0.1 can only be accessed by the local machine) 
should guard against DNS rebinding by validating the Host HTTP header. 

This means passing a restrictive hostname pattern to either a HostMatches router 
or the first argument of Application.add_handlers:

# BAD: uses a default host pattern of r'.*'
app = Application([('/foo', FooHandler)])

# GOOD: only matches localhost or its ip address.
app = Application()
app.add_handlers(r'(localhost|127\.0\.0\.1)',
                 [('/foo', FooHandler)])

# GOOD: same as previous example using tornado.routing.
app = Application([
    (HostMatches(r'(localhost|127\.0\.0\.1)'),
        [('/foo', FooHandler)]),
    ])

In addition, the default_host argument to Application and the DefaultHostMatches router must not be
used in applications that may be vulnerable to DNS rebinding, 
because it has a similar effect to a wildcard host pattern.


###Tornado-Running and deploying in multihost (only in unix)

Due to the Python GIL (Global Interpreter Lock), it is necessary to run multiple Python processes to take full advantage
of multi-CPU machines. Typically it is best to run one process per CPU.

Tornado includes a built-in multi-process mode to start several processes at once. This requires a slight alteration to
the standard main function:

def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8888)
    server.start(0) # forks one process per cpu
    IOLoop.current().start()

This is the easiest way to start multiple processes and have them all share the same port, although it has some limita-
tions. First, each child process will have its own IOLoop, so it is important that nothing touches the global IOLoop
instance (even indirectly) before the fork. 
Second, it is difficult to do zero-downtime updates in this model. 
Finally, since all the processes share the same port it is more difficult to monitor them individually.


###Tornado-Running behind a load balancer

When running behind a load balancer like nginx, it is recommended to pass xheaders=True 
to the HTTPServer constructor. 
This will tell Tornado to use headers like X-Real-IP 
to get the users IP address instead of attributing all traffic to the balancer's IP address.

This is a barebones nginx config file 
It assumes nginx and the Tornado servers are running on the same machine, 
and the four Tornado servers are running on ports 8000 - 8003:

user nginx;
worker_processes 1;

error_log /var/log/nginx/error.log;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
}

http {
    # Enumerate all the Tornado servers here
    upstream frontends {
        server 127.0.0.1:8000;
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
        server 127.0.0.1:8003;
    }

     include /etc/nginx/mime.types;
     default_type application/octet-stream;

     access_log /var/log/nginx/access.log;

     keepalive_timeout 65;
     proxy_read_timeout 200;
     sendfile on;
     tcp_nopush on;
     tcp_nodelay on;
     gzip on;
     gzip_min_length 1000;
     gzip_proxied any;
     gzip_types text/plain text/html text/css text/xml
                application/x-javascript application/xml
                application/atom+xml text/javascript;

     # Only retry if there was a communication error, not a timeout
     # on the Tornado server (to avoid propagating "queries of death"
     # to all frontends)
     proxy_next_upstream error;

     server {
         listen 80;

          # Allow file uploads
          client_max_body_size 50M;

          location ^~ /static/ {
              root /var/www;
              if ($query_string) {
                  expires max;
              }
          }
          location = /favicon.ico {
              rewrite (.*) /static/favicon.ico;
          }
          location = /robots.txt {
              rewrite (.*) /static/robots.txt;
          }

          location / {
              proxy_pass_header Server;
              proxy_set_header Host $http_host;
              proxy_redirect off;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Scheme $scheme;
              proxy_pass http://frontends;
          }
     }
}



###Tornado-Template Syntax Reference

Template expressions are surrounded by double curly braces: {{ ... }}. 
The contents may be any python expression, 
which will be escaped according to the current autoescape setting 
and inserted into the output. 

Other template directives use {% %}.

To comment out a section so that it is omitted from the output, surround it with {# ... #}.

These tags may be escaped as {{!, {%!, and {#! 
if you need to include a literal {{, {%, or {# in the output.


{% apply *function* %}...{% end %} 
    Applies a function to the output of all template code between
    apply and end:
      {% apply linkify %}{{name}} said: {{message}}{% end %}

      Note that as an implementation detail apply blocks are implemented as nested functions and thus may interact
      strangely with variables set via {% set %}, or the use of {% break %} or {% continue %} within
      loops.
{% autoescape *function* %} 
    Sets the autoescape mode for the current file. This does not affect other
    files, even those referenced by {% include %}. Note that autoescaping can also be configured globally, at
    the Application or Loader .:
      {% autoescape xhtml_escape %}
      {% autoescape None %}

{% block *name* %}...{% end %} 
    Indicates a named, replaceable block for use with {% extends %}.
    Blocks in the parent template will be replaced with the contents of the same-named block in a child template.:
      <!-- base.html -->
      <title>{% block title %}Default title{% end %}</title>

      <!-- mypage.html -->
      {% extends "base.html" %}
      {% block title %}My page title{% end %}

{% comment ... %} 
    A comment which will be removed from the template output. Note that there is no {% end
    %} tag; the comment goes from the word comment to the closing %} tag.

{% extends *filename* %} 
    Inherit from another template. Templates that use extends should contain one
    or more block tags to replace content from the parent template. Anything in the child template not contained
    in a block tag will be ignored. For an example, see the {% block %} tag.
    
{% for *var* in *expr* %}...{% end %} 
    Same as the python for statement. {% break %} and {%
    continue %} may be used inside the loop.
    
{% from *x* import *y* %} 
    Same as the python import statement.
    
{% if *condition* %}...{% elif *condition* %}...{% else %}...{% end %}
    Conditional statement - outputs the first section whose condition is true. 
    (The elif and else sections     are optional)
    
{% import *module* %} 
    Same as the python import statement.
    
{% include *filename* %} 
    Includes another template file. The included file can see all the local variables
    as if it were copied directly to the point of the include directive (the {% autoescape %} directive is an
    exception). Alternately, {% module Template(filename, **kwargs) %} may be used to include
    another template with an isolated namespace.
    
{% module *expr* %} 
    Renders a UIModule. The output of the UIModule is not escaped:
     {% module Template("foo.html", arg=42) %}
     UIModules are a feature of the tornado.web.RequestHandler class (and specifically its render
     method) and will not work when the template system is used on its own in other contexts.
     
{% raw *expr* %} 
    Outputs the result of the given expression without autoescaping.
    
{% set *x* = *y* %} 
    Sets a local variable.
    
{% try %}...{% except %}...{% else %}...{% finally %}...{% end %} 
    Same  as    the  python try statement.
    
{% while *condition* %}... {% end %} 
    Same as the python while statement. {% break %} and
    {% continue %} may be used inside the loop.
    
{% whitespace *mode* %} 
    Sets the whitespace mode for the remainder of the current file (or until the next {%
    whitespace %} directive). See filter_whitespace for available options. New in Tornado 4.3.


###Tornado-tornado.locks ­ Synchronization primitives

These classes are very similar to those provided in the standard library's 
asyncio package.

Warning: Note that these primitives are not actually thread-safe and cannot be used in place of those from the
standard library's threading module­they are meant to coordinate Tornado coroutines in a single-threaded app,
not to protect shared objects in a multithreaded app.



class tornado.locks.Condition
    A condition allows one or more coroutines to wait until notified.
      Like a standard threading.Condition, but does not need an underlying lock that is acquired and released.
      With a Condition, coroutines can wait to be notified by other coroutines:
      from tornado import gen
      from tornado.ioloop import IOLoop
      from tornado.locks import Condition

      condition = Condition()

      async def waiter():
          print("I'll wait right here")
          await condition.wait()
          print("I'm done waiting")

      async def notifier():
          print("About to notify")
          condition.notify()
          print("Done notifying")

      async def runner():
          # Wait for waiter() and notifier() in parallel
          await gen.multi([waiter(), notifier()])

      IOLoop.current().run_sync(runner)

      I'll wait right here
      About to notify
      Done notifying
      I'm done waiting

      wait takes an optional timeout argument, which is either an absolute timestamp:

      io_loop = IOLoop.current()

      # Wait up to 1 second for a notification.
      await condition.wait(timeout=io_loop.time() + 1)

      . . . or a datetime.timedelta for a timeout relative to the current time:

      # Wait up to 1 second.
      await condition.wait(timeout=datetime.timedelta(seconds=1))

      The method returns False if there's no notification before the deadline.
      Changed in version 5.0: Previously, waiters could be notified synchronously from within notify . Now, the
      notification will always be received on the next iteration of the IOLoop.
      wait(timeout: Union[float, datetime.timedelta] = None)  Awaitable[bool]
          Wait for notify .
            Returns a Future that resolves True if the condition is notified, or False after a timeout.
      notify(n: int = 1)  None
          Wake n waiters.
      notify_all()  None
          Wake all waiters.




class tornado.locks.Event
    An event blocks coroutines until its internal flag is set to True.
      Similar to threading.Event.
      A coroutine can wait for an event to be set. Once it is set, calls to yield event.wait() will not block
      unless the event has been cleared:

      from tornado import gen
      from tornado.ioloop import IOLoop
      from tornado.locks import Event

      event = Event()

      async def waiter():
          print("Waiting for event")
          await event.wait()
          print("Not waiting this time")
          await event.wait()
          print("Done")

      async def setter():
          print("About to set the event")
          event.set()

      async def runner():
          await gen.multi([waiter(), setter()])

      IOLoop.current().run_sync(runner)

      Waiting for event
      About to set the event
      Not waiting this time
      Done

      is_set()  bool
          Return True if the internal flag is true.
      set()  None
          Set the internal flag to True. All waiters are awakened.
           Calling wait once the flag is set will not block.
      clear()  None
          Reset the internal flag to False.
           Calls to wait will block until set is called.
      wait(timeout: Union[float, datetime.timedelta] = None)  Awaitable[None]
          Block until the internal flag is true.
           Returns an awaitable, which raises tornado.util.TimeoutError after a timeout.



class tornado.locks.Semaphore(value: int = 1)
    A lock that can be acquired a fixed number of times before blocking.
      A Semaphore manages a counter representing the number of release calls minus the number of acquire
      calls, plus an initial value. The acquire method blocks if necessary until it can return without making the
      counter negative.
      Semaphores limit access to a shared resource. To allow access for two workers at a time:

      from tornado import gen
      from tornado.ioloop import IOLoop

    from tornado.locks import Semaphore

    sem = Semaphore(2)

    async def worker(worker_id):
        await sem.acquire()
        try:
             print("Worker %d is working" % worker_id)
             await use_some_resource()
        finally:
             print("Worker %d is done" % worker_id)
             sem.release()

    async def runner():
        # Join all workers.
        await gen.multi([worker(i) for i in range(3)])

    IOLoop.current().run_sync(runner)

    Worker   0   is   working
    Worker   1   is   working
    Worker   0   is   done
    Worker   2   is   working
    Worker   1   is   done
    Worker   2   is   done

    Workers 0 and 1 are allowed to run concurrently, but worker 2 waits until the semaphore has been released once,
    by worker 0.
    The semaphore can be used as an async context manager:

    async def worker(worker_id):
        async with sem:
            print("Worker %d is working" % worker_id)
            await use_some_resource()

         # Now the semaphore has been released.
         print("Worker %d is done" % worker_id)

    For compatibility with older versions of Python, acquire is a context manager, so worker could also be
    written as:

    @gen.coroutine
    def worker(worker_id):
        with (yield sem.acquire()):
            print("Worker %d is working" % worker_id)
            yield use_some_resource()

         # Now the semaphore has been released.
         print("Worker %d is done" % worker_id)

    Changed in version 4.3: Added async with support in Python 3.5.
    release()  None
        Increment the counter and wake one waiter.
    acquire(timeout:         Union[float,     datetime.timedelta]           =      None)                Await-
            able[tornado.locks._ReleasingContextManager]

            Decrement the counter. Returns an awaitable.
            Block if the counter is zero and wait for a release. The awaitable raises TimeoutError after the
            deadline.




class tornado.locks.BoundedSemaphore(value: int = 1)
    A semaphore that prevents release() being called too many times.
       If release would increment the semaphore's value past the initial value, it raises ValueError. Semaphores
       are mostly used to guard resources with limited capacity, so a semaphore released too many times is a sign of a
       bug.
       release()  None
           Increment the counter and wake one waiter.
       acquire(timeout:           Union[float,      datetime.timedelta]        =      None)              Await-
                able[tornado.locks._ReleasingContextManager]
           Decrement the counter. Returns an awaitable.
            Block if the counter is zero and wait for a release. The awaitable raises TimeoutError after the
            deadline.




class tornado.locks.Lock
    A lock for coroutines.
       A Lock begins unlocked, and acquire locks it immediately. While it is locked, a coroutine that yields
       acquire waits until another coroutine calls release.
       Releasing an unlocked lock raises RuntimeError.
       A Lock can be used as an async context manager with the async with statement:

       from tornado import locks
       lock = locks.Lock()
       
       async def f():
          async with lock:
              # Do something holding the lock.
              pass
       
          # Now the lock is released.

       For compatibility with older versions of Python, the acquire method asynchronously returns a regular context
       manager:

       async def f2():
          with (yield lock.acquire()):
              # Do something holding the lock.
              pass
       
          # Now the lock is released.

       Changed in version 4.3: Added async with support in Python 3.5.

     acquire(timeout:  Union[float,   datetime.timedelta]         =     None)                Await-
              able[tornado.locks._ReleasingContextManager]
         Attempt to lock. Returns an awaitable.
           Returns an awaitable, which raises tornado.util.TimeoutError after a timeout.
     release()  None
         Unlock.
           The first coroutine in line waiting for acquire gets the lock.
           If not locked, raise a RuntimeError.



class tornado.queues.Queue(maxsize: int = 0)
    Coordinate producer and consumer coroutines.
     If maxsize is 0 (the default) the queue size is unbounded.
     from tornado import gen
     from tornado.ioloop import IOLoop
     from tornado.queues import Queue

     q = Queue(maxsize=2)

     async def consumer():
         async for item in q:
             try:
                 print('Doing work on %s' % item)
                 await gen.sleep(0.01)
             finally:
                 q.task_done()

     async def producer():
         for item in range(5):
             await q.put(item)
             print('Put %s' % item)

     async def main():
         # Start consumer without waiting (since it never finishes).
         IOLoop.current().spawn_callback(consumer)
         await producer()     # Wait for producer to put all tasks.
         await q.join()       # Wait for consumer to finish all tasks.

           print('Done')

      IOLoop.current().run_sync(main)

      Put 0
      Put 1
      Doing   work on 0
      Put 2
      Doing   work on 1
      Put 3
      Doing   work on 2
      Put 4
      Doing   work on 3
      Doing   work on 4
      Done

      In versions of Python without native coroutines (before 3.5), consumer() could be written as:

      @gen.coroutine
      def consumer():
          while True:
              item = yield q.get()
              try:
                  print('Doing work on %s' % item)
                  yield gen.sleep(0.01)
              finally:
                  q.task_done()

      Changed in version 4.3: Added async for support in Python 3.5.
      property maxsize
          Number of items allowed in the queue.
      qsize()  int
          Number of items in the queue.
      put(item: _T, timeout: Union[float, datetime.timedelta] = None)  Future[None]
          Put an item into the queue, perhaps waiting until there is room.
           Returns a Future, which raises tornado.util.TimeoutError after a timeout.
           timeout may be a number denoting a time (on the same scale as tornado.ioloop.IOLoop.time,
           normally time.time), or a datetime.timedelta object for a deadline relative to the current time.
      put_nowait(item: _T )  None
          Put an item into the queue without blocking.
           If no free slot is immediately available, raise QueueFull.
      get(timeout: Union[float, datetime.timedelta] = None)  Awaitable[_T]
          Remove and return an item from the queue.
           Returns an awaitable which resolves once an item is available, or raises tornado.util.
           TimeoutError after a timeout.
           timeout may be a number denoting a time (on the same scale as tornado.ioloop.IOLoop.time,
           normally time.time), or a datetime.timedelta object for a deadline relative to the current time.
           Note: The timeout argument of this method differs from that of the standard library's queue.Queue.
           get. That method interprets numeric values as relative timeouts; this one interprets them as absolute dead-
           lines and requires timedelta objects for relative timeouts (consistent with other timeouts in Tornado).

     get_nowait()  _T
         Remove and return an item from the queue without blocking.
           Return an item if one is immediately available, else raise QueueEmpty .
     task_done()  None
         Indicate that a formerly enqueued task is complete.
           Used by queue consumers. For each get used to fetch a task, a subsequent call to task_done tells the
           queue that the processing on the task is complete.
           If a join is blocking, it resumes when all items have been processed; that is, when every put is matched
           by a task_done.
           Raises ValueError if called more times than put.
     join(timeout: Union[float, datetime.timedelta] = None)  Awaitable[None]
         Block until all items in the queue are processed.
           Returns an awaitable, which raises tornado.util.TimeoutError after a timeout.




class tornado.queues.PriorityQueue(maxsize: int = 0)
    A Queue that retrieves entries in priority order, lowest first.
     Entries are typically tuples like (priority number, data).
     from tornado.queues import PriorityQueue

     q = PriorityQueue()
     q.put((1, 'medium-priority item'))
     q.put((0, 'high-priority item'))
     q.put((10, 'low-priority item'))

     print(q.get_nowait())
     print(q.get_nowait())
     print(q.get_nowait())

     (0, 'high-priority item')
     (1, 'medium-priority item')
     (10, 'low-priority item')




class tornado.queues.LifoQueue(maxsize: int = 0)
    A Queue that retrieves the most recently put items first.
     from tornado.queues import LifoQueue

     q = LifoQueue()

      q.put(3)
      q.put(2)
      q.put(1)

      print(q.get_nowait())
      print(q.get_nowait())
      print(q.get_nowait())

      1
      2
      3



Exceptions
exception tornado.queues.QueueEmpty
    Raised by Queue.get_nowait when the queue has no items.

exception tornado.queues.QueueFull
    Raised by Queue.put_nowait when a queue is at its maximum size.


###Tornado-tornado.process -- Utilities for multiple processes

Utilities for working with multiple processes, including both forking the server into multiple processes and managing
subprocesses.
exception tornado.process.CalledProcessError
    An alias for subprocess.CalledProcessError.
exception tornado.process.CalledProcessError(returncode,                          cmd,         output=None,
                                                               stderr=None)
    Raised when run() is called with check=True and the process returns a non-zero exit status.
      Attributes: cmd, returncode, stdout, stderr, output
      property stdout
          Alias for output attribute, to match stderr
tornado.process.cpu_count()  int
    Returns the number of processors on this machine.
tornado.process.fork_processes(num_processes: Optional[int], max_restarts: int = None)  int
    Starts multiple worker processes.
      If num_processes is None or <= 0, we detect the number of cores available on this machine and fork that
      number of child processes. If num_processes is given and > 0, we fork that specific number of sub-processes.
      Since we use processes and not threads, there is no shared memory between any server code.
      Note that multiple processes are not compatible with the autoreload module (or the autoreload=True op-
      tion to tornado.web.Application which defaults to True when debug=True). When using multiple
      processes, no IOLoops can be created or referenced until after the call to fork_processes.

    In each child process, fork_processes returns its task id, a number between 0 and num_processes.
    Processes that exit abnormally (due to a signal or non-zero exit status) are restarted with the same id (up to
    max_restarts times). In the parent process, fork_processes returns None if all child processes have
    exited normally, but will otherwise only exit by throwing an exception.
    max_restarts defaults to 100.
tornado.process.task_id()  Optional[int]
    Returns the current task id, if any.
    Returns None if this process was not created by fork_processes.
class tornado.process.Subprocess(*args, **kwargs)
    Wraps subprocess.Popen with IOStream support.
    The constructor is the same as subprocess.Popen with the following additions:
       · stdin, stdout, and stderr may have the value tornado.process.Subprocess.STREAM,
         which will make the corresponding attribute of the resulting Subprocess a PipeIOStream. If this option
         is used, the caller is responsible for closing the streams when done with them.
    The Subprocess.STREAM option and the set_exit_callback and wait_for_exit methods do not
    work on Windows. There is therefore no reason to use this class instead of subprocess.Popen on that
    platform.
    Changed in version 5.0: The io_loop argument (deprecated since version 4.1) has been removed.
    set_exit_callback(callback: Callable[[int], None])  None
        Runs callback when this process exits.
         The callback takes one argument, the return code of the process.
         This method uses a SIGCHLD handler, which is a global setting and may conflict if you have other libraries
         trying to handle the same signal. If you are using more than one IOLoop it may be necessary to call
         Subprocess.initialize first to designate one IOLoop to run the signal handlers.
         In many cases a close callback on the stdout or stderr streams can be used as an alternative to an exit
         callback if the signal handler is causing a problem.
    wait_for_exit(raise_error: bool = True)  Future[int]
        Returns a Future which resolves when the process exits.
         Usage:

         ret = yield proc.wait_for_exit()

         This is a coroutine-friendly alternative to set_exit_callback (and a replacement for the blocking
         subprocess.Popen.wait).
         By default, raises subprocess.CalledProcessError if the process has a non-zero exit status. Use
         wait_for_exit(raise_error=False) to suppress this behavior and return the exit status without
         raising.
         New in version 4.2.
    classmethod initialize()  None
        Initializes the SIGCHLD handler.
         The signal handler is run on an IOLoop to avoid locking issues. Note that the IOLoop used for signal
         handling need not be the same one used by individual Subprocess objects (as long as the IOLoops are
         each running in separate threads).
         Changed in version 5.0: The io_loop argument (deprecated since version 4.1) has been removed.


-------------------
###OpenAPI 
API speifications
    https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#format
Mimetypes 
    https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#mimeTypes
Path
    https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#paths-object
HttpVerb
    https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#operationObject
Parameters 
    https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#parametersDefinitionsObject
Response 
    https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#responsesDefinitionsObject
Definition
    https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#definitionsObject
Schema 
    https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#schemaObject
    
#petstore-minimal.yaml
---
  swagger: "2.0"
  info: 
    version: "1.0.0"
    title: "Swagger Petstore"
    description: "A sample API that uses a petstore as an example to demonstrate features in the swagger-2.0 specification"
    termsOfService: "http://swagger.io/terms/"
    contact: 
      name: "Swagger API Team"
    license: 
      name: "MIT"
  host: "petstore.swagger.io"   # The host (name or ip) serving the API.
  basePath: "/api"              # The base path on which the API is served, which is relative to the host. If it is not included, the API is served directly under the host
  schemes:                      # [string] 	The transfer protocol of the API. Values MUST be from the list: "http", "https", "ws", "wss"
    - "http"                    
  consumes:                     # string] 	A list of MIME types the APIs can consume. This is global to all APIs but can be overridden on specific API calls
    - "application/json"    
  produces:                     # [string] 	A list of MIME types the APIs can produce. This is global to all APIs but can be overridden on specific API calls
    - "application/json"
  paths:                        # Paths Object - Required, eg /{path}
    /pets:                      # A relative path to an individual endpoint. The field name MUST begin with a slash. The path is appended to the basePath in order to construct the full URL
      get:                      # A definition of a GET operation on this path.
        description: "Returns all pets from the system that the user has access to"
        produces:               # [string] 	A list of MIME types the operation can produce.
          - "application/json"
        responses:              #Required. The list of possible responses
          "200":                # Any HTTP status code can be used as the property name 
            description: "A list of pets."
            schema:             # A definition of the response structure. It can be a primitive, an array or an object. If this field does not exist, it means no content is returned as part of the response.
              type: "array"     # One of seven type, https://tools.ietf.org/html/draft-zyp-json-schema-04#section-3.5
              items:            # https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.1
                $ref: "#/definitions/Pet" # #: whole document, then definition, then Pet , https://tools.ietf.org/html/draft-ietf-appsawg-json-pointer-04#section-6
  definitions: 
    Pet:                        # Schema Object
      type: "object"
      required: 
        - "id"
        - "name"
      properties: 
        id: 
          type: "integer"
          format: "int64"
        name: 
          type: "string"
        tag: 
          type: "string"

#petstore-simple.yaml
---
  swagger: "2.0"
  info: 
    version: "1.0.0"
    title: "Swagger Petstore"
    description: "A sample API that uses a petstore as an example to demonstrate features in the swagger-2.0 specification"
    termsOfService: "http://swagger.io/terms/"
    contact: 
      name: "Swagger API Team"
    license: 
      name: "MIT"
  host: "petstore.swagger.io"
  basePath: "/api"
  schemes: 
    - "http"
  consumes: 
    - "application/json"
  produces: 
    - "application/json"
  paths: 
    /pets: 
      get: 
        description: "Returns all pets from the system that the user has access to"
        operationId: "findPets" # Unique string used to identify the operation. The id MUST be unique among all operations described in the API. Tools and libraries MAY use the operationId to uniquely identify an operation, therefore, it is recommended to follow common programming naming conventions.
        produces: 
          - "application/json"
          - "application/xml"
          - "text/xml"
          - "text/html"
        parameters: 
          - 
            name: "tags"        # Parameter names are case sensitive. the name corresponds to the parameter name used based on the in property.
            in: "query"         # The location of the parameter. Possible values are "query", "header", "path", "formData" or "body".
            description: "tags to filter by"
            required: false     # Determines whether this parameter is mandatory. If the parameter is in "path", this property is required and its value MUST be true
            type: "array"       # he type of the parameter. Since the parameter is not located at the request body, it is limited to simple types (that is, not an object). The value MUST be one of "string", "number", "integer", "boolean", "array" or "file". If type is "file", the consumes MUST be either "multipart/form-data", " application/x-www-form-urlencoded" or both and the parameter MUST be in "formData".
            items:              # Describes the type of items in the array. Required if type is "array".
              type: "string"    # The internal type of the array. The value MUST be one of "string", "number", "integer", "boolean", or "array"
            collectionFormat: "csv" #Determines the format of the array if type array is used. Possible values are: csv - comma separated values foo,bar.  ssv - space separated values foo bar. tsv - tab separated values foo\tbar.  pipes - pipe separated values foo|bar
          - 
            name: "limit"
            in: "query"
            description: "maximum number of results to return"
            required: false
            type: "integer"
            format: "int32"
        responses: 
          "200":
            description: "pet response"
            schema: 
              type: "array"
              items: 
                $ref: "#/definitions/Pet"
          default:          # The documentation of responses other than the ones declared for specific HTTP response codes. It can be used to cover undeclared responses
            description: "unexpected error"
            schema: 
              $ref: "#/definitions/ErrorModel"
      post: 
        description: "Creates a new pet in the store.  Duplicates are allowed"
        operationId: "addPet"
        produces: 
          - "application/json"
        parameters: 
          - 
            name: "pet"
            in: "body"
            description: "Pet to add to the store"
            required: true
            schema:     # If in is "body", Required. The schema defining the type used for the body parameter.
              $ref: "#/definitions/NewPet"
        responses: 
          "200":
            description: "pet response"
            schema: 
              $ref: "#/definitions/Pet"
          default: 
            description: "unexpected error"
            schema: 
              $ref: "#/definitions/ErrorModel"
    /pets/{id}:             # Path templating refers to the usage of curly braces ({}) to mark a section of a URL path as replaceable using path parameters.
      get:  
        description: "Returns a user based on a single ID, if the user does not have access to the pet"
        operationId: "findPetById"
        produces: 
          - "application/json"
          - "application/xml"
          - "text/xml"
          - "text/html"
        parameters: 
          - 
            name: "id"      # If in is "path", the name field MUST correspond to the associated path segment from the path field in the Paths Object
            in: "path"
            description: "ID of pet to fetch"
            required: true  # If the parameter is in "path", this property is required and its value MUST be true
            type: "integer"
            format: "int64"
        responses: 
          "200":
            description: "pet response"
            schema: 
              $ref: "#/definitions/Pet"
          default: 
            description: "unexpected error"
            schema: 
              $ref: "#/definitions/ErrorModel"
      delete: 
        description: "deletes a single pet based on the ID supplied"
        operationId: "deletePet"
        parameters: 
          - 
            name: "id"
            in: "path"
            description: "ID of pet to delete"
            required: true
            type: "integer"
            format: "int64"
        responses: 
          "204":
            description: "pet deleted"
          default: 
            description: "unexpected error"
            schema: 
              $ref: "#/definitions/ErrorModel"
  definitions: 
    Pet: 
      type: "object"
      allOf:            # This keyword's value MUST be an array, validates successfully against all schemas defined by this keyword's value. https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.5.3
        - 
          $ref: "#/definitions/NewPet"
        - 
          required: 
            - "id"
          properties: 
            id: 
              type: "integer"
              format: "int64"
    NewPet: 
      type: "object"
      required: 
        - "name"
      properties: 
        name: 
          type: "string"
        tag: 
          type: "string"
    ErrorModel: 
      type: "object"
      required: 
        - "code"
        - "message"
      properties: 
        code: 
          type: "integer"
          format: "int32"
        message: 
          type: "string"


          
##Generate python code   
#https://swagger.io/tools/swagger-codegen/
$ wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.4.10/swagger-codegen-cli-2.4.10.jar -O swagger-codegen-cli.jar
        
#Client generation 
#Generating static html api documentation, use  -l html 
$ java -jar C:\swagger\swagger-codegen-cli.jar generate  -i  petstore-minimal.yaml   -l python  -o client/minimal    
   
#Then Read doc at 
README.md
docs/DefaultApi.md
docs/Pet.md

#install in virtual environment 
$ python setup.py install --user

#then 
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
configuration = swagger_client.Configuration()
#change this from server eg http://localhost:8080/api 
configuration.host = "http://petstore.swagger.io/api"
#many configurations are present , check swagger_client/configuration.py
api_instance = swagger_client.DefaultApi(swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.pets_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->pets_get: %s\n" % e)


#Server-stub generation 
#https://github.com/swagger-api/swagger-codegen/wiki/Server-stub-generator-HOWTO for more information.

#Python Flask (Connexion)
$ java -jar C:\swagger\swagger-codegen-cli.jar generate  -i  petstore-minimal.yaml  -l python-flask -o server/minimal/
#Python2 Flask (Connexion)
  -D supportPython2=true
  
#Then read and execute in virtual env
README.md

# Execute 
pip3 install -r requirements.txt
python3 -m swagger_server
```

#and open swagger-ui
http://localhost:8080/api/ui/

#Swagger definition lives here:
http://localhost:8080/api/swagger.json




##create virtual env 
$ pip install virtualenv

$ mkdir myproject
$ cd myproject
$ virtualenv venv
New python executable in venv/bin/python
Installing setuptools, pip............done.

$ . venv/bin/activate
#or in windows 
$ venv\scripts\activate


$ deactivate






###Editor and UI - Docker 
#https://github.com/swagger-api/swagger-ui/blob/master/docs/usage/installation.md

#Editor 
docker pull swaggerapi/swagger-editor
docker run -d -p 80:8080 swaggerapi/swagger-editor

check http://localhost:80 in your browser.


#swagger-ui 
docker pull swaggerapi/swagger-ui
docker run -p 80:8080 swaggerapi/swagger-ui
#start nginx with Swagger UI on port 80.

#Or you can provide your own swagger.json on your host
$ docker run -p 80:8080 -e SWAGGER_JSON=/foo/swagger.json -v /bar:/foo swaggerapi/swagger-ui

#The base URL of the web application can be changed by specifying the BASE_URL environment variable:
$ docker run -p 80:8080 -e BASE_URL=/swagger -e SWAGGER_JSON=/foo/swagger.json -v /bar:/foo swaggerapi/swagger-ui
#This will serve Swagger UI at /swagger instead of /.






###Connexion 
https://connexion.readthedocs.io/en/latest/

Connexion is a framework on top of Flask that automagically handles HTTP requests 
defined using OpenAPI (formerly known as Swagger), s
upporting both v2.0 and v3.0 of the specification

$ pip install connexion[swagger-ui]
$ pip install swagger_ui_bundle
$ pip install gevent tornado    #for working 

#also curl should be installed 
#eg https://develop.zendesk.com/hc/en-us/articles/360001068567-Installing-and-using-cURL#install
#for wget - http://gnuwin32.sourceforge.net/packages/wget.htm

##Features 
* mapping of REST operations to Python functions (using the operationId in swagger.yaml)
  * maps path, query and body parameters to keyword arguments
* bundled Swagger UI (served on /ui/ path)
* automatic JSON serialization for application/json content type
* schema validation for the HTTP request body and query parameters:
  * required object properties
  * primitive JSON types (string, integers, etc)
  * date/time values
  * string lengths
  * minimum/maximum values
  * regular expression patterns


#openapi/helloworld-api.yaml
#note operationId: hello.post_greeting, means module:hello, function:post_greeting
swagger: "2.0"

info:
  title: "{{title}}"
  version: "1.0"

basePath: /v1.0

paths:
  /greeting/{name}:
    post:
      summary: Generate greeting
      description: Generates a greeting message.
      operationId: hello.post_greeting # this defines which function to call 
      produces:
        - text/plain;
      responses:
        200:
          description: greeting response
          schema:
            type: string
          examples:
            "text/plain": "Hello John"
      parameters:
        - name: name
          in: path
          description: Name of the person to greet.
          required: true
          type: string

#hello.py 
import connexion


def post_greeting(name: str) -> str:
    return 'Hello {name}'.format(name=name)

if __name__ == '__main__':
    #FlaskApp is nothing but app = flask.Flask so, all app.* methods are available eg app.route
    #or server=gevent
    app = connexion.FlaskApp(__name__, port = 8080, specification_dir='openapi/', server='tornado')
    #or     
    #app = connexion.AioHttpApp(__name__, port = 8080, specification_dir='openapi/')
    app.add_api('helloworld-api.yaml', 
        arguments={'title': 'Hello World Example'}
        )
    app.run()

    
#Execute 
$ python hello.py 
#check swagger-ui at http://localhost:8080/v1.0/ui/
#and send POST http://localhost:8080/v1.0/greeting/{name}
#eg http://localhost:8080/v1.0/greeting/das
#note for tornado, crtl+c works only if you access endpoint after pressing 

#to run OpenAPI specifications directly before implementation of any operation handler function 
#This allows you to verify and inspect how your API will work with Connexion
$ connexion run openapi\helloworld-api.yaml --stub 
#check http://localhost:5000/v1.0/greeting/das

#or mock all api 
$ connexion run openapi\helloworld-api.yaml --mock=all -v 
#check http://localhost:5000/v1.0/greeting/das

##Using asyncio 

#hello.py 
import asyncio

import connexion
from aiohttp import web


@asyncio.coroutine
def post_greeting(name):
    return web.Response(text='Hello {name}'.format(name=name))


if __name__ == '__main__':
    app = connexion.AioHttpApp(__name__, port=9090, specification_dir='openapi/')
    app.add_api('helloworld-api.yaml', arguments={'title': 'Hello World Example'})
    app.run()
    
    
    
    
#openapi/helloworld-api.yaml 
openapi: "3.0.0"

info:
  title: Hello World
  version: "1.0"
servers:
  - url: http://localhost:9090/v1.0

paths:
  /greeting/{name}:
    post:
      summary: Generate greeting
      description: Generates a greeting message.
      operationId: hello.post_greeting
      responses:
        200:
          description: greeting response
          content:
            text/plain:
              schema:
                type: string
                example: "hello dave!"
      parameters:
        - name: name
          in: path
          description: Name of the person to greet.
          required: true
          schema:
            type: string
            example: "dave"



###Connexion - Using RestyResolver 
RestyResolver will give precedence to any operationId encountered in the specification
If operationId is not found , The RestyResolver will compose an operationId based on the path 
and HTTP method of the endpoints in your specification

app.add_api('swagger.yaml', resolver=RestyResolver('api'))
#then 
paths:
  /:
    get:
       # Implied operationId: api.get
  /foo:
    get:
       # Implied operationId: api.foo.search
    post:
       # Implied operationId: api.foo.post

  '/foo/{id}':
    get:
       # Implied operationId: api.foo.get
    put:
       # Implied operationId: api.foo.put
    copy:
       # Implied operationId: api.foo.copy
    delete:
       # Implied operationId: api.foo.delete

#Example 
#resty.py 
import logging

import connexion
from connexion.resolver import RestyResolver

logging.basicConfig(level=logging.INFO)
app = connexion.FlaskApp(__name__)
app.add_api('resty-api.yaml',
            arguments={'title': 'RestyResolver Example'},
            resolver=RestyResolver('api'))
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app
                
if __name__ == '__main__':
    app.run(port=9090)
    
#resty-api.yaml
swagger: '2.0'
info:
  title: Pet Shop Example API
  version: "0.1"
  description: Simple example API to store and retrieve pets
consumes:
  - application/json
produces:
  - application/json
security:
  # enable OAuth protection for all REST endpoints
  # (only active if the TOKENINFO_URL environment variable is set)
  - oauth2: [uid]
paths:
  /pets:
    get:
      tags: [Pets]
      operationId: app.get_pets
      summary: Get all pets
      parameters:
        - name: animal_type
          in: query
          type: string
          pattern: "^[a-zA-Z0-9]*$"
        - name: limit
          in: query
          type: integer
          format: int32
          minimum: 0
          default: 100
      responses:
        200:
          description: Return pets
          schema:
            type: object
            properties:
              pets:
                type: array
                items:
                  $ref: '#/definitions/Pet'
  /pets/{pet_id}:
    get:
      tags: [Pets]
      operationId: app.get_pet
      summary: Get a single pet
      parameters:
        - $ref: '#/parameters/pet_id'
      responses:
        200:
          description: Return pet
          schema:
            $ref: '#/definitions/Pet'
        404:
          description: Pet does not exist
    put:
      tags: [Pets]
      operationId: app.put_pet
      summary: Create or update a pet
      parameters:
        - $ref: '#/parameters/pet_id'
        - name: pet
          in: body
          schema:
            $ref: '#/definitions/Pet'
      responses:
        200:
          description: Pet updated
        201:
          description: New pet created
    delete:
      tags: [Pets]
      operationId: app.delete_pet
      summary: Remove a pet
      parameters:
        - $ref: '#/parameters/pet_id'
      responses:
        204:
          description: Pet was deleted
        404:
          description: Pet does not exist


parameters:
  pet_id:
    name: pet_id
    description: Pet's Unique identifier
    in: path
    type: string
    required: true
    pattern: "^[a-zA-Z0-9-]+$"

definitions:
  Pet:
    type: object
    required:
      - name
      - animal_type
    properties:
      id:
        type: string
        description: Unique identifier
        example: "123"
        readOnly: true
      name:
        type: string
        description: Pet's name
        example: "Susie"
        minLength: 1
        maxLength: 100
      animal_type:
        type: string
        description: Kind of animal
        example: "cat"
        minLength: 1
      tags:
        type: object
        description: Custom tags
      created:
        type: string
        format: date-time
        description: Creation time
        example: "2015-07-07T15:49:51.230+02:00"
        readOnly: true


securityDefinitions:
  oauth2:
    type: oauth2
    flow: implicit
    authorizationUrl: https://example.com/oauth2/dialog
    scopes:
      uid: Unique identifier of the user accessing the service.

        
#api/pets.py 
import connexion
import datetime
import logging

from connexion import NoContent

# our memory-only pet storage
PETS = {}


def get_pets(limit, animal_type=None):
    return {"pets": [pet for pet in PETS.values() if not animal_type or pet['animal_type'] == animal_type][:limit]}


def get_pet(pet_id):
    pet = PETS.get(pet_id)
    return pet or ('Not found', 404)


def put_pet(pet_id, pet):
    exists = pet_id in PETS
    pet['id'] = pet_id
    if exists:
        logging.info('Updating pet %s..', pet_id)
        PETS[pet_id].update(pet)
    else:
        logging.info('Creating pet %s..', pet_id)
        pet['created'] = datetime.datetime.utcnow()
        PETS[pet_id] = pet
    return NoContent, (200 if exists else 201)


def delete_pet(pet_id):
    if pet_id in PETS:
        logging.info('Deleting pet %s..', pet_id)
        del PETS[pet_id]
        return NoContent, 204
    else:
        return NoContent, 404

    
#api/__init__.py 
import api.pets  # noqa


#DockerFile 
#check Pipfile and Pipfile.lock from code dir 
FROM registry.opensource.zalan.do/stups/python:3.6.5-22

COPY Pipfile /
COPY Pipfile.lock /

RUN pipenv install --system --deploy --ignore-pipfile

CMD mkdir -p /api

COPY api/__init__.py /api
COPY api/app.py /api

COPY resty-api.yaml /
COPY resty.py /

WORKDIR /data
CMD /resty.py






###Connexion - Request, Response and Security handling 


##Request Handling

Request parameters will be provided to the handler functions as keyword arguments 
if they are included in the function's signature(with exact name as in swagger specification) 
otherwise body parameters can be accessed from connexion.request.json 
and query parameters can be accessed from connexion.request.args.

#Example 
paths:
  /foo:
    get:
      operationId: api.foo_get
      parameters:
        - name: message
          description: Some message.
          in: query
          type: string
          required: true

#And the view function:

# api.py file

def foo_get(message):
    # do something
    return 'You send the message: {}'.format(message), 200

    
Connexion will also use default values if they are provided.

In the OpenAPI 3.x.x spec, the requestBody does not have a name. 
By default it will be passed in as 'body'. 
You can optionally provide the x-body-name parameter in your requestBody schema to override the name of the parameter that will be passed to your handler function.

Please note that when you have a parameter defined as not required at your endpoint 
and your Python view have a non-named argument, 
when you call this endpoint WITHOUT the parameter you will get an exception of missing positional argument.
So use connexion.request.args

  

##Type casting
Whenever possible Connexion will try to parse your argument values 
and do type casting to related Python natives values. 
OpenAPI Type 	Python Type
integer 	    int
string 	        str
number 	        float
boolean 	    bool
array 	        list
null 	        None
object 	        dict

In the OpenAPI 2.0 Specification if you use the array type, 
you can define the collectionFormat do set the deserialization behavior. 
Connexion currently supports 'pipes' and 'csv' as collection formats. 
The default format is 'csv'

The default behavior for query parameters that have been defined multiple times 
is to join them all together. 
For example, if you provide a URI with the the query string ?letters=a,b,c&letters=d,e,f, 
connexion will set letters = ['a', 'b', 'c', 'd', 'e', 'f'].

You can override this behavior by specifying the URI parser in the app or api options.

from connexion.decorators.uri_parsing import Swagger2URIParser
options = {'uri_parsing_class': Swagger2URIParser}
app = connexion.App(__name__, specification_dir='swagger/', options=options)

#There are a handful of URI parsers included with connection.
OpenAPIURIParser default: OpenAPI 3.0 	
    This parser adheres to the OpenAPI 3.x.x spec, and uses the style parameter. 
    Query parameters are parsed from left to right, 
    so if a query parameter is defined twice, 
    then the right-most definition will take precedence. 
    For example, if you provided a URI with the query string ?letters=a,b,c&letters=d,e,f, 
    and style: simple, then connexion will set letters = ['d', 'e', 'f']. 

Swagger2URIParser default: OpenAPI 2.0 	
    This parser adheres to the Swagger 2.0 spec, 
    and will only join together multiple instance of the same query parameter 
    if the collectionFormat is set to multi. 
    Query parameters are parsed from left to right, 
    so if a query parameter is defined twice, then the right-most definition wins. 
    For example, if you provided a URI with the query string ?letters=a,b,c&letters=d,e,f, 
    and collectionFormat: csv, then connexion will set letters = ['d', 'e', 'f']
    
FirstValueURIParser 	
    This parser behaves like the Swagger2URIParser, 
    except that it prefers the first defined value.
    For example, if you provided a URI with the query string ?letters=a,b,c&letters=d,e,f 
    and collectionFormat: csv hen connexion will set letters = ['a', 'b', 'c']
    
AlwaysMultiURIParser 	
    This parser is backwards compatible with Connexion 1.x. 
    It joins together multiple instances of the same query parameter.
    
    
    
##Parameter validation
Connexion can apply strict parameter validation for query and form data parameters. 
When this is enabled, requests that include parameters not defined 
in the swagger spec return a 400 error. 
You can enable it when adding the API to your application:

app.add_api('my_apy.yaml', strict_validation=True)


##Nullable parameters
Sometimes your API should explicitly accept nullable parameters. 
However OpenAPI specification currently does not support officially a way 
to serve this use case, 
Connexion adds the x-nullable vendor extension to parameter definitions. 
It is supported by Connexion in all parameter types: body, query, formData, and path. 
Nullable values are the strings null and None.

/countries/cities:
   parameters:
     - name: name
       in: query
       type: string
       x-nullable: true
       required: true


##Header Parameters
Currently, header parameters are not passed to the handler functions as parameters. 
But they can be accessed through the underlying connexion.request.headers object 
which aliases the flask.request.headers object.

def index():
    page_number = connexion.request.headers['Page-Number']

    
    
##Request Parameter validation   
Both the request body and parameters are validated against the specification, 
using jsonschema.

If the request doesn't match the specification connexion will return a 400 error.

By default, body and parameters contents are validated against OpenAPI schema 
via connexion.decorators.validation.RequestBodyValidator 
or connexion.decorators.validation.ParameterValidator, 

if you want to change the validation, you can override the defaults with:
validator_map = {
    'body': CustomRequestBodyValidator,
    'parameter': CustomParameterValidator
}
app = connexion.FlaskApp(__name__)
app.add_api('api.yaml', ..., validator_map=validator_map)



##Response Serialization
If the endpoint returns a Response object this response will be used as is.
eg 
flask.Response(response=None, status=None, headers=None, mimetype=None, content_type=None, direct_passthrough=False)
aiohttp.web.Response(*, body=None, status=200, reason=None, text=None, headers=None, content_type=None, charset=None, zlib_executor_size=sentinel, zlib_executor=None)


Otherwise, and by default and if the specification defines 
that an endpoint produces only JSON, 
connexion will automatically serialize the return value for you 
and set the right content type in the HTTP header.

If the endpoint produces a single non-JSON mimetype 
then Connexion will automatically set the right content type in the HTTP header.


##Returning status codes
There are two ways of returning a specific status code.
One way is to return a Response object that will be used unchanged.

The other is returning it as a second return value in the response. 
def my_endpoint():
    return 'Not Found', 404

    
##Returning Headers
There are two ways to return headers from your endpoints.

One way is to return a Response object that will be used unchanged.

The other is returning a dict with the header values as the third return value 
in the response:
def my_endpoint():
    return 'Not Found', 404, {'x-error': 'not found'}

    
##Response Validation
While, by default Connexion doesn’t validate the responses 
it’s possible to do so by opting in when adding the API:

import connexion

app = connexion.FlaskApp(__name__, specification_dir='swagger/')
app.add_api('my_api.yaml', validate_responses=True)
app.run(port=8080)

This will validate all the responses using jsonschema 
and is specially useful during development.


##Custom Validator
By default, response body contents are validated against OpenAPI schema 
via connexion.decorators.response.ResponseValidator, 
if you want to change the validation, you can override the default class with:

validator_map = {
    'response': CustomResponseValidator
}
app = connexion.FlaskApp(__name__)
app.add_api('api.yaml', ..., validator_map=validator_map)



##Error Handling
By default connexion error messages are JSON serialized according 
to Problem Details for HTTP APIs, https://tools.ietf.org/html/draft-ietf-appsawg-http-problem-00

Application can return errors using connexion.problem.






##Example with sqlalchemy 

#swagger.py 
swagger: '2.0'
info:
  title: Pet Shop Example API
  version: "0.1"
consumes:
  - application/json
produces:
  - application/json
paths:
  /pets:
    get:
      tags: [Pets]
      operationId: app.get_pets
      summary: Get all pets
      parameters:
        - name: animal_type
          in: query
          type: string
          pattern: "^[a-zA-Z0-9]*$"
        - name: limit
          in: query
          type: integer
          minimum: 0
          default: 100
      responses:
        200:
          description: Return pets
          schema:
            type: array
            items:
              $ref: '#/definitions/Pet'
  /pets/{pet_id}:
    get:
      tags: [Pets]
      operationId: app.get_pet
      summary: Get a single pet
      parameters:
        - $ref: '#/parameters/pet_id'
      responses:
        200:
          description: Return pet
          schema:
            $ref: '#/definitions/Pet'
        404:
          description: Pet does not exist
    put:
      tags: [Pets]
      operationId: app.put_pet
      summary: Create or update a pet
      parameters:
        - $ref: '#/parameters/pet_id'
        - name: pet
          in: body
          schema:
            $ref: '#/definitions/Pet'
      responses:
        200:
          description: Pet updated
        201:
          description: New pet created
    delete:
      tags: [Pets]
      operationId: app.delete_pet
      summary: Remove a pet
      parameters:
        - $ref: '#/parameters/pet_id'
      responses:
        204:
          description: Pet was deleted
        404:
          description: Pet does not exist


parameters:
  pet_id:
    name: pet_id
    description: Pet's Unique identifier
    in: path
    type: string
    required: true
    pattern: "^[a-zA-Z0-9-]+$"

definitions:
  Pet:
    type: object
    required:
      - name
      - animal_type
    properties:
      id:
        type: string
        description: Unique identifier
        example: "123"
        readOnly: true
      name:
        type: string
        description: Pet's name
        example: "Susie"
        minLength: 1
        maxLength: 100
      animal_type:
        type: string
        description: Kind of animal
        example: "cat"
        minLength: 1
      created:
        type: string
        format: date-time
        description: Creation time
        example: "2015-07-07T15:49:51.230+02:00"
        readOnly: true

#orm.py 
from sqlalchemy import Column, DateTime, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()


class Pet(Base):
    __tablename__ = 'pets'
    id = Column(String(20), primary_key=True)
    name = Column(String(100))
    animal_type = Column(String(20))
    created = Column(DateTime())

    def update(self, id=None, name=None, animal_type=None, tags=None, created=None):
        if name is not None:
            self.name = name
        if animal_type is not None:
            self.animal_type = animal_type
        if created is not None:
            self.created = created

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])


def init_db(uri):
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session

#api.py 
import datetime
import logging

import connexion
from connexion import NoContent

import orm

db_session = None


def get_pets(limit, animal_type=None):
    q = db_session.query(orm.Pet)
    if animal_type:
        q = q.filter(orm.Pet.animal_type == animal_type)
    return [p.dump() for p in q][:limit]


def get_pet(pet_id):
    pet = db_session.query(orm.Pet).filter(orm.Pet.id == pet_id).one_or_none()
    return pet.dump() if pet is not None else ('Not found', 404)


def put_pet(pet_id, pet):
    p = db_session.query(orm.Pet).filter(orm.Pet.id == pet_id).one_or_none()
    pet['id'] = pet_id
    if p is not None:
        logging.info('Updating pet %s..', pet_id)
        p.update(**pet)
    else:
        logging.info('Creating pet %s..', pet_id)
        pet['created'] = datetime.datetime.utcnow()
        db_session.add(orm.Pet(**pet))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)


def delete_pet(pet_id):
    pet = db_session.query(orm.Pet).filter(orm.Pet.id == pet_id).one_or_none()
    if pet is not None:
        logging.info('Deleting pet %s..', pet_id)
        db_session.query(orm.Pet).filter(orm.Pet.id == pet_id).delete()
        db_session.commit()
        return NoContent, 204
    else:
        return NoContent, 404

logging.basicConfig(level=logging.INFO)
db_session = orm.init_db('sqlite:///:memory:')
app = connexion.FlaskApp(__name__)
app.add_api('swagger.yaml')

application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(
        port=8080,
        threaded=False  # in-memory database isn't shared across threads
    )


    
###Connexion - Security 


##OAuth 2 Authentication and Authorization

Connexion supports one of the three OAuth 2 handling methods. 
With Connexion, the API security definition must include a x-tokenInfoFunc 
or set TOKENINFO_FUNC env var.


x-tokenInfoFunc must contain a reference to a function used to obtain the token info. 
This reference should be a string using the same syntax that is used to connect 
an operationId to a Python function when routing. 
For example, an x-tokenInfoFunc of auth.verifyToken would pass the user’s token string 
to the function verifyToken in the module auth.py. 
The referenced function accepts a token string as argument 
and should return a dict containing a scope field that is either a space-separated list 
or an array of scopes belonging to the supplied token. 
This list of scopes will be validated against the scopes required 
by the API security definition to determine if the user is authorized. 

You can supply a custom scope validation func with x-scopeValidateFunc 
or set SCOPEVALIDATE_FUNC env var, otherwise connexion.decorators.security.validate_scope will be used as default.

The recommended approach is to return a dict which complies with RFC 7662. 
Note that you have to validate the active or exp fields etc. yourself.

The sub property of the Token Info response will be passed in the user argument 
to the handler function.

##->file:oauth2_local_tokeninfo
$ python app.py

Now open your browser and go to http://localhost:8080/ui/ to see the Swagger UI.

You can use the hardcoded tokens to request the endpoint:
$ curl http://localhost:8080/secret   # missing authentication
$ curl -H 'Authorization: Bearer 123' http://localhost:8080/secret
$ curl -H 'Authorization: Bearer 456' http://localhost:8080/secret



##->file:oauth2_local_tokeninfo\app.yaml:
swagger: "2.0"

info:
  title: OAuth Example
  version: "1.0"

paths:
  /secret:
    get:
      summary: Return secret string
      operationId: app.get_secret
      responses:
        200:
          description: secret response
          schema:
            type: string
      security:
        # enable authentication and require the "uid" scope for this endpoint
        - oauth2: ['uid']

securityDefinitions:
  oauth2:
    type: oauth2
    flow: implicit
    authorizationUrl: https://example.com/oauth2/dialog
    x-tokenInfoFunc: app.token_info
    scopes:
      uid: Unique identifier of the user accessing the service.
   
##->file:oauth2_local_tokeninfo\app.py:
#!/usr/bin/env python3
'''
Basic example of a resource server
'''

import connexion

# our hardcoded mock "Bearer" access tokens
TOKENS = {
    '123': 'jdoe',
    '456': 'rms'
}


def get_secret(user) -> str:
    return 'You are: {uid}'.format(uid=user)


def token_info(access_token) -> dict:
    uid = TOKENS.get(access_token)
    if not uid:
        return None
    return {'uid': uid, 'scope': ['uid']}


if __name__ == '__main__':
    app = connexion.FlaskApp(__name__)
    app.add_api('app.yaml')
    app.run(port=8080)


   
    
##->file:oauth2
$ python mock_tokeninfo.py &                  # start mock in background
$ python app.py

Now open your browser and go to http://localhost:8080/ui/ to see the Swagger UI.





##->file:oauth2\app.yaml:
swagger: "2.0"

info:
  title: OAuth Example
  version: "1.0"

paths:
  /secret:
    get:
      summary: Return secret string
      operationId: app.get_secret
      responses:
        200:
          description: secret response
          schema:
            type: string
      security:
        # enable authentication and require the "uid" scope for this endpoint
        - oauth2: ['uid']

securityDefinitions:
  oauth2:
    type: oauth2
    flow: implicit
    authorizationUrl: https://example.com/oauth2/dialog
    # the token info URL is hardcoded for our mock_tokeninfo.py script
    # you can also pass it as an environment variable TOKENINFO_URL
    x-tokenInfoUrl: http://localhost:7979/tokeninfo
    scopes:
      uid: Unique identifier of the user accessing the service.

##->file:oauth2\app.py:
#!/usr/bin/env python3
'''
Basic example of a resource server
'''

import connexion


def get_secret(user) -> str:
    return 'You are: {uid}'.format(uid=user)


if __name__ == '__main__':
    app = connexion.FlaskApp(__name__)
    app.add_api('app.yaml')
    app.run(port=8080)





##->file:oauth2\mock_tokeninfo.yaml:
swagger: "2.0"

info:
  title: Mock OAuth Token Info
  version: "1.0"

paths:
  /tokeninfo:
    get:
      summary: OAuth2 token info
      operationId: mock_tokeninfo.get_tokeninfo
      responses:
        200:
          description: Token info object
          schema:
            type: object
            properties:
              uid:
                type: string
              scope:
                type: array
                items:
                  type: string


##->file:oauth2\mock_tokeninfo.py:
#!/usr/bin/env python3
'''
Mock OAuth2 token info
'''

import connexion
from connexion import request

# our hardcoded mock "Bearer" access tokens
TOKENS = {
    '123': 'jdoe',
    '456': 'rms'
}


def get_tokeninfo() -> dict:
    try:
        _, access_token = request.headers['Authorization'].split()
    except Exception:
        access_token = ''

    uid = TOKENS.get(access_token)

    if not uid:
        return 'No such token', 401

    return {'uid': uid, 'scope': ['uid']}


if __name__ == '__main__':
    app = connexion.FlaskApp(__name__)
    app.add_api('mock_tokeninfo.yaml')
    app.run(port=7979)


    
    


##Basic Authentication
With Connexion, the API security definition must include a x-basicInfoFunc 
or set BASICINFO_FUNC env var. 
It uses the same semantics as for x-tokenInfoFunc, 
but the function accepts three parameters: username, password and required_scopes. 

If the security declaration of the operation also has an oauth security requirement, 
required_scopes is taken from there, 
otherwise it’s None. This allows authorizing individual operations with oauth scope 
while using basic authentication for authentication.

##->file:basicauth
$ python app.py

Now open your browser and go to http://localhost:8080/ui/ to see the Swagger UI.
The hardcoded credentials are admin and secret.


##->file:basicauth\swagger.yaml:
swagger: "2.0"

info:
  title: Basic Auth Example
  version: "1.0"

paths:
  /secret:
    get:
      summary: Return secret string
      operationId: app.get_secret
      responses:
        200:
          description: secret response
          schema:
            type: string
      security:
        - basic: []
securityDefinitions:
  basic:
    type: basic
    x-basicInfoFunc: app.basic_auth




##->file:basicauth\app.py:
#!/usr/bin/env python3
'''
Basic example of a resource server
'''

import connexion


def basic_auth(username, password, required_scopes=None):
    if username == 'admin' and password == 'secret':
        return {'sub': 'admin'}

    # optional: raise exception for custom error response
    return None


def get_secret(user) -> str:
    return "You are {user} and the secret is 'wbevuec'".format(user=user)


if __name__ == '__main__':
    app = connexion.FlaskApp(__name__)
    app.add_api('swagger.yaml')
    app.run(port=8080)



##ApiKey Authentication
With Connexion, the API security definition must include a x-apikeyInfoFunc 
or set APIKEYINFO_FUNC env var. 

It uses the same semantics as for x-basicInfoFunc, 
but the function accepts two parameters: apikey and required_scopes.


##Bearer Authentication (JWT)

With Connexion, the API security definition must include a x-bearerInfoFunc 
or set BEARERINFO_FUNC env var. 
It uses the same semantics as for x-tokenInfoFunc, 
but the function accepts one parameter: token.

##HTTPS Support
When specifying HTTPS as the scheme in the API YAML file, 
all the URIs in the served Swagger UI are HTTPS endpoints. 
The problem: The default server that runs is a 'normal' HTTP server. 
This means that the Swagger UI cannot be used to play with the API. 
What is the correct way to start a HTTPS server when using Connexion?








###Connexion - Complex example
#Details- https://realpython.com/flask-connexion-rest-api-part-2/ 

##Project structure 
project
  build_database.py
  code.txt
  config.py
  models.py
  people.py
  server.py
  swagger.yml
  __init__.py
   static
       css
           home.css    
       js
          home.js
   templates
       home.html

##->file:config.py:
import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
#App = FlaskApp, has all app.* methods from Flask 
#or if aiohttp based use AioHttpApp
connex_app = connexion.FlaskApp(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Build the Sqlite ULR for SqlAlchemy
sqlite_url = "sqlite:////" + os.path.join(basedir, "people.db")

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)


##->file:server.py:
"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template

# local modules
import config


# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")


# create a URL route in our application for "/"
@connex_app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/

    :return:        the rendered template "home.html"
    """
    return render_template("home.html")


if __name__ == "__main__":
    connex_app.run(debug=True)


##->file:build_database.py:
import os
from config import db
from models import Person

# Data to initialize database with
PEOPLE = [
    {"fname": "Doug", "lname": "Farrell"},
    {"fname": "Kent", "lname": "Brockman"},
    {"fname": "Bunny", "lname": "Easter"},
]

# Delete database file if it exists currently
if os.path.exists("people.db"):
    os.remove("people.db")

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for person in PEOPLE:
    p = Person(lname=person.get("lname"), fname=person.get("fname"))
    db.session.add(p)

db.session.commit()


##->file:models.py:
from datetime import datetime
from config import db, ma


class Person(db.Model):
    __tablename__ = "person"
    person_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32))
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class PersonSchema(ma.ModelSchema):
    class Meta:
        model = Person
        sqla_session = db.session








##->file:swagger.yml:
swagger: "2.0"
info:
  description: This is the swagger file that goes with our server code
  version: "1.0.0"
  title: Swagger Rest Article
consumes:
  - application/json
produces:
  - application/json

basePath: /api

# Paths supported by the server application
paths:
  /people:
    get:
      operationId: people.read_all
      tags:
        - People
      summary: Read the entire set of people, sorted by last name
      description: Read the entire set of people, sorted by last name
      responses:
        200:
          description: Successfully read people set operation
          schema:
            type: array
            items:
              properties:
                person_id:
                  type: string
                  description: Id of the person
                fname:
                  type: string
                  description: First name of the person
                lname:
                  type: string
                  description: Last name of the person
                timestamp:
                  type: string
                  description: Creation/Update timestamp of the person

    post:
      operationId: people.create
      tags:
        - People
      summary: Create a person
      description: Create a new person
      parameters:
        - name: person
          in: body
          description: Person to create
          required: True
          schema:
            type: object
            properties:
              fname:
                type: string
                description: First name of person to create
              lname:
                type: string
                description: Last name of person to create
      responses:
        201:
          description: Successfully created person
          schema:
            properties:
              person_id:
                type: string
                description: Id of the person
              fname:
                type: string
                description: First name of the person
              lname:
                type: string
                description: Last name of the person
              timestamp:
                type: string
                description: Creation/Update timestamp of the person record

  /people/{person_id}:
    get:
      operationId: people.read_one
      tags:
        - People
      summary: Read one person
      description: Read one person
      parameters:
        - name: person_id
          in: path
          description: Id of the person to get
          type: integer
          required: True
      responses:
        200:
          description: Successfully read person from people data operation
          schema:
            type: object
            properties:
              person_id:
                type: string
                description: Id of the person
              fname:
                type: string
                description: First name of the person
              lname:
                type: string
                description: Last name of the person
              timestamp:
                type: string
                description: Creation/Update timestamp of the person record

    put:
      operationId: people.update
      tags:
        - People
      summary: Update a person
      description: Update a person
      parameters:
        - name: person_id
          in: path
          description: Id the person to update
          type: integer
          required: True
        - name: person
          in: body
          schema:
            type: object
            properties:
              fname:
                type: string
                description: First name of the person
              lname:
                type: string
                description: Last name of the person
      responses:
        200:
          description: Successfully updated person
          schema:
            properties:
              person_id:
                type: string
                description: Id of the person in the database
              fname:
                type: string
                description: First name of the person
              lname:
                type: string
                description: Last name of the person
              timestamp:
                type: string
                description: Creation/Update timestamp of the person record

    delete:
      operationId: people.delete
      tags:
        - People
      summary: Delete a person from the people list
      description: Delete a person
      parameters:
        - name: person_id
          in: path
          type: integer
          description: Id of the person to delete
          required: true
      responses:
        200:
          description: Successfully deleted a person



##->file:people.py:
"""
This is the people module and supports all the REST actions for the
people data
"""

from flask import make_response, abort
from config import db
from models import Person, PersonSchema


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people

    :return:        json string of list of people
    """
    # Create the list of people from our data
    people = Person.query.order_by(Person.lname).all()

    # Serialize the data for the response
    person_schema = PersonSchema(many=True)
    data = person_schema.dump(people).data
    return data


def read_one(person_id):
    """
    This function responds to a request for /api/people/{person_id}
    with one matching person from people

    :param person_id:   Id of person to find
    :return:            person matching id
    """
    # Get the person requested
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    # Did we find a person?
    if person is not None:

        # Serialize the data for the response
        person_schema = PersonSchema()
        data = person_schema.dump(person).data
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(
            404,
            "Person not found for Id: {person_id}".format(person_id=person_id),
        )


def create(person):
    """
    This function creates a new person in the people structure
    based on the passed in person data

    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    fname = person.get("fname")
    lname = person.get("lname")

    existing_person = (
        Person.query.filter(Person.fname == fname)
        .filter(Person.lname == lname)
        .one_or_none()
    )

    # Can we insert this person?
    if existing_person is None:

        # Create a person instance using the schema and the passed in person
        schema = PersonSchema()
        new_person = schema.load(person, session=db.session).data

        # Add the person to the database
        db.session.add(new_person)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_person).data

        return data, 201

    # Otherwise, nope, person exists already
    else:
        abort(
            409,
            "Person {fname} {lname} exists already".format(
                fname=fname, lname=lname
            ),
        )


def update(person_id, person):
    """
    This function updates an existing person in the people structure
    Throws an error if a person with the name we want to update to
    already exists in the database.

    :param person_id:   Id of the person to update in the people structure
    :param person:      person to update
    :return:            updated person structure
    """
    # Get the person requested from the db into session
    update_person = Person.query.filter(
        Person.person_id == person_id
    ).one_or_none()

    # Try to find an existing person with the same name as the update
    fname = person.get("fname")
    lname = person.get("lname")

    existing_person = (
        Person.query.filter(Person.fname == fname)
        .filter(Person.lname == lname)
        .one_or_none()
    )

    # Are we trying to find a person that does not exist?
    if update_person is None:
        abort(
            404,
            "Person not found for Id: {person_id}".format(person_id=person_id),
        )

    # Would our update create a duplicate of another person already existing?
    elif (
        existing_person is not None and existing_person.person_id != person_id
    ):
        abort(
            409,
            "Person {fname} {lname} exists already".format(
                fname=fname, lname=lname
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in person into a db object
        schema = PersonSchema()
        update = schema.load(person, session=db.session).data

        # Set the id to the person we want to update
        update.person_id = update_person.person_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_person).data

        return data, 200


def delete(person_id):
    """
    This function deletes a person from the people structure

    :param person_id:   Id of the person to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the person requested
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    # Did we find a person?
    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return make_response(
            "Person {person_id} deleted".format(person_id=person_id), 200
        )

    # Otherwise, nope, didn't find that person
    else:
        abort(
            404,
            "Person not found for Id: {person_id}".format(person_id=person_id),
        )



##->file:templates\home.html:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Application Home Page</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.0/normalize.min.css">
    <link rel="stylesheet" href="static/css/home.css">
    <script
      src="http://code.jquery.com/jquery-3.3.1.min.js"
      integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
      crossorigin="anonymous">
    </script>
</head>
<body>
    <div class="container">
        <h1 class="banner">People Demo Application</h1>
        <div class="section editor">
            <input id="person_id" type="hidden" value="" />
            <label for="fname">First Name
                <input id="fname" type="text" />
            </label>
            <br />
            <label for="lname">Last Name
                <input id="lname" type="text" />
            </label>
            <br />
            <button id="create">Create</button>
            <button id="update">Update</button>
            <button id="delete">Delete</button>
            <button id="reset">Reset</button>
        </div>
        <div class="people">
            <table>
                <caption>People</caption>
                <thead>
                    <tr>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Update Time</th>
                    </tr>
                </thead>
                <tbody>
                </tbody>
            </table>
        </div>
        <div class="error">
        </div>
    </div>
</body>
<script src="static/js/home.js"></script>
</html>



##->file:static\js\home.js:
/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/people',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(person) {
            let ajax_options = {
                type: 'POST',
                url: 'api/people',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(person)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(person) {
            let ajax_options = {
                type: 'PUT',
                url: `api/people/${person.person_id}`,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(person)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'delete': function(person_id) {
            let ajax_options = {
                type: 'DELETE',
                url: `api/people/${person_id}`,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $person_id = $('#person_id'),
        $fname = $('#fname'),
        $lname = $('#lname');

    // return the API
    return {
        reset: function() {
            $person_id.val('');
            $lname.val('');
            $fname.val('').focus();
        },
        update_editor: function(person) {
            $person_id.val(person.person_id);
            $lname.val(person.lname);
            $fname.val(person.fname).focus();
        },
        build_table: function(people) {
            let rows = ''

            // clear the table
            $('.people table > tbody').empty();

            // did we get a people array?
            if (people) {
                for (let i=0, l=people.length; i < l; i++) {
                    rows += `<tr data-person-id="${people[i].person_id}">
                        <td class="fname">${people[i].fname}</td>
                        <td class="lname">${people[i].lname}</td>
                        <td>${people[i].timestamp}</td>
                    </tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $person_id = $('#person_id'),
        $fname = $('#fname'),
        $lname = $('#lname');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(fname, lname) {
        return fname !== "" && lname !== "";
    }

    // Create our event handlers
    $('#create').click(function(e) {
        let fname = $fname.val(),
            lname = $lname.val();

        e.preventDefault();

        if (validate(fname, lname)) {
            model.create({
                'fname': fname,
                'lname': lname,
            })
        } else {
            alert('Problem with first or last name input');
        }
    });

    $('#update').click(function(e) {
        let person_id = $person_id.val(),
            fname = $fname.val(),
            lname = $lname.val();

        e.preventDefault();

        if (validate(fname, lname)) {
            model.update({
                person_id: person_id,
                fname: fname,
                lname: lname,
            })
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#delete').click(function(e) {
        let person_id = $person_id.val();

        e.preventDefault();

        if (validate('placeholder', lname)) {
            model.delete(person_id)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#reset').click(function() {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            person_id,
            fname,
            lname;

        person_id = $target
            .parent()
            .attr('data-person-id');

        fname = $target
            .parent()
            .find('td.fname')
            .text();

        lname = $target
            .parent()
            .find('td.lname')
            .text();

        view.update_editor({
            person_id: person_id,
            fname: fname,
            lname: lname,
        });
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));







##->file:static\css\home.css:
/*
 * This is the CSS stylesheet for the demo people application
 */

@import url(http://fonts.googleapis.com/css?family=Roboto:400,300,500,700);

body, .ui-btn {
    font-family: Roboto;
}

.container {
    padding: 10px;
}

.banner {
    text-align: center;
}

.editor {
    width: 50%;
    margin-left: auto;
    margin-right: auto;
    padding: 5px;
    border: 1px solid lightgrey;
    border-radius: 3px;
    margin-bottom: 5px;
}

label {
    display: inline-block;
    margin-bottom: 5px;
}

button {
    padding: 5px;
    margin-right: 5px;
    border-radius: 3px;
    background-color: #eee;
}

.people {
    width: 50%;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 5px;
}

table {
    width: 100%;
    border-collapse: collapse;
}

table, caption, th, td {
    border: 1px solid lightgrey;
}

table caption {
    height: 33px;
    font-weight: bold;
    padding-top: 5px;
    border-bottom: none;
}

tr {
    height: 33px;
}

tr:nth-child(even) {
    background-color: #f0f0f0
}

td {
    text-align: center;
}

.error {
    width: 50%;
    margin-left: auto;
    margin-right: auto;
    padding: 5px;
    border: 1px solid lightgrey;
    border-radius: 3px;
    background-color: #fbb;
    visibility: hidden;
}


##Quick Aiohttp 
#(requires min python 3.5.3+)
from aiohttp import web

async def handle(request):
    text = "Hello, World"
    #Response(*, body=None, status=200, reason=None, text=None, headers=None, content_type=None, charset=None, zlib_executor_size=sentinel, zlib_executor=None)
    return web.Response(text=text) 
    
async def post_handler(request):
    #GET data 
    #methods: getall(key[, default]), get(key[, default]), key in d
    gets = list(request.query.items())
    #post BODY  
    #posts = await requests.post() #methods: getall(key[, default]), get(key[, default]), key in d
    #text body 
    #posts = await requests.text()
    #json body 
    posts = await request.json() #python obj
    #Query String , .path, .query_string
    q = [ request.path_qs, #The URL including PATH_INFO and the query string
          request.path, #The URL including PATH INFO without the host or scheme
          request.raw_path,  #path may be URL-encoded 
          request.query_string,
          str(request.query),  #A multidict with all the variables in the query string.
          str(request.headers),  #A case-insensitive multidict proxy with all headers
          str(request.cookies), #A multidict of all request’s cookies.
        ]
    #Method 
    m = [request.method, request.content_type  , request.host, request.remote]
    #data 
    data = dict(query=gets, json=posts, q=q, m=m)
    return web.json_response(data)
    
async def handle_json(request):
    name = request.match_info.get('name', "Anonymous") # from PATH template 
    data = {'name': name}
    return web.json_response(data)

app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/{name}', handle_json)
app.router.add_post('/post', post_handler)             
               
#aiohttp.web.run_app(app, *, host=None, port=None, path=None, sock=None, shutdown_timeout=60.0, ssl_context=None, print=print, backlog=128, access_log_class=aiohttp.helpers.AccessLogger, access_log_format=aiohttp.helpers.AccessLogger.LOG_FORMAT, access_log=aiohttp.log.access_logger, handle_signals=True, reuse_address=None, reuse_port=None)               
web.run_app(app) 

##CLient 
#http://localhost:8080/
#http://localhost:8080/das
#http://localhost:8080/post?name=das or with post json 

import aiohttp
import asyncio
import json 

async def fetch(session, url):    
    data = dict(name='das')
    headers = {'Content-Type': 'application/json'}
    #for json,  post(url,json=data)
    #for query, .get(url, params=query_dict)
    #for post data , post(url, data=post_dict)
    async with session.post(url,data=json.dumps(data), headers=headers) as response:
        # rsp.text() or rsp.text(encoding='windows-1251'), resp.read() for binary body 
        return await response.json()  

async def main(loop):
    timeout = aiohttp.ClientTimeout(total=60.0)
    #timeout can be part of .get, .post etc 
    async with aiohttp.ClientSession(loop=loop, timeout=timeout) as session:
        result = await fetch(session, 'http://localhost:8080/post?name=das')
    return result

async def cookie():
    #ClientSession may be used for sharing cookies between multiple requests:
    async with aiohttp.ClientSession() as session:
        await session.get('http://httpbin.org/cookies/set?my_cookie=my_value')
        filtered = session.cookie_jar.filter_cookies('http://httpbin.org')
        assert filtered['my_cookie'].value == 'my_value'
        async with session.get('http://httpbin.org/cookies') as r:
            json_body = await r.json()
            assert json_body['cookies']['my_cookie'] == 'my_value'
            assert resp.headers['Content-Type'] == 'application/json'

async def few_info():
    async with aiohttp.ClientSession() as session:
        resp = await session.get('http://example.com/some/redirect/')
        assert resp.status == 200
        assert resp.url == URL('http://example.com/some/other/url/')
        assert len(resp.history) == 1
        assert resp.history[0].status == 301
        assert resp.history[0].url == URL('http://example.com/some/redirect/')            

async def download_large(filename, chunk_size=1024*1024):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.github.com/events') as resp:    
            with open(filename, 'wb') as fd:
                while True:
                    chunk = await resp.content.read(chunk_size)
                    if not chunk:
                        break
                    fd.write(chunk)

async def send_file():
    async with aiohttp.ClientSession() as session:
        url = 'http://httpbin.org/post'
        data = aiohttp.FormData()
        data.add_field('file',
                       open('report.xls', 'rb'),
                       filename='report.xls',
                       content_type='application/vnd.ms-excel')
        await session.post(url, data=data)    

async def send_large_file():
    async with aiohttp.ClientSession() as session:
        with open('report.xls', 'rb') as f:
           await session.post('http://httpbin.org/post', data=f)  
        #or chain 
        resp = await session.get('http://python.org')
        await session.post('http://httpbin.org/post', data=resp.content)

async def proxy():
    async with aiohttp.ClientSession() as session:
        proxy_auth = aiohttp.BasicAuth('user', 'pass')
        async with session.get("http://python.org",
                               proxy="http://proxy.com",
                               proxy_auth=proxy_auth) as resp:
            print(resp.status)   

loop = asyncio.get_event_loop()
result = loop.run_until_complete(main(loop))
# Zero-sleep to allow underlying connections to close
loop.run_until_complete(asyncio.sleep(0)) #for SSL, use 0.250
loop.close()

#SSL 
#By default aiohttp uses strict checks for HTTPS protocol. 
#Certification checks can be relaxed by setting ssl to False:

r = await session.get('https://example.com', ssl=False)

#or with sslContext 
import ssl 
sslcontext = ssl.create_default_context( cafile='/path/to/ca-bundle.crt')
r = await session.get('https://example.com', ssl=sslcontext)

#with self signed 
sslcontext = ssl.create_default_context( cafile='/path/to/ca-bundle.crt')
sslcontext.load_cert_chain('/path/to/client/public/device.pem',
                           '/path/to/client/private/device.key')
r = await session.get('https://example.com', ssl=sslcontext)


##Complex code 
from aiohttp import web
import aiohttp.web, aiohttp_jinja2, aiohttp_session
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import logging
import os,  uuid, shutil, asyncio , functools
import mimetypes, jinja2
from bs4 import BeautifulSoup
import lxml.etree # not used directly
import base64
from cryptography import fernet
from html import escape as html_escape
import multidict, urllib.parse
import aiosqlite
import aiohttp_csrf

routes = web.RouteTableDef()
logging.basicConfig(level=logging.DEBUG)

async def reverse_url(request, id, *args, **kwargs):
    """
    id is route name 
    args= query string eg "a=b"
    kwargs = path arg        
    """
    if args and kwargs:
        return request.app.router[id].url_for(**kwargs).with_query(*args)
    if args:
        return request.app.router[id].url_for().with_query(*args)
    if kwargs:
        return request.app.router[id].url_for(**kwargs)
    else:
        return request.app.router[id].url_for()
    
def debug_log_all(request):  
    q = [ request.headers.get('Referer', "NOReferer"),
          request.url, 
          request.path_qs, #The URL including PATH_INFO and the query string
          request.path, #The URL including PATH INFO without the host or scheme
          request.raw_path,  #path may be URL-encoded 
          request.query_string,
          str(request.query),  #A multidict with all the variables in the query string.
          str(request.headers),  #A case-insensitive multidict proxy with all headers
          str(request.cookies), #A multidict of all request’s cookies.
          str(list(request.keys())),
        ] 
    logging.debug(str(q))
    
@routes.get('/')
async def home(request):
    return web.Response(text= """
        <html><body>
        <h1 id="some1" class="some">Hello there!!</h1>
        <h1 id="some2" class="some">Hello there!!</h1>
        </body></html>    
        """, content_type="text/html") 
        
        
'''
url = request.app.router['user-info'].url_for(user='john_doe')
url_with_qs = url.with_query("a=b")
assert url_with_qs == '/john_doe/info?a=b'
'''

@routes.get('/main')   
def main_handler2(request):
    return web.Response(text= '<a href="%s">link to story 1</a>' %
                   request.app.router['story'].url_for(story_id="1"), content_type="text/html") 
                   
                   
@routes.get('/story/{story_id:\d+}', name='story')
def story_handler(request):
        return web.Response(text= 'this is story %s' % request.match_info['story_id'])
        
        
#template 
#Handlers should be coroutines accepting self only and returning response object 
#as regular web-handler. Request object can be retrieved by View.request property.
@routes.view('/env', name="env")
class MyFormHandler(aiohttp.web.View):
    def reverse_url(self, id, *args, **kwargs):
        """
        id is route name 
        args= query string eg "a=b"
        kwargs = path arg        
        """
        if args and kwargs:
            return self.request.app.router[id].url_for(**kwargs).with_query(*args)
        else:
            return self.request.app.router[id].url_for()
        if args:
            return self.request.app.router[id].url_for().with_query(*args)
        if kwargs:
            return self.request.app.router[id].url_for(**kwargs)
        
    #aiohttp_jinja2.template() should be applied before RouteTableDef.get() decorator 
    #and family, e.g. it must be the first (most down decorator in the chain):    
    @aiohttp_jinja2.template("env_get.html")
    async def get(self):
        #RequestHandler.render_string(template_name: str, **kwargs) -> bytes
        #could have used self.write(html_string) but to support xsrf use below 
        return dict(url= await reverse_url(self.request, "env"))
                 
    @aiohttp_jinja2.template("env.html")                 
    async def post(self):
        posts = await self.request.post()
        logging.debug(str(posts))
        envp = posts.get("envp","all").upper()
        env_dict = os.environ
        if os.environ.get(envp, "notfound") != "notfound":
            env_dict = { envp : os.environ.get(envp,"notfound") } 
        #logging.debug(str(env_dict))
        return dict(envs=env_dict.copy())  

'''
from jinja2 import * 
import os 
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(['html', 'xml'])
)
t = env.get_template('base.html')

s = t.render(envs=os.environ)


'''        
#Json,XML 

@routes.get('/helloj/{name:.*}') 
async def handle_json(request):
    def get_name(request,jdata):
        qname = request.query.get("name", None)
        jname = jdata.get("name", None)
        pname = request.match_info.get('name', None) # could be empty 
        logging.debug("qname<%s> jname<%s>/jdata<%s> pname<%s>" % (qname,jname,jdata,pname,))
        res = pname 
        if not res:
            if not jname:
                res = qname 
            else:
                res = jname 
        return res or "Jane Doe"
    name = get_name(request, await request.json() if request.body_exists else {} )
    data = {'name': name}
    return web.json_response(data)

@routes.get('/hellox/{name:.*}') 
async def handle_json(request):
    def name_xml(request,text):
        if request.headers.get('Content-Type', "other") == 'application/xml':
            soup = BeautifulSoup(text, 'xml')
            name = soup.find("name")
            return name.text if name else None 
        return None             
    def get_name(request, text):
        qname = request.query.get("name", None)
        xname = name_xml(request, text)
        pname = request.match_info.get('name', None)
        logging.debug("qname<%s> xname<%s>/text<%s> pname<%s>" % (qname,xname,text,pname,))
        res = pname 
        if not res:
            if not xname:
                res = qname 
            else:
                res = xname 
        return res or "Jane Doe"
    name = get_name(request, await request.text() if request.body_exists else {} )
    return web.Response(text= """
        <data><name>%s</name><age>%d</age></data>            
        """ %(name, 200), content_type="application/xml")
        
#login     
@aiohttp.web.middleware
async def current_user_middleware(request, handler):
    session = await aiohttp_session.get_session(request)
    request['current_user'] = session['current_user'] if 'current_user' in session else None
    resp = await handler(request)
    return resp


@routes.view('/login', name="login")
class LoginHandler(aiohttp.web.View):        
    def check_auth(self, username, password):
        return username == 'admin' and password == 'secret'
        
    def handle_post_query(self, url):
        charset =  self.request.charset or 'utf-8'
        posts = multidict.MultiDict()
        o = urllib.parse.urlparse(url)
        posts.extend(urllib.parse.parse_qsl(
                        qs=o.query,
                        keep_blank_values=True,
                        encoding=charset))
        return posts
        
    @aiohttp_jinja2.template("login.html")
    async def get(self):
        return dict(url=await reverse_url(self.request, "login"))

    async def post(self):        
        #debug_log_all(self.request)
        posts = await self.request.post()
        name = posts.get("name",None)
        password = posts.get("password", None) 
        if self.check_auth(name, password):
            session = await aiohttp_session.get_session(self.request)
            session['current_user'] = name 
            #aiohttp does not handle post query!!, so below hack 
            post_query = self.handle_post_query(self.request.headers['Referer'])
            #logging.debug(str(post_query))
            location = post_query.get("next", None) or (await reverse_url(self.request,"secure_site")) 
            raise aiohttp.web.HTTPFound(location=location) # redirect via raise
        else:
            location = await reverse_url(self.request, "login")
            raise aiohttp.web.HTTPFound(location=location) # redirect via raise 
            
    
def requires_auth(func):
    async def decorated(self, *args, **kwargs):
        request = None 
        try:
            request = self.request
        except:
            request = self
        us = request['current_user']
        if not us : 
            location = await reverse_url(request, "login", "next=%s" %(request.rel_url,))
            raise aiohttp.web.HTTPFound(location=location)  #method name ?next=curr
        if asyncio.iscoroutinefunction(func):
            coro = func
        else:
            coro = asyncio.coroutine(func)
        res = await coro(request, *args, **kwargs)
        return res
    return decorated
    
    
@routes.view('/secure', name="secure_site")
class SecureMainHandler(aiohttp.web.View):
    @requires_auth
    async def get(self):
        name = "ok" # html_escape(self.request['current_user'])
        return web.Response(text="Hello, " + name)  
        
        
@routes.get('/logout')        
@requires_auth
async def logout(request):
    session = await aiohttp_session.get_session(request)
    session['current_user'] = None 
    return web.Response(text="loggedout")       

        
#DB         
class NoResult(Exception):
    pass
        
class DBApi:
    def __init__(self, db):
        self.db = db
    def row_to_obj(self, row, cur):
        obj = {}
        for val, desc in zip(row, cur.description):
            obj[desc[0]] = val #first one is name 
        return obj        
        
    async def query(self, stmt, *args):
        async with aiosqlite.connect(self.db) as db:
            db.row_factory = aiosqlite.Row 
            async with db.execute(stmt, args) as cur:
                #in python3.6, https://www.python.org/dev/peps/pep-0530/#implementation
                #return [self.row_to_obj(row, cur) async for row in cur.fetchall()]
                return [self.row_to_obj(row, cur) for row in await cur.fetchall()]
                
    async def queryone(self, stmt, *args):
        results = await self.query(stmt, *args)
        if len(results) >= 0 :
            return results[0] 
        else:
            raise NoResult("No result")
            
async def maybe_create_tables(app):   
    logging.debug("DBPATH=%s" % (app['dbpath'], ))
    async with aiosqlite.connect(app['dbpath']) as db:
        try:
            async with db.execute("SELECT COUNT(*) FROM people LIMIT 1") as cursor:
                await cursor.fetchone()
        except :                
            await db.execute("""create table if not exists people (name string, age int)""")
            await db.execute("""insert into people values(?,?) """, ('xyz',20))
            await db.execute("""insert into people values(?,?) """, ('abc',20))
            await db.commit()

            
@routes.view("/db/{name:.*}", name="db")    
class DBHandler(aiohttp.web.View):
    async def get(self):
        name = self.request.match_info.get('name', None)
        try:
            if not name:
                people = await DBApi(app['dbpath']).query(
                    "SELECT * FROM people"
                )
                obj = {'all': people}
            else:
                entries = await DBApi(app['dbpath']).queryone(
                    "SELECT * FROM people where name=?", name
                )
                #find age , each row is dict because of db.row_factory = aiosqlite.Row
                obj = {'name': name, 'age': entries['age']}
        except Exception as ex:
            obj={'message': str(ex)}
        return web.json_response(obj)    
        
        
        
    
#Upload and download 
#CSRF 
async def setup_csrf(app):
    csrf_policy = aiohttp_csrf.policy.FormPolicyWithMultipart(app['FORM_FIELD_NAME'])
    csrf_storage = aiohttp_csrf.storage.CookieStorage(app['COOKIE_NAME'])
    aiohttp_csrf.setup(app, policy=csrf_policy, storage=csrf_storage)
    
    
@routes.view("/upload", name="upload")  
class UploadPOSTHandler(aiohttp.web.View):
    @aiohttp_csrf.csrf_protect
    @aiohttp_jinja2.template("upload.html")
    async def get(self):
        token = await aiohttp_csrf.generate_token(self.request)
        return dict(token_name=self.request.app['FORM_FIELD_NAME'], token=token)
        
    @aiohttp_csrf.csrf_protect
    async def post(self):   
        debug_log_all(self.request)
        reader = await self.request.multipart()
        # reader.next() will `yield` the fields of your form
        #so for other form fields 
        # field = await reader.next()
        # assert field.name == 'name'
        # name = await field.read(decode=True) #get value 
        # in our case 'file'
        field = await reader.next()
        assert field.name == 'file'
        filename = field.filename
        # You cannot rely on Content-Length if transfer is chunked.
        size = 0
        try:
            with open(os.path.join(self.request.app['upload_path'], filename), 'wb') as f:
                while True:
                    chunk = await field.read_chunk()  # 8192 bytes by default.
                    if not chunk:
                        break
                    size += len(chunk)
                    f.write(chunk)
        except IOError as e:
            logging.error("Failed to write file due to IOError %s", str(e))            
        location = await reverse_url(self.request, "download", filename=filename)
        raise aiohttp.web.HTTPFound(location=location)
        #return web.Response(text='{} sized of {} successfully stored'.format(filename, size))
      

        
#Download 
@routes.view("/download/{filename}", name="download")  
class DownloadHandler(aiohttp.web.View):
    async def get(self):
        filename = self.request.match_info.get('filename', "default_name")
        # chunk size to read
        chunk_size = 1024 * 1024 * 8 # 8 MiB
        mtype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        headers = {}
        headers["Content-Disposition"] = 'attachment; filename="%s"' %(filename,) 
        headers["Content-Type"] =  mtype
        response = web.StreamResponse(status=200,reason='OK',headers=headers )    
        await response.prepare(self.request)  #start the response 
        with open(os.path.join(self.request.app['upload_path'],filename), 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                try:
                    await response.write(chunk) # write the cunk to response
                    await response.drain() # flush the current chunk to socket
                except Exception:
                    # this means the client has closed the connection
                    # so break the loop
                    break
                finally:
                    # deleting the chunk is very important because 
                    # if many clients are downloading files at the 
                    # same time, the chunks in memory will keep 
                    # increasing and will eat up the RAM
                    del chunk
                    # pause the coroutine so other handlers can run
                    await asyncio.sleep(0.000000001) # 1 nanosecond        
            await response.write_eof()
            return response


    

#CRTL+C handling 
#note loop once started , would check only any event in main thread 
#so crtl+c would be processed only when events reach to loop 
#iether by one browser url or via below method 

async def call_periodic(app, sleep, func):
    while True:
        func()
        await asyncio.sleep(sleep)

        
async def start_background_tasks(app,sleep, func):
    app['periodic'] = app.loop.create_task(call_periodic(app,sleep, func)) #every 5 seconds 


async def cleanup_background_tasks(app):
    app['periodic'].cancel()
    await app['periodic']

    
if __name__ == '__main__':
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": b'CvkgfR6WATWuWnJPLJWrcWHslRW9893sNPwl1Ko7qhk=', #fernet.Fernet.generate_key()
        'template_path': os.path.join(os.path.dirname(__file__), "templates"),
        "upload_path": os.path.join(os.path.dirname(__file__), "uploads"),
        'dbpath' : os.path.join(os.path.dirname(__file__), "people.db"),
        'FORM_FIELD_NAME' : '_csrf_token',
        'COOKIE_NAME' : 'csrf_token',
        }
    app = web.Application()
    #update static , now view function can access, request.app['key']
    for k, v in settings.items():
        app[k] = v 
    #session middleware must be first 
    secret_key = base64.urlsafe_b64decode(app['cookie_secret'])
    aiohttp_session.setup(app, EncryptedCookieStorage(secret_key))
    #then other middle ware 
    app.middlewares.append(current_user_middleware)
    #add routes 
    app.add_routes(routes)
    #static file 
    app.add_routes([web.static('/static', app['static_path']), ])
    #jinja setup , adds middleware 
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(app['template_path']))
    
    #signals
    app.on_startup.append(functools.partial(start_background_tasks, sleep=5, func=lambda:None))
    app.on_startup.append(maybe_create_tables)
    app.on_cleanup.append(cleanup_background_tasks)
    #csrf setup 
    app.on_startup.append(setup_csrf)
    
    web.run_app(app) 
    
'''
Urls 
http://localhost:8080/
http://localhost:8080/static/hello.html 

http://localhost:8080/main 
http://localhost:8080/story/2

http://localhost:8080/env

http://localhost:8080/helloj/das
http://localhost:8080/helloj/ with json  "{\"name\": \"dasn\"}"
http://localhost:8080/helloj/
http://localhost:8080/helloj/?name=dasq

http://localhost:8080/hellox/das
http://localhost:8080/hellox/ with <name>das</name> & application/xml


http://localhost:8080/secure
http://localhost:8080/login   with admin/secret
http://localhost:8080/logout

http://localhost:8080/upload
http://localhost:8080/download/data.jpg

http://localhost:8080/db/
http://localhost:8080/db/abc 


'''
#CSRF implementation 
https://github.com/asvetlov/aiohttp-csrf/tree/init
#take the above code , put in current directory 
#add in policy.py 
class FormPolicyWithMultipart(AbstractPolicy):

    def __init__(self, field_name):
        self.field_name = field_name

    async def check(self, request, original_value):
        reader = await request.multipart()
        field = await reader.next()
        assert field.name == self.field_name
        token = await field.read(decode=True)
        logging.debug('{} {}'.format(token.decode(), original_value))
        return token.decode() == original_value

#forms 


#->file:base.html:
<!DOCTYPE html>
<body>
{% block content %}   {# block can be inside another jinja2 statement #}
<table border="1">
<tr><th>Key</th><th>Value</th></tr>
{% if envs.items() %}  
{% for key,value in envs.items() %}

<tr>
<td>{{ key }}</td>
<td>{{ value }}</td>
</tr>

{% endfor %}
{% endif %}
</table>
{% endblock content %}
</body>
</html>


#->file:env.html:
{% extends "base.html" %}


{% block content %}
<table border="1">
<tr><th>Key</th><th>Value</th></tr>
{% if envs.items() %}  
{% for key,value in envs.items() %}
<tr style="background-color:lightgrey;">
<td style="color:red; font-style: bold;">{{ key }}</td>
<td>{{ value }}</td>
</tr>
{% endfor %}
{% endif %}
</table>
{% endblock content%}


#->file:env_get.html:
<html><body><form  action="{{url}}" method="POST">
Put env variable:
<input type="text" name="envp" value="ALL">
<input type="submit" value="Submit">
</form></body></html>


#->file:login.html:
<html><body><form  action="{{url}}" method="POST">
User Name: <input type="text" name="name"> <br/>
Password:<input type=password name="password">
<input type="submit" value="Sign in">
</form></body></html>


#->file:upload.html:
<!doctype html>
<title>Upload new File</title>
<body>
<h1>Upload new File</h1>
<form method="post" enctype="multipart/form-data">
{# add below at first #}
<input type="hidden" name="{{token_name}}" value="{{token}}" />
<input type=file name="file" />
<input type=submit value="Upload" />
</form>
</body></html>
        
   

###Logging

aiohttp uses following loggers (logging module) enumerated by names:
    'aiohttp.access'
    'aiohttp.client'
    'aiohttp.internal'
    'aiohttp.server'
    'aiohttp.web'
    'aiohttp.websocket'

#Set logging 
import logging
from aiohttp import web

app = web.Application()
logging.basicConfig(level=logging.DEBUG)
web.run_app(app, port=5000)

#Access logs
#Access logs are enabled by default. If the debug flag is set, 
and the default logger 'aiohttp.access' is used, 
access logs will be output to stderr if no handlers are attached. 

To override the default logger, pass an instance of logging.Logger to override the default logger.

web.run_app(app, access_log=None) to disable access logs.
In addition, access_log_format may be used to specify the log format.




### Web Server 

##Command Line Interface (CLI)

$ python -m aiohttp.web -H localhost -P 8080 package.module:init_func

package.module:init_func should be an importable callable 
that accepts a list of any non-parsed command-line arguments 
and returns an Application instance after setting it up:

def init_func(argv):
    app = web.Application()
    app.router.add_get("/", index_handler)
    return app

##Handler

async def handler(request):
    return web.Response()


app.add_routes([web.get('/', handler),
                web.post('/post', post_handler),
                web.put('/put', put_handler)])

#Or use route decorators:

routes = web.RouteTableDef()

@routes.get('/')
async def get_handler(request):
    ...

@routes.post('/post')
async def post_handler(request):
    ...

@routes.put('/put')
async def put_handler(request):
    ...

app.add_routes(routes)

#Wildcard HTTP method is also supported by route() or RouteTableDef.route(), 
#allowing a handler to serve incoming requests on a path having any HTTP method:

app.add_routes([web.route('*', '/path', all_handler)])

#By default endpoints added with GET method will accept HEAD requests 
#and return the same response headers as they would for a GET request. 
#You can also deny HEAD requests on a route:

web.get('/', handler, allow_head=False)


##Resources and Routes
Internally routes are served by Application.router (UrlDispatcher instance).

The router is a list of resources.
Resource is an entry in route table which corresponds to requested URL.
Resource in turn has at least one route.
Route corresponds to handling HTTP method by calling web handler.

The library implementation merges all subsequent route additions
for the same path adding the only resource for all HTTP methods.

Consider two examples:First one is optimized

app.add_routes([web.get('/path1', get_1),
                web.post('/path1', post_1),
                web.get('/path2', get_2),
                web.post('/path2', post_2)]

and:

app.add_routes([web.get('/path1', get_1),
                web.get('/path2', get_2),
                web.post('/path2', post_2),
                web.post('/path1', post_1)]


All registered resources in a router can be viewed using the 
UrlDispatcher.resources() method:

for resource in app.router.resources():
    print(resource)

A subset of the resources that were registered with a name 
can be viewed using the UrlDispatcher.named_resources() method:

for name, resource in app.router.named_resources().items():
    print(name, resource)

##File Uploads
make sure that the HTML <form> element has its enctype attribute set to 
enctype="multipart/form-data". 

<form action="/store/mp3" method="post" accept-charset="utf-8"
      enctype="multipart/form-data">

    <label for="mp3">Mp3</label>
    <input id="mp3" name="mp3" type="file" value=""/>

    <input type="submit" value="submit"/>
</form>

#Then, in the request handler you can access the file input field as a FileField instance. FileField is simply a container for the file as well as some of its metadata:
async def store_mp3_handler(request):

    # WARNING: don't do that if you plan to receive large files!
    data = await request.post()

    mp3 = data['mp3']

    # .filename contains the name of the file in string format.
    filename = mp3.filename

    # .file contains the actual file data that needs to be stored somewhere.
    mp3_file = data['mp3'].file

    content = mp3_file.read()

    return web.Response(body=content,
                        headers=MultiDict(
                            {'CONTENT-DISPOSITION': mp3_file}))


##WebSockets
To setup a WebSocket, create a WebSocketResponse in a request handler 
and then use it to communicate with the peer

Reading from the WebSocket (await ws.receive()) must only be done 
inside the request handler task; however, writing (ws.send_str(...)) to the WebSocket, 
closing (await ws.close()) and canceling the handler task may be delegated 
to other tasks. 

aiohttp.web creates an implicit asyncio.Task for handling every incoming request.
While aiohttp.web itself only supports WebSockets without downgrading to LONG-POLLING, etc., 
our team supports SockJS, an aiohttp-based library for implementing SockJS-compatible 
server code.

Parallel reads from websocket are forbidden, 
there is no possibility to call WebSocketResponse.receive() from two tasks.

import logging
import jinja2
import aiohttp_jinja2
from aiohttp import web
import aiohttp
from faker import Faker

log = logging.getLogger(__name__)


def get_random_name():
    fake = Faker()
    return fake.name()


async def index(request):
    ws_current = web.WebSocketResponse()
    ws_ready = ws_current.can_prepare(request)
    if not ws_ready.ok:
        return aiohttp_jinja2.render_template('index.html', request, {})

    await ws_current.prepare(request)

    name = get_random_name()
    log.info('%s joined.', name)

    await ws_current.send_json({'action': 'connect', 'name': name})

    for ws in request.app['websockets'].values():
        await ws.send_json({'action': 'join', 'name': name})
    request.app['websockets'][name] = ws_current

    while True:
        msg = await ws_current.receive()

        if msg.type == aiohttp.WSMsgType.text:
            for ws in request.app['websockets'].values():
                if ws is not ws_current:
                    await ws.send_json(
                        {'action': 'sent', 'name': name, 'text': msg.data})
        else:
            break

    del request.app['websockets'][name]
    log.info('%s disconnected.', name)
    for ws in request.app['websockets'].values():
        await ws.send_json({'action': 'disconnect', 'name': name})

    return ws_current

async def init_app():

    app = web.Application()

    app['websockets'] = {}

    app.on_shutdown.append(shutdown)

    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('aiohttpdemo_chat', 'templates'))

    app.router.add_get('/', index)

    return app


async def shutdown(app):
    for ws in app['websockets'].values():
        await ws.close()
    app['websockets'].clear()


def main():
    logging.basicConfig(level=logging.DEBUG)

    app = init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()

#index.html 
<!DOCTYPE html>
<meta charset="utf-8" />
<html>
  <head>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js">
    </script>
    <script language="javascript" type="text/javascript">
     $(function() {
       var conn = null;
       var name = "UNKNOWN";
       function log(msg) {
         var control = $('#log');
         var date = new Date();
         var date_prompt = '(' + date.toISOString().split('T')[1].slice(0,8) + ') ';
         control.html(control.html() + date_prompt + msg + '<br/>');
         control.scrollTop(control.scrollTop() + 1000);
       }
       function connect() {
         disconnect();
         var wsUri = (window.location.protocol=='https:'&&'wss://'||'ws://')+window.location.host;
         conn = new WebSocket(wsUri);
         //log('Connecting...');
         conn.onopen = function() {
           //log('Connected.');
           update_ui();
         };
         conn.onmessage = function(e) {
           var data = JSON.parse(e.data);
           switch (data.action) {
             case  'connect':
               name = data.name;
               log('Connected as ' + name);
               update_ui();
               break;
             case  'disconnect':
               name = data.name;
               log('Disconnected ' + name);
               update_ui();
               break;
             case 'join':
               log('Joined ' + data.name);
               break;
             case 'sent':
               log(data.name + ': ' + data.text);
               break;
           }
         };
         conn.onclose = function() {
           log('Disconnected.');
           conn = null;
           update_ui();
         };
       }
       function disconnect() {
         if (conn != null) {
           //log('Disconnecting...');
           conn.close();
           conn = null;
           name = 'UNKNOWN';
           update_ui();
         }
       }
       function update_ui() {
         if (conn == null) {
           $('#status').text('disconnected');
           $('#connect').html('Connect');
           $('#send').prop("disabled", true);
         } else {
           $('#status').text('connected (' + conn.protocol + ')');
           $('#connect').html('Disconnect');
           $('#send').prop("disabled", false);
         }
         $('#name').text(name);
       }
       $('#connect').on('click', function() {
         if (conn == null) {
           connect();
         } else {
           disconnect();
         }
         update_ui();
         return false;
       });
       $('#send').on('click', function() {
         var text = $('#text').val();
         // log('Sending: ' + text);
         log(text);
         conn.send(text);
         $('#text').val('').focus();
         return false;
       });
       $('#text').on('keyup', function(e) {
         if (e.keyCode === 13) {
           $('#send').click();
           return false;
         }
       });
     });
    </script>
  </head>
  <body>
    <h3>Chat!</h3>
    <div>
      <button id="connect">Connect</button>&nbsp;|&nbsp;Status:
      <span id="name">UNKNOWN</span>
      <span id="status">disconnected</span>
    </div>
    <div id="log"
         style="width:20em;height:15em;overflow:auto;border:1px solid black">
    </div>
    <form id="chatform" onsubmit="return false;">
      <input id="text" type="text" />
      <input id="send" type="button" value="Send" disabled/>
    </form>
  </body>
</html>


##Exceptions
aiohttp.web defines a set of exceptions for every HTTP status code.

Each exception is a subclass of HTTPException 
and relates to a single HTTP status code:

async def handler(request):
    raise aiohttp.web.HTTPFound('/redirect')


Each exception class has a status code according to RFC 2068: codes 
with 100-300 are not really errors; 400s are client errors, and 500s are server errors.

HTTP Exception hierarchy chart:

Exception
  HTTPException
    HTTPSuccessful
      * 200 - HTTPOk
      * 201 - HTTPCreated
      * 202 - HTTPAccepted
      * 203 - HTTPNonAuthoritativeInformation
      * 204 - HTTPNoContent
      * 205 - HTTPResetContent
      * 206 - HTTPPartialContent
    HTTPRedirection
      * 300 - HTTPMultipleChoices
      * 301 - HTTPMovedPermanently
      * 302 - HTTPFound
      * 303 - HTTPSeeOther
      * 304 - HTTPNotModified
      * 305 - HTTPUseProxy
      * 307 - HTTPTemporaryRedirect
      * 308 - HTTPPermanentRedirect
    HTTPError
      HTTPClientError
        * 400 - HTTPBadRequest
        * 401 - HTTPUnauthorized
        * 402 - HTTPPaymentRequired
        * 403 - HTTPForbidden
        * 404 - HTTPNotFound
        * 405 - HTTPMethodNotAllowed
        * 406 - HTTPNotAcceptable
        * 407 - HTTPProxyAuthenticationRequired
        * 408 - HTTPRequestTimeout
        * 409 - HTTPConflict
        * 410 - HTTPGone
        * 411 - HTTPLengthRequired
        * 412 - HTTPPreconditionFailed
        * 413 - HTTPRequestEntityTooLarge
        * 414 - HTTPRequestURITooLong
        * 415 - HTTPUnsupportedMediaType
        * 416 - HTTPRequestRangeNotSatisfiable
        * 417 - HTTPExpectationFailed
        * 421 - HTTPMisdirectedRequest
        * 422 - HTTPUnprocessableEntity
        * 424 - HTTPFailedDependency
        * 426 - HTTPUpgradeRequired
        * 428 - HTTPPreconditionRequired
        * 429 - HTTPTooManyRequests
        * 431 - HTTPRequestHeaderFieldsTooLarge
        * 451 - HTTPUnavailableForLegalReasons
      HTTPServerError
        * 500 - HTTPInternalServerError
        * 501 - HTTPNotImplemented
        * 502 - HTTPBadGateway
        * 503 - HTTPServiceUnavailable
        * 504 - HTTPGatewayTimeout
        * 505 - HTTPVersionNotSupported
        * 506 - HTTPVariantAlsoNegotiates
        * 507 - HTTPInsufficientStorage
        * 510 - HTTPNotExtended
        * 511 - HTTPNetworkAuthenticationRequired

All HTTP exceptions have the same constructor signature:
HTTPNotFound(*, headers=None, reason=None,
             body=None, text=None, content_type=None)

If not directly specified, headers will be added to the default response headers.

Classes HTTPMultipleChoices, HTTPMovedPermanently, HTTPFound, HTTPSeeOther, 
HTTPUseProxy, HTTPTemporaryRedirect have the following constructor signature:
HTTPFound(location, *, headers=None, reason=None,
          body=None, text=None, content_type=None)

where location is value for Location HTTP header.

HTTPMethodNotAllowed is constructed by providing the incoming unsupported method 
and list of allowed methods:
HTTPMethodNotAllowed(method, allowed_methods, *,
                     headers=None, reason=None,
                     body=None, text=None, content_type=None)

                     
                     
                     
                     
###Web Server Advanced

##Unicode support
aiohttp does requoting of incoming request path.

Unicode (non-ASCII) symbols are processed transparently on both route adding 
and resolving (internally everything is converted to percent-encoding form 
by yarl library).

But in case of custom regular expressions for Variable Resources please take care 
that URL is percent encoded: if you pass Unicode patterns they don’t match 
to requoted path.



##Web Handler Cancellation
web-handler execution could be canceled on every await 
if client drops connection without reading entire response’s BODY.

The behavior is very different from classic WSGI frameworks like Flask and Django.

Sometimes it is a desirable behavior: on processing GET request the code might 
fetch data from database or other web resource, the fetching is potentially slow.

Canceling this fetch is very good: 
the peer dropped connection already, there is no reason to waste time 
and resources (memory etc) by getting data from DB without any chance 
to send it back to peer.

But sometimes the cancellation is bad: on POST request very often is needed 
to save data to DB regardless to peer closing.

Cancellation prevention could be implemented in several ways:
    Applying asyncio.shield() to coroutine that saves data into DB.
    Spawning a new task for DB saving
    Using aiojobs or other third party library.

asyncio.shield() works pretty good. 
The only disadvantage is if you need to split web handler into exactly two async functions: one for handler itself and other for protected code.
For example the following snippet is not safe:

async def handler(request):
    await asyncio.shield(write_to_redis(request))
    await asyncio.shield(write_to_postgres(request))
    return web.Response(text='OK')

Cancellation might be occurred just after saving data in REDIS, 
write_to_postgres will be not called.

Spawning a new task is much worse: there is no place to await spawned tasks:

async def handler(request):
    request.loop.create_task(write_to_redis(request))
    return web.Response(text='OK')

In this case errors from write_to_redis are not awaited, 
it leads to many asyncio log messages Future exception was never retrieved 
and Task was destroyed but it is pending!.

Moreover on Graceful shutdown phase aiohttp don’t wait for these tasks, 
you have a great chance to loose very important data.

On other hand aiojobs provides an API for spawning new jobs 
and awaiting their results etc. 
It stores all scheduled activity in internal data structures 
and could terminate them gracefully:
All not finished jobs will be terminated on Application.on_cleanup signal.

from aiojobs.aiohttp import setup, spawn

async def coro(timeout):
    await asyncio.sleep(timeout)  # do something in background

async def handler(request):
    await spawn(request, coro())
    return web.Response()

app = web.Application()
setup(app)
app.router.add_get('/', handler)


#To prevent cancellation of the whole web-handler use @atomic decorator:
It prevents all handler async function from cancellation, 
write_to_db will be never interrupted.

from aiojobs.aiohttp import atomic

@atomic
async def handler(request):
    await write_to_db()
    return web.Response()

app = web.Application()
setup(app)
app.router.add_post('/', handler)



##Passing a coroutine into run_app and Gunicorn
run_app() accepts either application instance 
or a coroutine for making an application. 
The coroutine based approach allows to perform async IO before making an app:

async def app_factory():
    await pre_init()
    app = web.Application()
    app.router.add_get(...)
    return app

web.run_app(app_factory())

Gunicorn worker supports a factory as well. 
For Gunicorn the factory should accept zero parameters:

async def my_web_app():
    app = web.Application()
    app.router.add_get(...)
    return app

Start gunicorn:
$ gunicorn my_app_module:my_web_app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker


##Custom Routing Criteria
Sometimes you need to register handlers on more complex criteria 
than simply a HTTP method and path pair.

Although UrlDispatcher does not support any extra criteria, 
routing based on custom conditions can be accomplished by implementing 
a second layer of routing in your application.

The following example shows custom routing based on the HTTP Accept header:

class AcceptChooser:

    def __init__(self):
        self._accepts = {}

    async def do_route(self, request):
        for accept in request.headers.getall('ACCEPT', []):
            acceptor = self._accepts.get(accept)
            if acceptor is not None:
                return (await acceptor(request))
        raise HTTPNotAcceptable()

    def reg_acceptor(self, accept, handler):
        self._accepts[accept] = handler


async def handle_json(request):
    # do json handling

async def handle_xml(request):
    # do xml handling

chooser = AcceptChooser()
app.add_routes([web.get('/', chooser.do_route)])

chooser.reg_acceptor('application/json', handle_json)
chooser.reg_acceptor('application/xml', handle_xml)




##Static file handling

The best way to handle static files (images, JavaScripts, CSS files etc.) 
is using Reverse Proxy like nginx or CDN services.

But for development 

app.add_routes([web.static('/prefix', path_to_static_folder)])
routes.static('/prefix', path_to_static_folder)

When a directory is accessed within a static route then 
the server responses to client with HTTP/403 Forbidden by default. 

Displaying folder index instead could be enabled with show_index parameter set to True:
web.static('/prefix', path_to_static_folder, show_index=True)

When a symlink from the static directory is accessed, the server responses 
to client with HTTP/404 Not Found by default. 

To allow the server to follow symlinks, parameter follow_symlinks should be set to True:
web.static('/prefix', path_to_static_folder, follow_symlinks=True)

When you want to enable cache busting, parameter append_version can be set to True
Cache busting is the process of appending some form of file version hash 
to the filename of resources like JavaScript and CSS files. 
The performance advantage of doing this is that we can tell the browser 
to cache these files indefinitely without worrying about the client 
not getting the latest version when the file changes:
web.static('/prefix', path_to_static_folder, append_version=True)



##Data Sharing aka No Singletons Please
aiohttp.web discourages the use of global variables, aka singletons. 
Every variable should have its own context that is not global.

So, Application , Request and Response  support a collections.abc.MutableMapping interface 
(i.e. they are dict-like objects), Use them as data stores 

To avoid clashing with other aiohttp users and third-party libraries, 
please choose a unique key name for storing data.

##Application’s config

For storing global-like variables
app['my_private_key'] = data

and get it back in the web-handler:
async def handler(request):
    data = request.app['my_private_key']

In case of nested applications the desired lookup strategy could be the following:
    Search the key in the current nested application.
    If the key is not found continue searching in the parent application(s).
For this please use Request.config_dict read-only property:

async def handler(request):
    data = request.config_dict['my_private_key']

    
##Request and Response  storage
Variables that are only needed for the lifetime of a Request, or a Response 
can be stored in a Request/Response :

This is mostly useful for Middlewares and Signals handlers to store data 
for further processing by the next handlers in the chain.


async def handler(request):
  request['my_private_key'] = "data"
  ...

async def handler(request):
  [ do all the work ]
  response['my_metric'] = 123
  return response

  
  
##ContextVars support
Starting from Python 3.7 asyncio has Context Variables 
as a context-local storage (a generalization of thread-local concept 
that works with asyncio tasks also).

aiohttp server supports it in the following way:
1.A server inherits the current task’s context used when creating it. 
aiohttp.web.run_app() runs a task for handling all underlying jobs running the app, 
but alternatively Application runners can be used.

2.Application initialization / finalization events 
(Application.cleanup_ctx, Application.on_startup and Application.on_shutdown, 
Application.on_cleanup) are executed inside the same context.
E.g. all context modifications made on application startup a visible on teardown.

3.On every request handling aiohttp creates a context copy. 
web-handler has all variables installed on initialization stage. 
But the context modification made by a handler or middleware is invisible 
to another HTTP request handling call.

    
#An example of context vars usage:

from contextvars import ContextVar

from aiohttp import web

VAR = ContextVar('VAR', default='default')


async def coro():
    return VAR.get()


async def handler(request):
    var = VAR.get()
    VAR.set('handler')
    ret = await coro()
    return web.Response(text='\n'.join([var,
                                        ret]))


async def on_startup(app):
    print('on_startup', VAR.get())
    VAR.set('on_startup')


async def on_cleanup(app):
    print('on_cleanup', VAR.get())
    VAR.set('on_cleanup')


async def init():
    print('init', VAR.get())
    VAR.set('init')
    app = web.Application()
    app.router.add_get('/', handler)

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    return app


web.run_app(init())
print('done', VAR.get())


##Middlewares
A middleware is a coroutine that can modify either the request or response. 
Second argument should be named handler exactly.

The following code demonstrates middlewares execution order:

from aiohttp import web

async def test(request):
    print('Handler function called')
    return web.Response(text="Hello")

@web.middleware
async def middleware1(request, handler):
    print('Middleware 1 called')
    response = await handler(request)
    print('Middleware 1 finished')
    return response

@web.middleware
async def middleware2(request, handler):
    print('Middleware 2 called')
    response = await handler(request)
    print('Middleware 2 finished')
    return response


app = web.Application(middlewares=[middleware1, middleware2])
app.router.add_get('/', test)
web.run_app(app)

#Produced output:

Middleware 1 called
Middleware 2 called
Handler function called
Middleware 2 finished
Middleware 1 finished

#Example
A common use of middlewares is to implement custom error pages. 
from aiohttp import web

@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status != 404:
            return response
        message = response.message
    except web.HTTPException as ex:
        if ex.status != 404:
            raise
        message = ex.reason
    return web.json_response({'error': message})

app = web.Application(middlewares=[error_middleware])

##Middleware Factory
A middleware factory is a function that creates a middleware with passed arguments. 
For example, here’s a trivial middleware factory:

def middleware_factory(text):
    @middleware
    async def sample_middleware(request, handler):
        resp = await handler(request)
        resp.text = resp.text + text
        return resp
    return sample_middleware


app = web.Application(middlewares=[middleware_factory(' wink')])


##Signals
Although middlewares can customize request handlers before 
or after a Response has been prepared, they can’t customize a Response 
while it’s being prepared. 

For this aiohttp.web provides signals.

For example, a middleware can only change HTTP headers for unprepared responses 
(see StreamResponse.prepare()), 
but sometimes we need a hook for changing HTTP headers for streamed responses 
and WebSockets. 

This can be accomplished by subscribing to the 
Application.on_response_prepare signal:

async def on_prepare(request, response):
    response.headers['My-Header'] = 'value'

app.on_response_prepare.append(on_prepare)

Additionally, the Application.on_startup 
and Application.on_cleanup signals can be subscribed to 
for application component setup and tear down accordingly.

The following example will properly initialize and dispose an aiopg connection engine:

from aiopg.sa import create_engine

async def create_aiopg(app):
    app['pg_engine'] = await create_engine(
        user='postgre',
        database='postgre',
        host='localhost',
        port=5432,
        password=''
    )

async def dispose_aiopg(app):
    app['pg_engine'].close()
    await app['pg_engine'].wait_closed()

app.on_startup.append(create_aiopg)
app.on_cleanup.append(dispose_aiopg)

Signal handlers should not return a value but may modify incoming mutable parameters.
Signal handlers will be run sequentially, in order they were added. 
All handlers must be asynchronous since aiohttp 3.0.

#List of signals 
on_response_prepare
    A Signal that is fired at the beginning of StreamResponse.prepare() with parameters request and response
on_startup
    A Signal that is fired on application start-up.   
on_shutdown
    A Signal that is fired on application shutdown.
on_cleanup
    A Signal that is fired on application cleanup.
    Subscribers may use the signal for gracefully closing connections to database server etc.
    
    
    
##Cleanup Context
Bare Application.on_startup / Application.on_cleanup pair still has a pitfall: 
signals handlers are independent on each other.

E.g. we have [create_pg, create_redis] in startup signal 
and [dispose_pg, dispose_redis] in cleanup.

If, for example, create_pg(app) call fails create_redis(app) is not called. 
But on application cleanup both dispose_pg(app) 
and dispose_redis(app) are still called: 
cleanup signal has no knowledge about startup/cleanup pairs and their execution state.

The solution is Application.cleanup_ctx usage:
Asynchronous generators are supported by Python 3.6+, 
on Python 3.5 please use async_generator library.

async def pg_engine(app):
    app['pg_engine'] = await create_engine(
        user='postgre',
        database='postgre',
        host='localhost',
        port=5432,
        password=''
    )
    yield app['pg_engine'].close()
    await app['pg_engine'].wait_closed()

app.cleanup_ctx.append(pg_engine)

The attribute is a list of asynchronous generators, 
a code before yield is an initialization stage (called on startup), 
a code after yield is executed on cleanup. 
The generator must have only one yield.

aiohttp guarantees that cleanup code is called if 
and only if startup code was successfully finished.



##Nested applications
Sub applications are designed for solving the problem of the big monolithic code base. 
Let’s assume we have a project with own business logic 
and tools like administration panel and debug toolbar.

Administration panel is a separate application by its own nature 
but all toolbar URLs are served by prefix like /admin.

Thus we’ll create a totally separate application named admin 
and connect it to main app with prefix by Application.add_subapp():

admin = web.Application()
# setup admin routes, signals and middlewares

app.add_subapp('/admin/', admin)

Middlewares and signals from app and admin are chained.

It means that if URL is '/admin/something' middlewares from app are applied first 
and admin.middlewares are the next in the call chain.

The same is going for Application.on_response_prepare signal – 
the signal is delivered to both top level app and admin if processing URL is routed 
to admin sub-application.

Common signals like Application.on_startup, Application.on_shutdown 
and Application.on_cleanup are delivered to all registered sub-applications. 
The passed parameter is sub-application instance, not top-level application.

Third level sub-applications can be nested into second level ones – 
there are no limitation for nesting level.

Url reversing for sub-applications should generate urls with proper prefix.
But for getting URL sub-application’s router should be used:

admin = web.Application()
admin.add_routes([web.get('/resource', handler, name='name')])

app.add_subapp('/admin/', admin)

url = admin.router['name'].url_for()
The generated url from example will have a value URL('/admin/resource').

If main application should do URL reversing for sub-application 
it could use the following explicit technique:

admin = web.Application()
admin.add_routes([web.get('/resource', handler, name='name')])

app.add_subapp('/admin/', admin)
app['admin'] = admin

async def handler(request):  # main application's handler
    admin = request.app['admin']
    url = admin.router['name'].url_for()

    
    
    
##Expect Header
aiohttp.web supports Expect header.
By default it sends HTTP/1.1 100 Continue line to client, 
or raises HTTPExpectationFailed if header value is not equal to '100-continue'. 
It is possible to specify custom Expect header handler on per route basis. 
This handler gets called if Expect header exist in request after receiving 
all headers and before processing application’s Middlewares and route handler. 

Handler can return None, in that case the request processing continues as usual. 
If handler returns an instance of class StreamResponse, 
request handler uses it as response. 
Also handler can raise a subclass of HTTPException. 
In this case all further processing will not happen and client will receive appropriate 
http response.

A server that does not understand or is unable to comply 
with any of the expectation values in the Expect field of a request MUST respond 
with appropriate error status. 
The server MUST respond with a 417 (Expectation Failed) status 
if any of the expectations cannot be met or, 
if there are other problems with the request, some other 4xx status.
http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.20

If all checks pass, the custom handler must write a HTTP/1.1 100 Continue status code 
before returning.

The following example shows how to setup a custom handler for the Expect header:

async def check_auth(request):
    if request.version != aiohttp.HttpVersion11:
        return

    if request.headers.get('EXPECT') != '100-continue':
        raise HTTPExpectationFailed(text="Unknown Expect: %s" % expect)

    if request.headers.get('AUTHORIZATION') is None:
        raise HTTPForbidden()

    request.transport.write(b"HTTP/1.1 100 Continue\r\n\r\n")

async def hello(request):
    return web.Response(body=b"Hello, world")

app = web.Application()
app.add_routes([web.add_get('/', hello, expect_handler=check_auth)])



##Application runners
run_app() provides a simple blocking API for running an Application.

For starting the application asynchronously or serving 
on multiple HOST/PORT AppRunner exists.

The simple startup code for serving HTTP site on 'localhost', port 8080 looks like:
runner = web.AppRunner(app)
await runner.setup()
site = web.TCPSite(runner, 'localhost', 8080)
await site.start()

To stop serving call AppRunner.cleanup():
await runner.cleanup()


##Graceful shutdown
Stopping aiohttp web server by just closing all connections is not always satisfactory.
The problem is: if application supports websockets or data streaming 
it most likely has open connections at server shutdown time.

The library has no knowledge how to close them gracefully 
but developer can help by registering Application.on_shutdown signal handler 
and call the signal on web server closing.
Both run_app() and AppRunner.cleanup() call shutdown signal handlers.

Developer should keep a list of opened connections 
(Application is a good candidate).

from aiohttp import web
import weakref

app = web.Application()
app['websockets'] = weakref.WeakSet()

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].add(ws)
    try:
        async for msg in ws:
            ...
    finally:
        request.app['websockets'].discard(ws)

    return ws

#Signal handler may look like:

from aiohttp import WSCloseCode

async def on_shutdown(app):
    for ws in set(app['websockets']):
        await ws.close(code=WSCloseCode.GOING_AWAY,
                       message='Server shutdown')

app.on_shutdown.append(on_shutdown)



##Background tasks

To run such short and long running background tasks aiohttp 
provides an ability to register Application.on_startup signal handler(s) 
that will run along with the application’s request handler.

For example there’s a need to run one quick task 
and two long running tasks that will live till the application is alive. 

The appropriate background tasks could be registered as an Application.on_startup signal handlers 

async def listen_to_redis(app):
    try:
        sub = await aioredis.create_redis(('localhost', 6379))
        ch, *_ = await sub.subscribe('news')
        async for msg in ch.iter(encoding='utf-8'):
            # Forward message to all connected websockets:
            for ws in app['websockets']:
                ws.send_str('{}: {}'.format(ch.name, msg))
    except asyncio.CancelledError:
        pass
    finally:
        await sub.unsubscribe(ch.name)
        await sub.quit()


async def start_background_tasks(app):
    app['redis_listener'] = asyncio.create_task(listen_to_redis(app))


async def cleanup_background_tasks(app):
    app['redis_listener'].cancel()
    await app['redis_listener']


app = web.Application()
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)
web.run_app(app)


##Swagger support
aiohttp-swagger is a library that allow to add Swagger documentation 
and embed the Swagger-UI into your aiohttp.web project.


##CORS support
aiohttp.web itself does not support Cross-Origin Resource Sharing, 
but there is an aiohttp plugin for it: aiohttp_cors.


##Debug Toolbar
aiohttp-debugtoolbar is a very useful library that provides a debugging toolbar 
while you’re developing an aiohttp.web application.


$ pip install aiohttp_debugtoolbar

#Just call aiohttp_debugtoolbar.setup():

import aiohttp_debugtoolbar
from aiohttp_debugtoolbar import toolbar_middleware_factory

app = web.Application()
aiohttp_debugtoolbar.setup(app)


##Dev Tools
aiohttp-devtools provides a couple of tools to simplify development 
of aiohttp.web applications.

$ pip install aiohttp-devtools

* runserver provides a development server with auto-reload,
live-reload, static file serving and aiohttp_debugtoolbar_
integration.

* start is a cookiecutter command which does the donkey work
of creating new aiohttp.web Applications.

       
###Server Deployment
There are several options for aiohttp server deployment:
    Standalone server
    Running a pool of backend servers behind of nginx, HAProxy 
    or other reverse proxy server
    Using gunicorn behind of reverse proxy

##Standalone

Just call aiohttp.web.run_app() function passing aiohttp.web.Application instance.

The method is very simple and could be the best solution in some trivial cases. 
But it does not utilize all CPU cores.

For running multiple aiohttp server instances use reverse proxies.


##Nginx+supervisord
ginx is the perfect frontend server. 
It may prevent many attacks based on malformed http protocol etc.

Second, running several aiohttp instances behind nginx allows to utilize all CPU cores.

Third, nginx serves static files much faster than built-in aiohttp static file support.

#configure HTTP server 
http {
  server {
    listen 80;
    client_max_body_size 4G;

    server_name example.com;

    location / {
      proxy_set_header Host $http_host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_redirect off;
      proxy_buffering off;
      proxy_pass http://aiohttp;
    }

    location /static {
      # path for static files
      root /path/to/app/static;
    }

  }
}

This config listens on port 80 for server named example.com 
and redirects everything to aiohttp backend group.
Also it serves static files from /path/to/app/static path as example.com/static.

#Next we need to configure aiohttp upstream group:

http {
  upstream aiohttp {
    # fail_timeout=0 means we always retry an upstream even if it failed
    # to return a good HTTP response

    # Unix domain servers
    server unix:/tmp/example_1.sock fail_timeout=0;
    server unix:/tmp/example_2.sock fail_timeout=0;
    server unix:/tmp/example_3.sock fail_timeout=0;
    server unix:/tmp/example_4.sock fail_timeout=0;

    # Unix domain sockets are used in this example due to their high performance,
    # but TCP/IP sockets could be used instead:
    # server 127.0.0.1:8081 fail_timeout=0;
    # server 127.0.0.1:8082 fail_timeout=0;
    # server 127.0.0.1:8083 fail_timeout=0;
    # server 127.0.0.1:8084 fail_timeout=0;
  }
}

All HTTP requests for http://example.com except ones 
for http://example.com/static will be redirected to example1.sock, example2.sock, 
example3.sock or example4.sock backend servers. 

By default, Nginx uses round-robin algorithm for backend selection.


##Supervisord
After configuring Nginx we need to start our aiohttp backends. 
Better to use some tool for starting them automatically after system reboot 
or backend crash.

There are very many ways to do it: 
Supervisord, Upstart, Systemd, Gaffer, Circus, Runit etc.

#Here we’ll use Supervisord for example:

[program:aiohttp]
numprocs = 4
numprocs_start = 1
process_name = example_%(process_num)s

; Unix socket paths are specified by command line.
command=/path/to/aiohttp_example.py --path=/tmp/example_%(process_num)s.sock

; We can just as easily pass TCP port numbers:
; command=/path/to/aiohttp_example.py --port=808%(process_num)s

user=nobody
autostart=true
autorestart=true

aiohttp server

The last step is preparing aiohttp server for working with supervisord.
Assuming we have properly configured aiohttp.web.Application 
and port is specified by command line, the task is trivial:

# aiohttp_example.py
import argparse
from aiohttp import web

parser = argparse.ArgumentParser(description="aiohttp server example")
parser.add_argument('--path')
parser.add_argument('--port')


if __name__ == '__main__':
    app = web.Application()
    # configure app

    args = parser.parse_args()
    web.run_app(app, path=args.path, port=args.port)

    
    
##Nginx+Gunicorn

aiohttp can be deployed using Gunicorn, 
which is based on a pre-fork worker model. 
Gunicorn launches your app as worker processes for handling incoming requests.

In opposite to deployment with bare Nginx the solution does not 
need to manually run several aiohttp processes 
and use tool like supervisord for monitoring it. 

But nothing is for free: running aiohttp application under gunicorn is slightly slower.

Create a directory for your application:
>> mkdir myapp
>> cd myapp

Create Python virtual environment:
>> python3 -m venv venv
>> source venv/bin/activate

>> pip install gunicorn
>> pip install aiohttp

#Application
from aiohttp import web

async def index(request):
    return web.Response(text="Welcome home!")


my_web_app = web.Application()
my_web_app.router.add_get('/', index)

#Application factory
As an option an entry point could be a coroutine that accepts no parameters 
and returns an application instance:

from aiohttp import web

async def index(request):
    return web.Response(text="Welcome home!")


async def my_web_app():
    app = web.Application()
    app.router.add_get('/', index)
    return app

#Start Gunicorn
When Running Gunicorn, you provide the name of the module, i.e. my_app_module, 
and the name of the app or application factory, i.e. my_web_app, 
along with other Gunicorn Settings provided as command line flags 
or in your config file.
    the --bind flag to set the server’s socket address;
    the --worker-class flag to tell Gunicorn that we want to use a custom 
    worker subclass instead of one of the Gunicorn default worker types;
    you may also want to use the --workers flag to tell Gunicorn 
    how many worker processes to use for handling requests. 
    you may also want to use the --accesslog flag to enable the access log 
    to be populated. 
    
The custom worker subclass is defined in aiohttp.GunicornWebWorker:

>> gunicorn my_app_module:my_web_app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker
[2017-03-11 18:27:21 +0000] [1249] [INFO] Starting gunicorn 19.7.1
[2017-03-11 18:27:21 +0000] [1249] [INFO] Listening at: http://127.0.0.1:8080 (1249)
[2017-03-11 18:27:21 +0000] [1249] [INFO] Using worker: aiohttp.worker.GunicornWebWorker
[2015-03-11 18:27:21 +0000] [1253] [INFO] Booting worker with pid: 1253

Gunicorn is now running and ready to serve requests to your app’s worker processes.

The Gunicorn documentation recommends deploying Gunicorn behind an Nginx proxy server. 
See the official documentation for more information about suggested nginx configuration.
http://docs.gunicorn.org/en/latest/deploy.html




