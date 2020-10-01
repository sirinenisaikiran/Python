###Contents 
Pytest 
Pytest - Example 
Test coverage 
File and Directory Access
filecmp — File and Directory Comparisons
fileinput — Iterate over lines from multiple input streams
Data Compression and Archiving
shutil — High-level file operations
doctest

----------------------------------------------------------



###*** Pytest 

#use assert to check truthness 

#Methods name should begin with test*
##pytests/first_test.py
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5
    
##In Test class 
#class name must begins with Test 
#Methods name should begin with test*
class TestClass(object):
    def test_one(self):
        x = "this"
        assert 'h' in x

     def test_two(self):
         x = "hello"
         assert hasattr(x, 'check')

#Run 
$ pytest -v first_test.py 

#Alternate calling syntax 
#same as ealier but currdir is added to sys.path 
$ python -m pytest -v first_test.py 

#To see all builtin fixtures 

$ pytest --fixtures

#default fixture 
#cache, capsys,capfd,doctest_namespace,pytestconfig,record_xml_property,monkeypatch,recwarn,tmpdir_factory,tmpdir


#check default markers
pytest --markers   
         
#For running marker
pytest -v -m <<marker>>
pytest -v -m "not <<marker>>"


##Marking test functions and selecting them for a run

# content of test_server.py
import pytest

@pytest.mark.webtest
def test_send_http():
    pass # perform some webtest test for your app
    
def test_something_quick():
    pass
    
def test_another():
    pass
    
    
class TestClass(object):
    def test_method(self):
         pass

         
#Registering markers
# content of pytest.ini
[pytest]
markers =
    webtest: mark a test as a webtest.
    
#Run    
$ pytest -v -m webtest     
         




##Pytest - Few imp command line 

-v, --verbose         increase verbosity.
-q, --quiet           decrease verbosity.
--tb=style            traceback print mode (auto/long/short/line/native/no).
--full-trace          don't cut any tracebacks (default is to cut).
-s, –capture=no
    Normally stdout and stderr are captured and only shown for failing tests. 
    The -s option can be used to disable capturing, showing stdcalls 
    for print statements, logging calls, etc.
--collect-only
    Shows a list of the tests without running them
-x, –exitfirst
    Exit instantly after the first failure.
–lf, –last-failed
    Runs only the set of tests that failed at the last run, or all tests if none failed

##Example 
pytest -x                    # stop after first failure
pytest --maxfail=2            # stop after two failures

#To check test case IDs
pytest --collect-only first_test.py 

pytest test_mod.py   # run tests in module
pytest somepath      # run all tests below somepath
pytest -k stringexpr # only run tests with names that match the
                     # "stringExpression", e.g. "MyClass and not method"
                     # will select TestMyClass.test_something
                     # but not TestMyClass.test_method_simple
pytest test_mod.py::test_func # only run tests that match the "node ID",
                              # e.g. "test_mod.py::test_func" will select
                              # only test_func in test_mod.py
pytest test_mod.py::TestClass::test_method # run a single method in
                                             # a single class

#Import `pkg' and use its filesystem location to find and run tests:
pytest --pyargs pkg # run all tests found below directory of pkg


#string expr could be
"stringexpr"
"not stringexpr"
"stringexpr1 and stringexpr2"
"stringexpr1 and not stringexpr2"
"stringexpr1 or stringexpr2"

#Disabling plugins
pytest -p no:doctest

#Creating JUnitXML format files
pytest --junitxml=path

#Creating resultlog format files
pytest --resultlog=path

#Profiling test execution duration
pytest --durations=10

#invoke PDB debugger and tracing
import pytest
def test_function():
    ...
    pytest.set_trace()      #here pdb would be invoked 

#Dropping to PDB (Python Debugger) on failures
pytest --pdb
pytest -x --pdb   # drop to PDB on first failure, then end test session
pytest --pdb --maxfail=3  # drop to PDB for first three failures

#on any failure the exception information is stored on sys.last_value, sys.last_type and sys.last_traceback. 
>>> import sys
>>> sys.last_traceback.tb_lineno
42
>>> sys.last_value
AssertionError('assert result == "ok"',)


#Modifying Python traceback printing
pytest --showlocals # show local variables in tracebacks
pytest -l           # show local variables (shortcut)

pytest --tb=auto            # (default) 'long' tracebacks for the first and last
                             # entry, but 'short' style for the other entries
pytest   --tb=long          # exhaustive, informative traceback formatting
pytest   --tb=short         # shorter traceback format
pytest   --tb=line          # only one line per failure
pytest   --tb=native        # Python standard library formatting
pytest   --tb=no            # no traceback at all



#Capturing
pytest -s            # disable all capturing
pytest --capture=sys # replace sys.stdout/stderr with in-mem files
pytest --capture=fd  # also point filedescriptors 1 and 2 to temp file





##Pytest - Fixtures and request object
#Test functions can receive fixture objects by naming them as an input argument. 

#fixture is a function returning a value , which is DIed when used in testcase argument 

#Fixture functions are registered by marking them with @pytest.fixture.

#fixture takes another fixture or builtin fixtures or  request (instance of FixtureRequest)
        
# content of ./test_smtpsimple.py
import pytest

@pytest.fixture
def smtp():
    import smtplib
    return smtplib.SMTP("smtp.gmail.com") #yield is better then any code after yield is taken as fixture teardown 

def test_ehlo(smtp):  #smtp is Died 
    response, msg = smtp.ehlo()
    assert response == 250
    assert 0 # for demo purposes

#to see available fixtures.   
$ pytest --fixtures test_simplefactory.py
 
    
#API 
#(return a) decorator to mark a fixture factory function.
pytest.fixture(scope='function', params=None, autouse=False, ids=None, name=None)
    scope – the scope for which this fixture is shared, 
        one of “function” (default), “class”, “module” or “session”.
    params – an optional list of parameters which will cause multiple invocations of the fixture function 
        and all of the tests using it. 
        each of params are accessed by request.param inside fixture function
    autouse – if True, the fixture func is activated for all tests that can see it. 
        If False (the default) then an explicit reference is needed to activate the fixture.
    ids – list of string ids each corresponding to the params 
        so that they are part of the test id           
    name – the name of the fixture. 
       This defaults to the name of the decorated function.
       
##Fixture function can accept the 'request' object (instance of FixtureRequest)
#to introspect the test function, class or module context  

#Example - to read an optional server URL from the test module 

# content of conftest.py
import pytest
import smtplib

@pytest.fixture(scope="module")
def smtp(request):
    server = getattr(request.module, "smtpserver", "smtp.gmail.com") #get 'smtpserver' of module 
    smtp = smtplib.SMTP(server)
    yield smtp
    print ("finalizing %s (%s)" % (smtp, server))
    smtp.close()


# content of test_anothersmtp.py
smtpserver = "mail.python.org"              # will be read by smtp fixture
def test_showhelo(smtp):
    assert 0, smtp.helo()

#Running it:
$ pytest -qq --tb=short test_anothersmtp.py     


#API 
class FixtureRequest
      A request for a fixture from a test or fixture function.
      A request object gives access to the requesting test context 
      param 
        Optional, attribute in case the fixture is parametrized indirectly.
      fixturename = None
          fixture for which this request is being performed
      scope = None
          Scope string, one of "function", "class", "module", "session"
      node
          underlying collection node (depends on current request scope)
      config
          the pytest config object associated with this request.
      function
          test function object if the request has a per-function scope.
      cls
            class (can be None) where the test function was collected.
      instance
          instance (can be None) on which test function was collected.
      module
          python module object where the test function was collected.
      fspath
          the file system path of the test module which collected this test.
      keywords
          keywords/markers dictionary for the underlying node.
      session
          pytest session object.
      addfinalizer(finalizer)
          add finalizer/teardown function to be called after the last test within the requesting test context finished
          execution.
      applymarker(marker)
          Apply a marker to a single test function invocation. 
          This method is useful if you don't want to have a
          keyword/marker on all function invocations.
                Parameters marker ­ a _pytest.mark.MarkDecorator object created by a call to
                   pytest.mark.NAME(...).
      raiseerror(msg)
          raise a FixtureLookupError with the given message.
      cached_setup(setup, teardown=None, scope='module', extrakey=None)
          (deprecated) Return a testing resource managed by setup & teardown calls. scope and extrakey
          determine when the teardown function will be called so that subsequent calls to setup would recreate
          the resource. With pytest-2.3 you often do not need cached_setup() as you can directly declare a
          scope on a fixture function and register a finalizer through request.addfinalizer().
                Parameters
                     · teardown ­ function receiving a previously setup resource.
                     · setup ­ a no-argument function creating a resource.
                     · scope ­ a string value out of function, class, module or session indicating the
                       caching lifecycle of the resource.
                     · extrakey ­ added to internal caching key of (funcargname, scope).
      getfixturevalue(argname)
          Dynamically run a named fixture function.
            Declaring fixtures via function argument is recommended where possible. But if you can only decide
            whether to use another fixture at test setup time, you may use this function to retrieve it inside a fixture or
            test function body.
      getfuncargvalue(argname)
          Deprecated, use getfixturevalue.
         
         
         
 
  
       
       
       

##Pytest - Monkeypatching/mocking modules and environments
        
#to pretend that os.expanduser returns a certain directory, 
#use monkeypatch(a builtin fixture).setattr()

# content of test_module.py
import os.path
def getssh(): # pseudo application code
    return os.path.join(os.path.expanduser("~admin"), '.ssh')

def test_mytest(monkeypatch):
    def mockreturn(path):
        return '/abc'
    monkeypatch.setattr(os.path, 'expanduser', mockreturn) #module_name, method_name, new_method_name 
    x = getssh()
    assert x == '/abc/.ssh'
      
      
#Example - preventing "requests" library  from remote operations
#delete the method request.session.Session.request 
#so that any attempts within tests to create http requests will fail

# content of conftest.py
import pytest
@pytest.fixture(autouse=True)  #automatically activate 
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.sessions.Session.request")        
         
         
         
##reference 
monkeypatch
    The returned ``monkeypatch`` fixture provides these
    helper methods to modify objects, dictionaries or os.environ::

    monkeypatch.setattr(obj, name, value, raising=True)
    monkeypatch.delattr(obj, name, raising=True)
    monkeypatch.setitem(mapping, name, value)
    monkeypatch.delitem(obj, name, raising=True)
    monkeypatch.setenv(name, value, prepend=False)
    monkeypatch.delenv(name, value, raising=True)
    monkeypatch.syspath_prepend(path)
    monkeypatch.chdir(path)

    All modifications will be undone after the requesting
    test function or fixture has finished. The ``raising``
    parameter determines if a KeyError or AttributeError
    will be raised if the set/deletion operation has no target.
    
    
    
##Pytest - parametrizing test functions

#The builtin pytest.mark.parametrize decorator enables parametrization of arguments for a test function
#enables running a test case multiple times 

pytest.mark.parametrize(argnames, argvalues, indirect=False, ids=None, scope=None)
    argnames – a comma-separated string denoting one or more argument names, 
               or a list/tuple of argument strings.
    argvalues – If only one argname was specified argvalues is a list of values. 
                If N argnames were specified, argvalues must be a list of N-tuples, 
                where each tuple-element specifies a value for its respective argname.
    indirect – The list of argnames or boolean. 
               A list of arguments’ names (subset of argnames). 
               If True the list contains all names from the argnames. 
               Each argvalue corresponding to an argname in this list 
               will be passed as request.param to its respective argname 
               fixture function so that it can perform more expensive 
               setups during the setup phase of a test rather 
               than at collection time.
    ids – list of string ids, or a callable. 
          If strings, each is corresponding to the argvalues so that they are part of the test id. 
          If None is given as id of specific test, 
          the automatically generated id for that argument will be used. 
          If callable, it should take one argument (a single argvalue) 
          and return a string or return None. 
          If None, the automatically generated id for that argument will be used. 
          If no ids are provided they will be generated automatically 
          from the argvalues.
    scope – if specified it denotes the scope of the parameters. 
            The scope is used for grouping tests by parameter instances.
            It will also override any fixture-function defined scope, 
            allowing to set a dynamic scope using test context 
            or configuration.


#Example - the @parametrize decorator defines three different (test_input,expected) tuples 
#so that the test_eval function will run three times using them in turn



# content of test_expectation.py
import pytest
@pytest.mark.parametrize("test_input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    ("6*9", 42),
])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
    
#to 'mark' individual test instances within parametrize
# content of test_expectation.py
import pytest
@pytest.mark.parametrize("test_input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    pytest.param("6*9", 42,marks=pytest.mark.xfail),
    pytest.param("1+3", 4,marks=pytest.mark.bar),      #.bar must be in .ini file 
])
def test_eval(test_input, expected):
    assert eval(test_input) == expected


##To get all combinations of multiple parametrized arguments you can stack parametrize decorators
#Example - This will run the test with the arguments set to x=0/y=2, x=0/y=3, x=1/y=2 and x=1/y=3.

import pytest
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_foo(x, y):
    pass


##OR Use pytest_generate_tests hook which is called when collecting a test function
class Metafunc(function, fixtureinfo, config, cls=None, module=None)
    Metafunc objects are passed to the pytest_generate_tests hook. 
    They help to inspect a test function and to generate tests according 
    to test configuration or values specified in the class 
    or module where a test function is defined.
    config = None
        access to the _pytest.config.Config object for the test session
    module = None
        the module object where the test function is defined in.
    function = None
        underlying python test function
    fixturenames = None
        set of fixture names required by the test function
    cls = None
        class object where the test function is defined in or None.
    parametrize(argnames, argvalues, indirect=False, ids=None, scope=None)
        Add new invocations to the underlying test function using the list of argvalues 
        for the given argnames. 
        Parametrization is performed during the collection phase. 
        
##Example 
# content of test_strings.py
def test_valid_string(stringinput):  #fixturename is 'stringinput'
    assert stringinput.isalpha()

# content of conftest.py
def pytest_addoption(parser):
    parser.addoption("--stringinput", action="append", default=[],
        help="list of stringinputs to pass to test functions")

def pytest_generate_tests(metafunc):
    if 'stringinput' in metafunc.fixturenames:
        metafunc.parametrize("stringinput", metafunc.config.getoption('stringinput'))


#pass two stringinput values, our test will run twice:
$ pytest -q --stringinput="hello" --stringinput="world" test_strings.py
..
2 passed in 0.12 seconds       




###*** Pytest - Example 

##->file:first_test.py:
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5
    
    
#to assert that some code raises an exception you can use the raises helper:

import pytest
def f():
    raise SystemExit(1)

def test_mytest():
    with pytest.raises(SystemExit):
        f()
        
        
##In Test class 
class TestClass(object):
    def test_one(self):
        x = "this"
        assert 'h' in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')
        



##->file:func_test.py:
def test_needsfiles(tmpdir):
    print (tmpdir)
    assert 0
    
    


##Testing MyInt under package pkg 
##->file:class\pkg\MyInt.py:
import functools

@functools.total_ordering
class MyInt:
    def __init__(self, value):
        self.v = value 
    def __str__(self):
        return "MyInt(%d)" % ( self.v,)
    def __add__(self, other):
        return MyInt(self.v + other.v)
    def __sub__(self, other):
        return MyInt(self.v - other.v)
    def square(self):
        return self.v * self.v 
    def __eq__(self, other):
        return self.v == other.v
    def __lt__(self, other):
        return self.v < other.v
        
        
##->file:class\conftest.py: define  all fixtures 

from pkg.MyInt import MyInt
import pytest

#define two fixtures
@pytest.fixture(scope='module')
def one(request):
    """returns MyInt(1)"""
    yield MyInt(1)
    print("tear down code of one fixture")


@pytest.fixture(scope='module')
def zero(request):
    """returns MyInt(0)"""    
    def fin():
        print("tear down code of zero fixture")
    request.addfinalizer(fin)
    return MyInt(0)

	

#Generate two testcases for test_many(param1, op, param2, op2, result)
#checking 'param1' in args ie fixures- then function must be test_many 
#or check function.__name__
def pytest_generate_tests(metafunc):   #pytest_generate_tests is a builtin hook 
	if metafunc.function.__name__ == 'test_many':  #or 'param1' in metafunc.fixturenames:
        #argnames, argvalues, indirect=False, ids=None, scope=None
		metafunc.parametrize(["param1", "op", "param2", "op2","result"],
						[pytest.param( MyInt(2), '-',  MyInt(2), "==", MyInt(0), marks=pytest.mark.addl),
						(MyInt(2), '+',  MyInt(2), "==", MyInt(4)),
						] , ids = [ "Testing sub",
									 "Testing add",
						])
						

                        
# handling command line options
def pytest_addoption(parser):
	parser.addoption("--myint", action="store", type = "int", default=10, help="testing eq")

@pytest.fixture
def commandMyInt(request):
    return request.config.getoption("--myint") #returns value of this option 


##->file:class\pytest.ini:
[pytest]
markers =
	addl: testing addl functionalities 


##->file:class\test_myint.py:
##pytest -v -s test_myint.py  #-s is for printing (print statement)
#pytest --markers
#pytest -v -m addl test_myint.py 
#pytest -v -k "Testing" test_myint.py #check 'Testing' in Ids , check conftests.py/pytest_generate_tests
#pytest --collect-only test_myint.py #to get all those ids 
#pytest --fixtures test_myint.py  #to check all fixtures


import pytest
from pkg.MyInt import MyInt


def test_add_myint(one, zero):
	assert one + zero == one 

@pytest.mark.addl
def test_sub_myint(one, zero):
	assert one - zero == one
	

def process(op, a, b):
	if op == '+': return a + b
	if op == '-': return a - b	
	if op == '==': return a == b
	if op == '!=': return a != b
	if op == '>': return a > b
	if op == '<': return a < b
	if op == '>=': return a >= b
	if op == '<=': return a <= b
	
#Note sequence in 1st arg of parametrize and test_eval args are not same 
#Note the generated ids
@pytest.mark.parametrize("a, op, b, expected", [
    ( MyInt(2), '+',  MyInt(2), MyInt(4)),
    pytest.param(MyInt(2), '-',  MyInt(2), MyInt(0), marks=pytest.mark.addl),
  ])
def test_eval(a, b, op, expected):
	assert process(op,a,b) == expected
    
    
#generated through pytest_generate_tests
def test_many(param1, op, param2, op2, result):
	assert process(op2, process(op,param1,param2),result)
    
    
    
#Test command line 
class TestMyInt:
    def test_commandline(self,commandMyInt):
        print("testing..", commandMyInt)
        assert MyInt(commandMyInt) == MyInt(commandMyInt)




###Example of cache 
##->file:misc\test_misc.py:
#pytest -v -s test_misc.py 
#then again execute 
#pytest -v -s test_misc.py  #now faster for test_function

##executing to only re-run the failures
#pytest --lf -v -s test_misc.py
#to run the failures first and then the rest of the tests.
#pytest --ff -v -s test_misc.py



import pytest, time


##cache fixture is valid for various runs 
#few standard fixture 
def test_one(cache, tmpdir):
    print("tmpdir=",tmpdir)
    if cache.get("myapp/key1", None) is not None:
        print("old value", cache.get("myapp/key1", None))
    else:
        print("setting myapp/key1")
        cache.set("myapp/key1", 10)
        
        
#another     
def test_two(cache, tmpdir):
    print("tmpdir=",tmpdir)
    if cache.get("myapp/key1", None) is not None:
        print("old value", cache.get("myapp/key1", None))
    else:
        print("setting myapp/key1")
        cache.set("myapp/key1", 10)
        
#config.cache is valid between different runs 
#first time long sleep ,next run it is fast 
@pytest.fixture
def mydata(request):
    val = request.config.cache.get("example/value", None)
    if val is None:
        time.sleep(9*0.6) # expensive computation :)
        val = 42
        request.config.cache.set("example/value", val)
    return val
#in first run, it is slow, next run it is fast 
def test_function(mydata):
    assert mydata == 42
    
    
##Testing --lf, --ff
@pytest.mark.parametrize("i", range(10))
def test_num(i):
    if i in (7, ):
       pytest.fail("bad luck")


###*** Test coverage 
#Any unexpected error, remove .cache file 
$ pip install pytest pytest-cov

$ pytest -v classTest 

$ pytest --cov=class/pkg class/   #check coverage of 'class/pkg' by running all tests under class/



###*** File and Directory Access
#https://docs.python.org/3/library/filesys.html      

#For example stat method 

>>> import os
>>> statinfo = os.stat('somefile.txt')
>>> statinfo
os.stat_result(st_mode=33188, st_ino=7876932, st_dev=234881026,
st_nlink=1, st_uid=501, st_gid=501, st_size=264, st_atime=1297230295,
st_mtime=1297230027, st_ctime=1297230027)
>>> statinfo.st_size
264

##To use module stat 's predefined constant 
#check other stat https://docs.python.org/3/library/stat.html

import os, sys
from stat import *

def walktree(top, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname).st_mode
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print('Skipping %s' % pathname)

def visitfile(file):
    print('visiting', file)

if __name__ == '__main__':
    walktree(sys.argv[1], visitfile)



###*** filecmp — File and Directory Comparisons
from filecmp import dircmp
def print_diff_files(dcmp):
    for name in dcmp.diff_files:
        print("diff_file %s found in %s and %s" % (name, dcmp.left,  dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)

dcmp = dircmp('dir1', 'dir2') 
print_diff_files(dcmp) 

##API 
filecmp.cmp(f1, f2, shallow=True)
    Compare the files named f1 and f2, returning True if they seem equal, False otherwise.
    If shallow is true, files with identical os.stat() signatures are taken to be equal.
    Otherwise, the contents of the files are compared.

filecmp.cmpfiles(dir1, dir2, common, shallow=True)
    Compare the files in the two directories dir1 and dir2 whose names are given by common.
    Returns three lists of file names: match, mismatch, errors. 
    
class filecmp.dircmp(a, b, ignore=None, hide=None)
    Construct a new directory comparison object, to compare the directories a and b. 
    ignore is a list of names to ignore, and defaults to filecmp.DEFAULT_IGNORES. 
    hide is a list of names to hide, and defaults to [os.curdir, os.pardir].
    The dircmp class provides the following attributes:
    report()
        Print (to sys.stdout) a comparison between a and b.
    report_partial_closure()
        Print a comparison between a and b and common immediate subdirectories.
    report_full_closure()
        Print a comparison between a and b and common subdirectories (recursively).
    left
        The directory a.
    right
        The directory b.
    left_list
        Files and subdirectories in a, filtered by hide and ignore.
    right_list
        Files and subdirectories in b, filtered by hide and ignore.
    common
        Files and subdirectories in both a and b.
    left_only
        Files and subdirectories only in a.
    right_only
        Files and subdirectories only in b.
    common_dirs
        Subdirectories in both a and b.
    common_files
        Files in both a and b.
    common_funny
        Names in both a and b, such that the type differs between the directories, or names for which os.stat() reports an error.
    same_files
        Files which are identical in both a and b, using the class’s file comparison operator.
    diff_files
        Files which are in both a and b, whose contents differ according to the class’s file comparison operator.
    funny_files
        Files which are in both a and b, but could not be compared.
    subdirs
        A dictionary mapping names in common_dirs to dircmp objects.


###*** fileinput — Iterate over lines from multiple input streams
 
import fileinput
for line in fileinput.input():
    process(line)


#This iterates over the lines of all files listed in sys.argv[1:], 
#defaulting to sys.stdin if the list is empty. 
#If a filename is '-', it is also replaced by sys.stdin. 
#To specify an alternative list of filenames, pass it as the first argument to input(). 
#A single file name is also allowed.

#with predefined list 
#not thread safe , creates global state 
with fileinput.input(files=('spam.txt', 'eggs.txt')) as f:
    for line in f:
        process(line)

#thread safe 
with fileinput.FileInput(files=('spam.txt', 'eggs.txt')) as f:
    for line in f:
        process(line)
        
        
##API 
fileinput.input(files=None, inplace=False, backup='', bufsize=0, mode='r', openhook=None)
    not thread safe , creates global state 
    Create an instance of the FileInput class.

class fileinput.FileInput(files=None, inplace=False, backup='', bufsize=0, mode='r', openhook=None)
    it has a readline() method which returns the next input line, 
    and a __getitem__() method which implements the sequence behavior. 
    The sequence must be accessed in strictly sequential order; 
    random access and readline() cannot be mixed.
    mode must be one of 'r', 'rU', 'U' and 'rb'.
    The openhook, when given, must be a function that takes two arguments, filename and mode, 
    and returns an accordingly opened file-like object. 
    You cannot use inplace and openhook together.
    Return instance has following attributes 
    filename()
        Return the name of the file currently being read. 
        Before the first line has been read, returns None.
    fileno()
        Return the integer “file descriptor” for the current file. 
        When no file is opened (before the first line and between files), returns -1.
    lineno()
        Return the cumulative line number of the line that has just been read. 
        Before the first line has been read, returns 0. 
        After the last line of the last file has been read, returns the line number of that line.
    filelineno()
        Return the line number in the current file.
        Before the first line has been read, returns 0. 
        After the last line of the last file has been read, 
        returns the line number of that line within the file.
    isfirstline()
        Returns true if the line just read is the first line of its file, otherwise returns false.
    isstdin()
        Returns true if the last line was read from sys.stdin, otherwise returns false.
    nextfile()
        Close the current file so that the next iteration will read the first line from the next file (if any); 
        lines not read from the file will not count towards the cumulative line count. 
        The filename is not changed until after the first line of the next file has been read. 
        Before the first line has been read, this function has no effect;
        it cannot be used to skip the first file. 
        After the last line of the last file has been read, this function has no effect.
    close()
        Close the sequence.


###*** Data Compression and Archiving
#https://docs.python.org/3/library/archiving.html


##tarfile Mode and Action 
'r' or 'r:*'        Open for reading with transparent compression (recommended). 
'r:'                Open for reading exclusively without compression. 
'r:gz'              Open for reading with gzip compression. 
'r:bz2'             Open for reading with bzip2 compression. 
'r:xz'              Open for reading with lzma compression. 
'x' or 'x:'         Create a tarfile exclusively without compression. 
'x:gz'              Create a tarfile with gzip compression. 
'x:bz2'             Create a tarfile with bzip2 compression. 
'x:xz'              Create a tarfile with lzma compression.
'a' or 'a:'         Open for appending with no compression. The file is created if it does not exist. 
'w' or 'w:'         Open for uncompressed writing. 
'w:gz'              Open for gzip compressed writing. 
'w:bz2'             Open for bzip2 compressed writing. 
'w:xz'              Open for lzma compressed writing. 


##a TarFile object that processes its data as a stream of blocks
#Use this with sys.stdin, a socket file object or a tape device
#Does not support random access 
#Mode       Action
'r|*'       Open a stream of tar blocks for reading with transparent compression. 
'r|'        Open a stream of uncompressed tar blocks for reading. 
'r|gz'      Open a gzip compressed stream for reading. 
'r|bz2'     Open a bzip2 compressed stream for reading. 
'r|xz'      Open an lzma compressed stream for reading. 
'w|'        Open an uncompressed stream for writing. 
'w|gz'      Open a gzip compressed stream for writing. 
'w|bz2'     Open a bzip2 compressed stream for writing. 
'w|xz'      Open an lzma compressed stream for writing. 


#extract an entire tar archive to the current working directory:

import tarfile
tar = tarfile.open("sample.tar.gz")
tar.extractall()
tar.close()

#extract a subset of a tar archive with TarFile.extractall() 
#using a generator function instead of a list:


import os
import tarfile

def py_files(members):
    for tarinfo in members:
        if os.path.splitext(tarinfo.name)[1] == ".py":
            yield tarinfo

tar = tarfile.open("sample.tar.gz")
tar.extractall(members=py_files(tar))
tar.close()


#create an uncompressed tar archive from a list of filenames:
import tarfile
tar = tarfile.open("sample.tar", "w")
for name in ["foo", "bar", "quux"]:
    tar.add(name)
tar.close()

#OR 
import tarfile
with tarfile.open("sample.tar", "w") as tar:
    for name in ["foo", "bar", "quux"]:
        tar.add(name)




##Example zipfile , creation a ZIP (tarfile is similar)
$ python -m zipfile -c monty.zip spam.txt eggs.txt
$ python -m zipfile -c monty.zip life-of-brian_1979/

#extract a ZIP archive into the specified directory, use the -e option:
$ python -m zipfile -e monty.zip target-dir/

#For a list of the files in a ZIP archive, use the -l option:
$ python -m zipfile -l monty.zip


##Testing correct ZIP Files
import zipfile

for filename in [ 'README.txt', 'example.zip',   'bad_example.zip', 'notthere.zip' ]:
    print '%20s  %s' % (filename, zipfile.is_zipfile(filename))

#Output 
README.txt  False
example.zip  True
bad_example.zip  False
notthere.zip  False

##Reading Meta-data from a ZIP Archive
import datetime
import zipfile

zf = zipfile.ZipFile('example.zip', 'r')
print zf.namelist()  #list of files 

def print_info(archive_name):
    zf = zipfile.ZipFile(archive_name)
    for info in zf.infolist():
        print info.filename
        print '\tComment:\t', info.comment
        print '\tModified:\t', datetime.datetime(*info.date_time)
        print '\tSystem:\t\t', info.create_system, '(0 = Windows, 3 = Unix)'
        print '\tZIP version:\t', info.create_version
        print '\tCompressed:\t', info.compress_size, 'bytes'
        print '\tUncompressed:\t', info.file_size, 'bytes'
        print

print_info('example.zip')

#Writing 
with ZipFile('spam.zip', 'w') as myzip:
    myzip.write('eggs.txt')

#Reading 
with ZipFile('spam.zip') as myzip:
    with myzip.open('eggs.txt') as myfile:
        print(myfile.read())
        
#Create PY file zip 
zf = PyZipFile('myprog.zip')
def notests(s):
    fn = os.path.basename(s)
    return (not (fn == 'test' or fn.startswith('test_')))
zf.writepy('myprog', filterfunc=notests)

#The writepy() method makes archives with file names like this:
string.pyc                   # Top level name
test/__init__.pyc            # Package directory
test/testall.pyc             # Module test.testall
test/bogus/__init__.pyc      # Subpackage directory
test/bogus/myfile.pyc        # Submodule test.bogus.myfile
        

##API 
class zipfile.ZipFile(file, mode='r', compression=ZIP_STORED, allowZip64=True, compresslevel=None)
    Open a ZIP file
    The mode parameter should be 'r' to read an existing file, 'w' to truncate and write a new file, 
    'a' to append to an existing file, or 'x' to exclusively create and write a new file.
    compression is the ZIP compression method to use when writing the archive, 
    and should be ZIP_STORED, ZIP_DEFLATED, ZIP_BZIP2 or ZIP_LZMA; 
    Returns instance which have following attributes 
    ZipFile.close()
        Close the archive file. 
    ZipFile.getinfo(name)
        Return a ZipInfo object with information about the archive member name. 
    ZipFile.infolist()
        Return a list containing a ZipInfo object for each member of the archive. 
    ZipFile.namelist()
        Return a list of archive members by name.
    ZipFile.open(name, mode='r', pwd=None, *, force_zip64=False)
        Access a member of the archive as a binary file-like object. n
        ame can be either the name of a file within the archive or a ZipInfo object. 
        The mode parameter, if included, must be 'r' (the default) or 'w'. 
        pwd is the password used to decrypt encrypted ZIP files.
        With mode 'r' the file-like object (ZipExtFile) is read-only and provides the following methods: 
            read(), readline(), readlines(), seek(), tell(), __iter__(), __next__(). 
        With mode='w', a writable file handle is returned, which supports the write() method. 
        While a writable file handle is open, attempting to read or write other files in the ZIP file 
        will raise a ValueError.
        When writing a file, if the file size is not known in advance but may exceed 2 GiB, 
        pass force_zip64=True to ensure that the header format is capable of supporting large files. 
    ZipFile.extract(member, path=None, pwd=None)
        Extract a member from the archive to the current working directory;
        member must be its full name or a ZipInfo object. 
        Returns the normalized path created (a directory or new file).
    ZipFile.extractall(path=None, members=None, pwd=None)
        Extract all members from the archive to the current working directory. 
        path specifies a different directory to extract to. 
    ZipFile.printdir()
        Print a table of contents for the archive to sys.stdout.
    ZipFile.setpassword(pwd)
        Set pwd as default password to extract encrypted files.
    ZipFile.read(name, pwd=None)
        Return the bytes of the file name in the archive. 
        name is the name of the file in the archive, or a ZipInfo object. 
        The archive must be open for read or append. 
        pwd is the password used for encrypted files 
    ZipFile.testzip()
        Read all the files in the archive and check their CRC’s and file headers. 
        Return the name of the first bad file, or else return None.
    ZipFile.write(filename, arcname=None, compress_type=None, compresslevel=None)
        Write the file named filename to the archive, giving it the archive name arcname 
        (by default, this will be the same as filename, but without a drive letter and with leading path separators removed). 
    ZipFile.writestr(zinfo_or_arcname, data, compress_type=None, compresslevel=None)
        Write the string data to the archive; 
        zinfo_or_arcname is either the file name it will be given in the archive, or a ZipInfo instance.
    ZipFile.filename
        Name of the ZIP file.
    ZipFile.debug
        The level of debug output to use. This may be set from 0 (the default, no output) to 3 (the most output). 
        Debugging information is written to sys.stdout.
    ZipFile.comment
        The comment text associated with the ZIP file. 

class zipfile.PyZipFile(file, mode='r', compression=ZIP_STORED, allowZip64=True, optimize=-1)
    If the optimize parameter to PyZipFile was not given or -1, the corresponding file is a *.pyc file, compiling if necessary.
    Instances have one method in addition to those of ZipFile objects:
    writepy(pathname, basename='', filterfunc=None)
        Search for files *.py and add the corresponding file to the archive.


###*** shutil — High-level file operations

shutil.make_archive(base_name, format[, root_dir[, base_dir[, verbose[, dry_run[, owner[, group[, logger]]]]]]])
    Create an archive file (such as zip or tar) and return its name.
    base_name is the name of the file to create, including the path, minus any format-specific extension. 
    format is the archive format: one of “zip” (if the zlib module is available), “tar”, “gztar” (if the zlib module is available), “bztar” (if the bz2 module is available), or “xztar” (if the lzma module is available).
    root_dir is a directory that will be the root directory of the archive; for example, we typically chdir into root_dir before creating the archive.
    base_dir is the directory where we start archiving from; i.e. base_dir will be the common prefix of all files and directories in the archive.
    root_dir and base_dir both default to the current directory.
    If dry_run is true, no archive is created, but the operations that would be executed are logged to logger
shutil.unpack_archive(filename[, extract_dir[, format]])
    Unpack an archive. 
    filename is the full path of the archive.
    extract_dir is the name of the target directory where the archive is unpacked. 
    If not provided, the current working directory is used.
    format is the archive format: one of “zip”, “tar”, “gztar”, “bztar”, or “xztar”. 
    
#Example 
from shutil import make_archive
import os
archive_name = os.path.expanduser(os.path.join('~', 'myarchive'))
root_dir = os.path.expanduser(os.path.join('~', '.ssh'))
>>> make_archive(archive_name, 'gztar', root_dir)
'/Users/tarek/myarchive.tar.gz'


#remove a directory tree on Windows where some of the files have their read-only bit set. 
#It uses the onerror callback to clear the readonly bit and reattempt the remove. 
#Any subsequent failure will propagate.

import os, stat
import shutil

def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)

shutil.rmtree(directory, onerror=remove_readonly)


#example that uses the ignore_patterns() helper:
from shutil import copytree, ignore_patterns

copytree(source, destination, ignore=ignore_patterns('*.pyc', 'tmp*'))


#example that uses the ignore argument to add a logging call:
from shutil import copytree
import logging

def _logpath(path, names):
    logging.info('Working in %s', path)
    return []   # nothing will be ignored

copytree(source, destination, ignore=_logpath)

##API 
shutil.copyfileobj(fsrc, fdst[, length])
    Copy the contents of the file-like object fsrc to the file-like object fdst. 
shutil.copyfile(src, dst, *, follow_symlinks=True)
    Copy the contents (no metadata) of the file named src to a file named dst and return dst. 
    src and dst are path names given as strings. 
shutil.copymode(src, dst, *, follow_symlinks=True)
    Copy the permission bits from src to dst. 
    The file contents, owner, and group are unaffected. 
    src and dst are path names given as strings. 
shutil.copystat(src, dst, *, follow_symlinks=True)
    Copy the permission bits, last access time, last modification time, and flags from src to dst. 
    The file contents, owner, and group are unaffected. 
    src and dst are path names given as strings.
shutil.copy(src, dst, *, follow_symlinks=True)
    Copies the file src to the file or directory dst. src and dst should be strings. 
    If dst specifies a directory, the file will be copied into dst using the base filename from src. 
    Returns the path to the newly created file.
shutil.copy2(src, dst, *, follow_symlinks=True)
    Identical to copy() except that copy2() also attempts to preserve all file metadata.
shutil.ignore_patterns(*patterns)
    This factory function creates a function that can be used as a callable 
    for copytree()’s ignore argument, 
shutil.copytree(src, dst, symlinks=False, ignore=None, copy_function=copy2, ignore_dangling_symlinks=False)
    Recursively copy an entire directory tree rooted at src, returning the destination directory. 
    The destination directory, named by dst, must not already exist; 
shutil.rmtree(path, ignore_errors=False, onerror=None)
    Delete an entire directory tree; 
    path must point to a directory (but not a symbolic link to a directory). 
shutil.move(src, dst, copy_function=copy2)
    Recursively move a file or directory (src) to another location (dst) and return the destination.
    If the destination is an existing directory, then src is moved inside that directory. 
    If the destination already exists but is not a directory
shutil.disk_usage(path)
    Return disk usage statistics about the given path as a named tuple 
    with the attributes total, used and free, 
    which are the amount of total, used and free space, in bytes. 
    On Windows, path must be a directory; on Unix, it can be a file or directory.
shutil.chown(path, user=None, group=None)
    Change owner user and/or group of the given path.
shutil.which(cmd, mode=os.F_OK | os.X_OK, path=None)
    Return the path to an executable which would be run if the given cmd was called. 

###*** Doctest 
#The output should exactly match interpretor output including blanks
#Next test case is either blank line or >>> (should not contain any blanks)

def square(x):
    r"""Saure function
    takes one arg
    
    >>> square(10)#doctest: +REPORT_NDIFF
    100
    
    >>> [1,2,3] #doctest: +ELLIPSIS
    [...
    
    >>> [1,2,3,4] #doctest: +NORMALIZE_WHITESPACE
    [1, 2, 
    3, 4]
    
    >>> print(1,2,3,4,sep='\n\n')
    1
    <BLANKLINE>
    2
    <BLANKLINE>
    3
    <BLANKLINE>
    4
    
    >>> 1/0
    Traceback (most recent call last):
    ...
    ZeroDivisionError: division by zero

    """
    z = x*x 
    return z
    
#python -m doctest -v filename 
#or 
#with below, python filename -v 
if __name__ == "__main__":
    import doctest
    doctest.testmod()