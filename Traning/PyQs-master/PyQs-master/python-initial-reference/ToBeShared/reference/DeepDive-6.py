Relative import 
__init__.py 's use 
property 
pickle — Python object serialization
Context Management Pattern - to be used with 'with'
Iterator Pattern
Lazy computations via yield from
New style class and Accessor methods 
proxy Pattern 
Decorator patterns - same in py2.7 and py3.x
singleton Pattern 
Abstract class 
Quick introduction to Multithreading and MultiProccessing 
Multi Threading 
multiprocessing 
Web Page & CGI Programming
Django - Chapter-1
Django - chapter-2 
Django - Chapter-3 
Django - Chapter-4
Django -chapter-5 
Example - Django blog using Django packages 
Simple blog using Django
-------------------------------------------------


###*** Relative import 
#A single leading dot indicates a relative import, 
#starting with the current package. 

#Two or more leading dots give a relative import to the parent(s) of the current package,

#Example 
package/
    __init__.py
    subpackage1/
        __init__.py
        moduleX.py
        moduleY.py
    subpackage2/
        __init__.py
        moduleZ.py
    moduleA.py


#Current file is moduleX.py :
 
from .moduleY import spam
from .moduleY import spam as ham
from . import moduleY
from ..subpackage1 import moduleY
from ..subpackage2.moduleZ import eggs
from ..moduleA import foo
from ...package import bar  ##package\__init__.py must have bar 



###*** __init__.py 's use 

#Ex:
package/
    __init__.py
    file.py
    file2.py



##USAGE-1: Normally, use import like
from package.file import File

#if package/__init__.py contains below 
from file import File

#Can use like below in user file
from package import File

##USAGE-2: when you do below

from package import *

#default behaviour of import * in module file 
#is to import all symbols that do not begin with an underscore, from the given namespace

#default behaviour of import * for package if there is no __all__ or not code , not to import anything 

# __all__ is a list of strings defining what symbols in a module(module name, function, object) will be exported 

#if  package/__init__.py contains below 
from file import func, var, Myclass 

__all__ = ['func', 'file2', 'var', 'Myclass']


#it imports all modules from __all__




##USAGE-3:Any class, methods defined in __init__.py would be automatically available 
#when user import the package 
#An example
database/
    __init__.py
    schema.py
   ...

#__init__.py
import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine(os.environ['DATABASE_URL'])
Session = sessionmaker(bind=engine)

def method():
    pass
    
class C:
    pass

#User can do below
from database import Session, method, C
session = Session()



#Usage-4:__init__.py can  contain anything as it itself is a py file, 
#But below are generally used for special purpose(not so standardised)
__version__ = '0.1'
__author__ = 'Cardinal Biggles'

>>> import email
>>> email.__version__
'5.1.0'





###*** property 

##property - attribute -  Py3.x and Py2.7 works same way if Py2.7 class are new style(derives from object)
prop = property(fget, fset, fdel, doc)
#for readonly - make property(fget, None, None, doc)

class D(object):	
    def __init__(self, p):
        self._prop = p
    def p_get(self):
        return self._prop
    def p_set(self, val):
        self._prop = val
    def p_del(self):
        del self._prop	
    prop = property(p_get, p_set, p_del,"This is property")   #instance.prop

#Or using a decorator, for read-only, keep only @property section

class C:
    def __init__(self):
        self._x = None

    @property			#get 
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter				#set
    def x(self, value):
        self._x = value

    @x.deleter				#del 
    def x(self):
        del self._x
        
        
        
###*** pickle — Python object serialization
#a Python object hierarchy is converted into a byte stream, 
#and 'unpickling' is the inverse operation

#Important methods
#fix_imports must be true and protocol =2  for compatibility with python2
#Protocol can be 3 (default one) for new proptocol of Python3

pickle.dump(obj, file, protocol=None, *, fix_imports=True)  #dumps obj to file which has .write() method eg file or io.BytesIO 
pickle.dumps(obj, protocol=None, *, fix_imports=True)       #dumps obj to bytes string
class pickle.Pickler(file, protocol=None, *, fix_imports=True)
    dump(obj)
        Write a pickled representation of obj to the open file object given in the constructor.


#unpickling
pickle.load(file, *, fix_imports=True, encoding="ASCII", errors="strict") #file object 
pickle.loads(bytes_object, *, fix_imports=True, encoding="ASCII", errors="strict")  #reads from bytes 
class pickle.Unpickler(file, *, fix_imports=True, encoding="ASCII", errors="strict")
    load()
        Read a pickled object representation from the open file object given in the constructor, and return the reconstituted object 


>>> a = 100.2
>>> b = pickle.loads(pickle.dumps(a))
>>> b == a
True


#The following types can be pickled:
#When functions, classes are pickled, and then unpickled, 
#the module defining class/functions must be be imported to get their definition

#While class is pickled, only instance data is pickled, 
#neither class variables nor class method definition

1.None, True, and False
2.integers, floating point numbers, complex numbers
3.strings, bytes, bytearrays
4.tuples, lists, sets, and dictionaries containing only picklable objects
5.functions defined at the top level of a module (using def, not lambda)
6.built-in functions defined at the top level of a module
7.classes that are defined at the top level of a module
8.instances of such classes whose __dict__ 
  or the result of calling __getstate__() is picklable 



#Default behaviour of class instance for pickle and unpickle are  Ok for most of the cases
#but can be customized by 
object.__getstate__()		
    if the class defines the method __getstate__(), it is called 
    and the returned object is pickled as the contents for the instance,
    instead of the contents of the instance's dictionary

object.__setstate__(state)
    Upon unpickling, if the class defines __setstate__(), 
    it is called with the unpickled state

#Example:
class TextReader:
    """Print and number lines in a text file."""
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename)
        self.lineno = 0
    def readline(self):
        self.lineno += 1
        line = self.file.readline()
        if not line:
            return None
        if line.endswith('\n'):
            line = line[:-1]
        return "%i: %s" % (self.lineno, line)
    def __getstate__(self):
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['file']
        return state
    def __setstate__(self, state):
        # Restore instance attributes (i.e., filename and lineno).
        self.__dict__.update(state)
        # Restore the previously opened file's state. To do so, we need to
        # reopen it and read from it until the line count is restored.
        file = open(self.filename)
        for _ in range(self.lineno):
            file.readline()
        # Finally, save the file.
        self.file = file


#usage 
>>> reader = TextReader("hello.txt")
>>> reader.readline()
'1: Hello world!'
>>> reader.readline()
'2: I am line number two.'
>>> new_reader = pickle.loads(pickle.dumps(reader))
>>> new_reader.readline()
'3: Goodbye!'



###*** Context Management Pattern - to be used with 'with'
#same in py2.7 and Py3.x


from __future__ import print_function  #py2.x
from __future__ import with_statement  #py2.x

class A(object):
	def __init__(self, name):
		self.name = name
	def hello(self):
		print('hello %s!' % (self.name,))
	def __enter__(self):
		print('Enter the function')
		return self   #must return self or a class which implements __exit__
	def __exit__(self, exc_type, exc_value, traceback):
		print('Exit the function')


with A("das") as a:
	print(a.hello())
	


###*** Iterator Pattern
		
# Examples of Iterators - Single Pass
class Squares0: 				
	def __init__(self, start, stop): 	
		self.start = start
		self.stop = stop
		self.c = start
	def __iter__(self):
		return self				#must return self or a class instance which implements __next__
	def __next__(self):			# for py3.3 , for py2.7 it is next()
		if self.c >= self.stop : raise StopIteration
		self.c += 1
		return (self.c-1)**2
s = Squares0(1,10)
I1 = iter(s); I2=iter(s)
next(I1), next(I2)  #(1, 4)
next(I1), next(I2) #(9, 16)

#Alternate version- MultiPass- use Yield
class Squares: 				
	def __init__(self, start, stop): 	
		self.start = start
		self.stop = stop
	def __iter__(self):
		for value in range(self.start, self.stop + 1):
			yield value ** 2

			
>>> i = iter(Squares(1,5))
>>> next(i)
1


##Generator  pattern along with Iterator


def generate_ints(N):
    for i in range(N):
        yield i*i

def counter (maximum):
    i = 0
    while i < maximum:
        val = (yield i)
        # If value provided, change counter
        if val is not None:
            i = val
        else:
            i += 1
			
s = iter(counter(1000))
next(s)
s.send(50)
next(s)


##generator object for both version

a =  (x*x for x in range(100))
next(a)
next(a)


#Upto some n
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

#Infinite
def fib():
    a, b = 0, 1
    while 1:
        yield a
        a, b = b, a + b

a = iter(fib())
next(a)
0

import itertools as it

for x in it.islice(next(a), 20):
    print x


class Fib: 				
	def __init__(self, a=0, b=1): 	
		self.a, self.b = a,b 
	def __iter__(self):
		while 1:
			yield self.a
			self.a, self.b = self.b, self.a + self.b

	
#with functions			
def fib1():
	a,b = 0,1
	def g():
		nonlocal a,b  #else UnboundLocalError: local variable 'b' referenced before assignment
		a,b = b, a+b
		return a
	return g
    
###*** Lazy computations via yield from
	
#https://docs.python.org/3/library/itertools.html

#itertools.count(start,[step])   -> start, start+step...
#itertools.repeat(element, [n])

#dropwhile(predicate, iterable)
#takewhile(predicate, iterable)
#islice(iterable, start, stop[, step]) or islice(iterable, stop)
#tee(iterable, n=2) --> tuple of n independent iterators. (memoized version of it, hence very fast)


# Few lazy definition
from itertools import *

def iterate(x,f):
	yield f(x)
	yield from iterate(f(x),f)
	
#eg #itertools.count(start,[step])  can be implemented as 

def count(st):
	import functools
	import operator
	f = functools.partial(operator.add, 1)
	yield st
	yield from iterate(st, f)
	
	
#Few more functions
def tail(iterable):  
	return islice(iterable, 1, None)
	

def take(iterable, n):  
	return list(islice(iterable, 0, n))

def head(iterable):  
	return list(islice(iterable, 1))

#or if islice is not wanted

def tail(it):
	it = iter(it)
	next(it)
	return it


def take(it, n):
	it = iter(it)
	return [ next(it) for i in range(n) ]


def head(it):
	it = iter(it);
	return next(it)
	
#few fibs implementations

def fibfrom(a = 0, b = 1):
	yield a
	yield from fibfrom(b, a+b)
	

>>> take(fibfrom(), 100)

def fib_inf():
	yield from iterate( (0,1) , lambda t: ( t[1], t[0] + t[1]) )

>>> take(map(lambda x: x[0], fib_inf()), 10)

#inefficient as double recursion via fibs() and  tail(fibs()) and no memoization
def fibs():
	import operator
	yield 0
	yield 1
	yield from map(operator.add, fibs(), tail(fibs()))

>>> take(fibs(), 10)

#efficient, using tee to copy instead of double recursion
def fibs():
	import operator
	import itertools
	yield 1
	yield 1
	fibs1, fibs2 = itertools.tee(fibs())
	yield from map(operator.add, fibs1, tail(fibs2))

	        
        
        
        

###*** New style class and Accessor methods 
__getattr__(), __setattr__(),   __delattr__()
'''
-In Python 3.X, all classes are automatically 'new style'
whether they explicitly inherit from object or not.

-In Python 2.x, you need to inheritate from object to get "New Style", eg 
class MyClass(object) :

Properties of 'new style'

1. object as root class

2. Attribute/special method Fetch from an instance of class and from class

    case 1. Instance,I, attribute access – Search below
        a. The __dict__ of the instance I
        b. The __dict__ of all classes on the __mro__ found at I's __class__, from left to right  

    case 2. Class attribute access – Search Below
        a. The __dict__ of all classes on the __mro__ found at C itself, from left to right
        b. The __dict__ of all metaclasses on the __mro__ found at C's __class__, from left to right

3. In both rule 1 and 2, skip step (a) 
   for built-in  implicit operations ( eg __SpecialMethod__  for  str, len , [], in  etc)
   searches only class (case 1) or metaclass(case 2)

4. For Built-in  implicit operations ie __SpecialMethod__ (Py3.x):
   __getattr__ (if __SpecialMethod__ undefined)and __getattribute__ (for all read access)
   of class(case 1) or metaclass(case 2 ) are not called  
   but not skipped for explicit method(via .__SpecialMethod__(..)) invocation

Hence required operator overloading methods for builtins 
must be implemented at class(case 1) and metaclass(case 2)
'''

#name is string , value is of actual type 
def __getattr__(self, name): 		# On undefined attribute fetch [obj.name], for old and new style
def __getattribute__(self, name): 	# On all attribute fetch [obj.name], new style
def __setattr__(self, name, value): # On all attribute assignment [obj.name=value]
def __delattr__(self, name): 		# On all attribute deletion [del obj.name]

##builtins method to access above 
getattr(object, name[, default]) -> value  # object.name 
setattr(object, name, value)               #object.name = value
delattr(object, name)					   # del object.name

#Class -Attribute fetching - WARNING 

class Example 
    def __getattr__(self, attrname): 	
            if attrname == 'age':
                return 40
            else:
                raise AttributeError(attrname)

    def __setattr__(self, attr, value):  			# for all setting
            if attr == 'age':
                self.__dict__[attr] = value + 10 	# does not include __slot__
            else:
                raise AttributeError(attr + ' not allowed')

    def __getattribute__(self, name):
            x = object.__getattribute__(self, name)   # Must use object. else infine loop


#Note following would loops infinitely in __setattr__
self.age = value + 10 			# Loops
setattr(self, attr, value + 10) # Loops (attr is 'age')

#use below in __setattr__
self.__dict__[attr] = value + 10 			# OK: doesn't loop
object.__setattr__(self, attr, value + 10) 	# OK: doesn't loop (new-style only)
		
#To be inclusive of slot and properties, use always object.__setattr__


##Detailed Example 
class Meta(type):
	def __getattribute__(*args):
		print("Metaclass getattribute invoked")
		return type.__getattribute__(*args)


class C(object, metaclass=Meta):
	def __len__(self):
		return 10
	def __getattribute__(*args):
		print("Class getattribute invoked")
		return object.__getattribute__(*args)

c = C()
>>> c.__len__()                 # Explicit lookup via instance, class's
Class getattribute invoked      #__getattribute__ called 
10

>>> type(c).__len__(c)          # Explicit lookup via type, metaclass's getttribute
Metaclass getattribute invoked
10
>>> len(c)                      # Implicit lookup , __getattribute__ of class skipped
10

>>> len(C)						# Implicit lookup , __getattribute__ of metaclass skipped
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: object of type 'Meta' has no len()

>>> bool(c)               #from object's
True

>>> c < C()                        #Implicit lookup , __getattribute__ of class skipped
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unorderable types: C() < C()

>>> c.__lt__(C())                 # Explicit lookup via instance, class's getttribute
Class getattribute invoked
NotImplemented

>>> C.__lt__(C,C)                 # Explicit lookup via type, metaclass's getttribute
Metaclass getattribute invoked
NotImplemented

>>> c.__len__ = lambda self : 3    #instance's

>>> len(c)						   # only class's one called, instance skipped
10

>>> c.__len__()                    # if you add from outside, you have to pass 'self' explicitly  
Class getattribute invoked
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: <lambda>() missing 1 required positional argument: 'self'

>>> c.__len__(c)                  #class's getattribute gets the calls, but self has to be explicit
Class getattribute invoked
3

>>> getattr(c, '__len__')       #Explicit lookup via instance, class's getttribute
Class getattribute invoked
<function <lambda> at 0x0239C4B0>

>>> getattr(c, '__lt__')  	#Explicit lookup via instance, class's getttribute
Class getattribute invoked
<method-wrapper '__lt__' of C object at 0x02361F90>

>>> getattr(c, '__lt__')(c)
Class getattribute invoked
NotImplemented





###*** proxy Pattern 

def __getattr__(self, name): 		# On undefined attribute fetch [obj.name], for old and new style
def __getattribute__(self, name): 	# On all attribute fetch [obj.name], new style
def __setattr__(self, name, value): # On all attribute assignment [obj.name=value]
def __delattr__(self, name): 		# On all attribute deletion [del obj.name]

#Note in new style(Py3, Py2.7 when deriving from object), you must implement for all overloading operator explicitly 
#because - __getattr__ and __getattribute__ are not called for builtins eg [], len etc 


#proxy - pattern

class Implementation2:
    def f(self):
        print("Implementation.f()")
    def g(self):
        print("Implementation.g()")
    def h(self):
        print("Implementation.h()")

class Proxy2:
    def __init__(self):
        self.__implementation = Implementation2()
    def __getattr__(self, name):
        return getattr(self.__implementation, name)

p = Proxy2()
p.f(); p.g(); p.h();




    

###*** Decorator patterns - same in py2.7 and py3.x

def ConvertString(org):
	def _inner(*args, **kargs):
		res = org(*args, **kargs)
		return str(res)
	return _inner

	
@ConvertString
def f(x,y):
	return x+y


##stacking of decorator
def  mockReturnConstant(fun):
	def _mydec(*args, **kargs):		
		res = fun(*args, **kargs)		
		return 10
	return _mydec
	
@ConvertString        #last application's decorator must be at first
@mockReturnConstant
def f(x):
	return x*x

#tracing
def  mydec(fun):
	def _mydec(*args, **kargs):
		print("calling " + fun.__name__)
		res = fun(*args, **kargs)
		print("ending " + fun.__name__)
		return res
	return _mydec

@mydec
def f(x):
	return x*x
	
f(2)

##Decorator taking argument
def makeDefault100(f):
	def org(*args):
		val = args[1] if len(args) > 1 else 100
		return f(*args) if len(args) > 1 else f(*args,y=val)
	return org

@makeDefault100
def f1(x,y):
	return x+y

	
f1(2)
f1(2,3)	

# Example with Decorator argument
def makeDefault(d):
	def aDec(f):
		def org(*args):
			val = args[1] if len(args) > 1 else d
			return f(*args) if len(args) > 1 else f(*args,y=val)
		return org
	return aDec

@makeDefault(50)
def f1(x,y):
	return x+y

	
f1(2)
f1(2,3)	

##Creating a well defined decorator , 
#such that all attributes of original are preserved
from functools import wraps

def iter_f(func):
	@wraps(func)
    def newf(*args, **kwargs):
        for i in range(10):
            res = func(*args, **kwargs)
			print(res)
    return newf

@iter_f
def f(x):
	return x*x
	
	
def iter_f(d):
	def inner(f):
		@wraps(f)
		def org(*args, **kwargs):
			for i in range(10):
				res = f(*args, **kwargs)
				print(res)
		return org
	return inner
	
	
@iter_f(10)
def f(x):
	return x*x

##Recursive decorator
	
def  mea(fun):
	def _inner(*args, **kargs):
		import time
		now = time.time()
		res = fun(*args,**kargs)
		print(time.time() - now)
		return res
	return _inner
	
	
@mea
def f(x,y):
	return x+y
	

#for recursion it calls many times
@mea
def fib(n):
	return n if n<2 else  fib(n-1) + fib(n-2)
	
#to fix

def  mea(fun):
	def _inner(*args, _first = False, **kargs):
		import time
		if _inner.first :
			_inner.first = False
			_first = True
		now = time.time()
		res = fun(*args,**kargs)
		if _first : 
			_inner.first = True;
			print(time.time() - now)
		return res
	_inner.first = True
	return _inner
	
@mea
def fib(n):
	return n if n<2 else  fib(n-1) + fib(n-2)
	
	
##class decorator
#use below, 
#but for builtins( ie len(x) etc), __getattr__/__getattribute__ is not called
def __getattr__(self, name): 			# On undefined attribute fetch [obj.name], for old and new style
def __getattribute__(self, name): 		# On all attribute fetch [obj.name], new style
def __setattr__(self, name, value): 	# On all attribute assignment [obj.name=value]
def __delattr__(self, name): 			# On all attribute deletion [del obj.name]

#Note in new style(Py3, Py2.7 when deriving from object), you must implement for all overloading operator explicitly 
#because - __getattr__ and __getattribute__ are not called for builtins eg [], len etc 



def decorator(cls): 					# On @ decoration
	class Wrapper:
		def __init__(self, *args): 		# On instance creation
			self.wrapped = cls(*args)
		def __getattr__(self, name): 	# On attribute fetch
			print("Getting " + name + "...")
			return getattr(self.wrapped, name)
	return Wrapper

@decorator
class C: 							# C = decorator(C)
	def __init__(self, x, y): 		# Run by Wrapper.__init__
		self.attr = 'spam'

x = C(6, 7) 		# Really calls Wrapper(6, 7)
print(x.attr) 		# Runs Wrapper.__getattr__, prints "spam"


    
###*** singleton Pattern 

#simple by using __new__ .
# __new__ gets called when instantiation with 'cls' , must call object.__new__ to get a instance, __new__ calls __init__ automatically 
class SingleTone(object):
    __instance = None             #__ means names are mangled 
    def __new__(cls, val):
        if SingleTone.__instance is None:
            SingleTone.__instance = object.__new__(cls)
        SingleTone.__instance.val = val
        return SingleTone.__instance

	
#complex 	way 
class OnlyOne(object):
    class __OnlyOne:
        def __init__(self):
            self.val = None
        def __str__(self):
            return str(self.val)
    instance = None
    def __new__(cls): 				# __new__ always a classmethod
        if not OnlyOne.instance:
            OnlyOne.instance = OnlyOne.__OnlyOne()
        return OnlyOne.instance
    def __getattr__(self, name):     #name is str ,  for any attributes, but not for builtins eh len() etc 
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)

x = OnlyOne()
x.val = 'sausage'
print(x)
y = OnlyOne()
y.val = 'eggs'
print(y)
z = OnlyOne()
z.val = 'spam'
print(z)  #spam 
print(x)  #spam 
print(y)  #spam 


#Singleton using Borg patterns - can be implemented by using inheritance of class Borg
#is to have a single set of state data for all objects
#by setting all the __dict__  to the same static piece of storage

class Borg:
	_shared_state = {}
	def __init__(self):
		self.__dict__ = self._shared_state

		

class Singleton(Borg):
	def __init__(self, arg):
		Borg.__init__(self)
		self.val = arg
	def __str__(self): return self.val

x = Singleton('sausage')
print(x)
y = Singleton('eggs')
print(y)
z = Singleton('spam')
print(z)
print(x)
print(y)


output = '''
sausage
eggs
spam
spam
spam
'''


##using class decorator
class SingletonDecorator:
	def __init__(self,klass):
		self.klass = klass
		self.instance = None
	def __call__(self,*args,**kwds):
		if self.instance == None:
			self.instance = self.klass(*args,**kwds)
		return self.instance


@SingletonDecorator		#not for py2.x
class foo: pass         #foo = SingletonDecorator(foo)  for py2.x


x=foo()
y=foo()
z=foo()
x.val = 'sausage'
y.val = 'eggs'
z.val = 'spam'
print(x.val) #spam 
print(y.val)
print(z.val)


##Using metaclass - Example here for no change after  once creation
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs): #called at instance creation
        if cls not in cls._instances:
            cls._instances[cls] = type.__call__(*args, **kwargs)
        return cls._instances[cls]

#Python2
class MyClass(object):
    __metaclass__ = Singleton

#Python3
class MyClass(metaclass=Singleton):
	def __init__(self,val):
		self.val = val
	def __str__(self):
		return str(self.val)



x = MyClass('sausage')
y=MyClass('eggs')
z=MyClass('spam')
print(x)
print(y)
print(z)
print(x is y is z)



###*** Abstract class 
#In Python 3.X, 

from abc import ABCMeta, abstractmethod

class Super(metaclass=ABCMeta):
		@abstractmethod
		def method(self, arg):
			pass

			
#In Python 2.6 and 2.7, 
class Super:
		__metaclass__ = ABCMeta
		@abstractmethod
		def method(self, arg):
			pass

			

>>> X = Super()
TypeError: Can't instantiate abstract class Super with abstract methods action

>>> class Sub(Super): pass
>>> X = Sub()
TypeError: Can't instantiate abstract class Sub with abstract methods action

class A(Super):
	def method(self, arg):
		print(arg)


>>> a = A()
>>> a.method(2)
2





  
###*** Quick introduction to Multithreading and MultiProccessing 
#note timeout is always in seconds 

##Threading 
#from package threading 
Thread(target,args)     start/join          starts target , no stopping
                        current_thread()    Returns current Thread , has getName() etc 
                        local()             threadlocal, sets by .var_name
#Sync
Thread          join()                      calling thread blocks                
Lock            acquire/release/with        under with, gets lock
RLock           acquire/release/with        under with, gets lock, reentrant
Condition       with/wait_for/notify/notifyAll  consumer wait, producer notify, both under with
Event           is_set/set/wait             one set, other/s checks or wait
Semaphore(n)    acquire/release/with        under with till a number , then blocks
Timer(t,fn)     start                       starts fn after t

#From package Queue 
Queue           put/get/task_done/join      puts pickable objects and gets       
#sharing variable
                global                      Any global variable 
 
#parallelwork 
#from concurrent.futures
ThreadPoolExecutor(max_workers=2) returns executor
executor.map(fn, lst)      Blocks till all work done parallely, returns iterator
executor.submit(fn, val)   Returns future 
                           Future has result, add_done_callback(fn), done() methods
as_completed(fs)           Retruns iterator of completed future 
wait(fs)                   returns done,not_done futures 
 
 
 
 
 
 
 
##multiprocessing 
#(must be in a file under if __name__ == '__main__':)
Process(target,args)     start/join/terminate  starts target 
                         current_process()     Returns current Process 
                                               has name, daemon, pid
#Sync
Process          join()                      calling thread blocks                
Lock            acquire/release/with        under with, gets lock
RLock           acquire/release/with        under with, gets lock, reentrant
Condition       with/wait/notify/notifyAll  consumer wait, producer notify, both under with
Event           is_set/set/wait             one set, other/s checks or wait
Semaphore(n)    acquire/release/with        under with till a number , then blocks

#sending/recvinng 
Queue           put/get/task_done/join      puts pickable objects and gets       
Pipe            send/recv/close             child.send what parent.recv, 
                                            Pipe returns parent, child and Process args is child
#sharing variable 
Value(type, var)         Value returns var can be shared 
Array(type, arr)         Array returns var can be shared 
Manager()                Retuns server process, supports all sync primitives that can be shared
                         Supports Value, Array
                         Supports list and dict that can be shared 
                         
#parallelwork
Pool(n)         map(fn,lst)/join/terminate
                apply_async(fn, args, [callback]) returns result object
                res.get(timeout=n)  gets the result
                res.ready()/res.successful()

#from concurrent.futures
ProcessPoolExecutor(max_workers=2) returns executor
executor.map(fn, lst)      Blocks till all work done parallely, returns iterator
executor.submit(fn, val)   Returns future 
                           Future has result, add_done_callback(fn), done() methods
as_completed(fs)           Retruns iterator of completed future 
wait(fs)                   returns done,not_done futures




###*** Multi Threading 

class threading.local
    Thread-local data is data whose values are thread specific. 
    To manage thread-local data, just create an instance of local (or a subclass) 
    and store attributes on it
    mydata = threading.local()
    mydata.x = 1
    The instance’s values will be different for separate threads.
    
class threading.Thread(group=None, target=None, name=None, 
            args=(), kwargs={}, *, daemon=None)
    start()
        Start the thread’s activity.
    run()
        You may override this method in a subclass. 
    join(timeout=None)
        Wait until the thread terminates.
    name
        A string used for identification purposes only. 
    getName()
    setName()
    ident
    is_alive()
    daemon
        A boolean value indicating whether this thread is a daemon thread (True) or not (False). 
        This must be set before start() is called, otherwise RuntimeError is raised. 
        when main returns, your process will not exit if there are non-daemon threads still running.
        But process exits when only demonic threads are present, (and in process cleanup, those are also killed automatically)
        If a thread returns after work, then this flag does not matter 
        Daemon threads are usually for things that run in a loop and don't exit on their own
    isDaemon()
    setDaemon()

#Other methods 
threading.active_count()
threading.current_thread()
threading.get_ident()
threading.enumerate()
    Return a list of all Thread objects currently alive.
    The list includes daemonic threads, dummy thread objects created by current_thread(), 
    and the main thread. 
    It excludes terminated threads and threads that have not yet been started.
threading.main_thread()
threading.settrace(func)
    Set a trace function for all threads started from the threading module. 
    The func will be passed to sys.settrace() for each thread, before its run() method is called.
threading.setprofile(func)
    Set a profile function for all threads started from the threading module. 
    The func will be passed to sys.setprofile() for each thread, before its run() method is called.
threading.stack_size([size])
    Return the thread stack size used when creating new threads. 
    The optional size argument specifies the stack size to be used for subsequently created threads, 
    and must be 0 (use platform or configured default) 
    or a positive integer value of at least 32,768 (32 KiB). 

    
    
#Example 
import threading
import time
import random

def  f():
	time.sleep(random.randint(10,15))
	print(threading.current_thread().getName())


th = list();

for ele in range(20):
	t = threading.Thread(target=f, name="Thread " + str(ele))
	t.start()
	th.append(t)

#--------------------Join--------------------------------


import time
import random

def w():
	time.sleep(random.randint(10,15))
	print("Thread finished")
	
t = threading.Thread(target=w)
t.start(); print("Main thread")


t = threading.Thread(target=w)
t.start(); t.join(); print("Main thread")



		
#--------------------------------CONCURRENT EXAMPLES-----------------------
#Version Py3.x
#GIL is not initialised until the threading support is imported, or initialised via the C API, 
#GIL is released for i/o bound eg network or using NumPy modules
#for CPython, alternate approach is
#use  multiprocessing module, migrate from threaded code to multiprocess code, (good for long code)
#use concurrent.futures, Use ThreadPoolExecutor  to dispatch  to multiple threads (for IO bound operations) 
#or Use ProcessPoolExecutot to dispatch to multiple processes (for CPU bound operations), 
#or use the asyncio module in Python 3.4 (which provides full support for explicit asynchronous programming in the standard library) 
#or use async/await syntax for native coroutines in Python 3.5.
#or use event driven eg Twisted library

#fs is list of futures , can only be created by ex.submit(...)
concurrent.futures.wait(fs, timeout=None, return_when=ALL_COMPLETED)
    returns (done_futures, pending_futures)
    return_when can be FIRST_COMPLETED, FIRST_EXCEPTION,ALL_COMPLETED
concurrent.futures.as_completed(fs, timeout=None)
    Returns an iterator over the Future instances 
    given by fs that yields futures as they complete 
    (finished or were cancelled).
    
class concurrent.futures.ProcessPoolExecutor(max_workers=None, mp_context=None, 
            initializer=None, initargs=())
    Uses multiprocessing module, 
    calling code must be wrapped inside __name__ == '__main__' block 
    only picklable objects can be executed and returned.
class concurrent.futures.ThreadPoolExecutor(max_workers=None, thread_name_prefix='', 
        initializer=None, initargs=())
    initializer is an optional callable that is called at the start of each worker thread/process; 
    initargs is a tuple of arguments passed to the initializer
    submit(fn, *args, **kwargs)
        returns a Future 
    map(func, *iterables, timeout=None, chunksize=1)
        returns Iterator of values of the result, not future 
    shutdown(wait=True)
    
    
class concurrent.futures.Future
    Future instances are created by Executor.submit() 
    cancel()
        Attempt to cancel the call. Returns true/false if cancelled 
    cancelled()
        Return True if the call was successfully cancelled.
    running()
        Return True if the call is currently being executed and cannot be cancelled.
    done()
        Return True if the call was successfully cancelled or finished running.
    result(timeout=None)
        Return the value returned by the call. Blocks till timeout if not done 
        If the future is cancelled before completing then CancelledError will be raised.
        If the call raised, this method will raise the same exception.
    exception(timeout=None)
        Return the exception raised by the call. 
    add_done_callback(fn_with_one_arg_of_future)
        calls fn when the future is cancelled or finishes running.
        Added callables are called in the order that they were added 
        and are always called in a thread which added them 
        If the callable raises a Exception subclass, 
        it will be logged and ignored.
    
#Example 
import threading
import concurrent.futures  #in Py2, must do, pip install futures
import requests
import time

def load(url):
    import requests
    import time
    import threading
    time.sleep(5)
    print("Starting to download ", url, " from thread ", threading.current_thread().getName())
    conn = requests.get(url)    
    return [url, len(conn.text)]

def load(url):    
    import time 
    import random 
    time.sleep(5)
    print("Starting to download ", url, " from thread ", 
            threading.current_thread().getName())
    res = [url, random.randint(2000,3000)]    
    return res
    
    
result = []
#note with - since executor has to be shutdown, hence blocks for completion 
def exmap(urls):
    global result;
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        result= ex.map(load, urls)

        
urls = ["http://www.google.co.in" for i in range(10) ]
exmap(urls)	 #blocks
result = list(result)

#for non blocking for 'with'
t = threading.Thread(target=exmap, args=(urls,))
t.start()
result = list(result)

#OR 
ex = concurrent.futures.ThreadPoolExecutor(max_workers=10)
result = ex.map(load, urls)
#One by one , blocks if result is not ready 
next(result)  #wait, as_completed can not be used here 

#below blocks for complete result 
#Might raise exception if load fails
#hence use with try block 
list(result)
ex.shutdown()


#2nd version with submit, retures Future 

ex = concurrent.futures.ThreadPoolExecutor(max_workers=2)
result = [ex.submit(load, url) for url in urls ]
#do ur work 

#below blocks , Might raise exception if load fails
#hence use with try block 
output = [res.result() for res in concurrent.futures.as_completed(result)] #with Key, fs[res] has to be before res.result()
len(output)
ex.shutdown()

#could use 
done, not_done = concurrent.futures.wait(fs, timeout=None, return_when=ALL_COMPLETED) #FIRST_COMPLETED,FIRST_EXCEPTION
#done set contains done futures



##Another Example with Prime

import concurrent.futures
import time 

import random 

#time.sleep(random.randint(10,15))
def is_prime(n):
    import math
    if n == 2 : return True 
    if n % 2 == 0:	return False
    sqrt_n = int(math.sqrt(n))
    a = [1 for i in range(3, sqrt_n + 1, 2) if n % i == 0]
    return False if sum(a) > 0 else True
	
    
   

#map 
nos = list(range(1000))
ex = concurrent.futures.ThreadPoolExecutor(max_workers=2)
result = zip(nos, ex.map(is_prime, nos))  
#do ur work 

#One by one , blocks if result is not ready 
next(result)

#below blocks for complete result 
list(result)
ex.shutdown() 
 
    
#submit 
nos = list(range(1000))
ex = concurrent.futures.ThreadPoolExecutor(max_workers=2)
fs = { ex.submit(is_prime, e): e for e in nos }
#do ur work 
#below blocks , fs[res] must be before calling res.result()
output = [  (fs[res] , res.result()) 
            for res in concurrent.futures.as_completed(fs)]
ex.shutdown()   
    
    
##Copy example 
import shutil
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
    e.submit(shutil.copy, 'src1.txt', 'dest1.txt')
    e.submit(shutil.copy, 'src2.txt', 'dest2.txt')
    e.submit(shutil.copy, 'src3.txt', 'dest3.txt')
    e.submit(shutil.copy, 'src3.txt', 'dest4.txt')

##Deadlocks can occur 
#when the callable associated with a Future waits 
#on the results of another Future. 
#Use asyncio for this type of coding 

import concurrent.futures
import time
def wait_on_b():
    time.sleep(5)
    print(b.result()) # b will never complete because it is waiting on a.
    return 5

def wait_on_a():
    time.sleep(5)
    print(a.result()) #comment this, then works # a will never complete because it is waiting on b.
    return 6


executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
a = executor.submit(wait_on_b)
b = executor.submit(wait_on_a)
a.result() ##Deadlock 

#OR 
def wait_on_future():
    f = executor.submit(pow, 5, 2)
    # This will never complete because there is only one worker thread and
    # it is executing this function.
    return f.result()

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
a = executor.submit(wait_on_future)
a.result()  #blocks 






##with Process Pool - must be in separate file and 'if' clause is must
#no GIL for cpython
import concurrent.futures
import math

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n % 2 == 0:
        return False
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))

if __name__ == '__main__':
    main()
    
    




##Thread synchronization


##Lock

import threading
import time

def worker(lock):
    with lock:
        print('Acquired by' + threading.current_thread().getName())
        time.sleep(5)
        print('Released by' + threading.current_thread().getName())
		
        

lock = threading.Lock()
for i in range(2):
	w = threading.Thread(target=worker, args=(lock,))
	w.start()
	
	
##RLock

import threading
import time

def worker(lock):
	with lock:
		print('Acquired by' + threading.current_thread().getName())
		with lock:
			time.sleep(5)
            print('Releasing by' + threading.current_thread().getName())
        

lock = threading.RLock()
for i in range(2):
	w = threading.Thread(target=worker, args=(lock,))
	w.start()





##Synchronization with Condition

#follow below pattern
#The while loop checking for the application’s condition is necessary 
#because wait() can return after an arbitrary long time, 
#and the condition which prompted the notify() call may no longer hold true

# Consume one item
with cv:
    while not an_item_is_available():  #Initially returns False, producer makes it true 
        cv.wait()
    get_an_available_item() #make an_item_is_available return false

# Produce one item
with cv:
    make_an_item_available()  #make an_item_is_available return true
    cv.notify()

#OR , use wait_for(predicate, timeout=None)
# Consume an item
with cv:
    cv.wait_for(an_item_is_available)
    get_an_available_item()



#example
import threading
import time
import random

shared_var = 0
available = False 

def consumer(cond):
        global available
        print('Starting ' + threading.current_thread().getName())
        with cond:		
            cond.wait_for(lambda : available)
            print('[Consumer] Got Resource ', threading.current_thread().getName(), shared_var)  #access global shared_var
            available = False


def producer(cond, max):	
    global shared_var                #must as it sets global
    global available
    i = 0
    while i <= max:
        with cond:				
            shared_var = random.randint(20,100);
            print('Notify One Consumer ',  threading.current_thread().getName(), shared_var)
            available = True
            cond.notify()			#for only one consumer, for all -use cond.notifyAll()
        time.sleep(1) 			#some other work, Note, consumer would be awakened here only after 'with scope'
        i += 1
	

condition = threading.Condition()
for i in range(10):
	w = threading.Thread(target=consumer, args=(condition,))
	w.start()

p = threading.Thread(name='Producer', target=producer, args=(condition,10))
p.start()




##Semaphore

import random

def worker(s):
	print('Waiting to join the pool ' + threading.current_thread().getName())
	with s:
		print('Got access ' + threading.current_thread().getName())
		time.sleep(random.randrange(10))


s = threading.Semaphore(2) #at a time only 2 can access
for i in range(4):
	t = threading.Thread(target=worker, name=str(i), args=(s,))
	t.start()

    
#A Semaphore can be released more times than it's acquired, 
#and that will raise its counter above the starting value. 

#A BoundedSemaphore can't be raised above the starting value

from threading import Semaphore, BoundedSemaphore

# Usually, you create a Semaphore that will allow a certain number of threads
# into a section of code.
s1 = Semaphore(5)

# When you want to enter the section of code, you acquire it first.
s1.acquire()

# Then you do whatever sensitive thing needed to be restricted to five threads.
# When you're finished, you release the semaphore.
s1.release()

# That's all fine, but you can also release it without acquiring it first.
s1.release()

# The counter is now 6! That might make sense in some situations, but not in most.

# If that doesn't make sense in your situation, use a BoundedSemaphore.
s2 = BoundedSemaphore(5)
s2.acquire()
s2.release()
try:
    s2.release()
except ValueError:
    print('As expected, it complained.')

	
##Event - one thread signals an event and other threads wait for it. 
#no 'with block'

import threading
import time
                    
def wait_for_event(e):
	event_is_set = e.wait()
	print('Got access ' + threading.current_thread().getName())

def wait_for_event_timeout(e, t):
	while not e.isSet():
		event_is_set = e.wait(t)
		if event_is_set:
			print('processing event')
		else:
			print('doing other work')


e = threading.Event()
t1 = threading.Thread(name='block', target=wait_for_event, args=(e,))
t1.start()

t2 = threading.Thread(name='non-block', target=wait_for_event_timeout, args=(e, 2))
t2.start()

time.sleep(3)
e.set()
# both threads are awakened


##Timer - triggers a code after certain time


def hello():	
	print("hello, world")

t = threading.Timer(5.0, hello)
t.start() # after 5 seconds, "hello, world" will be printed


##Barrier 
#fixed number of threads that need to wait for each other. 
#Each of the threads tries to pass the barrier by calling the wait() method 
#and will block until all of the threads have made the call. 
#At this points, the threads are released simultanously

b = threading.Barrier(2)
def server():
	time.sleep(5)
	b.wait()
	print("server got access..")

	

def client():
	time.sleep(10)
	b.wait()
	print("client got access..")

threading.Thread(target=server).start()
threading.Thread(target=client).start()



##Queue
import queue
import threading
import time

def worker(q):
	while True:
		item = q.get()
		print(threading.current_thread().getName(), item)
		time.sleep(2)
		q.task_done()

		
que = queue.Queue()
for i in range(2):
	t = threading.Thread(target=worker, args=(que,))
	t.start()

for item in range(10):  #Only one thread get one item 
	que.put(item)

que.join()       # block until all tasks are done





###*** multiprocessing 


class multiprocessing.Process(group=None, target=None, 
            name=None, args=(), kwargs={}, *, daemon=None)
    run()
        You may override this method in a subclass. 
    start()
        Start the process’s activity.
    join([timeout])
    name
    is_alive()
    daemon
        The process’s daemon flag, a Boolean value. 
        This must be set before start() is called.
        The initial value is inherited from the creating process.
        These are not Unix daemons or services, 
        Simillar to thread counterpart 
        When main returns, process would wait for all nondemonic process to exit (ie .join)
        Process then exits and all demonic processes are terminated automatically 
        Used for process which does work in looping 
    pid
    exitcode
    authkey
    sentinel
        A numeric handle of a system object which will become “ready” when the process ends.
        You can use this value if you want to wait on several events at once 
        using multiprocessing.connection.wait(). Otherwise calling join() is simpler.
    terminate()
        Terminate the process.
        If this method is used when the associated process is using a pipe or queue 
        then the pipe or queue is liable to become corrupted 
        and may become unusable by other process. 
        Similarly, if the process has acquired a lock or semaphore etc. 
        then terminating it is liable to cause other processes to deadlock.
    kill()
        Same as terminate() but using the SIGKILL signal on Unix.
    close()
        Close the Process object
        
#other methods 
multiprocessing.active_children()
multiprocessing.cpu_count()
    Return the number of CPUs in the system.
multiprocessing.current_process()
multiprocessing.freeze_support()
multiprocessing.get_all_start_methods()
multiprocessing.get_context(method=None)
multiprocessing.get_start_method(allow_none=False)
multiprocessing.set_executable()
    Sets the path of the Python interpreter to use when starting a child process.
multiprocessing.set_start_method(method)


#Example      
#Processing Must be in separate file and with if __name__ block and run as script - no GIL
#Process - child process 
#Pool - pool of child process , has .map(), .apply_async() etc 

from multiprocessing import Process

def f(name):
		print('hello', name, "from ", multiprocessing.current_process().name)


if __name__ == '__main__':
    p = Process(target=f, args=('das',))
    p.start()
    p.join()
      
      
      
#Example 
import multiprocessing, time, signal
p = multiprocessing.Process(target=time.sleep, args=(1000,))
>>> print(p, p.is_alive())
<Process(Process-1, initial)> False
p.start()
>>> print(p, p.is_alive())
<Process(Process-1, started)> True
p.terminate()
time.sleep(0.1)
print(p, p.is_alive())
<Process(Process-1, stopped[SIGTERM])> False
>>> p.exitcode == -signal.SIGTERM
True


##Add support for when a program which uses multiprocessing has been frozen to produce a Windows executable. 
#(Has been tested with py2exe, PyInstaller and cx_Freeze.)

from multiprocessing import Process, freeze_support

def f():
    print('hello world!')

if __name__ == '__main__':
    freeze_support()
    Process(target=f).start()

    
    

##Pool 

   
class multiprocessing.pool.Pool([processes[, initializer[, 
            initargs[, maxtasksperchild[, context]]]]])
    initializer(initargs) are called in worker process 
    apply(func[, args[, kwds]])
        Call func with arguments args and keyword arguments kwds. 
        It blocks until the result is ready. 
    apply_async(func[, args[, kwds[, callback[, error_callback]]]])
        callback is fn(result)
        error_callback is for error , fn(exception)
    map(func, iterable[, chunksize])
    map_async(func, iterable[, chunksize[, callback[, error_callback]]])
    imap(func, iterable[, chunksize])
        A lazier version of map().
    imap_unordered(func, iterable[, chunksize])
        ordering of the results from the returned iterator should be considered arbitrary. 
    starmap(func, iterable[, chunksize])
        Like map() except that the elements of the iterable are expected to be iterables 
        that are unpacked as arguments.
        Hence an iterable of [(1,2), (3, 4)] results in [func(1,2), func(3,4)].
    starmap_async(func, iterable[, chunksize[, callback[, error_callback]]])
    close()
    terminate()
        Stops the worker processes immediately without completing outstanding work. 
    join()
        Wait for the worker processes to exit. 
        One must call close() or terminate() before using join().


class multiprocessing.pool.AsyncResult
    The class of the result returned by Pool.apply_async() and Pool.map_async().
    get([timeout])
    wait([timeout])
    ready()
        Return whether the call has completed.
    successful()
        Return whether the call completed without raising an exception. 


#Example 
from multiprocessing import Pool
import time

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(processes=4) as pool:         # start 4 worker processes
        result = pool.apply_async(f, (10,)) # evaluate "f(10)" asynchronously in a single process
        print(result.get(timeout=1))        # prints "100" unless your computer is *very* slow

        print(pool.map(f, range(10)))       # prints "[0, 1, 4,..., 81]"

        it = pool.imap(f, range(10))
        print(next(it))                     # prints "0"
        print(next(it))                     # prints "1"
        print(it.next(timeout=1))           # prints "4" unless your computer is *very* slow

        result = pool.apply_async(time.sleep, (10,))
        print(result.get(timeout=1))        # raises multiprocessing.TimeoutError



##Exmaple with Process Pool - must be in separate file and 'if' clause is must
from multiprocessing import *

def is_prime(n):
	import math
	if n % 2 == 0:	return False
	sqrt_n = int(math.sqrt(n))
	a = [1 for i in range(3, sqrt_n + 1, 2) if n % i == 0]
	return False if sum(a) > 0 else True
	
	
def main_p(primes, max_w=10):
	p = Pool(max_w)
	d = dict(zip(primes, p.map(is_prime, primes)))
	return d
	
if __name__ == '__main__':    
	print(main_p(list(range(3,98))))



##Another Example of POOL 

import multiprocessing
import time
import random
import sys

#
# Functions used by test code
#

def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % (
        multiprocessing.current_process().name,
        func.__name__, args, result
        )

def calculatestar(args):
    return calculate(*args)

def mul(a, b):
    time.sleep(0.5 * random.random())
    return a * b

def plus(a, b):
    time.sleep(0.5 * random.random())
    return a + b

def f(x):
    return 1.0 / (x - 5.0)

def pow3(x):
    return x ** 3

def noop(x):
    pass

#
# Test code
#

def test():
    PROCESSES = 4
    print('Creating pool with %d processes\n' % PROCESSES)

    with multiprocessing.Pool(PROCESSES) as pool:
        #
        # Tests
        #

        TASKS = [(mul, (i, 7)) for i in range(10)] + \
                [(plus, (i, 8)) for i in range(10)]

        results = [pool.apply_async(calculate, t) for t in TASKS]
        imap_it = pool.imap(calculatestar, TASKS)
        imap_unordered_it = pool.imap_unordered(calculatestar, TASKS)

        print('Ordered results using pool.apply_async():')
        for r in results:
            print('\t', r.get())
        print()

        print('Ordered results using pool.imap():')
        for x in imap_it:
            print('\t', x)
        print()

        print('Unordered results using pool.imap_unordered():')
        for x in imap_unordered_it:
            print('\t', x)
        print()

        print('Ordered results using pool.map() --- will block till complete:')
        for x in pool.map(calculatestar, TASKS):
            print('\t', x)
        print()

        #
        # Test error handling
        #

        print('Testing error handling:')

        try:
            print(pool.apply(f, (5,)))
        except ZeroDivisionError:
            print('\tGot ZeroDivisionError as expected from pool.apply()')
        else:
            raise AssertionError('expected ZeroDivisionError')

        try:
            print(pool.map(f, list(range(10))))
        except ZeroDivisionError:
            print('\tGot ZeroDivisionError as expected from pool.map()')
        else:
            raise AssertionError('expected ZeroDivisionError')

        try:
            print(list(pool.imap(f, list(range(10)))))
        except ZeroDivisionError:
            print('\tGot ZeroDivisionError as expected from list(pool.imap())')
        else:
            raise AssertionError('expected ZeroDivisionError')

        it = pool.imap(f, list(range(10)))
        for i in range(10):
            try:
                x = next(it)
            except ZeroDivisionError:
                if i == 5:
                    pass
            except StopIteration:
                break
            else:
                if i == 5:
                    raise AssertionError('expected ZeroDivisionError')

        assert i == 9
        print('\tGot ZeroDivisionError as expected from IMapIterator.next()')
        print()

        #
        # Testing timeouts
        #

        print('Testing ApplyResult.get() with timeout:', end=' ')
        res = pool.apply_async(calculate, TASKS[0])
        while 1:
            sys.stdout.flush()
            try:
                sys.stdout.write('\n\t%s' % res.get(0.02))
                break
            except multiprocessing.TimeoutError:
                sys.stdout.write('.')
        print()
        print()

        print('Testing IMapIterator.next() with timeout:', end=' ')
        it = pool.imap(calculatestar, TASKS)
        while 1:
            sys.stdout.flush()
            try:
                sys.stdout.write('\n\t%s' % it.next(0.02))
            except StopIteration:
                break
            except multiprocessing.TimeoutError:
                sys.stdout.write('.')
        print()
        print()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    test()




 
    
    
    
    
    
    
    
    
    
    
##Process Pipe and Queue 
#for sharing objects (only pickable)
#Pipe , Queue are  used to share objects between processes 
#those objects must be picklable


multiprocessing.Pipe([duplex])
    Returns a pair (conn1, conn2) of Connection objects representing the ends of a pipe.
    If duplex is True (the default) then the pipe is bidirectional. 
    If duplex is False then the pipe is unidirectional: 
    conn1 can only be used for receiving messages 
    and conn2 can only be used for sending messages.
    
class multiprocessing.Queue([maxsize])
    qsize()
        Return the approximate size of the queue.
        Nonreliable     
    empty()
        Return True if the queue is empty, False otherwise. 
        Nonreliable     
    full()
        Return True if the queue is full, False otherwise. 
        Nonreliable     
    put(obj[, block[, timeout]])
        Put obj into the queue. 
        If the optional argument block is True (the default) and timeout is None (the default), 
        block if necessary until a free slot is available. 
    put_nowait(obj)
        Equivalent to put(obj, False).
    get([block[, timeout]])
        Remove and return an item from the queue. 
        If optional args block is True (the default) and timeout is None (the default), 
        block if necessary until an item is available. 
    get_nowait()
        Equivalent to get(False).
    close()
        Indicate that no more data will be put on this queue by the current process. 
        The background thread will quit once it has flushed all buffered data to the pipe. 
        This is called automatically when the queue is garbage collected.
    join_thread()
        Join the background thread. 
        This can only be used after close() has been called. 
        It blocks until the background thread exits, 
        By default if a process is not the creator of the queue 
        then on exit it will attempt to join the queue’s background thread. 
        The process can call cancel_join_thread() to make join_thread() do nothing.
    cancel_join_thread()
        Prevent join_thread() from blocking. 

    
class multiprocessing.SimpleQueue
    It is a simplified Queue type, very close to a locked Pipe.
    empty()
        Return True if the queue is empty, False otherwise.
    get()
        Remove and return an item from the queue.
    put(item)
        Put item into the queue.
        
class multiprocessing.JoinableQueue([maxsize])
    JoinableQueue, a Queue subclass, 
    task_done()
        Indicate that a formerly enqueued task is complete. 
        Used by queue consumers. 
        For each get() used to fetch a task, a subsequent call to task_done() tells the queue 
        that the processing on the task is complete.
    join()
        Block until all items in the queue have been gotten and processed.



#example 
from __future__ import print_function
from multiprocessing import Process, Queue, Pipe, RLock



class A(object):
    def __init__(self, v):
        self.value = v 
    def __repr__(self):
        return "A(%d)" % (self.value,)

def queuef(q, obj):
    q.put([42, None, 'hello', {'from': 'queue'}, obj])
    
def pipef(conn, obj):
    conn.send([42, None, 'hello', {'from': 'pipe'}, obj])
    conn.close()
    
if __name__ == '__main__':
    #lck
    lck = RLock()
    #A
    a = A(20)
    #Queue
    q = Queue()
    p = Process(target=queuef, args=(q, a))
    p.start()
    with lck:
        print(q.get())    # prints "[42, None, 'hello']"
    p.join()
    #Pipe
    parent_conn, child_conn = Pipe()
    p = Process(target=pipef, args=(child_conn, a))
    p.start()
    with lck:
        print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()
    
    
##Example - how to use queues to feed tasks to a collection of worker processes 
#and collect the results:

import time
import random

from multiprocessing import Process, Queue, current_process, freeze_support

#
# Function run by worker processes
#

def worker(input, output):
    for func, args in iter(input.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)

#
# Function used to calculate result
#

def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % \
        (current_process().name, func.__name__, args, result)

#
# Functions referenced by tasks
#

def mul(a, b):
    time.sleep(0.5*random.random())
    return a * b

def plus(a, b):
    time.sleep(0.5*random.random())
    return a + b

#
#
#

def test():
    NUMBER_OF_PROCESSES = 4
    TASKS1 = [(mul, (i, 7)) for i in range(20)]
    TASKS2 = [(plus, (i, 8)) for i in range(10)]

    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    # Submit tasks
    for task in TASKS1:
        task_queue.put(task)

    # Start worker processes
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue)).start()

    # Get and print results
    print('Unordered results:')
    for i in range(len(TASKS1)):
        print('\t', done_queue.get())

    # Add more tasks using `put()`
    for task in TASKS2:
        task_queue.put(task)

    # Get and print some more results
    for i in range(len(TASKS2)):
        print('\t', done_queue.get())

    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')


if __name__ == '__main__':
    freeze_support()
    test()
    
   
    
##Guidelines of using multiprocess
Avoid large shared state
    Use queues or pipes rather than low level synchronization
Picklability
    Ensure that the arguments to the methods of proxies are picklable.
    proxies means pipe, quue, manager objects etc which are used for sharing data 
Thread safety of proxies
    Do not use a proxy object from more than one thread unless you protect it with a lock.
    There is never a problem with different processes using the same proxy.
Joining zombie processes
    On Unix when a process finishes but has not been joined it becomes a zombie.
    There should never be very many because each time a new process starts 
    (or active_children() is called) all completed processes 
    which have not yet been joined will be joined
Avoid terminating processes
    Using the Process.terminate method to stop a process is liable 
    to cause any shared resources (such as locks, semaphores, pipes and queues) 
    currently being used by the process to become broken or unavailable to other processes.
Joining processes that use queues
    Bear in mind that a process that has put items in a queue will wait 
    before terminating until all the buffered items are consumed 
    OR call the Queue.cancel_join_thread method of the queue to avoid this behaviour.
    #deadlock
    #A fix here would be to swap the last two lines (or simply remove the p.join() line).

    from multiprocessing import Process, Queue

    def f(q):
        q.put('X' * 1000000)

    if __name__ == '__main__':
        queue = Queue()
        p = Process(target=f, args=(queue,))
        p.start()
        p.join()                    # this deadlocks
        obj = queue.get()
Beware of replacing sys.stdin with a “file like object”
    Never Replace sys.stdin with any file object while using multiprocesses 
    Check documentation for why and what to be done if required 
    https://docs.python.org/3/library/multiprocessing.html#programming-guidelines
Explicitly pass resources to child processes
    #Wrong 
    from multiprocessing import Process, Lock
    def f():
        ... do something using "lock" ...
    if __name__ == '__main__':
        lock = Lock()
        for i in range(10):
            Process(target=f).start()

    #Right
    from multiprocessing import Process, Lock
    def f(l):
        ... do something using "l" ...
    if __name__ == '__main__':
        lock = Lock()
        for i in range(10):
            Process(target=f, args=(lock,)).start()




    
    
    

##Multiprocess - Low level Synchronizaion 
#Note that one can also create synchronization primitives by using a manager object 

#multiprocessing contains equivalents of all the synchronization primitives from threading

#A Semaphore can be released more times than it's acquired, 
#and that will raise its counter above the starting value. 

#A BoundedSemaphore can't be raised above the starting value
    
class multiprocessing.Barrier(parties[, action[, timeout]])
class multiprocessing.BoundedSemaphore([value])
class multiprocessing.Condition([lock])
class multiprocessing.Event
class multiprocessing.Lock
class multiprocessing.RLock
class multiprocessing.Semaphore([value])


#Exmaple 
from multiprocessing import Process, Lock

def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in range(10):
        Process(target=f, args=(lock, num)).start()

    
##Multiprocess -Shared memory for sharing objects (only pickable)
#Data can be stored in a shared memory map using Value or Array. 

multiprocessing.Value(typecode_or_type, *args, lock=True)
    Access inner value by 'value' attribute 
    Lock= False, means  unsynchronized 
    Lock=True/None, means new internal RLock is created 
    lock = userdefined Lock/Rlock, then that would be used 
multiprocessing.Array(typecode_or_type, size_or_initializer, *, lock=True)
    Sychronized version of array module
    CHeck typecode by https://docs.python.org/3.4/library/array.html#module-array

#quick 
double  d 
int     i 
str     Array('c', b'hello world')

##Example 
from multiprocessing import Process, Value, Array

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print num.value
    print arr[:]


    
    
##Multiprocessing Manager  for sharing objects 
#Manager controls a server process(very heavy weight) which holds Python objects 
#and allows other processes to manipulate them using proxies
#supports datastructure : list, dict, Namespace,
#Lock, RLock, Semaphore, BoundedSemaphore, Condition, Event, Queue, Value and Array     

#code 
from __future__ import print_function
from multiprocessing import Process, Value, Array, RLock, Manager, Event


def sharedf(n, a, ev):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]
    ev.set()  #wake up main 
    
     
def managerf(d, l, ev): #d = dict, l = list 
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()
    ev.set()    #wake up main 
    
  

if __name__ == '__main__':
    event = Event()  #flag is false
    lock = RLock()
    #Data can be stored in a shared memory map using Value or Array
    num = Value('d', 0.0)    #typecode from array module, eg int(i), double(d), long(l),
    arr = Array('i', range(10))
    p1 = Process(target=sharedf, args=(num, arr, event))
    p1.start()
    event.wait()   #or call event.is_set() 
    with lock:
        print(num.value)
        print(arr[:])
  
    #Using manager 
    manager = Manager()
    event2 = manager.Event()
    d = manager.dict()
    l = manager.list(range(10))
    p2 = Process(target=managerf, args=(d, l, event2))
    p2.start()
    event2.wait()   #or call event.is_set() 
    with lock:
        print(d)
        print(l)        
    p1.join()
    p2.join()
 

##Multiprocessing gotcha 
#multiprocessing.Lock, etc  can be shared to child process when using Process  
import time,multiprocessing

def f(lck, i):
    with lck:
        print('hello world ', i)
    time.sleep(1)

if __name__ == '__main__':
    lock = multiprocessing.RLock()
    procs = []
    for num in range(10):  
        p = multiprocessing.Process(target=f, args=(lock, num)) #10 child processes are created 
        procs.append(p)
        p.start()
    for p in procs:
        p.join()

#Note multiprocessing.Lock etc can not be shared between processes 
#when are created via multiprocessing.Pool or concurrent.futures.ThreadPoolExecutor
#as we don't have direct control on process creation 

#Note, in this cases, only pickable object can be shared 
#What can be pickled 
    -None, True, and False
    -integers, long integers, floating point numbers, complex numbers
    -normal and Unicode strings
    -tuples, lists, sets, and dictionaries containing only picklable objects
    -functions defined at the top level of a module
    -built-in functions defined at the top level of a module
    -classes that are defined at the top level of a module
    -instances of such classes whose __dict__ or the result of calling __getstate__() is picklable 

#Hence You can't pass normal multiprocessing.Lock objects to Pool methods, 
#because they can't be pickled. 

#Solution -1 : is to create Manager() and pass a Manager.Lock()
#Very Heavy: using a Manager requires spawning another process to host the Manager server. 
#And all calls to acquire/release the lock have to be sent to that server via IPC.
def target(l):
    pass
    
def main():
    iterable = [1, 2, 3, 4, 5]
    pool = multiprocessing.Pool()
    m = multiprocessing.Manager()
    l = m.Lock()
    func = partial(target, l)
    pool.map(func, iterable)
    pool.close()
    pool.join()

#Solution 2: pass the regular multiprocessing.Lock() at Pool creation time, 
#using the initializer kwarg. 
#This will make lock instance global in all the child workers:
def target(iterable_item):
    for item in items:
        # Do cool stuff
        if (... some condition here ...):
            lock.acquire()
            # Write to stdout or logfile, etc.
            lock.release()
def init(l):
    global lock
    lock = l

def main():
    iterable = [1, 2, 3, 4, 5]
    l = multiprocessing.Lock()
    pool = multiprocessing.Pool(initializer=init, initargs=(l,))
    pool.map(target, iterable)
    pool.close()
    pool.join()


    
    
    
###*** Web Page & CGI Programming
#Web programming and automation using Python

#Common Gateway Interface 
#A CGI script is invoked by an HTTP server, eg to process <FORM> or <ISINDEX> element
#cgi script - print text to display in browser
#must be under ['/cgi-bin', '/htbin'] for builtin http.server 

#file :  cgi-bin/cgiEx.py

import cgi, os, sys 

#Enables long report if there is soem error 
import cgitb
cgitb.enable(logdir="logs")

#form is a dictionary 
#note form contains both GET parsed URL and/or POST form data if present 
form = cgi.FieldStorage()

#to access raw GET QUery 
# the query string, which contains the raw GET data
# (For example, for http://example.com/myscript.py?a=b&c=d&e
# this is "a=b&c=d&e")
#os.environ["QUERY_STRING"]

# the raw POST data
#sys.stdin.read()

'''
application/x-www-form-urlencoded 
    Default. 
    All characters are encoded before sent 
    (spaces are converted to "+" symbols, and special characters are converted to ASCII HEX values) 
multipart/form-data 
    No characters are encoded. 
    use this if  forms that have a file upload control 
text/plain 
    Spaces are converted to "+" symbols, but no special characters are encoded 
'''

string = """
<form method="post" action="cgiEx.py">
       <p>Name: <input type="text" name="name"/></p>
	   <p>address1: <input type="text" name="addr"/></p>
	   <p>address2: <input type="text" name="addr"/></p>
	   <input type="submit" value="Submit" />
     </form>  
"""



#headers section
print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers

#content section
print("<HTML>")
print("<TITLE>CGI script output</TITLE>")
print("<BODY>")
print("<H1>This is my first CGI script</H1>")
print("Hello, world!")
print("</br>")

if 'REQUEST_METHOD'  in os.environ and os.environ['REQUEST_METHOD'].upper() == 'POST':
    if "name" not in form or "addr" not in form:
        print("<H1>Error</H1>")
        print("Please fill in the name and addr fields.")
        print("</BODY></HTML>")
        sys.exit(0)
    print(form.getfirst("name","").upper(), ",".join(form.getlist("addr")) )
    #or could be form['name'].value 
else:   #IT IS GET 
    print('QUERY_STRING=', os.environ["QUERY_STRING"], "</br>")
    print('name=', form.getfirst("name", "no name found"),"</br>")
    print(string)
    
print("</BODY></HTML>")





#run http server from outside of this script 
#python3: python -m http.server --bind 127.0.0.1 --cgi 8080
#py2.7: python -m CGIHTTPServer  8080
#in browser http://localhost:8080/cgi-bin/cgiEx.py

#or python -m http.server 8000 --bind 127.0.0.1
#or , to serve a specific dir 
#python -m http.server --directory /tmp/






##Check all input types 
#https://www.w3schools.com/html/html_form_input_types.asp


##for  an uploaded file field 
#http.server has problem with large file > 194KB 
#Lib/http/server.py:1164: 
            if self.command.lower() == "post" and nbytes > 0:                
                data = self.rfile.read(nbytes)
                while len(data) < nbytes:
                    print(length, nbytes, len(data), "call again")
                    data += self.rfile.read(nbytes)


#use action="test.py" to test it 
string = """
<form enctype="multipart/form-data"  method="post">
<p>File: <input type="file" name="file"></p>
<p>Name: <input type="text" name="name"/></p>
<p><input type="submit" value="Upload"></p>
</form>
"""
html = """\
    Content-Type: text/html\n
    <html><body>
    <p>%s</p>
    </body></html>
    """

import cgi, os, sys , os.path
import tempfile
#Enables long report if there is soem error 
import cgitb
cgitb.enable(logdir="logs")


# Windows needs stdio set for binary mode. THIS IS MUST 
#else Standard input is opened by default in "text" mode

try: 
    import msvcrt
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY) # stdin  = 0
    msvcrt.setmode (sys.stdout.fileno(), os.O_BINARY) # stdout = 1
except ImportError:
    pass
    
    

#form is a dictionary 
#note form contains both GET parsed URL and/or POST form data if present 
form = cgi.FieldStorage()

     

if 'REQUEST_METHOD'  in os.environ and os.environ['REQUEST_METHOD'].upper() == 'POST':
    if 'file' not in form:
        #how come it is not there 
        sys.exit(0) 
        
    fileitem = form['file']
    # Test if the file was uploaded
    if fileitem.file:
        # strip leading path from file name
        # to avoid directory traversal attacks
        fn = os.path.basename(fileitem.filename if fileitem.filename else "somedummy.du")
        #curdir is outside cgi-bin  
        # gets truncated         
        with open(os.path.normpath(os.path.join(os.getcwd(), 'uploaded_files' , fn)), 'wb') as f:
            while True:
                chunk = fileitem.file.read(100000)
                if not chunk: break
                f.write(chunk)
        message = 'The file "' + fn + '" was uploaded successfully'
    else:
        message = 'No file was uploaded'

    print( html % (message,))
else:
    print(html % (string,))


##Content-type 
#type/subtype followed by an optional semicolon delimited attribute-value pairs (known as parameters).
#https://www.iana.org/assignments/media-types/media-types.xhtml
text
    This type indicates that the content is plain text and no special software is required to read the contents. 
    The subtype represents more specific details about the content, which can be used by the client for special processing, if any. 
    For instance, Content-Type: text/html indicates that the body content is html, 
    and the client can use this hint to kick rendering engine while displaying the response.
multipart
    As the name indicates, this type consists of multiple parts of the independent data types. 
    For instance, Content-Type: multipart/form-data is used for submitting forms 
    that contain the files, non-ASCII data, and binary data.
image
    This type represents the image data. 
    For instance, Content-Type: image/png indicates that the body content is a .png image.
audio
    This type indicates the audio data. 
    For instance, Content-Type: audio/mpeg indicates that the body content is MP3 or other MPEG audio.
video
    This type indicates the video data. 
    For instance Content-Type:, video/mp4 indicates that the body content is MP4 video.
application
    This type represents the application data or binary data. 
    For instance, Content-Type: application/json; charset=utf-8 designates the content to be in JSON format, encoded with UTF-8 character encoding
    In this case write string of json eg sys.stdout.write(json.dumps(obj))
    For Content-Type: application/xml , Get XML string xml.etree.ElementTree.tostring(element, encoding="us-ascii", method="xml")
    

      
##File Download 
#write file content to stdout 
import cgi 
import cgi, os
import cgitb; cgitb.enable()

try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass
    

print("Content-Type: application/octet-stream")
print("Content-Disposition: attachment; filename=%s" % filename)
print()

#actual  downloading 
fo = open(filename, "rb")
while True:
    buffer = fo.read(4096)
    if buffer:
        sys.stdout.write(buffer)
    else:
        break
fo.close()
    
#f.read() could cause a problem if the file is huge. 
#To prevent that, use shutil.copyfileobj:
import os
import shutil
import sys

with open(os.path.abspath('test.png'), 'rb') as f:
    sys.stdout.buffer.write("Content-Type: image/png\n\n")
    shutil.copyfileobj(f, sys.stdout.buffer)
    
        
##Other important methods
cgi.print_environ()
    Format the shell environment in HTML.
cgi.print_form(form)  #form is dict of { key:value} which will be formatted
    Format a form in HTML.
cgi.print_directory()
    Format the current directory in HTML.
cgi.print_environ_usage()
    Print a list of useful (used by CGI) environment variables in HTML.

cgi.escape(s, quote=False)
    Convert the characters '&', '<' and '>'  and quotes (if quote=True) in string s to HTML-safe sequences
    Deprecated, Must use quote=True 
    or  Use html.escape(s, quote=True) for escaping and html.unescape(s) for unescaping 

cgi.test()
    Robust test CGI script, usable as main program. 
    Writes minimal HTTP headers and formats all information provided to the script in HTML form

cgi.parse_qs(qs, keep_blank_values=False, strict_parsing=False)
    Use urllib.parse.parse_qs(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace')
    Parse a query string given as a string argument (data of type application/x-www-form-urlencoded). 
    Data are returned as a dictionary
    
cgi.parse_qsl(qs, keep_blank_values=False, strict_parsing=False)
    Use urllib.parse.parse_qsl(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace')
    Parse a query string given as a string argument (data of type application/x-www-form-urlencoded). Data are returned as a list of name, value pairs

    
##Reading HTTP headers 
#you can't read the HTTP header directly, 
#but the web server put into environment variables , os.environ 

#Important env variables 
#check Metavariables http://www.ietf.org/rfc/rfc3875.txt
AUTH_TYPE
CONTENT_LENGTH 
CONTENT_TYPE
GATEWAY_INTERFACE
PATH_INFO
PATH_TRANSLATED
QUERY_STRING
REMOTE_ADDR
REMOTE_HOST
REMOTE_IDENT  
REMOTE_USER
REQUEST_METHOD 
SCRIPT_NAME
SERVER_NAME
SERVER_PORT
SERVER_PROTOCOL
SERVER_SOFTWARE

    
    
    
###*** Django - Chapter-1
 
'''
examplesite from setup to Production deplyoment 
    urls, views and settings, template language 
    Objective- Understanding  Application development
settings, urls, views(inc class based) and deployment steps
'''
#Py3.x
#REF: https://docs.djangoproject.com/en/2.0/

### Install version 
$ pip install Django==2.0.6
#Note The last version to support Python 2.7 is Django 1.11 
$ pip install Django==1.11

###STEP 0: Python 2.7 , it's python.exe must be in PATH
#django-admin is installed in Scripts dir, must be in Path (> django-1.7) 
# < django-1.7 , use django-admin.py which is installed in Lib\site-packages\django\bin

#check help 
$ django-admin help startproject
$ django-admin help startapp

##Django2.0 changes compared to 1.11 
#django.conf.urls.url() is also named as   django.urls.re_path()
#but use django.urls.path for simplicity 
#urls.py 
from django.urls import include, path, re_path

#django.urls.path() function allows a simpler, more readable URL routing syntax. 
url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
#could be written as:
path('articles/<int:year>/', views.year_archive),



###STEP 1.1: Creating project , Project contains App, App contains MVC
$ django-admin startproject examplesite

###STEP 1.2 : check dir structure 

.   
¦   manage.py
+---examplesite
        settings.py       #setting files 
        urls.py           #route file  
        wsgi.py           #Web Server Gateway Interface file  exposing 'application'
        __init__.py
 
###STEP 1.3 : check settings at examplesite\settings.py 
#check https://docs.djangoproject.com/en/2.0/ref/settings/
    
##To get attributes programitically 
#check https://docs.djangoproject.com/en/2.0/topics/settings/, eg how to use Django standalone 
from django.conf import settings #check dir(settings) in python manage.py shell 
STATIC = getattr(settings, "STATIC", None)  #'/static/'   



###File: settings.py 

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#This is Project DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+f$pnly#@8zf-5m4kwpy6*qodji4-6r^0%2@=e5fvmafpbk*pb'
#Used for many hash calculation, must be secret , in production ,use it from env string or from file  
#eg 
#import os
#SECRET_KEY = os.environ['SECRET_KEY']
#or 
#with open('/etc/secret_key.txt') as f:
#    SECRET_KEY = f.read().strip()




# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#A list of strings representing the host/domain names that this Django site can serve
#could be list of  'www.example.com', '.example.com' or '*' 
#Django uses the Host header provided by the client to construct URLs in certain cases
#this prevent HTTP Host header attacks
ALLOWED_HOSTS = []

#SSL activation 
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# Application definition

INSTALLED_APPS = [
    "sslserver",                        #for runsslserver , install it at first , pip install django-sslserver
    'django.contrib.admin',             #for admin module 
    'django.contrib.auth',              #authentication module
    'django.contrib.contenttypes',      #track all of the models installed in your Django-powered project, and attach permissions
    'django.contrib.sessions',          #for Session handling  
    'django.contrib.messages',          #for  "flash message"
    'django.contrib.staticfiles',       #static file handling 
    'my_app',                           #my app, order is significant , app means containing model 
    'my_app2',
    
]


#Using session 
#By default, Django stores sessions in your database , Other options are file, cookie etc , Use SESSION_ENGINE  setting
#command: python manage.py migrate #to install the single database table that stores session data.
# each HttpRequest object – the first argument to any Django view function – will have a session attribute, which is a dictionary-like object.
#eg request.session.get('has_commented', False) or request.session['has_commented'] = True


#hooks into Django’s request/response processing
#Check bundled middleware at https://docs.djangoproject.com/en/2.0/ref/middleware/
#middleware = a decorator like function given below 
#def simple_middleware(get_response):
#    # One-time configuration and initialization.
#
#    def middleware(request):
#        # Code to be executed for each request before
#        # the view (and later middleware) are called.
#
#        response = get_response(request)
#
#        # Code to be executed for each request/response after
#        # the view is called.
#
#        return response
#
#    return middleware

#Django 2.0 has MIDDLEWARE  instead of MIDDLEWARE_CLASSES
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', #provides several security enhancements to the request/response cycle. eg SSL
    'django.contrib.sessions.middleware.SessionMiddleware',  #for Session handling  
    'django.middleware.common.CommonMiddleware',  #Adds a few conveniences , check https://docs.djangoproject.com/en/2.0/ref/middleware/#module-django.middleware.common
    'django.middleware.csrf.CsrfViewMiddleware', #Cross Site Request Forgery protection, in template use <form action="" method="post">{% csrf_token %}
    'django.contrib.auth.middleware.AuthenticationMiddleware', #authentication module
    'django.contrib.messages.middleware.MessageMiddleware', #for  "flash message", SessionMiddleware must be enabled and appear before MessageMiddleware 
    'django.middleware.clickjacking.XFrameOptionsMiddleware', #protection against clickjacking
]
#Handling flash message 
#adding 
#from django.contrib import messages
#messages.add_message(request, messages.INFO, 'Hello world.') #message.tags is messages.INFO
#displaying in template 
#{% if messages %}
#<ul class="messages">
#    {% for message in messages %}
#    <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
#    {% endfor %}
#</ul>
#{% endif %}



ROOT_URLCONF = 'examplesite.urls'  #urls.py file 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  #other could be 'django.template.backends.jinja2.Jinja2'
        'DIRS': [],                      #Directories where the engine should look for template source files, in search order ,for example to include project\templates, use 'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,                #Whether the engine should look for my_app/templates/
        'OPTIONS': {                     #depending upon BACKEND , https://docs.djangoproject.com/en/2.0/topics/templates/#module-django.template.backends.django
            'context_processors': [      #a list of dotted Python paths to callables that are used to populate the context when a template is rendered with a request. 
                                         #These callables take a request object as their argument and return a dict of items to be merged into the context.
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',  #for admin module
                'django.contrib.messages.context_processors.messages', #for  "flash message",
            ],
            #loaders to be used for template file loading 
            #by default below is not required and 'APP_DIRS': True means filesystem.Loader and app_directories.Loader are active
            #To use make APP_DIRS as false 
        #    'loaders' : [
        #            'django.template.loaders.cached.Loader'      #for caching below loader 
        #            'django.template.loaders.filesystem.Loader'  #Loads templates from the filesystem, according to DIRS
        #            'django.template.loaders.app_directories.Loader' #For each app in INSTALLED_APPS, the loader looks for a templates subdirectory.
        #                                                             #The order of INSTALLED_APPS is significant, first template found is loaded ignoring same name in other apps
        #    ],                                                       #Hence use namespace eg another subdir as my_app eg my_app/templates/my_app/template.html and always use as my_app/template.html
        },
    },
]
#below would override all settings of TEMPLATES, hence deprecated  
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates')
)

#For putting the site under WSGI enabled server eg apache httpd
WSGI_APPLICATION = 'examplesite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'django',
#        'USER': 'root',
#        'PASSWORD': '',
#        'HOST': '127.0.0.1',
#    }
#}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
#Validators are class with (OPTIONS are sent to constructor)method: validate(self, password, user=None) method, if error raises ValidationError else return None
#can be also called manually with django.contrib.auth.password_validation.validate_password(password, user=None, password_validators=None)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

#internationalization  Writing code such that it is locale sensitive 
#localization           Writing translation for each locale 
#both are done by below settings 

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True
#Steps for I/L 
#Use django.utils.translation.ugettext("string_tobe_localized") in any py file 
#or in template , {% trans "string_tobe_localised" %}
#create 'locale' subdir in each my_app (MUST)
#Use command: django-admin makemessages -l locale_code  #must have  GNU gettext utilities installed,
#for example 'en-us' is language code, 'en_US' is locale name/code
#Above generates .po file eg in my_app/locale/<locale_code>/LC_MESSAGES/django.po
#contains 

#: path/to/python/module.py:23
#msgid "string_tobe_localised"
#msgstr ""    #<-- here you put translated version of "string_tobe_localised"
#To reexamine , Use django-admin makemessages -a
#Then , compile as  (create .mo file from .po file) 
#django-admin compilemessages





# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash. so below URLs are actually  from above MEDIA_ROOT
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'         #prefix to access static file in URL  it is under my_app/static/
                                #Preferred to have another my_app subdir as a namespace as first file found is loaded across all installed apps  
                                # my_app/static/my_app/file.ext and is used as my_app/file.ext

#For any other user defined static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
]

#in template , handle as 
#{% load static %}
#<img src="{% static "my_app/example.jpg" %}" alt="My image"/>
#when file is my_app/static/my_app/example.jpg


#printing to console 
#check other Backend at https://docs.djangoproject.com/en/2.0/topics/email/
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ndas1971@gmail.com'
EMAIL_HOST_PASSWORD = 'xyzabc'

#Login required 

SESSION_EXPIRE_AT_BROWSER_CLOSE = True    # everytime browser is closed, session is expired, ELSE persistant session 
SESSION_COOKIE_AGE  = 5*60 # in seconds 


##Logging 
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
            },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'file.log',
            'formatter': 'simple'
            },
        },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
            },
         'examplesite': {                      #Put the root of your module to handle the logging
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
            },
        }
    }

#This is required for correct logging 
import logging.config
logging.config.dictConfig(LOGGING)

#usage of log 
#import logging
#log = logging.getLogger(__name__)
#log.debug("GET " + str(request.GET))




###File: urls.py 
"""
The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path 

urlpatterns = [
    path('admin/', admin.site.urls),
]

##Other syntax 
from django.conf.urls import url
#OR 
from django.urls import re_path 
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #or
    re_path(r'^admin/', admin.site.urls),
]

   
        
###STEP 1.4  : check quickly 
$ cd examplesite
$ python manage.py help runserver
$ python manage.py runserver  8000 #<<port>>

#Open  http://127.0.0.1:8000/




###Step1.5.1 - Add one static file 
#in settings.py 
STATICFILES_DIRS = (
    "static/",    
   )
#examplesite/static/hello.html 
#can contain css, js etc 
<!DOCTYPE html>
<html> 
 <head> 
    <title>  Demo </title>
    
    <style>
        .mainDiv {
                border: 1px solid red;
                padding: 5px;
                min-height: 10px;
            }
    </style>  

    <script >
         function clck(evt){   //click is reserved method
           alert(evt);
         }        
    </script>    
 </head> 
 <body>
 <div class="mainDiv" id="mainDiv"  onclick="clck(event)"> 
 Hello
 </div>  
 </body>   
</html>

#check 
$ python manage.py runserver  8000 #<<port>>
#With URL http://127.0.0.1:8000/static/hello.html

###Step1.5.2 - Add path to urls.py 
1. When Django starts , it check root url file from examplesite\settings.py 
    ROOT_URLCONF = 'examplesite.urls'

2. examplesite\urls.py file is processed , urlpatterns is [path, path, ...] 
    django.conf.urls.url(regex, view, kwargs=None, name=None)
    #or 
    django.urls.re_path(regex, view, kwargs=None, name=None)
    #or for non regex path 
    django.urls.path(path, view, kwargs=None, name=None)
    view : callable object 
    kwargs : allows to pass additional arguments to the view function 
    name: used for performing  URL reversing ie go to view callable from 'name' (name must be unique)
            for example 
            •In templates: Using the {% url 'name' }
            •In Python code: Using the django.urls.reverse('name') function.
                    

3.  Add following in examplesite/urls.py

from . import views
urlpatterns = [                #previously it is patterns('', url...)
    #....
    url(r'^$', views.index, name='index'),      # name is for reverse URL resolve 
    #url(r'^hello2/(?P<id>\d+)', views.index2, kwargs={'url': 'index'}, name = "views_index"), 
    path('hello2/<int:id>', views.index2, kwargs={'url': 'index'}, name = "views_index")
    url(r'hello/$', views.hello) #matches  http://address:port/hello and calls hello method of views module 
   ]

4. Add examplesite/views.py 

from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world")

4.2 Update views.py with below 
#render() is a new shortcut for render_to_response  that will automatically use RequestContext 
#Always use render 
#handling Query 
from django.shortcuts import render

def index2(request, id, url):  #path('hello2/<int:id>', views.index2, kwargs={'url': 'index'}, name = "views_index")
    query = request.GET.dict()
    #log.debug("GET " + str(request.GET))
    return render(request, 'index.html', {'id': id, 'queries':query})

    
# templates/index.html 
#contains reverse url etc 
#'if' tag may use the operators and, or, not, ==, !=, <, >, <=, >=, in, not in, is, and is not 

# Filter is used after | , 
#REF: https://docs.djangoproject.com/en/2.0/ref/templates/builtins/ 
#Arithmetic operation on value 
#Generally it is recommended you do this calculation in your view. 
#or use  'add' filter(builtin) or use pip django-mathfilters and then {% load mathfilters %}   <li>13 - 17 = {{ 13|sub:17 }}</li>

<h1> List of Queries for id {{ id }} </h1>

{% if queries.items %}
    Number of Queries: {{ queries.items | length }}       
{% else %}
    No Queries.
{% endif %}

<br />
<a href="{% url 'views_index' id|add:100 %}" > Refresh </a>



#check 
$ python manage.py runserver  8000 #<<port>>
#With URL http://127.0.0.1:8000/hello2/23?size=20


##Understand the error as templates are not found  
#Solution - update settings.py 
TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...
    }...]
    

4.3 Update views.py with below to handle redirect

from django.http import HttpResponseRedirect  
from django.urls  import reverse
def hello(request):
    return HttpResponseRedirect(reverse('index'))


5.  Add following in examplesite/urls.py

from django.conf.urls import include 

urlpatterns = [                #previously it is patterns('', url...)
    #....  
    url(r'^dummy/', include('dummy.urls')), #match .../dummy/ and pass the remaining strings to urls.py of module dummy 
]

5.1 Create dummy module with __init__.py 
5.2 , Update dummy/views.py 
from django.http import HttpResponse
def index(request, name):           #comes from url's (\w+), this positional args 
    return HttpResponse("Hello " + name)


5.3 Update dummy/urls.py 
from django.conf.urls import url, include 
from . import views

#after dummy/
urlpatterns = [    
    url(r'^(\w+)/$',  views.index),    #views 's index method has 2nd arg as (\w+)
]                                                           



6. Add following in examplesite/urls.py - Using class based view 
from django.views.generic import TemplateView

urlpatterns = [
    ...
    url(r'^about/$', TemplateView.as_view(template_name="about.html")),
]
6.1 Create templates/about.html
<h1> This is new Project </h1>


6.2 - Lets Create userdefined MyView 
#check attributes in https://ccbv.co.uk/projects/Django/2.0/django.views.generic.base/TemplateView/
#Template context data is created in get_context_data
#examplesite/views.py 

from django.views.generic.base import TemplateView
import os 

class MyView(TemplateView):

    template_name = "environ.html"

    def get_context_data(self, **kwargs):
        context = super(MyView, self).get_context_data(**kwargs)
        context['objects'] = os.environ
        return context
        
6.3 Update urls.py 
from .views import MyView

urlpatterns = [
    ...
    url(r'^environ/$', MyView.as_view()),
]


6.3 Update templates/environ.html to include template language 
#check all builtin tags and filters - https://docs.djangoproject.com/en/2.0/ref/templates/builtins/

#Note template 'for' is for list only. 
#To access dictionary or list of list, use with .items  
#Can not access dictionary like {{ objects[k] }} as {{ }} contains only variable name like in 'for' in object.items (Note without end ())
#Variable names consist of any combination of alphanumeric characters and the underscore ("_"). 

#The dot (".")  appears in variable sections and interpreted as either(in order)
#Dictionary lookup ie dicts["key"] for dicts.key
#Attribute or method lookup for any python class  
    #If the resulting value is callable, it is called with no arguments. 
    #The result of the call becomes the template value.
#Numeric index lookup
#After ., string must be literal not any var 

{# single line comment #}

{% comment %} 
The for loop sets a number of variables available within the loop
forloop.counter         The current iteration of the loop (1-indexed) 
forloop.counter0        The current iteration of the loop (0-indexed) 
forloop.revcounter      The number of iterations from the end of the loop (1-indexed) 
forloop.revcounter0     The number of iterations from the end of the loop (0-indexed) 
forloop.first           True if this is the first time through the loop 
forloop.last            True if this is the last time through the loop 
forloop.parentloop      For nested loops, this is the loop surrounding the current one 
{% endcomment %}

<h1> List of environ variables </h1>

<table border="1">
  <tr>
    <th>Variable</th>
    <th >Value</th>
  </tr>  
 {% for k,v in objects.items %}
    <tr >
        <td >{{ k }}</td>
        <td> {{ v }}</td>
        
    </tr>
{% endfor %}

</table>

#check 
$ python manage.py runserver  8000 #<<port>>
#With URL http://127.0.0.1:8000/environ


###Step1.6 Deploy 
##Under apache httpd with mod_wsgi - enable mod_wsgi in http.conf 
#below mod_wsgi is valid only for python 2.7 
#copy examplesite to C:/indigoampp/apache-2.2.15/wsgi-bin/django/
LoadModule wsgi_module modules/mod_wsgi.so

WSGIScriptAlias  /first "C:/indigoampp/apache-2.2.15/wsgi-bin/django/examplesite/examplesite/wsgi.py"
WSGIPythonPath   "C:/indigoampp/apache-2.2.15/wsgi-bin/django/examplesite/"

<Directory "C:/indigoampp/apache-2.2.15/wsgi-bin/django/examplesite/examplesite">
	Order allow,deny
   Allow from all
</Directory>

# Then check 
http://localhost/first/hello

#NOTE:
#If multiple Django sites are run in a single mod_wsgi process, 
#all of them will use the settings of whichever one happens to run first. 
#This can be solved by changing:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ project_name }}.settings")
#in wsgi.py, to:
os.environ["DJANGO_SETTINGS_MODULE"] = "{{ project_name }}.settings"


##Other deployment options 
#gunicorn(linux)/Waitress(windows)Or oracle virtualbox with linux - very fast  , or uwsgi(unix)- another fast 
#https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/gunicorn/
#Or can use gevent which is asynchronous server (very fast) or tornado etc 

'''
$ pip install gevent 

'''

from gevent.pywsgi import WSGIServer
from examplesite.wsgi import application as app

http_server = WSGIServer(('127.0.0.1', 8000), app)
http_server.serve_forever()


###Serving Static files 
#During Development , it is OK as Django automatically takes care of that with above settings 
#but production through wsgi.py application, 
#as Django doesn’t serve files itself
#it leaves that job to whichever deployement Web server(as it is scalable)

1.Set the STATIC_ROOT setting to the directory from which you’d like to serve these files, 
STATIC_ROOT = "/var/www/example.com/static/"

2.Run the collectstatic management command:
  This will copy all files from your static folders into the STATIC_ROOT directory
$ python manage.py collectstatic

3. configure in webserver, for example, in http with mod_wsgi 
#This example sets up Django at the site root, 
#but serves robots.txt, favicon.ico, and anything in the /static/ and /media/ URL space as a static file. 
#All other URLs will be served using mod_wsgi:

Alias /robots.txt /path/to/mysite.com/static/robots.txt
Alias /favicon.ico /path/to/mysite.com/static/favicon.ico

Alias /media/ /path/to/mysite.com/media/
Alias /static/ /path/to/mysite.com/static/

<Directory /path/to/mysite.com/static>
    Require all granted
</Directory>

<Directory /path/to/mysite.com/media>
    Require all granted
</Directory>

WSGIScriptAlias / /path/to/mysite.com/mysite/wsgi.py

<Directory /path/to/mysite.com/mysite>
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>


##To serve static file under gevent , add below in urls.py 
##If using with GEVENT as wsgi automatically shuts off static file serving 
#but static only works with Debug=False 

from django.conf import settings 
import os
from django.conf.urls.static import static

if os.environ['GEVENT']:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

##OR using django-gevent-deploy
pip install django-gevent-deploy

#Then 
$ python manage.py rungevent [[addr]:port] [pool_size]



##STEP-3.0 : Using bootstrap 
#base.html 
{% load static %}
<!DOCTYPE html>
<html>
<head>
  <title>Django</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="{% static "css/bootstrap.min.css" %}">
  <script src="{% static "js/jquery.min.js" %}"></script>
  <script src="{% static "js/bootstrap.min.js" %}"></script>
    <body>

        <div class="jumbotron jumbotron-fluid  text-center">
          <h1>Django  site</h1>
          <p>OK, this is my first project </p>
        </div>


        <div class="container">
        {% block container %}
        {% endblock container%}
        </div>

    </body>
</html>

#environ.html 
{% extends "base.html" %}

{% block container %}
{{block.super}}
<div class="table-responsive">
<table class="table">       <!- "table table-dark table-striped table-bordered table-condensed table-hover" ->
  <caption>List of Environment variables</caption>
  <thead class="thead-dark">    <!- thead-light ->
    <tr>
      <th scope="col">Key</th>
      <th scope="col" colspan="3">Value</th>
    </tr>
  </thead>
  <tbody>
    {% for k,v in objects.items %}
    <tr>
      <th scope="row">{{k}}</th>
      <td colspan="3">{{v}}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
</div>
{% endblock %}



### Quick URlConf 

##What the URLconf searches against
#This does not include GET or POST parameters, or the domain name.
#For example, in a request to https://www.example.com/myapp/, the URLconf will look for myapp/.
#In a request to https://www.example.com/myapp/?page=3, the URLconf will look for myapp/.

##Path converters for django.urls.path 
str 
    Matches any non-empty string, excluding the path separator, '/'. 
    This is the default if a converter isn’t included in the expression.
int 
    Matches zero or any positive integer. Returns an int.
    eg path('hello2/<int:id>'..), then view function would have one arg 'id' 
slug 
    Matches any slug string consisting of ASCII letters or numbers, plus the hyphen and underscore characters. 
    For example, building-your-1st-django-site.
uuid 
    Matches a formatted UUID. 
    To prevent multiple URLs from mapping to the same page, dashes must be included and letters must be lowercase. 
    For example, 075194d3-6885-417e-a8a8-6c931e272f00. Returns a UUID instance.
path 
    Matches any non-empty string, including the path separator, '/'. 
    This allows you to match against a complete URL path rather than just a segment of a URL path as with str.
    
##Custom Converters 
#A converter is a class that includes the following:
    A regex class attribute, as a string.
    A to_python(self, value) method, 
        which handles converting the matched string into the type that should be passed to the view function. 
        It should raise ValueError if it can’t convert the given value.
    A to_url(self, value) method, 
        which handles converting the Python type into a string to be used in the URL.
#Example 
#converts.py 
class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value

#Usage 
from django.urls import path, register_converter

from . import converters, views

register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    path('articles/<yyyy:year>/', views.year_archive),  #def year_archive(request, year):
    ...
]

##Regex Match using re_path 
from django.urls import path, re_path #re_path is same as django.conf.urls.url
from . import views

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$', views.article_detail),
]
#Equivalent to 
urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    path('articles/<int:year>/', views.year_archive),
    path('articles/<int:year>/<int:month>/', views.month_archive),
    path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
]
#Note 
    There’s no need to add a leading slash, because every URL has that. 
    For example, it’s articles, not /articles.
    A request to /articles/2005/03/ would match the third entry in the list. 
        Django would call the function views.month_archive(request, year=2005, month=3).
    /articles/2003/ would match the first pattern in the list, not the second one,
        because the patterns are tested in order, and the first one is the first test to pass. 
        Here, Django would call the function views.special_case_2003(request)
    /articles/2003 would not match any of these patterns, 
        because each pattern requires that the URL end with a slash.
    /articles/2003/03/building-a-django-site/ would match the final pattern. 
        Django would call the function views.article_detail(request, year=2003, month=3, slug="building-a-django-site").

##Nested arguments
from django.urls import re_path

urlpatterns = [
    re_path(r'^blog/(page-(\d+)/)?$', blog_articles),                  # bad
    re_path(r'^comments/(?:page-(?P<page_number>\d+)/)?$', comments),  # good
]
#for example, blog/page-2/ will result in a match to blog_articles with two positional arguments: page-2/ and 2. 
#The second pattern for comments will match comments/page-2/ with keyword argument page_number set to 2. 
#The outer argument in this case is a non-capturing argument (?:...).


##Specifying defaults for view arguments

# URLconf
from django.urls import path

from . import views

urlpatterns = [
    path('blog/', views.page),
    path('blog/page<int:num>/', views.page),
]

# View (in blog/views.py)
def page(request, num=1):
    # Output the appropriate page of blog entries, according to num.

##Captured parameters
#An included URLconf receives any captured parameters from parent URLconfs, 
# In settings/urls/main.py
from django.urls import include, path

urlpatterns = [
    path('<username>/blog/', include('foo.urls.blog')),
]
#the captured "username" variable is passed to the included URLconf,
#eg, views.blog.index and views.blog.archive gets one keyword arg username 
# In foo/urls/blog.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog.index),
    path('archive/', views.blog.archive),
]


##Including other URLconfs
#Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point 
#and sends the remaining string to the included URLconf for further processing. 
from django.urls import include, path

urlpatterns = [
    path('community/', include('aggregator.urls')),
    path('contact/', include('contact.urls')),
]
#Another way 
# the /credit/reports/ URL will be handled by the credit_views.report() Django view.
from django.urls import include, path

from apps.main import views as main_views
from credit import views as credit_views

extra_patterns = [
    path('reports/', credit_views.report),
    path('reports/<int:id>/', credit_views.report),
    path('charge/', credit_views.charge),
]

urlpatterns = [
    path('', main_views.homepage),
    path('help/', include('apps.help.urls')),
    path('credit/', include(extra_patterns)),
]
#OR views.history gets(and others) two keyword arg page_slug, page_id
from django.urls import include, path
from . import views

urlpatterns = [
    path('<page_slug>-<page_id>/', include([
        path('history/', views.history),
        path('edit/', views.edit),
        path('discuss/', views.discuss),
        path('permissions/', views.permissions),
    ])),
]




##Passing extra options to view functions
from django.urls import path
from . import views

urlpatterns = [
    path('blog/<int:year>/', views.year_archive, {'foo': 'bar'}),
]
#for a request to /blog/2005/, Django will call 
views.year_archive(request, year=2005, foo='bar')
#In case of conflicts ,  the arguments in the dictionary will be used instead of the arguments captured in the URL.

##Passing extra options to include()
# main.py
from django.urls import include, path

urlpatterns = [
    path('blog/', include('inner'), {'blog_id': 3}),
]

# inner.py
from django.urls import path
from mysite import views

urlpatterns = [
    path('archive/', views.archive),  #views.archive would get keyword arg blog_id 
    path('about/', views.about),
]

#OR , is equivalent to 

# main.py
from django.urls import include, path
from mysite import views

urlpatterns = [
    path('blog/', include('inner')),
]

# inner.py
from django.urls import path

urlpatterns = [
    path('archive/', views.archive, {'blog_id': 3}),
    path('about/', views.about, {'blog_id': 3}),
]


##Reverse resolution of URLs
#The string used for the URL name can contain any characters , 
#use some prefix to decrease clashes 
from django.urls import path

from . import views

urlpatterns = [
    #...
    path('articles/<int:year>/', views.year_archive, name='news-year-archive'),
    #...
]
#in template code by using:

<a href="{% url 'news-year-archive' 2012 %}">2012 Archive</a>
{# Or with the year in a template context variable: #}
<ul>
{% for yearvar in year_list %}
<li><a href="{% url 'news-year-archive' yearvar %}">{{ yearvar }} Archive</a></li>
{% endfor %}
</ul>

#Or in Python code:
from django.http import HttpResponseRedirect
from django.urls import reverse

def redirect_to_year(request):
    # ...
    year = 2006
    # ...
    return HttpResponseRedirect(reverse('news-year-archive', args=(year,)))

    
    
    
##URL namespaces
#URL namespaces allow to uniquely reverse named URL patterns even if different applications use the same URL names. 
    
#Namespaced syntax  
'namespace(application or instance):view_name'
#Example 
'admin:index'. 
    This indicates a namespace of 'admin', and a named URL of 'index'.
# Namespaces can also be nested. 
'sports:polls:index' 
    look for a pattern named 'index' in the namespace 'polls' 
    that is itself defined within the top-level namespace 'sports'.
    
    
##Defining application namespace 
#This describes the name of the application that is being deployed.
#Every instance of a single application will have the same application namespace

#OR Use app_name attribute and include()  like below 
#polls/urls.py

from django.urls import path

from . import views

app_name = 'polls' #The URLs defined in polls.urls will have an application namespace polls.
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    ...
]

#urls.py

from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
]

#OR Use include() like below 
from django.urls import include, path

from . import views

polls_patterns = ([
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
], 'polls') #2nd arg is application namespace 

urlpatterns = [
    path('polls/', include(polls_patterns)),
]
    
##Defining instance  namespace 
#This identifies a specific instance of an application. 
#Instance namespaces should be unique across entire project. 

#If the instance namespace is not specified, it will default to the included URLconf’s application namespace. 
#ie it will also be the default instance for that namespace.

#OR Use  namespace argument to include(). 
#Example - two instances of the polls application 
#one called 'author-polls' and one called 'publisher-polls'. 
#urls.py
from django.urls import include, path

urlpatterns = [
    path('author-polls/', include('polls.urls', namespace='author-polls')),
    path('publisher-polls/', include('polls.urls', namespace='publisher-polls')),
]

#polls/urls.py

from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    
]

    
##Lookup - Reversing namespaced URLs

#For given a namespaced URL (e.g. 'polls:index') to resolve, 
1.First, Django looks for a matching application namespace (ie 'polls'). 
  This will yield a list of instances of that application eg 'author-polls' and  'publisher-polls'
  
2.If there is a current application defined, Django finds and returns the URL resolver for that instance. 
  For example , Given 
        reverse('polls:index', current_app=self.request.resolver_match.namespace)
    and in the template:
        {% url 'polls:index' %}
    and Inside 'detail' view of  'author-polls' instance, both above would resolve to "/author-polls/"
    Note in 'url' tag , by default current application resolves to currently activated urlpatterns
    Override this default by setting the current application on the request.current_app attribute.
    
4.If there is no current application. Django looks for a default application instance. 
  The default application instance is with instance namespace matching the application namespace 
  (in this example, an instance of polls called 'polls', but not existing as only two instances 'author-polls' and  'publisher-polls').

5.If there is no default application instance, Django will pick the last deployed instance of the application, 
  whatever its instance name may be(in this example , 'publisher-polls' instance)
  For example ,if we were rendering a page somewhere else on the site 
  'polls:index' will resolve to the last registered instance of polls. ie 'publisher-polls' index view 
  
6.If the provided namespace doesn’t match an application namespace in step 1, 
  Django will attempt a direct lookup of the namespace as an instance namespace.
  For example, 'author-polls:index' will always resolve to the index page of the instance 'author-polls'
  
7.If there are nested namespaces, these steps are repeated for each part of the namespace 
   until only the view name is unresolved. 
   
   
   
   
   
   
### Quick View Functions 

from django.http import HttpResponse
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
    
## More Usages of HttpResponse
from django.http import HttpResponse
response = HttpResponse("Here's the text of the Web page.")
response = HttpResponse("Text only, please.", content_type="text/plain")

#to add content incrementally, you can use response as a file-like object:
response = HttpResponse()
response.write("<p>Here's the text of the Web page.</p>")
response.write("<p>Here's another paragraph.</p>")

#Setting/removing  header fields
response = HttpResponse()
response['Age'] = 120
del response['Age']

#Redirect 
return  HttpResponseRedirect(url='absolute or relative path')

#Telling the browser to treat the response as a file attachment
#mydata is iterator of the data eg like file, generator etc 
data = open(file_full_path, 'rb')
response = HttpResponse(open(file_full_path, 'rb'), content_type='application/vnd.ms-excel')
response['Content-Disposition'] = 'attachment; filename="foo.xls"'
data.close()

#Download a file using StreamingResponse (eg for large text file)
import mimetypes 
def download(request, document_file_name):
    # Handle file download
    file_full_path = os.path.join(settings.MEDIA_ROOT, document_file_name)
    filename = os.path.basename(file_full_path)
    #wud autoclose 
    response = StreamingHttpResponse(open(file_full_path, 'rb'), content_type=mimetypes.guess_type(file_full_path)[0]) 
    response['Content-Disposition'] = "attachment; filename={0}".format(filename)
    response['Content-Length'] = os.path.getsize(file_full_path) 
    return response

#Or using FileResponse(subclass of HttpResponse) for binary file download 
    from django.http import FileResponse
    response = FileResponse(open('myfile.png', 'rb')) #it would autoclose 
    response['Content-Disposition'] = "attachment; filename=myfile.png"
    response['Content-Length'] = os.path.getsize(myfile.png) 
    return response 

#To send json response 
class JsonResponse(data, encoder=DjangoJSONEncoder, safe=True, json_dumps_params=None, **kwargs)[source]¶
    The json_dumps_params parameter is a dictionary of keyword arguments to pass to the json.dumps() call used to generate the response.

#Safe=True, if root object is a dict   
from django.http import JsonResponse
response = JsonResponse({'foo': 'bar'}, content_type='application/json')

#In order to serialize objects other than dict, set the safe parameter to False:
response = JsonResponse([1, 2, 3], safe=False, content_type='application/json')




###django-jsonview: Note to have view returning JSON always, use 
$ pip install django-jsonview



from jsonview.decorators import json_view

@json_view
def my_view(request):
    return {
        'foo': 'bar',
    }


#Class-based views (CBVs) can inherit from JsonView

from jsonview.views import JsonView


class MyView(JsonView):
    def get_context_data(self, **kwargs):
        context = super(MyView, self).get_context_data(**kwargs)
        context['my_key'] = 'some value'
        return context

# or, method decorator
from django.utils.decorators import method_decorator
from jsonview.decorators import json_view


class MyView(View):
    @method_decorator(json_view)
    def dispatch(self, *args, **kwargs):
        return super(MyView, self).dispatch(*args, **kwargs)

# or, in URLconf
patterns = [
    url(r'^/my-view/$', json_view(MyView.as_view())),
]

 
##Content Types
#To return a content type other than the standard application/json
from jsonview.decorators import json_view

@json_view(content_type='application/vnd.github+json')
def myview(request):
    return {'foo': 'bar'}

##Status Codes
#Tto return a different HTTP status code, just return two values instead of one. 
@json_view
def myview(request):
    if not request.user.is_subscribed():
        # Send a 402 Payment Required status.
        return {'subscribed': False}, 402
    # Send a 200 OK.
    return {'subscribed': True}

 
##Extra Headers
@json_view
def myview(request):
    return {}, 200, {'X-Server': 'myserver'}


##Raw Return Values
#Eg to return cached json string 

from django import http
from jsonview.decorators import JSON

@json_view
def caching_view(request):
    kached = cache.get('cache-key')
    if kached:
        return http.HttpResponse(kached, content_type=JSON)
    # Assuming something else populates this cache.
    return {'complicated': 'object'}

    
##Alternative JSON Implementations -instead of stdlib json 
JSON_MODULE = 'ujson'


##Configuring JSON Output
#update settings.py 
JSON_OPTIONS = {
    'indent': 4,
}


#Or to compactify it:
JSON_OPTIONS = {
    'separators': (',', ':'),
}


#jsonview uses DjangoJSONEncoder by default.
# To use a different JSON encoder, use the cls option:
JSON_OPTIONS = {
    'cls': 'path.to.MyJSONEncoder',
}

#If you are using a JSON module that does not support the ``cls`` kwarg, such as ujson
JSON_OPTIONS = {
    'cls': None,
}

#Default value of content-type is 'application/json' OR set as 
JSON_DEFAULT_CONTENT_TYPE = 'application/json; charset=utf-8'

 
##Atomic Requests
#Because @json_view catches exceptions, 
#the normal Django setting ATOMIC_REQUESTS does not correctly cause a rollback. 
#USe as below 
@json_view
@transaction.atomic
def my_func(request):
    # ...





###Returning errors
#There are subclasses of HttpResponse for a number of common HTTP status codes other than 200 (which means “OK”).

from django.http import HttpResponse, HttpResponseNotFound

def my_view(request):
    # ...
    if foo:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return HttpResponse('<h1>Page was found</h1>')
#OR 
from django.http import HttpResponse

def my_view(request):
    # ...

    # Return a "created" (201) response code.
    return HttpResponse(status=201)       
        
##The Http404 exception
#When you return an error such as HttpResponseNotFound, 
#you’re responsible for defining the HTML of the resulting error page:

return HttpResponseNotFound('<h1>Page not found</h1>')

#to have a consistent 404 error page across your site, 
#Django provides an Http404 exception
#Django will catch it and return the standard error page for  application, along with an HTTP error code 404.

from django.http import Http404
from django.shortcuts import render
from polls.models import Poll

def detail(request, poll_id):
    try:
        p = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404("Poll does not exist")
    return render(request, 'polls/detail.html', {'poll': p})

#to show customized HTML when Django returns a 404, 
#create an HTML template named 404.html and place it in the top level of template tree. 
#(eg Create project level templates /project/templates, and use with DIRS=[] in settings.py and put 404.html there)
#This template will then be served when DEBUG is set to False.

#When DEBUG is True,  provide a message to Http404 
#and it will appear in the standard 404 debug template. 


##Customizing error views
#specify the handlers as seen below in URLconf (setting them anywhere else will have no effect).

#The page_not_found() view is overridden by handler404:
handler404 = 'mysite.views.my_custom_page_not_found_view'

#The server_error() view is overridden by handler500:
handler500 = 'mysite.views.my_custom_error_view'

#The permission_denied() view is overridden by handler403:
handler403 = 'mysite.views.my_custom_permission_denied_view'

#The bad_request() view is overridden by handler400:
handler400 = 'mysite.views.my_custom_bad_request_view'

 

##Important attributes of django.http.HttpRequest 
#https://docs.djangoproject.com/en/2.0/ref/request-response/#ref-httpresponse-subclasses
HttpRequest.body        raw HTTP request body as a byte string
HttpRequest.path        example: /music/bands/the_beatles/
HttpRequest.get_full_path()  example: "/music/bands/the_beatles/?print=true"
HttpRequest.method      'GET' or 'POST' or others 
HttpRequest.content_type
HttpRequest.GET          QueryDict ,  dictionary-like object , access param as ['param']
HttpRequest.POST         QueryDict ,  dictionary-like object 
HttpRequest.FILES       {'name':  UploadedFile_instance}  ,
                        Must be : enctype="multipart/form-data" and <form> contains <input type="file" name="" />
                        Each value in FILES is an UploadedFile
HttpRequest.META        All headers in dictionary-like object
HttpRequest.COOKIES     A dictionary containing all cookies. Keys and values are strings.
HttpRequest.resolver_match    An instance of ResolverMatch representing the resolved URL

#Attributes set by middleware
HttpRequest.session     From the SessionMiddleware: A readable and writable, dictionary-like object that represents the current session.
HttpRequest.site        From the CurrentSiteMiddleware: An instance of Site or RequestSite as returned by get_current_site() representing the current site.
HttpRequest.user        From the AuthenticationMiddleware: An instance of AUTH_USER_MODEL representing the currently logged-in user. 
                        If the user isn’t currently logged in, user will be set to an instance of AnonymousUser. 
                        #to test 
                        if request.user.is_authenticated:
                            ... # Do something for logged-in users.
                        else:
                            ... # Do something for anonymous users.

##Quick Upload 
#for example for <input type="file" name="file">
#request.FILES['file'] would be UploadedFile and used as handle_uploaded_file(request.FILES['file'])
#request.FILES will only contain data if the request method was POST ie request.method == 'POST'
#and the <form> has the attribute enctype="multipart/form-data". 

#UploadedFile.name, UploadedFile.size (in bytes)
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)



##Where uploaded data is stored
#By default, if an uploaded file is smaller than 2.5 megabytes, 
#Django will hold the entire contents of the upload in memory. 

#if an uploaded file is too large, Django will write the uploaded file to a temporary file stored in  system’s temporary directory.



##Important Attributes of HttpResponse        
HttpResponse.__init__(content='', content_type=None, status=200, reason=None, charset=None)
HttpResponse.set_cookie(key, value='', max_age=None, expires=None, path='/', domain=None, secure=None, httponly=False)
    Sets a cookie. 
        max_age should be a number of seconds, or None (default) if the cookie should last only as long as the client’s browser session. If expires is not specified, it will be calculated.
        expires should either be a string in the format "Wdy, DD-Mon-YY HH:MM:SS GMT" or a datetime.datetime object in UTC. If expires is a datetime object, the max_age will be calculated.
        Use domain if you want to set a cross-domain cookie. For example, domain="example.com" will set a cookie that is readable by the domains www.example.com, blog.example.com, etc. Otherwise, a cookie will only be readable by the domain that set it.
        Use httponly=True if you want to prevent client-side JavaScript from having access to the cookie.
HttpResponse.set_signed_cookie(key, value, salt='', max_age=None, expires=None, path='/', domain=None, secure=None, httponly=False)
    Like set_cookie(), but cryptographic signing the cookie before setting it. 
    Use in conjunction with HttpRequest.get_signed_cookie(). 
    You can use the optional salt argument for added key strength, but you will need to remember 
    to pass it to the corresponding HttpRequest.get_signed_cookie() call.
HttpResponse.delete_cookie(key, path='/', domain=None)
    Deletes the cookie with the given key. Fails silently if the key doesn’t exist.
HttpResponse.writelines(lines)
    Writes a list of lines to the response. 
    Line separators are not added. 
    This method makes an HttpResponse instance a stream-like object.

    
##django.http.request.QueryDict 
#in general immutable or use mutable=True in ctor
#create a shell 
$ python manage.py shell 
from django.http.request import QueryDict
q = QueryDict('a=1&a=2&c=3')  #<QueryDict: {'a': ['1', '2'], 'c': ['3']}>
q['a']          # u'2'  #last item 
q.getlist('a')  #[u'1', u'2']  #all items as list 
q.lists()       #[(u'a', [u'1', u'2']), (u'c', [u'3'])]
'a' in q        # True
q.urlencode()   # u'a=1&a=2&c=3'

#urldecode is automatic  
q = QueryDict('a=1+3&a=2&c=3') #<QueryDict: {u'a': [u'1 3', u'2'], u'c': [u'3']}>
q = QueryDict('a=1%203&a=2&c=3') #<QueryDict: {u'a': [u'1 3', u'2'], u'c': [u'3']}>


##Django shortcut functions
django.shortcuts.render(request, template_name, context=None, content_type=None, status=None, using=None)
    from django.shortcuts import render
    def my_view(request):
        # View code here...
        return render(request, 'myapp/index.html', {
            'foo': 'bar',
        }, content_type='application/xhtml+xml')
    #This example is equivalent to:
    from django.http import HttpResponse
    from django.template import loader
    def my_view(request):
        # View code here...
        t = loader.get_template('myapp/index.html')
        c = {'foo': 'bar'}
        return HttpResponse(t.render(c, request), content_type='application/xhtml+xml')
django.shortcuts.render_to_response(template_name, context=None, content_type=None, status=None, using=None)
    Deprecated since version 2.0., Use 'render'
    Note there is no 'request' 
django.shortcuts.redirect(to, permanent=False, *args, **kwargs)
    The arguments could be:
        A model: the model’s get_absolute_url() function will be called.
        A view name, possibly with arguments: reverse() will be used to reverse-resolve the name.
        An absolute or relative URL, which will be used as-is for the redirect location.
    By default issues a temporary redirect; pass permanent=True to issue a permanent redirect.
    #By passing some object; that object’s get_absolute_url() method will be called to figure out the redirect URL:
    from django.shortcuts import redirect
    def my_view(request):
        object = MyModel.objects.get(...)
        return redirect(object)
    #By passing the name of a view and optionally some positional or keyword arguments; 
    #the URL will be reverse resolved using the reverse() method:
    def my_view(request):
        return redirect('some-view-name', foo='bar')

    #By passing a hardcoded URL to redirect to:
    def my_view(request):
        return redirect('/some/url/')

    #This also works with full URLs:
    def my_view(request):
        return redirect('https://example.com/')

        
##Allowed HTTP methods
#check other decorators - https://docs.djangoproject.com/en/2.0/topics/http/decorators/
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"]) #request methods should be in uppercase.
def my_view(request):
    # I can assume now that only GET or POST requests make it this far
    # ...
    pass
        
        
###Quick Django Debug 

##Using Debug  tag  with django.template.context_processors.debug
#If this processor is enabled, every RequestContext will contain debug 
#and and sql_queries variables – but only if your DEBUG setting is set to True 
#and the request’s IP address (request.META['REMOTE_ADDR']) is in the INTERNAL_IPS setting
<div id="django-debug"><pre>{% debug|escape %}</pre></div>


##OR install https://github.com/jazzband/django-debug-toolbar
$ pip install django-debug-toolbar

#then in settings.py 
INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS = [
    # ...
    'django.contrib.staticfiles',
    # ...
    'debug_toolbar',
]

STATIC_URL = '/static/'

MIDDLEWARE = [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
]


#in urls.py , end 
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns

#then check http://127.0.0.1:8000/environ/, debug toolbar is displayed 
#for example to check all variables available to above template 
#select Templates -> environ.html -> toggle context to see all context objects in that view 
#context objects are displayed directly eg for objects , use objects directly 


     
        
        
###Quick Django Template 
#https://docs.djangoproject.com/en/2.0/ref/templates/language/
#https://docs.djangoproject.com/en/2.0/ref/templates/builtins/


##Automatic HTML escaping
#By default in Django, every template automatically escapes the output of every variable tag. 
    < is converted to &lt;
    > is converted to &gt;
    ' (single quote) is converted to &#39;
    " (double quote) is converted to &quot;
    & is converted to &amp;

#To turn it off For individual variables
#use the safe filter:
This will be escaped: {{ data }}
This will not be escaped: {{ data|safe }}

#To turn it off  For template blocks
#Auto-escaping is on by default.
#The auto-escaping tag passes its effect onto templates that extend the current one 
#as well as templates included via the include tag

Hello {{ name }}

{% autoescape off %}
    This will not be auto-escaped: {{ data }}.

    Nor this: {{ other_data }}
    {% autoescape on %}
        Auto-escaping applies again: {{ name }}
    {% endautoescape %}
{% endautoescape %}


##Include tag 
#Loads a template(called template fragment) and renders it with the current context. 

{% include "foo/bar.html" %}

#template_name is variable 
{% include template_name %}


#An included template is rendered within the context of the template that includes it. 
#Example if Context has 'person' is set to "John" and 'greeting' is set to "Hello".

{% include "name_snippet.html" %}

#name_snippet.html 
{{ greeting }}, {{ person|default:"friend" }}!


#OR pass additional context to the template 
{% include "name_snippet.html" with person="Jane" greeting="Hello" %}


#OR To render the context only with the variables provided 
{% include "name_snippet.html" with greeting="Hi" only %}


  
### Custom template tags and filters
#When a Django app is added to INSTALLED_APPS, any tags it defines in the templatetags directory would be loaded 
#Check default tags and filters in django/template/defaultfilters.py and django/template/defaulttags.py
#For example, if  custom tags/filters are in a file called poll_extras.py in app 'polls'
polls/
    __init__.py
    models.py
    templatetags/
        __init__.py
        poll_extras.py
    views.py

#Usage , Note use with module name 
{% load poll_extras %}

#For example, in the filter {{ var|foo:"bar" }}, 
#the filter foo would be passed the variable var and the argument "bar".

#poll_extras.py
#get Register instance 
from django import template
register = template.Library()

def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')

def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()

register.filter('cut', cut)
register.filter('lower', lower)

#OR using as decorator 
@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg, '')

@register.filter
def lower(value):
    return value.lower()
    
#Usage 
{{ somevariable|cut:"0" }}
{{ somevariable|lower }}

#OR use with OPTIONS of django.template.backends.django.DjangoTemplates
OPTIONS={
    'libraries': {
        'myapp_tags': 'path.to.myapp.tags',
        'admin.urls': 'django.contrib.admin.templatetags.admin_urls',
    },
}
#Usage 
{% load myapp_tags %}


##Writing custom template tags - Simple tags - django.template.Library.simple_tag()
#This function takes a function that accepts any number of arguments, wraps it in a render function 
#and registers it with the template system.

import datetime
from django import template

register = template.Library()

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


#If template tag needs to access the current context, use the takes_context 
#Note that the first argument must be called context.
@register.simple_tag(takes_context=True)
def current_time(context, format_string):
    timezone = context['timezone']
    return your_get_current_time_method(timezone, format_string)

#to rename your tag, provide a custom name for it:
register.simple_tag(lambda x: x - 1, name='minusone')

@register.simple_tag(name='minustwo')
def some_function(value):
    return value - 2

#simple_tag functions may accept any number of positional or keyword arguments. For example:
@register.simple_tag
def my_tag(a, b, *args, **kwargs):
    warning = kwargs['warning']
    profile = kwargs['profile']
    ...
    return ...

#Usage like python, keyword is used with = 
{% my_tag 123 "abcd" book.title warning=message|lower profile=user.profile %}
#to store the tag results in a template variable 
{% current_time "%Y-%m-%d %I:%M %p" as the_time %}
<p>The time is {{ the_time }}.</p>





### Session handling 
#https://docs.djangoproject.com/en/2.1/topics/http/sessions/
##Enabling sessions
1.Edit the MIDDLEWARE setting to contain 'django.contrib.sessions.middleware.SessionMiddleware'. 
2.Add 'django.contrib.sessions' in INSTALLED_APPS
  By default, Django stores sessions in database (using the model django.contrib.sessions.models.Session). 
3.Install the single database table that stores session data
  $ python manage.py migrate 

##Using file-based sessions
1.set the SESSION_ENGINE setting to "django.contrib.sessions.backends.file".
2.set the SESSION_FILE_PATH setting (which defaults to output from tempfile.gettempdir(), most likely /tmp) 
  to control where Django stores session files. 
  Be sure to check that  Web server has permissions to read and write to this location.

##Using cookie-based sessions
1.set the SESSION_ENGINE setting to "django.contrib.sessions.backends.signed_cookies".
  The session data will be stored using  cryptographic signing with SECRET_KEY setting.

##Using sessions in views
#When SessionMiddleware is activated, each HttpRequest object has  session attribute - SessionBase, dict like object 
#Access by request.session in view function and in template 

#in view 
def post_comment(request, new_comment):
    if request.session.get('has_commented', False):  #default return False 
        return HttpResponse("You've already commented.")
    c = comments.Comment(comment=new_comment)
    c.save()
    request.session['has_commented'] = True
    return HttpResponse('Thanks for your comment!')

    
#in template 
{{ request.session.has_commented }}



###Using Cookies 
#Better use Session based handling which give extra security 

#Example 
response = rrender(request, 'rango/index.html', context_dict)
visits = int(request.COOKIES.get('visits', '0'))

# Does the cookie last_visit exist?
if 'last_visit' in request.COOKIES:
    # Yes it does! Get the cookie's value.
    last_visit = request.COOKIES['last_visit']
    # Cast the value to a Python date/time object.
    last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        # ...reassign the value of the cookie to +1 of what it was before...
        response.set_cookie('visits', visits+1)
        # ...and update the last visit cookie, too.
        response.set_cookie('last_visit', datetime.now())
else:
    # Cookie last_visit doesn't exist, so create it to the current date/time.
    response.set_cookie('last_visit', datetime.now())

# Return response back to the user, updating any cookies that need changed.
return response


##Setting test cookies
#When you set a cookie, you can’t actually tell whether a browser accepted it until the browser’s next request.

from django.http import HttpResponse
from django.shortcuts import render

def login(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            return HttpResponse("You're logged in.")
        else:
            return HttpResponse("Please enable cookies and try again.")
    request.session.set_test_cookie()
    return render(request, 'foo/login_form.html')


    
    

###Django Flash messages 
#Every message is tagged with a specific level that determines its priority (e.g., info, warning, or error).
#The messages framework allows to temporarily store messages in one request and retrieve them for display in a subsequent request (usually the next one). 

##Setup 
1.Add 'django.contrib.messages' is in INSTALLED_APPS.
2.MIDDLEWARE contains 'django.contrib.sessions.middleware.SessionMiddleware' 
  and 'django.contrib.messages.middleware.MessageMiddleware'.
  The default storage backend relies on sessions. 
3.The 'context_processors' option of the DjangoTemplates backend 
  defined in TEMPLATES setting contains 'django.contrib.messages.context_processors.messages'.

##Storage backends
storage.session.SessionStorage
storage.cookie.CookieStorage
(default)storage.fallback.FallbackStorage
    first uses CookieStorage, and falls back to using SessionStorage 
    for the messages that could not fit in a single cookie.
#Explicit settings 
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


##Levels 
#Tag         Level 
debug       DEBUG       Development-related messages that will be ignored (or removed) in a production deployment 
info        INFO        Informational messages for the user 
success     SUCCESS     An action was successful, e.g. “Your profile was updated successfully” 
warning     WARNING     A failure did not occur but may be imminent 
error       ERROR       An action was not successful or some other failure occurred 


##Adding a message

from django.contrib import messages
messages.add_message(request, messages.INFO, 'Hello world.')

messages.debug(request, '%s SQL statements were executed.' % count)
messages.info(request, 'Three credits remain in your account.')
messages.success(request, 'Profile details updated.')
messages.warning(request, 'Your account expires in three days.')
messages.error(request, 'Document deleted.')

##Failing silently when the message framework is disabled
messages.add_message(
    request, messages.SUCCESS, 'Profile details updated.',
    fail_silently=True,
)
messages.info(request, 'Hello world.', fail_silently=True)



##Displaying messages
{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}

#Outside of templates,  get_messages():
from django.contrib.messages import get_messages

storage = get_messages(request)
for message in storage:
    do_something_with_the_message(message)


    
    
    
    
    
    
    
    
    
    
    
    
    
    

###*** Django - chapter-2 

''' basic - book
        model layer 
        admin module               
        ListView as standard view 
        
Objectives- Basic Model 
Generic display views, Query Performance, Migration concepts
'''
###STEP 1: Then create a application, inside examplesite
$ cd examplesite
$ python manage.py startapp books   #note books is the name of app 

#check settings.py has below 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


###STEP2.0: MVC 
#Update books/models.py, books/view.py and html template file (books/templates/books) for  site in books

###STEP2.1: MVC- Model - the database tables
#REF: https://docs.djangoproject.com/en/2.0/ref/models/fields/
#books/models.py
# models.py (the database tables)
from django.db import models

class Book(models.Model):                   #two field  
	name = models.CharField(max_length=50)
	pub_date = models.DateField()
	
	def __str__(self):              # __str__ on Python 3, __unicode__ in Python2
		return self.name

###STEP2.2: MVC - Views - (the business logic)
#books/views.py
from django.shortcuts import render

# Create  views here.

from .models import Book

def latest_books(request):
	book_list = Book.objects.order_by('-pub_date')
	return render(request, 'books/latest_books.html', {'book_list': book_list})

    
###STEP2.3: MVC - view template 

#books/templates/books/latest_books.html : {% %} for template code, {{ }} for var name 
{% load static %}
<!DOCTYPE>
<html>
    <head>
        <title>DJANGO</title>
        <link rel="stylesheet" type="text/css" href="{% static 'books/style.css' %}" />
    </head>
    <body>
        {% for book in book_list %} 
            <h1>{{ book.name }}  {{ book.pub_date}}</h1>
        {% endfor %} 
    </body>
</html>

###STEP2.4: MVC - view -  Addition of Static files 

#books/static/books/style.css
body {
    background: white url("images/background.gif") no-repeat right bottom;
}

h1 {
    color: red;
}
#books/static/books/images/background.gif
#note the location because of href="{% static 'books/style.css' %}" in style.css

###STEP3.6: MVC - test  Adding testing of Models 
#books/tests.py
from django.test import TestCase
# Create  tests here.
import datetime
from django.test import Client
from books.models import Book

class BookTests(TestCase):

    def setUp(self):
        # django uses separate table test_books in DB  and removes after test
        # hence populate few data in that else test would fail
        Book.objects.create(name="first book", pub_date=datetime.date.today())
        Book.objects.create(name="first book 12", pub_date=datetime.date.today())
        self.c =  Client()

		
    def test_sample(self):
        """First test case"""
        response = self.c.get('http://127.0.0.1:8000/latest/')
        # we can call unittest methods
        self.assertRegexpMatches(response.content.decode('ascii'), "first book") #for py2, decode is not required
        

    def test_not_empty(self):
        """Second Test case"""
        book_list = Book.objects.order_by('-pub_date')
        # we can call unittest methods
        self.assertTrue(book_list)






###STEP4.1:Update examplesite/urls.py to include url to be handled

import books.views

urlpatterns = [
    url(r'latest/$', books.views.latest_books),
    #...
]


###STEP4.2: Modify INSTALLED_APPS in examplesite/settings.py to include books application
##Note order is significant , first means apps' template file would override all below's
INSTALLED_APPS = {
...
'books',
}

###STEP5.0: Activating models

#Notify django that models is changed 
#Must when you change model ***
$ python manage.py makemigrations books

#(creates migrations/0001_initial.py) and create migration code. 
$ cat books/migrations/0001_initial.py

###STEP5.1: Check the db creation command by  
#(0001 is parameter which denotes which migration point to display)

$ python manage.py sqlmigrate books 0001


#Note- check DB tablename, must be in lowercase. eg books_book , appName_modelName 
#If you would like to change DB table name use Meta options
#REF: https://docs.djangoproject.com/en/2.0/ref/models/options/
#eg: in models.py/Book class

class Book(models.Model):
	name = models.CharField(max_length=50)
	pub_date = models.DateField()
	class Meta:
		db_table = 'books'
		


###STEP 5.2:Create the Databse tables now
$ python manage.py migrate

#Check from SQL , note many auth_* and django_* tables are created along with books_book
$ python manage.py dbshell
show tables;		# for sqllite SELECT * FROM sqlite_master WHERE type='table';
DROP TABLE appname_modelname;
exit; 			# for sqlite, .exit

#DBShell for sqllite3 
$ python manage.py dbshell 

sqllite> .tables 
sqllite> .schema finance_stock


### STEP 5.3:Check everything is OK
$ python manage.py shell


from books.models import Book  

Book.objects.all() # []

# Create New
# for DateTimeField use  timezone.now() from django.utils import timezone
import datetime
b1 = Book(name="first book", pub_date=datetime.date.today())
# Save the object into the database. You have to call save() explicitly.
b1.save()

#Get object
#REF: https://docs.djangoproject.com/en/2.0/ref/models/querysets/
Book.objects.all()
Book.objects.filter(id=1)
Book.objects.filter(name__startswith='first')
Book.objects.filter(name__endswith='12') #[]





###STEP 6.1:Testing
# Django uses test DB , hence  populate test DB at first (during setUp phase)
#-v is verbose level 
$ python manage.py test -v 3  books

###STEP 6.2 : Run the server by
$ python manage.py runserver

#If below error
Error: [Errno 10013] An attempt was made to access a socket in a way forbidden b
#change port
python manage.py runserver 8080
#check  http://127.0.0.1:8000/latest





###STEP 6.2:AppConfig
#Django contains a registry of installed applications that stores configuration 
#and provides introspection. It also maintains a list of available models.

#This registry is simply called apps and it’s available in django.apps:

>>> from django.apps import apps
>>> apps.get_app_config('admin').verbose_name
'Admin'
#This file is created to help the user include any application configuration for the app
#REF: https://docs.djangoproject.com/en/2.0/ref/applications/




###STEP7.1: MVC - Admin module - you can create user, groups and books
1. check required settings in settings.py , 
   TEMPLATES::OPTIONS::context_processors , MIDDLEWARE_CLASSES and INSTALLED_APPS
2. create ModelAdmin and register, check examplesite\books\admin.py 
3. Hook to <<project>>\urls.py, by url(r'^admin/', admin.site.urls) (default), (note <Django-1.9, url(r'^admin/', include(admin.site.urls)) )

#file books\admin.py :
from django.contrib import admin

from books.models import Book       #note import is always from root, hence .\books\models.py


class BookAdmin(admin.ModelAdmin):
	fields = ['pub_date', 'name']  # reorder

#Now you can create Book instance via admin 
admin.site.register(Book, BookAdmin)  # register  models and ModelAdmin instances with instance of django.contrib.admin.sites.AdminSite created by django.contrib.admin.site 
                                      #Customize the AdminSite for custom behaviour 

#By default following would do if there is no customization of BookAdmin
admin.site.register(Book)

##Discovery of admin files
#When you put 'django.contrib.admin' in  INSTALLED_APPS setting, 
#Django automatically looks for an admin module in each application and imports it.

##ModelAdmin options
#Chek full list https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#modeladmin-options


#To override an admin template for a specific app, 
#copy and edit the template from the django/contrib/admin/templates/admin directory, 
#and save it to <<project>>\templates\ (DIRS in setting.py must be set to check this)
#Note  app must come before 'django.contrib.admin' in settings.INSTALLED_APPS



#Note you have to create superuser to use the admin module 
#Note: must create superuser 
#Create  superuser eg  admin/adminadminadmin
$ python manage.py createsuperuser 

#change passowrd
$ python manage.py changepassword <user_name>

#To give a normal user privileges, open a shell with python manage.py shell and try:
from django.contrib.auth.models import User
user = User.objects.get(username='normaluser')
user.is_superuser = True
user.save()

#Iterate users/superusers
from django.contrib.auth.models import User
User.objects.filter(is_superuser=True)

#then change password
usr = User.objects.get(username=' username')
usr.set_password('raw password')
usr.save()


#Then check at   http://127.0.0.1:8000/admin  (admin/adminadminadmin)
#Some Errors are displayed in DEBUG level , CHange it to INFO to suppress that (settings.py)
'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',   
            'propagate': True,
            },
            
#Add Books , delete and update 




###STEP7.2: Migration 
#REF: https://docs.djangoproject.com/en/2.0/topics/migrations/
migrate
    which is responsible for applying and unapplying migrations.
makemigrations
    which is responsible for creating new migrations based on the changes you have made to  models.
sqlmigrate
    which displays the SQL statements for a migration.
showmigrations
    which lists a project’s migrations and their status.


#Change model files and admin file to include email
#books/models.py 
class Book(models.Model):                   #two field  
    name = models.CharField(max_length=50)
    pub_date = models.DateField()	
    email = models.EmailField(null=True, blank=True)
    def __str__(self):             
        return self.name

#Note null is used here else migration would ask for values for older rows 
#which could be other option if this field is non-nullable 

#Avoid using null on string-based fields such as CharField and TextField because empty string values will always be stored as empty strings, not as NULL. 
#If a string-based field has null=True, that means it has two possible values for “no data”: NULL, and the empty string
#Note that blank is different than null. null is purely database-related, whereas blank is validation-related. 
#If a field has blank=True, form validation will allow entry of an empty value. 
#If a field has blank=False, the field will be required.


#Then execute 
$ python manage.py makemigrations books
$ python manage.py sqlmigrate books 0002
$ python manage.py migrate



###STEP 8: Usage of generic display view 

#for example ListView - Displays model.objects.all() (to change, update queryset=WITHQUERY)
#or DetailView for rendering one object of the Model
#REF: https://docs.djangoproject.com/en/2.0/ref/class-based-views/generic-display/
#check all attributes - https://ccbv.co.uk/projects/Django/2.0/django.views.generic.list/ListView/


##Class-based generic views - flattened index 
#All generic view derive from View and has TemplateMixin(attributes similar to TemplateView)
Simple generic views 
    View
    TemplateView
    RedirectView
Detail Views 
    DetailView
List Views 
    ListView
Editing views 
    FormView
    CreateView
    UpdateView
    DeleteView
Date-based views 
    ArchiveIndexView
    YearArchiveView
    MonthArchiveView
    WeekArchiveView
    DayArchiveView
    TodayArchiveView
    DateDetailView


##Each request served by a class-based view has an independent state;
##therefore, it is safe to store state variables on the instance (i.e., self.size = 3 is a thread-safe operation).

urlpatterns = [
    path('view/', MyView.as_view(size=42)), #calls MyView(size=42)
]


class django.views.generic.base.View
    All other class-based views inherit from this base class. 
    It isn’t strictly a generic view and thus can also be imported from django.views.
    Note View.as_view(**initargs) has populated below 
    initargs are keyword based initialization parameters of UserDefinedListViewClass 
    Inside class, can access below 
        self.request = request 
        self.args = args     #all positional args in the path
        self.kwargs = kwargs  #all keywords arg in the path
    Attributes
        http_method_names
            The list of HTTP method names that this view will accept.
            Calls same named method on the View, eg get(request, *args, **kwargs) for GET
            Default:  ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
       
    #Example views.py:
    from django.http import HttpResponse
    from django.views import View

    class MyView(View):
        def get(self, request, *args, **kwargs):
            return HttpResponse('Hello, World!')
            
    #Example urls.py:
    from django.urls import path

    from myapp.views import MyView

    urlpatterns = [
        path('mine/', MyView.as_view(), name='my-view'),
    ]

class django.views.generic.base.TemplateView
    Renders a given template, with the context containing parameters captured in the URL.
    Ancestors (MRO)
        •django.views.generic.base.TemplateResponseMixin
        •django.views.generic.base.ContextMixin
        •django.views.generic.base.View
    Attributes  and defined in 
        content_type = None     
        extra_context = None     
        http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']     
        response_class = <class 'django.template.response.TemplateResponse'>     
        template_engine = None     
        template_name = None    
    


##Example 
#Update views.py 
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.utils import timezone

from .models import Book

#Template file : ListView.template_name or by default , <<appName>>/templates/<<appName>>/<<modelName>>_list.html
#Containing a context containing a variable called 'object_list' that contains all the publisher objects. 
#While this view is executing, self.object_list will contain the list of objects 
class BookListView(ListView):
    model = Book
    template_name = "books/booklist.html"  #under <<appName>>/template
    #context_object_name = 'books'         #rename 'object_list'
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
        
#Use DetailView.get_object() is the method that retrieves the object 
#Note default template name is <<appName>>/templates/<<appName>>/<<modelName>>_detail.html
#in template, context variable name is 'object'
#Note if 'DetailView.get_object()' is not overridden, then URL must contain pk_keyword as determined by 'pk_url_kwarg = 'pk''
#eg  book/<int:pk>/, then DetailView would display that object 
class BookDetailView(DetailView):
    model = Book
    extra_context = {'now': datetime.date.today()}
    template_name = "books/book.html"
    #add another extra context 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_list'] = Book.objects.all()
        return context       
        
 
#urls.py     
import books.views
from django.urls import path


urlpatterns = [
    url(r'latest/$', books.views.latest_books),
    url(r'books/$', books.views.BookListView.as_view()),
    path('book/<int:pk>/', BookDetailView.as_view(), name='author-detail'),
]

#Lets use template inheritance 
#books/static/base.html 
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css" />
    <title>{% block title %}My amazing site{% endblock %}</title>
</head>

<body>
    <div id="sidebar">
        {% block sidebar %}
        <ul>            
            <li><a href="/latest/">Latest</a></li>
        </ul>
        {% endblock %}
    </div>

    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>

#books/template/books/booklist.html 
{% extends "base.html" %}

{% block title %}Books at {{ now }}{% endblock %}

{% block content %}
    <ul>
    {% for book in object_list %}
        <li>{{ book.pub_date|date }} - {{ book.name }}</li>
    {% empty %}
        <li>No articles yet.</li>
    {% endfor %}
    </ul>
{% endblock %}

#books/template/books/book.html 
{% extends "base.html" %}

{% block title %}Books at {{ now }}{% endblock %}

{% block content %}
    <ul>
        <li>{{ object.pub_date|date }} - {{ object.name }}</li>
    </ul>
{% endblock %}

#check
python manage.py runserver 8080
# with http://127.0.0.1:8000/books/




###Model - Few important concepts 
    
##Overriding predefined model methods
#Overridden model methods are not called on bulk operations        

#A classic use-case for overriding the built-in methods is 
#if you want something to happen whenever you save an object. 
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def save(self, *args, **kwargs):
        do_something()
        super().save(*args, **kwargs)  # Call the "real" save() method.
        do_something_else()

#You can also prevent saving:
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def save(self, *args, **kwargs):
        if self.name == "Yoko Ono's blog":
            return # Yoko shall never have her own blog!
        else:
            super().save(*args, **kwargs)  # Call the "real" save() method.



    
            
##Validating Models 
Model.full_clean(exclude=None, validate_unique=True)
    The optional exclude argument lets you provide a list of field names to exclude from validation
    All three steps are performed when Model.full_clean() is called 
        1.Validate the model fields - Model.clean_fields(exclude=None)
        2.Validate the model as a whole - Model.clean()
        3.Validate the field uniqueness - Model.validate_unique() 
    ModelForm.is_valid() will perform these validation steps for all the fields that are included on the form
    Note that full_clean() will not be called automatically when Model.save() is called 
    Call seperately 

    from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
    try:
        article.full_clean()
    except ValidationError as e:
        # Do something based on the errors contained in e.message_dict.
        # Display them to a user, or handle them programmatically.
        non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        pub_date_field_errors = e.message_dict["pub_date"]
        

Model.clean_fields(exclude=None)
    This method will validate all fields on  model
    You can’t raise validation errors in Model.clean() for fields that don’t appear in a model form 
    (a form may limit its fields using Meta.fields or Meta.exclude). 
    Instead override Model.clean_fields() as it receives the list of fields that are excluded from validation. 
    #Example 
        class Article(models.Model):
            ...
            def clean_fields(self, exclude=None):
                super().clean_fields(exclude=exclude)
                if self.status == 'draft' and self.pub_date is not None:
                    if exclude and 'status' in exclude:
                        raise ValidationError(
                            _('Draft entries may not have a publication date.')
                        )
                    else:
                        raise ValidationError({
                            'status': _(
                                'Set status to draft if there is not a '
                                'publication date.'
                             ),
                        })

       

 
Model.clean()
    This method should be used to provide custom model validation
    #Example 
        import datetime
        from django.core.exceptions import ValidationError
        from django.db import models
        from django.utils.translation import gettext_lazy as _

        class Article(models.Model):
            ...
            def clean(self):
                # Don't allow draft entries to have a pub_date.
                if self.status == 'draft' and self.pub_date is not None:
                    raise ValidationError(_('Draft entries may not have a publication date.'))
                # Set the pub_date for published items if it hasn't been set already.
                if self.status == 'published' and self.pub_date is None:
                    self.pub_date = datetime.date.today()
    ValidationError exception raised by Model.clean() was instantiated with a string, 
    so it will be stored in a special error dictionary key, NON_FIELD_ERRORS. 
    This key is used for errors that are tied to the entire model instead of to a specific field:
 
    To assign exceptions to a specific field, instantiate the ValidationError with a dictionary, 
    where the keys are the field names
    class Article(models.Model):
        ...
        def clean(self):
            # Don't allow draft entries to have a pub_date.
            if self.status == 'draft' and self.pub_date is not None:
                raise ValidationError({'pub_date': _('Draft entries may not have a publication date.')})
            ...
            #OR with multiple fields 
            raise ValidationError({
                'title': ValidationError(_('Missing title.'), code='required'),
                'pub_date': ValidationError(_('Invalid date.'), code='invalid'),
            })

                        
        
Field.validators
    A list of validators to run for this field
    #Example 
    from django.core.exceptions import ValidationError
    from django.utils.translation import gettext_lazy as _

    def validate_even(value):
        if value % 2 != 0:
            raise ValidationError(
                _('%(value)s is not an even number'),
                params={'value': value},
            )
    #usage 
    from django.db import models
    class MyModel(models.Model):
        even_field = models.IntegerField(validators=[validate_even])

    #Can be used with Form as well 
    from django import forms
    class MyForm(forms.Form):
        even_field = forms.IntegerField(validators=[validate_even])
    #Standard Validator ,django.core.validators , each has __call__(self, value), so can be used as instance
    class RegexValidator(regex=None, message=None, code=None, inverse_match=None, flags=0)
    class EmailValidator(message=None, code=None, whitelist=None)
    class URLValidator(schemes=None, regex=None, message=None, code=None)
    class MaxValueValidator(max_value, message=None)
        Raises a ValidationError with a code of 'max_value' if value is greater than max_value.
    class MinValueValidator(min_value, message=None)
        Raises a ValidationError with a code of 'min_value' if value is less than min_value.
    class MaxLengthValidator(max_length, message=None)
        Raises a ValidationError with a code of 'max_length' if the length of value is greater than max_length.
    class MinLengthValidator(min_length, message=None)
        Raises a ValidationError with a code of 'min_length' if the length of value is less than min_length.
    class DecimalValidator(max_digits, decimal_places)
    class FileExtensionValidator(allowed_extensions, message, code)
    class ProhibitNullCharactersValidator(message=None, code=None)

    

##List of Fields
#https://docs.djangoproject.com/en/2.0/ref/models/fields/
django.db.models.fields.Field(verbose_name=None, name=None, primary_key=False,
                 max_length=None, unique=False, blank=False, null=False,
                 db_index=False, rel=None, default=NOT_PROVIDED, editable=True,
                 serialize=True, unique_for_date=None, unique_for_month=None,
                 unique_for_year=None, choices=None, help_text='', db_column=None,
                 db_tablespace=None, auto_created=False, validators=(),
                 error_messages=None)

class BigIntegerField(**options)
class BinaryField(**options)
class BooleanField(**options)
class CharField(max_length=None, **options)
class DateField(auto_now=False, auto_now_add=False, **options)
class DateTimeField(auto_now=False, auto_now_add=False, **options)
class DecimalField(max_digits=None, decimal_places=None, **options)
class DurationField(**options)
class EmailField(max_length=254, **options)
  
class FilePathField(path=None, match=None, recursive=False, max_length=100, **options)
class FloatField(**options)
class GenericIPAddressField(protocol='both', unpack_ipv4=False, **options)
class IntegerField(**options)
class NullBooleanField(**options)
class PositiveIntegerField(**options)
class PositiveSmallIntegerField(**options)
class SlugField(max_length=50, **options)
class SmallIntegerField(**options)
class TextField(**options)
class TimeField(auto_now=False, auto_now_add=False, **options)
class URLField(max_length=200, **options)
class UUIDField(**options)

class ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, **options)
class FileField(upload_to=None, max_length=100, **options)


    
        
###*** Django - Chapter-3 
'''
ManytoOne , ManyToMany and Making Queries 
Objectives- Understanding Associations, Models, Queries
'''


###STEP 1: create a application, inside examplesite

$ python manage.py startapp baeapp 

#Update settings.INSTALLED_APPS to include 'baeapp'

#Update baeapp/models.py 
#Note *_set is renamed by attribute 'related_name' and reverse filter by 'related_query_name'


from django.db import models

class Blog(models.Model):                     #Many(Entry) to One(Blog), blog.entry_set and reverse filter= entry__*
    name = models.CharField(max_length=100)   #ForeignKey on Many side 
    tagline = models.TextField()   

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Author(models.Model):                     #Many(entry) to Many(Author), author.entry_set, reverse filter= entry__*
    name = models.CharField(max_length=200)     #ManyToManyField could be on any side 
    email = models.EmailField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Entry(models.Model):          
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)     #Many(Entry) to One(Blog), entry.blog, , reverse filter = blog__* 
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author) #Many(entry) to Many(Author), entry.authors, filter= author__*
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):              # __unicode__ on Python 2
        return self.headline
        
    class Meta:
            ordering = ('headline',)


##Many-to-one relationships
#Many - Entry, One - Blog, use django.db.models.ForeignKey(Blog) on Entry ie Many side 
#Many side table would have one foreign key, eg blog (default db_column = blog_id)
#hence One blog id can be  linked across many Entry rows 

#all Blog objects ,  Blog.objects. (has add, get, filter, all methods)
#('objects' is default manager, Blog._default_manager)

#filter from Blog to Entry(reverse filter), entry__ENTRYATTRIBUTES
#all entries of a Blog instance , b.entry_set. (this has add, get, filter, all methods)
#instance of below class has create, save, delete methods and field names as attributes 
class Blog(models.Model):
       .

#All Entry objects , Entry.objects. (this has add, get, filter, all methods)
#Entry instance has one blog, e.blog.  (this has add, get, filter, all methods)
#filter from Entry to Blog, blog__BLOGATTRIBUTES
# instance of below class has create, save, delete methods and field names as attributes
class Entry(models.Model):
       .


##Many-to-many relationships- use ManyToManyField on either of side (not both)
#Generally, ManyToManyField instances should go in the object that’s going to be edited on a form
#Django implements through one intermideate table , Entry.authors.through

#Many - Entry, Many - Author, use django.db.models.ManyToManyField(Author) on Entry ie any one side 


#all Author objects ,  Author.objects.  (this has add,  get, filter, all methods)
#all entries of a Author instance , a.entry_set.  (this has add, get, filter, all methods)
#filter from Author to Entry(reverse filter), entry__
#Note entry_set is created by Django, nothing is explicitly mentioned
#instance of below class has create, save, delete methods and field names as attributes
class Author(models.Model): 
       
            
            
#All Entry objects , entry.objects.  (this has add,  get, filter, all methods)
#authors of an Entry, e.authors (from field name) (this has add, get, filter, all methods)
#filter from Entry to Author, author__



###STEP 2:Create the Database tables now
$ python manage.py makemigrations baeapp
$ python manage.py migrate


### STEP 3:Query 
#https://docs.djangoproject.com/en/1.10/ref/models/querysets
$ python manage.py shell


from baeapp.models import Blog, Author, Entry 


#To display SQL queries, use Debugtoolbar , http://django-debug-toolbar.readthedocs.io/en/stable/installation.html
#And then python manage.py  debugsqlshell, , then each ORM call that results in a database query will be output in the shell.
#OR use , connection.queries includes all SQL statements – INSERTs, UPDATES, SELECTs, etc. Each time your app hits the database, the query will be recorded.

>>> from django.db import connection
>>> connection.queries
[{'sql': 'SELECT polls_polls.id, polls_polls.question, polls_polls.pub_date FROM polls_polls',
'time': '0.002'}]

#For multiple databases, you can use the same interface on each member of the connections dictionary:
>>> from django.db import connections
>>> connections['my_db_alias'].queries

#to clear the query list manually at any point in your functions, just call reset_queries(), like this:
from django.db import reset_queries
reset_queries()


###When QuerySets(lazy) are evaluated
1.Iteration. 
    for e in Entry.objects.all():
        print(e.headline)

2.Slicing
3.Pickling/Caching
4.repr()
5.len()
6.list()
    entry_list = list(Entry.objects.all())
7.bool()
    if Entry.objects.filter(headline="Test"):
       print("There is at least one Entry with the headline Test")

###QuerySet reference 
#https://docs.djangoproject.com/en/2.0/ref/models/querysets/


        
        
        
###Creating and Saving 
b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
b.save()        #performs an INSERT SQL statement ,Django doesn’t hit the database until you explicitly call save().

#Entry - Many 
import datetime
e = Entry(blog=b, headline='Any headline', body_text='body', pub_date=datetime.date.today(),
            mod_date=datetime.date.today(), n_comments=2, n_pingbacks=3, rating=10)
e.save()

###Updating changes to objects
b.name = 'Cheddar Talk'
b.save()

###Updating ForeignKey 
entry = Entry.objects.get(pk=1)
cheese_blog = Blog.objects.get(name="Cheddar Talk")
entry.blog = cheese_blog
entry.save()
entry       #from __str__ , <Entry: Any headline>

###Updating a ManyToManyField – use the add() method on the field to add a record to the relation. 
joe = Author.objects.create(name="Joe")
entry.authors.add(joe)


#To add multiple records to a ManyToManyField in one go, 
john = Author.objects.create(name="John")
paul = Author.objects.create(name="Paul")
george = Author.objects.create(name="George")
ringo = Author.objects.create(name="Ringo")
entry.authors.add(john, paul, george, ringo)
entry.save()

###Retrieving objects
#construct a QuerySet via a Manager on  model class
#It can have zero, one or many filters. 
#In SQL terms, a QuerySet equates to a SELECT statement, and a filter is a limiting clause such as WHERE or LIMIT.
#Each model has at least one Manager, and it’s called 'objects' by default

Blog.objects  #<django.db.models.manager.Manager object at 0x03CE1610>

#Retrieving all objects
all_entries = Entry.objects.all()



### Field Lookup - Retrieving specific objects with filters
#REF: https://docs.djangoproject.com/en/2.0/ref/models/querysets/#field-lookups
filter(**kwargs)
exclude(**kwargs)
get(**kwargs)

#**kwargs should be in the format of Field lookups 
#Basic lookups keyword arguments take the form 
field__lookuptype=value 

#For reverse relation, by default, related_query_name is reverse Model name in lowercase 
#or defined on ManyToManyField or ForeignKey
<<related_query_name>>__field__lookuptype=value 

#lookuptype
exact,iexact,contains,icontains,in
gt,gte,lt,lte,startswith,istartswith,endswith,iendswith,range
,date,year,month,day,week,week_day,quarter,time,hour,minute,second,isnull,regex,iregex

#Example 
Entry.objects.filter(pub_date__lte='2006-01-01')
Entry.objects.filter(blog_id=4)
Entry.objects.get(headline__exact="Cat bites dog")
Blog.objects.get(id__exact=14)  # Explicit form
Blog.objects.get(id=14)         # __exact is implied
Blog.objects.get(name__iexact="beatles blog")
Entry.objects.get(headline__contains='Lennon')
Entry.objects.get(headline__icontains='Lennon')
Entry.objects.filter(id__in=[1, 3, 4])

#can use objects 
inner_qs = Blog.objects.filter(name__contains='Cheddar')
entries = Entry.objects.filter(blog__in=inner_qs)  #reverse filter 

#__in with g from values() or values_list(), must have one field in the result. 
#For example, this will work (filtering on the blog names):
inner_qs = Blog.objects.filter(name__contains='Ch').values('name')
entries = Entry.objects.filter(blog__name__in=inner_qs)

#This example will raise an exception, since the inner query is trying to extract two field values, 
#where only one is expected:
# Bad code! Will raise a TypeError.
inner_qs = Blog.objects.filter(name__contains='Ch').values('name', 'id')
entries = Entry.objects.filter(blog__name__in=inner_qs) #Error 


##gt, gte, lt, lte 
Entry.objects.filter(id__gt=4)

## startswith, istartswith, endswith, iendswith (i means ignore case)
Entry.objects.filter(headline__startswith='Will')

##Range test (inclusive).
import datetime
start_date = datetime.date(2005, 1, 1)
end_date = datetime.date(2005, 3, 31)
Entry.objects.filter(pub_date__range=(start_date, end_date))

##for date(DateField) and datetime fields, date, year, month, day, week_day(day of week from 1 (Sunday) to 7 (Saturday).)
#For datetime( DateTimeField) , hour, minute, second
Entry.objects.filter(pub_date__date=datetime.date(2005, 1, 1))
Entry.objects.filter(pub_date__date__gt=datetime.date(2005, 1, 1))
Entry.objects.filter(pub_date__year=2005)
Entry.objects.filter(pub_date__year__gte=2005)
Entry.objects.filter(pub_date__month=12)
Entry.objects.filter(pub_date__month__gte=6)


##isnull
#Takes either True or False, which correspond to SQL queries of IS NULL and IS NOT NULL, 

Entry.objects.filter(pub_date__isnull=True)

##regex
Entry.objects.get(title__regex=r'^(An?|The) +')
Entry.objects.get(title__iregex=r'^(an?|the) +')




##Lookups that span relationships
#To span a relationship, use the field name of related field separated by double underscores
#This spanning can be as deep as you’d like.
>>> Entry.objects.filter(blog__name='Beatles Blog')  #filed name= blog with __ and blog field 

#To refer to a “reverse” relationship, use the lowercase name of the model(or related_query_name given during creation)
>>> Blog.objects.filter(entry__headline__contains='Lennon')

#If you are filtering across multiple relationships 
#and one of the intermediate models doesn’t have a value that meets the filter condition, 
#Django will treat it as if there is an empty (all values are NULL), but valid, object there. 

##Note the difference 
#Following will return Blog objects that have an empty name on the author 
#and also those which have an empty author on the entry. 
Blog.objects.filter(entry__authors__name__isnull=True)
#If you don’t want those latter objects, you could write:
Blog.objects.filter(entry__authors__isnull=False, entry__authors__name__isnull=True)


##Note the difference 
#To select all blogs that contain entries with both “Lennon” in the headline 
#and that were published in 2008 (the same entry satisfying both conditions)
Blog.objects.filter(entry__headline__contains='Lennon', entry__pub_date__year=2008)


#To select all blogs that contain an entry with “Lennon” in the headline 
#as well as an entry that was published in 2008
Blog.objects.filter(entry__headline__contains='Lennon').filter(entry__pub_date__year=2008)


#the following query would exclude blogs that contain both entries 
#with “Lennon” in the headline and entries published in 2008:
#However, unlike the behavior when using filter(), this will not limit blogs based on entries that satisfy both conditions.
Blog.objects.exclude(
    entry__headline__contains='Lennon',
    entry__pub_date__year=2008,
)


#to select all blogs that do not contain entries published with “Lennon” 
#that were published in 2008, you need to make two queries:

Blog.objects.exclude(
    entry__in=Entry.objects.filter(
        headline__contains='Lennon',
        pub_date__year=2008,
    ),
)



##Chaining filters
#The result of refining a QuerySet is itself a QuerySet, 
>>> Entry.objects.filter(
     headline__startswith='What'
  ).exclude(
      pub_date__gte=datetime.date.today()
  ).filter(
      pub_date__gte=datetime(2005, 1, 30)
  )

##Filtered QuerySets are unique
#Each time you refine a QuerySet, 
#you get a brand-new QuerySet that is in no way bound to the previous QuerySet. 
#Each refinement creates a separate and distinct QuerySet that can be stored, used and reused.

#These three QuerySets are separate.
q1 = Entry.objects.filter(headline__startswith="What")
q2 = q1.exclude(pub_date__gte=datetime.date.today())
q3 = q1.filter(pub_date__gte=datetime.date.today())



##QuerySets are lazy
#QuerySets are lazy – the act of creating a QuerySet doesn’t involve any database activity. 
#Django won’t actually run the query until the QuerySet is evaluated. 


q = Entry.objects.filter(headline__startswith="Any")
q = q.filter(pub_date__lte=datetime.date.today())
q = q.exclude(body_text__icontains="food")
print(q)   #now it is evaluated 

##QuerySets are iterators 
>>> for e in q:
    print(e.blog)

Cheddar Talk
>>> list(q)
[<Entry: Any headline>]
>>> [e.blog for e in q]
[<Blog: Cheddar Talk>]
>>> entry in q
True

##Retrieving a single object with get()
#filter() will always give you a QuerySet, even if only a single object matches the query - in this case, it will be a QuerySet containing a single element.
#If you know there is only one object that matches  query
one_entry = Entry.objects.get(pk=1)

##Limiting QuerySets
Entry.objects.all()[:5]

#This returns the sixth through tenth objects (OFFSET 5 LIMIT 5):
Entry.objects.all()[5:10]

#Negative indexing (i.e. Entry.objects.all()[-1]) is not supported.

#Generally, slicing a QuerySet returns a new QuerySet – it doesn’t evaluate the query. 
#An exception is if you use the “step” parameter of Python slice syntax. 
Entry.objects.all()[:10:2]

## Performance considerations
#To retrieve a single object rather than a list (e.g. SELECT foo FROM bar LIMIT 1), 
#use a simple index instead of a slice  
Entry.objects.order_by('headline')[0]





##Filters can reference fields on the model
#Instances of F() act as a reference to a model field within a query. 
#These references can then be used in query filters to compare the values of two different fields on the same model instance.

from django.db.models import F
Entry.objects.filter(n_comments__gt=F('n_pingbacks'))

#Django supports the use of addition, subtraction, multiplication, division, modulo, and power arithmetic with F() objects, 
#both with constants and with other F() objects. 

Entry.objects.filter(n_comments__gt=F('n_pingbacks') * 2)
Entry.objects.filter(rating__lt=F('n_comments') + F('n_pingbacks'))


#to span relationships in an F() object. 
Entry.objects.filter(authors__name=F('blog__name'))


#For date and date/time fields, you can add or subtract a timedelta object.
from datetime import timedelta
Entry.objects.filter(mod_date__gt=F('pub_date') + timedelta(days=3))


#The F() objects support bitwise operations by .bitand() and .bitor(), for example:
>>> F('somefield').bitand(16)



##The pk lookup shortcut
#stands for'primary key'

#these three statements are equivalent:
Blog.objects.get(id__exact=14) # Explicit form
Blog.objects.get(id=14) # __exact is implied
Blog.objects.get(pk=14) # pk implies id__exact

# Get blogs entries with id 1, 4 and 7
>>> Blog.objects.filter(pk__in=[1,4,7])

# Get all blog entries with id > 14
>>> Blog.objects.filter(pk__gt=14)


#these three statements are equivalent:
Entry.objects.filter(blog__id__exact=3) # Explicit form
Entry.objects.filter(blog__id=3)        # __exact is implied
Entry.objects.filter(blog__pk=3)        # __pk implies __id__exact



##Escaping percent signs and underscores in LIKE statements
#iexact, contains, icontains, startswith, istartswith, endswith and iendswith
#will automatically escape – the percent sign and the underscore. 
Entry.objects.filter(headline__contains='%')    #SELECT   WHERE headline LIKE '%\%%';



##Caching and QuerySets  
#Each QuerySet contains a cache to minimize database access

## Performance considerations
#For example, the following will create two QuerySets, evaluate them, and throw them away
#That means the same database query will be executed twice
print([e.headline for e in Entry.objects.all()])
print([e.pub_date for e in Entry.objects.all()])

#To avoid this problem, simply save the QuerySet and reuse it:
queryset = Entry.objects.all()
print([p.headline for p in queryset]) # Evaluate the query set.
print([p.pub_date for p in queryset]) # Re-use the cache from the evaluation.



## Performance considerations
#limiting the queryset using an array slice or an index will not populate the cache.
queryset = Entry.objects.all()
print(queryset[5]) # Queries the database
print(queryset[5]) # Queries the database again

#if the entire queryset has already been evaluated, the cache will be checked instead:
>>> queryset = Entry.objects.all()
>>> [entry for entry in queryset] # Queries the database
>>> print(queryset[5]) # Uses cache
>>> print(queryset[5]) # Uses cache


#Here are some examples of other actions that will result in the entire queryset being evaluated and therefore populate the cache:
[entry for entry in queryset]
bool(queryset)
entry in queryset
list(queryset)


##order_by(*fields)
#By default, results returned by a QuerySet are ordered by the ordering tuple given by the ordering option in the model’s Meta. 
#or
Entry.objects.filter(pub_date__year=2005).order_by('-pub_date', 'headline')
#will be ordered by pub_date descending, then by headline ascending. 

#To order by a field in a different model
Entry.objects.order_by('blog__name', 'headline')


#If you try to order by a field that is a relation to another model, 
#Django will use the default ordering on the related model, or order by the related model’s primary key if there is no Meta.ordering specified. 
Entry.objects.order_by('blog')
# is identical to:
Entry.objects.order_by('blog__id')


## Performance considerations
# No Join as by default blog_id is the DB column name 
Entry.objects.order_by('blog_id')
# Join
Entry.objects.order_by('blog__id')


#You can also order by query expressions by calling asc() or desc() on the expression:
from django.db.models.functions import Coalesce
#Coalesce :Accepts a list of at least two field names or expressions 
#and returns the first non-null value 
Entry.objects.order_by(Coalesce('summary', 'headline').desc())


from django.db.models.functions import Lower
Entry.objects.order_by(Lower('headline').desc())


##reverse()
#Use the reverse() method to reverse the order in which a queryset’s elements are returned. Calling reverse() a second time restores the ordering back to the normal direction.
my_queryset.reverse()[:5]



##distinct(*fields)
Author.objects.distinct()
Entry.objects.order_by('pub_date').distinct('pub_date') 
Entry.objects.order_by('blog').distinct('blog')
Entry.objects.order_by('author', 'pub_date').distinct('author', 'pub_date')
Entry.objects.order_by('blog__name', 'mod_date').distinct('blog__name', 'mod_date')
Entry.objects.order_by('author', 'pub_date').distinct('author')
 

##values(*fields)
#Returns a QuerySet that returns dictionaries, rather than model instances, 

# This list contains a Blog object.
Blog.objects.filter(name__startswith='Beatles')
<QuerySet [<Blog: Beatles Blog>]>

# This list contains a dictionary.
Blog.objects.filter(name__startswith='Beatles').values()
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>

#projection
Blog.objects.values()
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>
Blog.objects.values('id', 'name')
<QuerySet [{'id': 1, 'name': 'Beatles Blog'}]>


#•If you have a field called foo that is a ForeignKey, 
#the default values() call will return a dictionary key called foo_id, 

Entry.objects.values()      #<QuerySet [{'blog_id': 1, 'headline': 'First Entry',  },  ]>
Entry.objects.values('blog') #<QuerySet [{'blog': 1},  ]>
Entry.objects.values('blog_id') #<QuerySet [{'blog_id': 1},  ]>


#•When using values() together with distinct(), 
#be aware that ordering can affect the results. 

#note that you can call filter(), order_by(), etc. after the values() call, 
#that means that these two calls are identical:
Blog.objects.values().order_by('id')
Blog.objects.order_by('id').values()

#you can also refer to fields on related models 
#with reverse relations through OneToOneField, ForeignKey and ManyToManyField attributes:
Blog.objects.values('name', 'entry__headline')



##values_list(*fields, flat=False)
#This is similar to values() except that instead of returning dictionaries, 
#it returns tuples when iterated over. 

Entry.objects.values_list('id', 'headline')  #[(1, 'First entry'),  ]

#If you only pass in a single field, you can also pass in the flat parameter. 
Entry.objects.values_list('id').order_by('id')  #[(1,), (2,), (3,),  ]
Entry.objects.values_list('id', flat=True).order_by('id') #[1, 2, 3,  ]

Entry.objects.values_list('headline', flat=True).get(pk=1) #'First entry'


## Performance considerations
#values() and values_list() are both intended as optimizations for a specific use case: 
#retrieving a subset of data without the overhead of creating a model instance. 

#Authors with multiple entries appear multiple times and authors 
#without any entries have None for the entry headline.

Author.objects.values_list('name', 'entry__headline')
[('Noam Chomsky', 'Impressions of Gaza'),
 ('George Orwell', 'Why Socialists Do Not Believe in Fun'),
 ('George Orwell', 'In Defence of English Cooking'),
 ('Don Quixote', None)]



##dates(field, kind, order='ASC')
•"year" returns a list of all distinct year values for the field.
•"month" returns a list of all distinct year/month values for the field.
•"day" returns a list of all distinct year/month/day values for the field.
##datetimes(field_name, kind, order='ASC', tzinfo=None)
#kind should be either "year", "month", "day", "hour", "minute" or "second". 
Entry.objects.dates('pub_date', 'year')
Entry.objects.dates('pub_date', 'month')
Entry.objects.filter(headline__contains='Lennon').dates('pub_date', 'day')





## Performance considerations
select_related(*fields)
#Returns a QuerySet that will “follow” foreign-key relationships, 
#selecting additional related-object data when it executes its query. 

# Hits the database.
e = Entry.objects.get(id=5)
# Hits the database again to get the related Blog object.
b = e.blog

#And here’s select_related lookup:
# Hits the database.
e = Entry.objects.select_related('blog').get(id=5)

# Doesn't hit the database, because e.blog has been prepopulated
# in the previous query.
b = e.blog


#Example 
#The order of filter() and select_related() chaining isn’t important.
from django.utils import timezone

# Find all the blogs with entries scheduled to be published in the future.
blogs = set()

for e in Entry.objects.filter(pub_date__gt=timezone.now()).select_related('blog'):
    # Without select_related(), this would make a database query for each
    # loop iteration in order to fetch the related blog for each entry.
    blogs.add(e.blog)


## Performance considerations
prefetch_related(*lookups)
#Returns a QuerySet that will automatically retrieve, in a single batch, 
#related objects for each of the specified lookups.

#select_related works by creating an SQL join 
#select_related gets the related objects in the same database query. 
#select_related is limited to single-valued relationships - foreign key and one-to-one.

#prefetch_related, on the other hand, does a separate lookup for each relationship, 
#and does the ‘joining’ in Python. Hence no limitation like select_related 
#This allows it to prefetch many-to-many and many-to-one objects, 
Entry.objects.all()     #["Hawaiian (ham, pineapple)", "Seafood (prawns, smoked salmon)" 
Entry.objects.all().prefetch_related('authors')






##Complex lookups with Q objects
#Q objects can be combined using the & and | operators
##Q objects can be negated using the ~ operator
#Each lookup function that takes keyword-arguments (e.g. filter(), exclude(), get())
#can also be passed one or more Q objects as positional (not-named) arguments. 
#this Q object encapsulates a single LIKE query:

from django.db.models import Q
Q(question__startswith='What')

Q(question__startswith='Who') | Q(question__startswith='What')
#WHERE question LIKE 'Who%' OR question LIKE 'What%'

Q(question__startswith='Who') | ~Q(pub_date__year=2005)

#If you provide multiple Q object arguments to a lookup function, 
#the arguments will be “AND”ed together
Poll.objects.get(
    Q(question__startswith='Who'),
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
)

#roughly translates into the SQL:
SELECT * from polls WHERE question LIKE 'Who%'
    AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')


#Lookup functions can mix the use of Q objects and keyword arguments. 
#All arguments provided to a lookup function (be they keyword arguments or Q objects) are “AND”ed together. 
#However, if a Q object is provided, it must precede the definition of any keyword arguments. 
Poll.objects.get(
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),
    question__startswith='Who',
)


#would be a valid query, equivalent to the previous example; but:
# INVALID QUERY
Poll.objects.get(
    question__startswith='Who',
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
)




##Comparing objects
#To compare two model instances
some_entry == other_entry
some_entry.id == other_entry.id

#Comparisons will always use the primary key
some_obj == other_obj
some_obj.name == other_obj.name



##Deleting objects
#This method immediately deletes the object and returns the number of objects deleted and a dictionary with the number of deletions per object type
e.delete()  #(1, {'weblog.Entry': 1})
Entry.objects.filter(pub_date__year=2005).delete()  #(5, {'webapp.Entry': 5})
#by default it emulates the behavior of the SQL constraint ON DELETE CASCADE 
#– in other words, any objects which had foreign keys pointing at the object to be deleted will be deleted along with it


b = Blog.objects.get(pk=1)
# This will delete the Blog and all of its Entry objects.
b.delete()

#If you do want to delete all the objects, then you have to explicitly request a complete query set:
Entry.objects.all().delete()


##Copying model instances
blog = Blog(name='My blog', tagline='Blogging is easy')
blog.save() # blog.pk == 1

blog.pk = None
blog.save() # blog.pk == 2






        
##Aggregation functions
#SQLite can’t handle aggregation on date/time fields out of the box. 
#Django currently emulates these features using a text field. 
#Attempts to use aggregation on date/time fields in SQLite will raise NotImplementedError.
#Aggregation functions return None when used with an empty QuerySet.

#All of the aggregate functions, like Sum() and Count(), inherit from Aggregate().

class Aggregate(expression, output_field=None, filter=None, **extra)
    expression
        A string that references a field on the model, or a query expression.
    output_field
        An optional argument that represents the model field of the return value
        When combining multiple field types, Django can only determine the output_field if all fields are of the same type. 
        Otherwise, you must provide the output_field yourself.
    filter
        An optional Q object that’s used to filter the rows that are aggregated.

##List of Aggregate Functions 
class Avg(expression, output_field=FloatField(), filter=None, **extra)
class Count(expression, distinct=False, filter=None, **extra)
class Max(expression, output_field=None, filter=None, **extra)
class Min(expression, output_field=None, filter=None, **extra)
class StdDev(expression, sample=False, filter=None, **extra)
class Sum(expression, output_field=None, filter=None, **extra)
class Variance(expression, sample=False, filter=None, **extra)
 
 
##Aggregate Example 
from django.db import models
class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
class Publisher(models.Model):
    name = models.CharField(max_length=300)
    num_awards = models.IntegerField()
class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()
class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)
    registered_users = models.PositiveIntegerField()
    
    
##Aggregate - Generating aggregates over a QuerySet
#to generate summary values over an entire QuerySet. 
#For example, say you wanted to calculate the average price of all books available for sale. 
Book.objects.all()
from django.db.models import Avg
>>> Book.objects.all().aggregate(Avg('price'))
{'price__avg': 34.35}
#The all() is redundant in this example, so this could be simplified to:
>>> Book.objects.aggregate(Avg('price'))
{'price__avg': 34.35}

#aggregate() is a terminal clause for a QuerySet that, when invoked, returns a dictionary of name-value pairs. 
#The name is an identifier for the aggregate value; the value is the computed aggregate. 
#The name is automatically generated from the name of the field and the aggregate function. 
#To manually specify a name for the aggregate value, 
>>> Book.objects.aggregate(average_price=Avg('price'))
{'average_price': 34.35}

#To generate more than one aggregate,
>>> from django.db.models import Avg, Max, Min
>>> Book.objects.aggregate(Avg('price'), Max('price'), Min('price'))
{'price__avg': 34.35, 'price__max': Decimal('81.20'), 'price__min': Decimal('12.99')}


##Aggregate - Generating aggregates for each item in a QuerySet - using the annotate() clause
#To generate an independent summary for each object in a QuerySet. 
#For example, if you are retrieving a list of books, you may want to know how many authors contributed to each book. 

#When an annotate() clause is specified, each object in the QuerySet will be annotated with the specified values.
#The syntax for these annotations is identical to that used for the aggregate() clause.

#Unlike aggregate(), annotate() is not a terminal clause. 
#The output of the annotate() clause is a QuerySet; 
#this QuerySet can be modified using any other QuerySet operation, including filter(), order_by(), 


#For example, to annotate books with the number of authors:
# Build an annotated queryset
>>> from django.db.models import Count
>>> q = Book.objects.annotate(Count('authors'))
# Interrogate the first object in the queryset
>>> q[0]
<Book: The Definitive Guide to Django>
>>> q[0].authors__count
2
# Interrogate the second object in the queryset
>>> q[1]
<Book: Practical Django Projects>
>>> q[1].authors__count
1

#To override this default name by providing an alias 
>>> q = Book.objects.annotate(num_authors=Count('authors'))
>>> q[0].num_authors
2
>>> q[1].num_authors
1


##Aggregate - Following relationships backwards
#traversing “reverse” relationships. 
#The lowercase name of related models and double-underscores are used here too.

#For example,  for all publishers, annotated with their respective total book stock counters 
#(note how we use 'book' to specify the Publisher -> Book reverse foreign key hop):
>>> from django.db.models import Avg, Count, Min, Sum
>>> Publisher.objects.annotate(Count('book'))
#(Every Publisher in the resulting QuerySet will have an extra attribute called book__count.)

#for the oldest book of any of those managed by every publisher:
>>> Publisher.objects.aggregate(oldest_pubdate=Min('book__pubdate'))
#(The resulting dictionary will have a key called 'oldest_pubdate'. 
#If no such alias were specified, it would be the rather long 'book__pubdate__min'.)


#For example, for every author, annotated with the total number of pages considering all the books the author has (co-)authored 
#(note how we use 'book' to specify the Author -> Book reverse many-to-many hop):
>>> Author.objects.annotate(total_pages=Sum('book__pages'))
#(Every Author in the resulting QuerySet will have an extra attribute called total_pages. 
#If no such alias were specified, it would be the rather long book__pages__sum.)

#Or ask for the average rating of all the books written by author(s) we have on file:
>>> Author.objects.aggregate(average_rating=Avg('book__rating'))
#(The resulting dictionary will have a key called 'average_rating'. 
#If no such alias were specified, it would be the rather long 'book__rating__avg'.)           
       
       
##Aggregate - Filtering on annotations
#Annotated values can also be filtered. 

#For example, to generate a list of books that have more than one author
>>> Book.objects.annotate(num_authors=Count('authors')).filter(num_authors__gt=1)

#If you need two annotations with two separate filters you can use the filter argument with any aggregate. 
#For example, to generate a list of authors with a count of highly rated books:
#Each Author in the result set will have the num_books and highly_rated_books attributes.
>>> highly_rated = Count('books', filter=Q(books__rating__gte=7))
>>> Author.objects.annotate(num_books=Count('books'), highly_rated_books=highly_rated)



##Conditional Expressions
#Conditional expressions let you use if … elif … else logic within filters, annotations, aggregations, and updates. 
#A conditional expression evaluates a series of conditions for each row of a table 
#and returns the matching result expression. 

#Conditional expressions can also be combined and nested like other expressions.

from django.db import models
class Client(models.Model):
    REGULAR = 'R'
    GOLD = 'G'
    PLATINUM = 'P'
    ACCOUNT_TYPE_CHOICES = (
        (REGULAR, 'Regular'),
        (GOLD, 'Gold'),
        (PLATINUM, 'Platinum'),
    )
    name = models.CharField(max_length=50)
    registered_on = models.DateField()
    account_type = models.CharField(
        max_length=1,
        choices=ACCOUNT_TYPE_CHOICES,
        default=REGULAR,
    )

class When(condition=None, then=None, **lookups)
    A When() object is used to encapsulate a condition and its result for use in the conditional expression. 
    Using a When() object is similar to using the filter() method. 
    The condition can be specified using field lookups or Q objects. 
    The result is provided using the then keyword.
    Some examples:
        >>> from django.db.models import F, Q, When
        >>> # String arguments refer to fields; the following two examples are equivalent:
        >>> When(account_type=Client.GOLD, then='name')
        >>> When(account_type=Client.GOLD, then=F('name'))
        >>> # You can use field lookups in the condition
        >>> from datetime import date
        >>> When(registered_on__gt=date(2014, 1, 1),
                 registered_on__lt=date(2015, 1, 1),
                 then='account_type')
        >>> # Complex conditions can be created using Q objects
        >>> When(Q(name__startswith="John") | Q(name__startswith="Paul"),
                 then='name')
    Keep in mind that each of these values can be an expression.
    Since the then keyword argument is reserved for the result of the When(), 
    there is a potential conflict if a Model has a field named then. 
    This can be resolved in two ways:
        >>> When(then__exact=0, then=1)
        >>> When(Q(then=0), then=1)

class Case(*cases, **extra)
    A Case() expression is like the if … elif … else statement in Python. 
    Each condition in the provided When() objects is evaluated in order, until one evaluates to a truthful value. 
    The result expression from the matching When() object is returned.
    A simple example:
        >>>
        >>> from datetime import date, timedelta
        >>> from django.db.models import Case, CharField, Value, When
        >>> Client.objects.create(
                name='Jane Doe',
                account_type=Client.REGULAR,
                registered_on=date.today() - timedelta(days=36))
        >>> Client.objects.create(
                name='James Smith',
                account_type=Client.GOLD,
                registered_on=date.today() - timedelta(days=5))
        >>> Client.objects.create(
                name='Jack Black',
                account_type=Client.PLATINUM,
                registered_on=date.today() - timedelta(days=10 * 365))
        >>> # Get the discount for each Client based on the account type
        >>> Client.objects.annotate(
                discount=Case(
                    When(account_type=Client.GOLD, then=Value('5%')),
                    When(account_type=Client.PLATINUM, then=Value('10%')),
                    default=Value('0%'),
                    output_field=CharField(),
                ),
            ).values_list('name', 'discount')
        <QuerySet [('Jane Doe', '0%'), ('James Smith', '5%'), ('Jack Black', '10%')]>
    Case() accepts any number of When() objects as individual arguments. 
    Other options are provided using keyword arguments. 
    If none of the conditions evaluate to TRUE, then the expression given with the default keyword argument is returned. 
    If a default argument isn’t provided, None is used.
    If we wanted to change our previous query to get the discount based on how long the Client has been with us, 
    we could do so using lookups:
        >>> a_month_ago = date.today() - timedelta(days=30)
        >>> a_year_ago = date.today() - timedelta(days=365)
        >>> # Get the discount for each Client based on the registration date
        >>> Client.objects.annotate(
                discount=Case(
                    When(registered_on__lte=a_year_ago, then=Value('10%')),
                    When(registered_on__lte=a_month_ago, then=Value('5%')),
                    default=Value('0%'),
                    output_field=CharField(),
                )
            ).values_list('name', 'discount')
        <QuerySet [('Jane Doe', '5%'), ('James Smith', '0%'), ('Jack Black', '10%')]>
    Remember that the conditions are evaluated in order, 
    so in the above example we get the correct result even though the second condition matches both Jane Doe and Jack Black. 
    This works just like an if … elif … else statement in Python.
    Case() also works in a filter() clause. 
    For example, to find gold clients that registered more than a month ago and platinum clients that registered more than a year ago:
        >>> a_month_ago = date.today() - timedelta(days=30)
        >>> a_year_ago = date.today() - timedelta(days=365)
        >>> Client.objects.filter(
                registered_on__lte=Case(
                    When(account_type=Client.GOLD, then=a_month_ago),
                    When(account_type=Client.PLATINUM, then=a_year_ago),
                ),
            ).values_list('name', 'account_type')
        <QuerySet [('Jack Black', 'P')]>       
       
##Conditional update
#Example -  to change the account_type for our clients to match their registration dates. 
>>> a_month_ago = date.today() - timedelta(days=30)
>>> a_year_ago = date.today() - timedelta(days=365)
>>> # Update the account_type for each Client from the registration date
>>> Client.objects.update(
        account_type=Case(
            When(registered_on__lte=a_year_ago,
                 then=Value(Client.PLATINUM)),
            When(registered_on__lte=a_month_ago,
                 then=Value(Client.GOLD)),
            default=Value(Client.REGULAR)
        ),
    )
>>> Client.objects.values_list('name', 'account_type')
<QuerySet [('Jane Doe', 'G'), ('James Smith', 'R'), ('Jack Black', 'P')]>

##Conditional aggregation
#Example - to find out how many clients there are for each account_type? 
#We can use the filter argument of aggregate functions to achieve this:

>>> # Create some more Clients first so we can have something to count
>>> Client.objects.create(
        name='Jean Grey',
        account_type=Client.REGULAR,
        registered_on=date.today())
>>> Client.objects.create(
        name='James Bond',
        account_type=Client.PLATINUM,
        registered_on=date.today())
>>> Client.objects.create(
        name='Jane Porter',
        account_type=Client.PLATINUM,
        registered_on=date.today())
>>> # Get counts for each value of account_type
>>> from django.db.models import Count
>>> Client.objects.aggregate(
        regular=Count('pk', filter=Q(account_type=Client.REGULAR)),
        gold=Count('pk', filter=Q(account_type=Client.GOLD)),
        platinum=Count('pk', filter=Q(account_type=Client.PLATINUM)),
    )
{'regular': 2, 'gold': 1, 'platinum': 3}







  

##Func() expressions
#https://docs.djangoproject.com/en/2.1/ref/models/expressions/#func-expressions

#Func() expressions are the base type of all expressions that involve database functions like COALESCE and LOWER, 
#or aggregates like SUM. 

#They can be used directly:
from django.db.models import F, Func
queryset.annotate(field_lower=Func(F('field'), function='LOWER'))

#or they can be used to build a library of database functions:
class Lower(Func):
    function = 'LOWER'
queryset.annotate(field_lower=Lower('field'))

#result in a queryset where each model is annotated with an extra attribute field_lower produced, 



##Window functions
#Window functions provide a way to apply functions on partitions. 
#Unlike a normal aggregation function which computes a final result for each set defined by the group by, 
#window functions operate on frames and partitions, and compute the result for each row.

#Among Django’s built-in database backends, MySQL 8.0.2+, PostgreSQL, and Oracle support window expressions.
#For example, to annotate each movie with the average rating for the movies 
#by the same studio in the same genre and release year:

from django.db.models import Avg, F, Window
from django.db.models.functions import ExtractYear
Movie.objects.annotate(
    avg_rating=Window(
        expression=Avg('rating'),
        partition_by=[F('studio'), F('genre')],
        order_by=ExtractYear('released').asc(),
    ),
)













###*** Django - Chapter-4
'''
Forms     
    Show ModelForm handling     
    Objectives - Handiing forms, Form class and Edit  views
Seccurity features
'''

###Note there are three ways to create a form to update Database 
1. Use view eg CreateView, DeleteView, UpdateView 
2. Or manually code all these updates after inheriting from ModelForm
3. Or Use admin module
#Both forms are demonstrated here 
#Note above are used to create a Form based on Model 
#for Simply creating html form, inherit from Form (infact ModelForm inherits Form)

###STEP 1: Then create a application, inside examplesite

$ python manage.py startapp modelform 


#modelform/urls.py 
from django.conf.urls import url, include 

from . import views


urlpatterns = [        
    url(r'^book-create/',  views.create_book, name="modelex-book-create"),  
    url(r'^author-create/',  views.AuthorCreate.as_view(), name="modelex-author-create"),
    url(r'^books/',  views.latest_books , name="modelex-books-list"),
    url(r'^authors/',  views.latest_authors , name="modelex-authors-list"),
]

#modelform/models.py 
from django.db import models
TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
)


class Author(models.Model):    #.book_set, reverse relation = book__
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)
    def __str__(self):              # __unicode__ on Python 2
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)  # .authors, forward relation = author__
    def __str__(self):              # __unicode__ on Python 2
        return self.name
 

    
  
#modelform/forms.py 
from django.forms import ModelForm
from .models import *
from django import forms

'''
#Not required as we have used CreateView which directly creates a form from model 
class AuthorForm(ModelForm):    
    class Meta:
        model = Author
        fields = ['name', 'title', 'birth_date']
        widgets = {
            'name': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
''' 

class BookForm(ModelForm):
    def clean(self):      
        '''additional validation'''
        cleaned_data = super(BookForm, self).clean()
        name = cleaned_data.get("name")      #it is a dict    
        if len(name) < 2:            
                raise forms.ValidationError("Name Length Error")
    class Meta:
        model = Book
        fields = ['name', 'authors']
        widgets = {
            'name': forms.Textarea(attrs={'cols': 80, 'rows':2}), #can update  class, id comes from string of variable name  
        }
        

#modelform/views.py 

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from  django.urls import *


from .forms import BookForm
from .models import *

'''
def create_author(request):   

    # if this is a POST request we need to process the form data
    if request.method == 'POST':      
        # create a form instance and populate it with data from the request:
        form = AuthorForm(request.POST)
        log.debug("POST " + str(request.POST))
        # check whether it's valid:
        if form.is_valid():            
            form.save(commit=True)           
            return HttpResponseRedirect(reverse('modelex-authors-list'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AuthorForm()
    return render(request, 'create.html', {'form': form, 'create_string': 'modelex-author-create'})
'''   

#check attributes https://ccbv.co.uk/projects/Django/2.0/django.views.generic.edit/CreateView/
#default value: template_name_suffix =  '_form' , 
#default template_name to be '<<app>>/templates/<<app>>/<<model>>_form.html'.
from django.views.generic.edit import CreateView
from django.utils import timezone
class AuthorCreate(CreateView):
    model = Author   
    success_url = reverse_lazy('modelex-authors-list')  # _lazy is must else ImproperlyConfigured error 
    fields = ['name', 'title', 'birth_date']    
    #Put any extra context here 
    def get_context_data(self, **kwargs):
        ''' Any context var for form '''
        context = super(AuthorCreate, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #Do some addl activity, super class saves it in database 
        return super(AuthorCreate, self).form_valid(form)

       
#Instead of hardcoding below, we can use general editng view as given above 
#REF: https://docs.djangoproject.com/en/2.0/ref/class-based-views/generic-editing/
#       
def create_book(request):  
    # if this is a POST request we need to process the form data
    if request.method == 'POST':      
        # create a form instance and populate it with data from the request:
        form = BookForm(request.POST)        
        # check whether it's valid:
        if form.is_valid():        #calls form validation as well as model validation    
            #now form.cleaned_data (a dict of all fields) are available 
            #form.data is uncleaned ones
            form.save(commit=True)           
            return HttpResponseRedirect(reverse('modelex-books-list'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = BookForm()
    return render(request, 'create.html', {'form': form, 'create_string': 'modelex-book-create'})
  
    
def latest_books(request):    
    book_list = Book.objects.prefetch_related('authors').all()
    return render(request, 'list.html', {'book_list': book_list})

def latest_authors(request):   
    a_list = Author.objects.prefetch_related('book_set').all()
    return render(request, 'list_a.html', {'a_list': a_list})
    


#modelform/templates/list.html 
{% load staticfiles %}
<!DOCTYPE>
<html>
    <head>
        <title>Books</title>       
    </head>
    <body>
        {% for book in book_list %} 
            <h1>{{ book.name }}  </h1>
            {% for author in book.authors.all %} 
              <h2>  {{ author.name}}</h2>
            {% endfor %} 
        {% endfor %} 
    </body>
</html>

#modelform/templates/list_a.html  
{% load staticfiles %}
<!DOCTYPE>
<html>
    <head>
        <title>Authors</title>       
    </head>
    <body>
        {% for author in a_list %} 
            <h1>{{ author.name }}  </h1>
            {% for book in author.book_set.all %} 
              <h2>  {{ book.name}}</h2>
            {% endfor %} 
        {% endfor %} 
    </body>
</html>

#modelform/templates/create.html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Contact form</title>	
        <style type="text/css">
            table.gridtable {
                font-family: verdana,arial,sans-serif;
                font-size:11px;
                color:#333333;
                border-width: 1px;
                border-color: #666666;
                border-collapse: collapse;
            }
            table.gridtable th {
                border-width: 1px;
                padding: 8px;
                border-style: solid;
                border-color: #666666;
                background-color: #dedede;
            }
            table.gridtable td {
                border-width: 1px;
                padding: 8px;
                border-style: solid;
                border-color: #666666;
                background-color: #ffffff;
            }
        </style>   
	</head>

	<body>
        <form action="{% url create_string %}" method="post">
            {% csrf_token %}
            <table class="gridtable">
                {{ form.as_table }}
            </table >
            <input type="submit" value="Submit" />
        </form>
	</body>

</html>  

#modelform/templates/modelform/author_form.html 
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Author Create form</title>	
        <style type="text/css">
            table.gridtable {
                font-family: verdana,arial,sans-serif;
                font-size:11px;
                color:#333333;
                border-width: 1px;
                border-color: #666666;
                border-collapse: collapse;
            }
            table.gridtable th {
                border-width: 1px;
                padding: 8px;
                border-style: solid;
                border-color: #666666;
                background-color: #dedede;
            }
            table.gridtable td {
                border-width: 1px;
                padding: 8px;
                border-style: solid;
                border-color: #666666;
                background-color: #ffffff;
            }
        </style>   
	</head>

	<body>
        <form action="" method="post">
            {% csrf_token %}
            <table class="gridtable">
                {{ form.as_table }}
            </table >
            <input type="submit" value="Save" />
        </form>
	</body>

</html> 




###STEP 2:Create the Database tables now
$ python manage.py makemigrations modelform
$ python manage.py migrate

#examplesite/urls.py 
urlpatterns = [   
    url(r'^modelform/' , include('modelform.urls')),
]

#modelform/admin.py 

# Register your models here.
from .models import Author, Book 

admin.site.register(Author)
admin.site.register(Book)

#Create  superuser eg  admin/adminadminadmin
$ python manage.py createsuperuser 


#check
python manage.py runserver 8080
# http://127.0.0.1:8080/modelform/author-create
# http://127.0.0.1:8080/modelform/book-create
# http://127.0.0.1:8080/modelform/books
# http://127.0.0.1:8080/modelform/authors










###Quick Django Forms 
#REF:  https://docs.djangoproject.com/en/2.0/ref/forms/fields/

#fields 
class CharField(max_length=None, min_length=None, strip=True, empty_value='', **kwargs)
class IntegerField(max_value=None, min_value=None, **kwargs)
class FloatField(max_value=None, min_value=None, **kwargs) #Super IntegerField
class DecimalField(max_value=None, min_value=None, max_digits=None, decimal_places=None, **kwargs)#Super IntegerField
class BaseTemporalField(input_formats=None, **kwargs)
class DateField(BaseTemporalField)
class TimeField(BaseTemporalField)
class DateTimeField(BaseTemporalField)
class DurationField(Field)
class RegexField(max_length=None, min_length=None, strip=True, empty_value='',regex, **kwargs)#Super CharField
class EmailField(CharField)
class FileField(max_length=None, allow_empty_file=False, **kwargs)
class ImageField(FileField)
class URLField(CharField)
class BooleanField(Field):
class NullBooleanField(BooleanField)
class ChoiceField(choices=(), **kwargs)
class TypedChoiceField(coerce=lambda val: val, empty_value='', **kwargs)#Super ChoiceField
class MultipleChoiceField(ChoiceField):
class TypedMultipleChoiceField(coerce=lambda val: val, **kwargs): #Super MultipleChoiceField
class ComboField(fields, **kwargs)
class MultiValueField(fields, *, require_all_fields=True, **kwargs)
class FilePathField(path, *, match=None, recursive=False, allow_files=True,allow_folders=False, **kwargs)
class SplitDateTimeField(input_date_formats=None, input_time_formats=None, **kwargs) #Super MultiValueField
class GenericIPAddressField(protocol='both', unpack_ipv4=False, **kwargs) #Super CharField
class SlugField(allow_unicode=False, **kwargs):
class UUIDField(CharField)#Super CharField       
        
        
        
#Create a form from forms.XyzField, XyzField takes many parameters
#further attributes can be given by 'attrs' and Each field has one default Widget to display in html form
#Example 
from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100, attrs={'class': 'myClass'})

#is equivalent to below , note no <form> tags, or a submit button
#Note automatic id and 'name' is created from variable name 
    <label for="your_name">Your name: </label>
    <input id="your_name" type="text" name="your_name" maxlength="100" required />


##Bound and unbound form instances - Field.is_bound attribute
• An unbound form has no data associated with it. 
  When rendered to the user, it will be empty or will contain default values.
  #Example 
  form = BookForm() #unbound 
• A bound form has submitted data , (eg from POST data)
  and hence can be used to tell if that data is valid. 
  If an invalid bound form is rendered, it can include inline error messages 
  #example 
  form = BookForm(request.POST)       #create bound form 

  
  
##Form rendering options - other than {{form}}
#provide the surrounding <table> or <ul>
•{{ form.as_table }}    will render them as table cells wrapped in <tr> tags
•{{ form.as_p }}        will render them wrapped in <p> tags
•{{ form.as_ul }}       will render them wrapped in <li> tags


##Rendering fields manually
#Each field is available as an attribute of the form using {{ form.name_of_field }}
#label ID is available as {{ form.name_of_field.id_for_label }}
#Any error in field is available as {{ form.name_of_field.errors }}
#{{ form.non_field_errors }} contains all nonfield form error 

#Example with four fields with var name = subject, message, sender, cc_myself 
{{ form.non_field_errors }}
<div class="fieldWrapper">
    {{ form.subject.errors }}
    <label for="{{ form.subject.id_for_label }}">Email subject:</label>
    {{ form.subject }}
</div>
<div class="fieldWrapper">
    {{ form.message.errors }}
    <label for="{{ form.message.id_for_label }}">Your message:</label>
    {{ form.message }}
</div>
<div class="fieldWrapper">
    {{ form.sender.errors }}
    <label for="{{ form.sender.id_for_label }}">Your email address:</label>
    {{ form.sender }}
</div>
<div class="fieldWrapper">
    {{ form.cc_myself.errors }}
    <label for="{{ form.cc_myself.id_for_label }}">CC yourself?</label>
    {{ form.cc_myself }}
</div>


#Or  <label> elements can also be generated using the label_tag()
<div class="fieldWrapper">
    {{ form.subject.errors }}
    {{ form.subject.label_tag }}
    {{ form.subject }}
</div>


#Rendering form error messages
#{{ form.sender.errors }} would look as below 
<ul class="errorlist">
    <li>Sender is required.</li>
</ul>

#Or iterate manually
{% if form.sender.errors %}
    <ol>
    {% for error in form.sender.errors %}
        <li><strong>{{ error|escape }}</strong></li>
    {% endfor %}
    </ol>
{% endif %}


#{{ form.non_field_errors }} would look like:
<ul class="errorlist nonfield">
    <li>Generic validation error</li>
</ul>


##Looping over the form’s fields - {% for %} loop
{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
        {% if field.help_text %}
        <p class="help">{{ field.help_text|safe }}</p>
        {% endif %}
    </div>
{% endfor %}


##Useful attributes on {{ field }} 
{{ field.label }}           The label of the field, e.g. forms.CharField(label='Your name')
{{ field.label_tag }}       The field’s label wrapped in the appropriate HTML <label> tag. 

{{ field.id_for_label }}    The ID that will be used for this field (id_email , <label for="id_email">Email address:</label>). 
{{ field.value }}           The value of the field. e.g someone@example.com.
{{ field.html_name }}       The name of the field that will be used in the input element’s name field. 
                            This takes the form prefix into account, if it has been set.
{{ field.help_text }}       Any help text that has been associated with the field.
{{ field.errors }}          Outputs a <ul class="errorlist"> containing any validation errors corresponding to this field. You can customize the presentation of the errors with a {% for error in field.errors %} loop. In this case, each object in the loop is a simple string containing the error message.
{{field.as_hidden }}        Outputs as hidden 
{{ field.is_hidden }}       This attribute is True if the form field is a hidden field and False otherwise.
                             {% if field.is_hidden %}
                               {# Do something special #}
                             {% endif %}
{{ field.field }}           The Field instance from the form class that this BoundField wraps. 
                            You can use it to access Field attributes, 
                            e.g. {{ char_field.field.max_length }}.


##Note to create hidden input 
forms.CharField(widget = forms.HiddenInput(), required = False)
#or make 
show_hidden_initial=True

#For normal form 
class MyForm(forms.Form):
    slug = forms.CharField(widget=forms.HiddenInput())

class Myform(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Myform, self).__init__(*args, **kwargs)
        self.fields['slug'].widget = forms.HiddenInput()    
#or 
class MyModelForm(forms.ModelForm):
    class Meta:
        model = TagStatus
        fields = ('slug', 'ext')
        widgets = {'slug': forms.HiddenInput()}



                        
                            
##Looping over hidden and visible fields- hidden_fields() and visible_fields(). 
{# Include the hidden fields #}
{% for hidden in form.hidden_fields %}
{{ hidden }}
{% endfor %}
{# Include the visible fields #}
{% for field in form.visible_fields %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
    </div>
{% endfor %}




##Forms - Using validators   
#Django’s form (and model) fields support use of simple utility functions and classes known as validators. 
#A validator is  a callable object or function that takes a value and  returns nothing if the value is valid 
#or raises a ValidationError if not.
from django.core import validators
from django.forms import CharField

class SlugField(CharField):
    default_validators = [validators.validate_slug]


slug = forms.SlugField()
#is equivalent to:
slug = forms.CharField(validators=[validators.validate_slug])

#Userdefined 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )

#usage 
from django.db import models

class MyModel(models.Model):
    even_field = models.IntegerField(validators=[validate_even])

from django import forms

class MyForm(forms.Form):
    even_field = forms.IntegerField(validators=[validate_even])



#Standard Validator ,django.core.validators , each has __call__(self, value), so can be used as instance
class RegexValidator(regex=None, message=None, code=None, inverse_match=None, flags=0)
    message   
        The error message used by ValidationError if validation fails. Defaults to "Enter a valid value".
    code   
        The error code used by ValidationError if validation fails. Defaults to "invalid".
    inverse_match   
        The match mode for regex. Defaults to False.
    flags   
        The flags used when compiling the regular expression string regex. If regex is a pre-compiled regular expression, and flags is overridden, TypeError is raised. Defaults to 0.
class EmailValidator(message=None, code=None, whitelist=None)
class URLValidator(schemes=None, regex=None, message=None, code=None)
class MaxValueValidator(max_value, message=None)
    Raises a ValidationError with a code of 'max_value' if value is greater than max_value.
class MinValueValidator(min_value, message=None)
    Raises a ValidationError with a code of 'min_value' if value is less than min_value.
class MaxLengthValidator(max_length, message=None)
    Raises a ValidationError with a code of 'max_length' if the length of value is greater than max_length.
class MinLengthValidator(min_length, message=None)
    Raises a ValidationError with a code of 'min_length' if the length of value is less than min_length.
class DecimalValidator(max_digits, decimal_places)
class FileExtensionValidator(allowed_extensions, message, code)
class ProhibitNullCharactersValidator(message=None, code=None)
#Methods 
validate_email   
    An EmailValidator instance without any customizations.
validate_slug   
    A RegexValidator instance that ensures a value consists of only letters, numbers, underscores or hyphens.
validate_unicode_slug   
    A RegexValidator instance that ensures a value consists of only Unicode letters, numbers, underscores, or hyphens.
validate_ipv4_address      
    A RegexValidator instance that ensures a value looks like an IPv4 address.
validate_ipv6_address      
    Uses django.utils.ipv6 to check the validity of an IPv6 address.
validate_ipv46_address      
    Uses both validate_ipv4_address and validate_ipv6_address to ensure a value is either a valid IPv4 or IPv6 address.
validate_comma_separated_integer_list   
    A RegexValidator instance that ensures a value is a comma-separated list of integers.
int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)      
    Returns a RegexValidator instance that ensures a string consists of integers separated by sep. It allows negative integers when allow_negative is True.
validate_image_file_extension   
    Uses Pillow to ensure that value.name (value is a File) has a valid image extension.



           
           
###ModelForm - form created directly from model fields 

#Example 
from django.db import models
from django.forms import ModelForm

TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
)

class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'title', 'birth_date']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']

#Usage 
>>> form = AuthorForm()

# Note forms.Form has 'data' variable, where as ModelForm has 'instance' variable 
#Otherwise, ModelForm has all varaibles of forms.Form eg .errors, .cleaned_data, etc 
>>> author = Author.objects.get(pk=1)
>>> form = AuthorForm(instance=author)

#Based on above AuthorForm, BookForm, Django created below autogenerated forms 

from django import forms

class AuthorForm(forms.Form):
    name = forms.CharField(max_length=100)
    title = forms.CharField(
        max_length=3,
        widget=forms.Select(choices=TITLE_CHOICES),
    )
    birth_date = forms.DateField(required=False)

class BookForm(forms.Form):
    name = forms.CharField(max_length=100)
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())


##Model field,models.       Form field, forms.
AutoField                   Not represented in the form 
BigAutoField                Not represented in the form 
BigIntegerField             IntegerField with min_value set to -9223372036854775808 and max_value set to 9223372036854775807. 
BooleanField                BooleanField 
CharField                   CharField with max_length set to the model field’s max_length and empty_value set to None if null=True. 
DateField                   DateField 
DateTimeField               DateTimeField 
DecimalField                DecimalField 
EmailField                  EmailField 
FileField                   FileField 
FilePathField               FilePathField 
FloatField                  FloatField 
ForeignKey                  ModelChoiceField 
ImageField                  ImageField 
IntegerField                IntegerField 
IPAddressField              IPAddressField 
GenericIPAddressField       GenericIPAddressField 
ManyToManyField             ModelMultipleChoiceField 
NullBooleanField            NullBooleanField 
PositiveIntegerField        IntegerField 
PositiveSmallIntegerField   IntegerField 
SlugField                   SlugField 
SmallIntegerField           IntegerField 
TextField                   CharField with widget=forms.Textarea 
TimeField                   TimeField 
URLField                    URLField 

#Note ForeignKey and ManyToManyField model field types are special cases:
1.ForeignKey is represented by django.forms.ModelChoiceField, 
  which is a ChoiceField whose choices are a model QuerySet.
2.ManyToManyField is represented by django.forms.ModelMultipleChoiceField, 
  which is a MultipleChoiceField whose choices are a model QuerySet.

#In addition, each generated form field has attributes set as follows:
1.If the model field has blank=True, then required=False on the form field. Otherwise, required=True.
2.The form field’s label is set to the verbose_name of the model field, with the first character capitalized.
3.The form field’s help_text is set to the help_text of the model field.
4.If the model field has choices set, then the form field’s widget will be set to Select, 
  with choices coming from the model field’s choices. 
  The choices will normally include the blank choice which is selected by default. 
  If the field is required, this forces the user to make a selection. 
  The blank choice will not be included if the model field has blank=False and an explicit default value (the default value will be initially selected instead).
     
        
        
##Validation on a ModelForm
#There are two main steps involved in validating a ModelForm
#form.is_valid() would call below methods and then form.cleaned_data dict is available 
1.Validating the form
  Triggered by form.is_valid() or accessing form.errors 
  Does form level validation , calls below methods just like model validation 
    Form.clean_fields(exclude=None)
        calls each field.clean()
    Form.clean()
        Override this to handle any custom validation 
2.Validating the model instance
  Once step1 is done, Django calls Model.Model.full_clean(exclude=None, validate_unique=True)
  This method calls sequentially and raises a ValidationError 
  that has a message_dict attribute containing errors from all three stages.
    Model.clean_fields(exclude=None)
        This method will validate all fields on your model
        Calls each field's 
            Field.clean(value, model_instance)
                """Convert the value's type and run validation. Validation errors
                from to_python() and validate() are propagated. Return the correct
                value if no error is raised.
                """
                value = self.to_python(value)
                self.validate(value, model_instance)
                self.run_validators(value)
                return value
    Model.clean()
        This method should be used to provide custom model validation, 
        and to modify attributes if required 
    Model.validate_unique(exclude=None)
        This method is similar to clean_fields(), 
        but validates all uniqueness constraints on model instead of individual field values
        
3.Note: Error messages defined at the form field level(django.forms.Field.error_messages) 
  or at the form Meta level always take precedence over the error messages defined at the model field level(django.db.models.Field.error_messages)
  Error messages defined on model fields are only used when the ValidationError is raised 
  during the model validation step and no corresponding error messages are defined at the form level.
  To override the error messages from NON_FIELD_ERRORS raised by model validation 
  by adding the NON_FIELD_ERRORS key to the error_messages dictionary of the ModelForm’s inner Meta class:
    from django.core.exceptions import NON_FIELD_ERRORS
    from django.forms import ModelForm

    class ArticleForm(ModelForm):
        class Meta:
            error_messages = {
                NON_FIELD_ERRORS: {
                    'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
                }
            }



  
##ModelForm - ModelForm.save() 
#ModelForm works exactly the same way as any other forms form. 
#For example, the is_valid() method is used to check for validity, 
#the is_multipart() method is used to determine whether a form requires multipart file upload 
#(and hence whether request.FILES must be passed to the form), 

#Difference of ModelForm.save(commit=True) compared to Form.save()
#This method creates and saves a database object from the data bound to the form. 
#Note that if the form hasn’t been validated, calling save() would check form.errors, if False=, raises ValidationError 
#A subclass of ModelForm can accept an existing model instance as the keyword argument 'instance'; 
#if this is supplied, save() will update that instance.
#If it’s not supplied, save() will create a new instance of the specified model:


from myapp.models import Article
from myapp.forms import ArticleForm

# Create a form instance from POST data.
f = ArticleForm(request.POST)

# Save a new Article object from the form's data.
>>> new_article = f.save()

# Create a form to edit an existing Article, but use
# POST data to populate the form.
a = Article.objects.get(pk=1)
f = ArticleForm(request.POST, instance=a)
f.save()



###Form handling with class-based views
#takes Form class while creating 
#REF: https://docs.djangoproject.com/en/2.0/ref/class-based-views/generic-editing/

#Reference of class based Views     
#Check attributes - https://ccbv.co.uk/projects/Django/2.0/django.views.generic.edit/FormView/

#By default , template name is <<app_name>>/templates/<<app_name>>/<<model>>_<<template_name_suffix>>.html 
#or value given in 'template_name' 
#In template , access if single object by 'object' or list of object by 'object_list'
#Populate more context by overriding 'get_context_data(...)' with calling super inside that 
#or populating 'extra_context' by a dict of context objects 
#Customize query by overriding 'get_queryset(...)' or by defining 'queryset'

#Date based views use paginator exactly like ListView, use page_obj as Paginator object and object_list/date_list for queryset 

Editing views 
   FormView
   CreateView
   UpdateView
   DeleteView

Date-based views
   ArchiveIndexView
   YearArchiveView
   MonthArchiveView
   WeekArchiveView
   DayArchiveView
   TodayArchiveView
   DateDetailView


class django.views.generic.edit.FormView   
    A view that displays a form. On error, redisplays the form with validation errors; 
    on success, redirects to a new URL, given by success_url
    Ancestors (MRO)
        •django.views.generic.base.TemplateResponseMixin
        •django.views.generic.edit.BaseFormView
        •django.views.generic.edit.FormMixin
        •django.views.generic.edit.ProcessFormView
        •django.views.generic.base.View
    Attributes  Defined in
        content_type = None   TemplateResponseMixin  
        extra_context = None   ContextMixin  
        form_class = None   FormMixin  
        http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']   View  
        initial = {}   FormMixin  
        prefix = None   FormMixin  
        response_class = <class 'django.template.response.TemplateResponse'>   TemplateResponseMixin  
        success_url = None   FormMixin  
        template_engine = None   TemplateResponseMixin  
        template_name = None   TemplateResponseMixin  
    #Various Data 
    View creation extra init params 
        Use     def as_view(cls, **initkwargs)
        initkwargs is key=value keyword arg and are available as self.key=value 
    Request Data 
        self.request
    context data 
        by default from def get_context_data(self, **kwargs)
            kwargs['form'] = self.get_form()
            kwargs['view'] = self
            kwargs.update(self.extra_context)
    Form creation extra init params 
        Override def get_form_kwargs(self)
        default is given below 
        def get_form_kwargs(self):
            """Return the keyword arguments for instantiating the form."""
            kwargs = {
                'initial': self.get_initial(),
                'prefix': self.get_prefix(),
            }
            if self.request.method in ('POST', 'PUT'):
                kwargs.update({
                    'data': self.request.POST,
                    'files': self.request.FILES,
                })
            return kwargs
    Extra work if form is valid or form is invalid 
        override below     
            def form_invalid(self, form):
                """If the form is invalid, render the invalid form."""
                return self.render_to_response(self.get_context_data(form=form))
            def form_valid(self, form):
                """If the form is valid, redirect to the supplied URL."""
                return HttpResponseRedirect(self.get_success_url())
        These are called in POST method 
        def post(self, request, *args, **kwargs):
            """
            Handle POST requests: instantiate a form instance with the passed
            POST variables and then check if it's valid.
            """
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
     


#Form processing generally has 3 paths:
1.Initial GET (blank or prepopulated form)
2.POST with invalid data (typically redisplay form with errors)
3.POST with valid data (process the data and typically redirect)

#forms.py

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass


#Check attributes - https://ccbv.co.uk/projects/Django/2.0/django.views.generic.edit/FormView/
#FormView inherits TemplateResponseMixin so template_name can be used here.
#The default implementation for form_valid() simply redirects to the success_url.
#views.py
from myapp.forms import ContactForm
from django.views.generic.edit import FormView

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
        
#Example myapp/contact.html:
<form method="post">{% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Send message" />
</form>



##Model forms 
CreateView
    Creating new instance of model 
DeleteView
    Deleting an existing instance, either int:pk in URL or get_object() is required 
UpdateView
    Deleting an existing instance, either int:pk in URL or get_object() is required 
#Check attributes - https://ccbv.co.uk/projects/Django/2.0/django.views.generic.edit/FormView/
#These generic views will automatically create a ModelForm
1.If the model attribute is given, that model class will be used.
2.If get_object() returns an object, the class of that object and that instance will be used further 
3.If a queryset is given, the model for that queryset will be used.
4.If URL has int:pk field, that pk is taken as the object 
4.Modelform views provide a form_valid(self, form) implementation that saves the model automatically. 
  Override this if any custom work is needed 
  Inside this function, access model object from 'form.instance'
5.No need to provide a success_url for CreateView or UpdateView 
  they will use get_absolute_url() on the model object if available.
6.To use a custom ModelForm (for instance to add extra validation) set form_class on view.
  and specify the model
7.These views inherit SingleObjectTemplateResponseMixin which uses template_name_suffix to construct the template_name based on the model.
  For Example, 
    CreateView and UpdateView use myapp/author_form.html
    DeleteView uses myapp/author_confirm_delete.html  
#models.py  
from django.db import models
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})

#views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from myapp.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['name']

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list') #use reverse_lazy() here, not just reverse() as the urls are not loaded when the file is imported
#urls.py
from django.urls import path
from myapp.views import AuthorCreate, AuthorDelete, AuthorUpdate

urlpatterns = [
    # ...
    path('author/add/', AuthorCreate.as_view(), name='author-add'),
    path('author/<int:pk>/', AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', AuthorDelete.as_view(), name='author-delete'),
]

##Models and request.user   
#To track the user that created an object using a CreateView, use a custom ModelForm to do this. 
#First, add the foreign key relation to the model:
#models.py

from django.contrib.auth.models import User
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # ...

#don’t include created_by in the list of fields to edit, and override form_valid() to add the user:
#views.py

from django.views.generic.edit import CreateView
from myapp.models import Author

#@login_required() is generally required to restrict this usages 
class AuthorCreate(CreateView):
    model = Author
    fields = ['name']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

  
  
  
  
  
    
###*** Django -chapter-5 
'''
    Django authetication
    how to handle signup form and handle users 
    upload a file 
    download a file 
    send a mail 
'''

###STEP 1: Then create a application, inside examplesite

$ python manage.py startapp advanced 

#examplesite/urls.py 
urlpatterns = [
   #...
    url(r'^advanced/' , include('advanced.urls')), 
]


###STEP 2: Sending mail 
#Turn on less secure APPs
# https://www.google.com/settings/security/lesssecureapps
#Or use OAuth separately 
#http://stackoverflow.com/questions/11445523/python-smtplib-is-sending-mail-via-gmail-using-oauth2-possible
#https://developers.google.com/api-client-library/python/guide/aaa_oauth

django.core.mail.send_mail(subject, message, from_email, recipient_list, fail_silently=False, 
        auth_user=None, auth_password=None, connection=None, html_message=None)

django.core.mail.send_mass_mail(datatuple, fail_silently=False, auth_user=None, auth_password=None, connection=None)[source]¶
    send_mass_mail() is intended to handle mass emailing.
    datatuple is a tuple in which each element is in this format:
        (subject, message, from_email, recipient_list)
    The return value will be the number of successfully delivered messages.

django.core.mail.mail_admins(subject, message, fail_silently=False, connection=None, html_message=None)[source]¶
    django.core.mail.mail_admins() is a shortcut for sending an email to the site admins, 
    as defined in the ADMINS setting.
    mail_admins() prefixes the subject with the value of the EMAIL_SUBJECT_PREFIX setting, 
    which is "[Django] " by default.
    The “From:” header of the email will be the value of the SERVER_EMAIL setting.
    If html_message is provided, the resulting email will be a multipart/alternative email with message as the text/plain content type and html_message as the text/html content type.
django.core.mail.mail_managers(subject, message, fail_silently=False, connection=None, html_message=None)[source]¶
    django.core.mail.mail_managers() is just like mail_admins(), 
    except it sends an email to the site managers, as defined in the MANAGERS setting.


#examplesite/settings.py 
#for gmail server 
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#for console output 
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ndas1971@gmail.com'
EMAIL_HOST_PASSWORD = 'abczxy'  #give correct password
EMAIL_USE_TLS = True

#advanced/urls.py 
from . import views
urlpatterns = [        
    url(r'^contact/',  views.contact, name="contact"),  
    url(r'^thanks/',  views.thanks, name='thanks'),   
    ]
    
#advanced/forms.py 
from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    
    
#advanced/views.py 
from django.shortcuts import render
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


from .forms import *

#This can be simplified via FormView
def contact(request):    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':        
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:            
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['ndas1971@gmail.com']
            if cc_myself:
                recipients.append(sender)            
            send_mail(subject, message, sender, recipients )
            return HttpResponseRedirect(reverse('thanks'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
    
def thanks(request):
    return HttpResponse("email sent")

#advanced/templates/contact.html 
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Contact form</title>	
        <style type="text/css">
        </style>   
	</head>

	<body>
        <form action="{% url 'contact' %}" method="post">
            {% csrf_token %}
            <table class="gridtable">
                {{ form.as_table }}
            </table >
            <input type="submit" value="Submit" />
        </form>
	</body>

</html>     


###STEP 3:Create the Database tables now
$ python manage.py makemigrations advanced
$ python manage.py migrate

#check
python manage.py runserver 8080
# http://127.0.0.1:8080/advanced/contact







###Django - Password Management 
#The password attribute of a User object is a string in this format:
<algorithm>$<iterations>$<salt>$<hash>
#Django chooses the algorithm to use by using PASSWORD_HASHERS[0] 
#Default 
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
#Argon2 is the winner of the 2015 Password Hashing Competition
#django.contrib.auth.hashers.Argon2PasswordHasher make this first entry to use this 
$ pip install django[argon2]

##Password validation
#Validation is controlled by the AUTH_PASSWORD_VALIDATORS setting
UTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# django.contrib.auth.password_validation
class MinimumLengthValidator(min_length=8)
    Validates whether the password meets a minimum length. 
    The minimum length can be customized with the min_length parameter.

class UserAttributeSimilarityValidator(user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7)
    Validates whether the password is sufficiently different from certain attributes of the user.
    The user_attributes parameter should be an iterable of names of user attributes to compare to. 
    If this argument is not provided, the default is used: 'username', 'first_name', 'last_name', 'email'. 
    Attributes that don’t exist are ignored.
    The minimum similarity of a rejected password can be set on a scale of 0 to 1 
    with the max_similarity parameter. 
    A setting of 0 rejects all passwords, 
    whereas a setting of 1 rejects only passwords that are identical to an attribute’s value.
class CommonPasswordValidator(password_list_path=DEFAULT_PASSWORD_LIST_PATH)
    Validates whether the password is not a common password. 
    This converts the password to lowercase (to do a case-insensitive comparison) 
    and checks it against a list of 1000 common password created by Mark Burnett.
    The password_list_path can be set to the path of a custom file of common passwords. 
    This file should contain one lowercase password per line and may be plain text or gzipped.
class NumericPasswordValidator
    Validates whether the password is not entirely numeric.
#methods 
validate_password(password, user=None, password_validators=None)
    Validates a password. If all validators find the password valid, returns None. 
    If one or more validators reject the password, raises a ValidationError with all the error messages from the validators.
    The user object is optional: if it’s not provided, some validators may not be able to perform any validation and will accept any password.

password_changed(password, user=None, password_validators=None)
    Informs all validators that the password has been changed. 
    This can be used by validators such as one that prevents password reuse. 
    This should be called once the password has been successfully changed.
    For subclasses of AbstractBaseUser, the password field will be marked as “dirty” when calling set_password() which triggers a call to password_changed() after the user is saved.

password_validators_help_texts(password_validators=None)
    Returns a list of the help texts of all validators. These explain the password requirements to the user.

password_validators_help_text_html(password_validators=None)
    Returns an HTML string with all help texts in an <ul>. 
    This is helpful when adding password validation to forms, as you can pass the output directly to the help_text parameter of a form field.

get_password_validators(validator_config)
    Get all Password 
    

###STEP 4:Upload/download, with User authentication 

#examplesite/settings.py 

#Session based login, hence set below to expire 
SESSION_EXPIRE_AT_BROWSER_CLOSE = True    # everytime browser is closed, session is expired, ELSE persistant session 
SESSION_COOKIE_AGE  = 5*60 # in seconds 


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash. so below URLs are actually  from above MEDIA_ROOT
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

#advanced/urls.py 
#Using auth_views
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [            
    url(r'^signup/',  views.signup, name = 'signup'),  
    url(r'^login/',  auth_views.login,  {'template_name': 'registration/login.html'}, name = 'login'),  
    url(r'^logout/',  auth_views.logout,{'template_name': 'registration/logout.html'}, name = 'logout'), 
    
    url(r'^list/$', views.document_list, name='document-lists'), #this contains upload 
    url(r'^documents/(?P<pk>\d+)/$', views.download , name = 'documents-download'),
  ] 
  
#advanced/models.py 
from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')   #auto Uploaded to MEDIA_ROOT
    
    
#advanced/forms.py 
from django import forms
from django.contrib.auth.models import User

#Used for model 
class DocumentForm(forms.Form):
    docfile = forms.FileField( label='Select a file' )  #<input type="file" name="docfile">
    
    
##Signup form
from django.contrib.auth.password_validation  import password_validators_help_text_html, validate_password

class SignupForm(forms.Form):
    user = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, help_text= password_validators_help_text_html())
    again_password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        user = cleaned_data.get("user")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        user_obj = User(username=user, password=password, email=email)
        validate_password(password, user_obj)
        if self.user_exists(user): 
            self.add_error('user', "User exists!!")
        
    def user_exists(self, username):
        user_count = User.objects.filter(username=username).count()
        if user_count == 0:
            return False
        return True
        
#advanced/views.py 
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import StreamingHttpResponse 


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


import mimetypes 
import os.path

from .forms import *
from .models import * 

    
@login_required(login_url='/advanced/login/')  # beginning / is must, reverse('login') -> gives error!! 
def document_list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = form.cleaned_data['docfile'])
            newdoc.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('document-lists'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    # Render list page with the documents and the form
    return render(request, 'upload_list.html',  {'documents': documents, 'form': form}  )


    
def download(request, pk=1):
    # Handle file download
    document    = Document.objects.get(pk = pk)    
    file_full_path = os.path.join(settings.MEDIA_ROOT, document.docfile.name)
    filename = os.path.basename(file_full_path)
    response = StreamingHttpResponse(document.docfile, content_type=mimetypes.guess_type(file_full_path)[0]) 
    response['Content-Disposition'] = "attachment; filename={0}".format(filename)
    response['Content-Length'] = os.path.getsize(file_full_path) 
    return response
    
    
    
    
def signup(request):
    # Handle file upload
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = create_user(username=form.cleaned_data['user'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            # Redirect to login page 
            return HttpResponseRedirect('%s?next=%s' % (reverse('login'), reverse('document-lists')) )
    else:
        form = SignupForm() # A empty, unbound form    
    # Render list page with the documents and the form
    return render(request, 'registration/signup.html',  {'form': form} )


 

    
def create_user(username, email, password):
    user = User(username=username, email=email) #or use User.objects.create_user()
    user.set_password(password)
    user.save()
    return user
 
#advanced/templates/base.html 
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css" />
    <title>{% block title %}My amazing site{% endblock %}</title>
    <script type="text/javascript" > {% block head_script %} {% endblock %}  </script>
</head>

<body> 
    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
 
#advanced/templates/registration/signup.html 
{% extends "base.html" %}

{% block title %}Create an account{% endblock %}

{% block head_script %} 
        function validateForm() { 
            if(document.frm.again_password.value != document.frm.password.value) { 
                alert("Both password must be same "); 
                document.frm.password.value = "";
                document.frm.again_password.value = "";
                document.frm.password.focus(); 
                return false; 
                }             
            return true;
        }

{% endblock %}

{% block content %}
  <h1>Create an account</h1>
  <form action="{% url 'signup' %}" method="post" name="frm" onsubmit="return validateForm()">
      {% csrf_token %}
      <table border="1">      {{ form.as_table }}  </table>
      <input type="submit" value="Create the account">
      
  </form>
{% endblock %}

#advanced/templates/registration/login.html 
{% extends "base.html" %}

{% block title %}Login form{% endblock %}


{% block content %}

{% if form.errors %}
<p>Your username and password didn't match. Please try again.</p>
{% endif %}

<form method="post" action="{% url 'login' %}">
{% csrf_token %}
<table>
<tr>
    <td>{{ form.username.label_tag }}</td>
    <td>{{ form.username }}</td>
</tr>
<tr>
    <td>{{ form.password.label_tag }}</td>
    <td>{{ form.password }}</td>
</tr>
</table>

<input type="submit" value="login" />
<p> <a href="{% url 'signup' %}">First time user? Please SignUp</a><p>
<input type="hidden" name="next" value="{{ next }}" />
</form>
{% endblock %}

#advanced/templates/registration/logout.html 
{% extends "base.html" %}

{% block title %}{{title}}{% endblock %}

{% block content %}
{{title}}
<br/>
<p> <a href="{% url 'login' %}?next={% url 'document-lists' %}">Login Again</a><p>  {# next is must else going to profile #}
{% endblock %}

#advanced/templates/upload_list.html 
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Django File Upload Example</title>	
	</head>

	<body>
		<!-- List of uploaded documents -->
		{% if documents %}
			<ul>
			{% for document in documents %}
				<li><a href='{% url "documents-download" document.id %}'>{{ document.docfile.name }}</a></li>
			{% endfor %}
			</ul>  
		{% else %}
			<p>No documents.</p>
		{% endif %}

		<!-- Upload form. Note enctype attribute! -->
		<form action="{% url 'document-lists' %}" method="post" enctype="multipart/form-data">
			{% csrf_token %}
			<table>
                {{ form.as_table }}
            </table>
			<p><input type="submit" value="Upload" /></p>
		</form>
        <br/>
		<p> <a href="{% url 'logout' %}">Logout</a><p>
	</body>

</html> 


###STEP 6:Create the Database tables now
$ python manage.py makemigrations advanced
$ python manage.py migrate

#check
python manage.py runserver 8080
# http://127.0.0.1:8080/advanced/list 



###Reference to Field.FileField and Field.ImageField
class ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, **options)
class FileField(upload_to=None, max_length=100, **options)

#Example 
class MyModel(models.Model):
    # file will be uploaded to MEDIA_ROOT/uploads
    upload = models.FileField(upload_to='uploads/')
    # or...
    # file will be saved to MEDIA_ROOT/uploads/2015/01/30
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/')
#OR 
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)
class MyModel(models.Model):
    upload = models.FileField(upload_to=user_directory_path)
    
#Usage 
1.define MEDIA_ROOT as the full path to a directory to store uploaded files. 
  Define MEDIA_URL as the base public URL of that directory. 
  Make sure that this directory is writable by the Web server’s user account.
  eg  MEDIA_ROOT is set to '/home/media', and upload_to is set to 'photos/%Y/%m/%d'.
2.Add the FileField or ImageField to  model, defining the upload_to option to specify 
  a subdirectory of MEDIA_ROOT to use for uploaded files.
3.All that will be stored in  database is a path to the file (relative to MEDIA_ROOT). 
  For example, if  ImageField is called mug_shot, get the absolute path to image in a template with 
  {{ object.mug_shot.url }}.
When you access a FileField on a model, you get an instance of FieldFile as a proxy for django.core.files.File
FieldFile.name
FieldFile.size
FieldFile.url
FieldFile.open(mode='rb')
    Unlike the standard Python open() method, it doesn’t return a file descriptor.
    Since the underlying file is opened implicitly when accessing it, it may be unnecessary to call this method 
    except to reset the pointer to the underlying file or to change the mode.
FieldFile.close()
FieldFile.save(name, content, save=True)
    This method takes a filename and file contents(django.core.files.File) 
    and passes them to the storage class for the field, then associates the stored file 
    with the model field. 
    from django.core.files import File
    # Open an existing file using Python's built-in open()
    f = open('/path/to/hello.world')
    myfile = File(f)

FieldFile.delete(save=True)
    Deletes the file associated with this instance and clears all attributes on the field. 
    Note that when a model is deleted, related files are not deleted. 

##Example 
from django.db import models
class Car(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.ImageField(upload_to='cars')

>>> car = Car.objects.get(name="57 Chevy")
>>> car.photo # proxy of File object
<ImageFieldFile: chevy.jpg>
>>> car.photo.name
'cars/chevy.jpg'
>>> car.photo.path
'/media/cars/chevy.jpg'
>>> car.photo.url
'http://media.example.com/cars/chevy.jpg'
#The file is saved as part of saving the model in the database, 
#so the actual file name used on disk cannot be relied on until after the model has been saved.

#example, you can change the file name by setting the file’s name to a path relative to the file storage’s location 
#(MEDIA_ROOT if you are using the default FileSystemStorage):
>>> import os
>>> from django.conf import settings
>>> initial_path = car.photo.path
>>> car.photo.name = 'cars/chevy_ii.jpg'
>>> new_path = settings.MEDIA_ROOT + car.photo.name
>>> # Move the file on the filesystem
>>> os.rename(initial_path, new_path)
>>> car.save()
>>> car.photo.path
'/media/cars/chevy_ii.jpg'
>>> car.photo.path == new_path
True

##File storage
#Django’s default file storage is given by the DEFAULT_FILE_STORAGE setting; 
#if you don’t explicitly provide a storage system, this is the one that will be used.

#Using default storage 
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

path = default_storage.save('/path/to/file', ContentFile('new content'))
>>> path
'/path/to/file'

>>> default_storage.size(path)
11
>>> default_storage.open(path).read()
'new content'

>>> default_storage.delete(path)
>>> default_storage.exists(path)
False

#For example, To store uploaded files under /media/photos regardless of what MEDIA_ROOT setting is:
from django.core.files.storage import FileSystemStorage
from django.db import models
fs = FileSystemStorage(location='/media/photos')
class Car(models.Model):
    photo = models.ImageField(storage=fs)


    
###Django User Model - Creating User programatically 
from django.contrib.auth.models import User

# Create user and save to the database
user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

# Update fields and then save again
user.first_name = 'John'
user.last_name = 'Citizen'
user.save()

##Manager methods User model has a custom manager , access by User.objects.
create_user(username, email=None, password=None, **extra_fields)        
    Creates, saves and returns a User.
create_superuser(username, email, password, **extra_fields)
    Creates superuser 
    #OR 
    $ python manage.py createsuperuser --username=joe --email=joe@example.com

#To change a user’s password, you have several options:
$ python manage.py manage.py changepassword *username
#OR 
>>> from django.contrib.auth.models import User
>>> u = User.objects.get(username='john')
>>> u.set_password('new password')
>>> u.save()



##Few Imp attributes of User
first_name
last_name
email
password
groups                  
    Many-to-many relationship to Group
    Group has 'permisions' and user_set 
user_permissions        
    Many-to-many relationship to Permission
    Permission has 'user_set' and 'group_set' 
is_staff                
    Boolean. 
    Designates whether this user can access the admin site.
is_active               
    Boolean. 
    Designates whether this user account should be considered active.
is_superuser            
    Boolean. 
    Designates that this user has all permissions without explicitly assigning them.
last_login
date_joined
set_password(raw_password)
check_password(raw_password)
set_unusable_password()             
    Marks the user as having no password set
has_usable_password()
get_group_permissions(obj=None)
    Returns a set of permission strings that the user has, through their groups.
    If obj is passed in, only returns the group permissions for this specific object.
get_all_permissions(obj=None)
    Returns a set of permission strings that the user has, both through group and user permissions.
    If obj is passed in, only returns the permissions for this specific object.
has_perm(perm, obj=None)
    Returns True if the user has the specified permission, 
    where perm is in the format "<app label>.<permission codename>". . 
    If the user is inactive, this method will always return False.
    If obj is passed in, this method won’t check for a permission for the model, but for this specific object.
has_perms(perm_list, obj=None)
    Returns True if the user has each of the specified permissions, 
    where each perm is in the format "<app label>.<permission codename>". 
    If the user is inactive, this method will always return False.
    If obj is passed in, this method won’t check for permissions for the model, but for the specific object.
has_module_perms(package_name)
    Returns True if the user has any permissions in the given package (the Django app label). 
    If the user is inactive, this method will always return False.
email_user(subject, message, from_email=None, **kwargs)
    Sends an email to the user. If from_email is None, Django uses the DEFAULT_FROM_EMAIL. 
    Any **kwargs are passed to the underlying send_mail() call.
class models.Group
    name
        Required. 80 characters or fewer. 
        Any characters are permitted. Example: 'Awesome Users'.
    permissions
        Many-to-many field to Permission:
        group.permissions.set([permission_list])
        group.permissions.add(permission, permission, ...)
        group.permissions.remove(permission, permission, ...)
        group.permissions.clear()



##Login and logout signals
user_logged_in()            
    Sent when a user logs in successfully.
    Args are sender, request, user 
user_logged_out()           
    Args are sender, request, user 
user_login_failed()         
    Args are sender, credentials, request
    
##Signal Connecting receiver functions
#Option-1
from django.core.signals import request_finished

request_finished.connect(my_callback)

#OR Option-2 
from django.core.signals import request_finished
from django.dispatch import receiver

@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")

#Connecting to signals sent by specific senders
from django.db.models.signals import pre_save
from django.dispatch import receiver
from myapp.models import MyModel


@receiver(pre_save, sender=MyModel)
def my_handler(sender, **kwargs):



###Permissions and Authorization 
#superuser is authenticated and has all permissions
#permission is a string of the form "<app label>.<permission codename>" and can have anything there 
#In general, Admin user(admin console) creates any permission string, group , 
#assigns that to group/user and code checks that permission for an logged in user 


#Django comes with a simple permissions system. 
#It provides a way to assign permissions to specific users and groups of users.
1.Access to see/view the "add" form and add an object 
    is limited to users with the "add" permission for that type of object.
2.Access to see/view the change list, view the "change" form and change an object 
    is limited to users with the "change" permission for that type of object.
3.Access to delete an object 
    is limited to users with the "delete" permission for that type of object.
    
#Permissions can be set not only per type of object, but also per specific object instance. 
#permissions are "<app label>.<permission codename>", app_level is defined in 'python manage.py createapp app_nameORapp_label' 
#permission codename can be any string and created vi Model's Meta OPTIONS or by programatically
#And checked by User.has_parm()

##Default permissions
#When django.contrib.auth is listed in INSTALLED_APPS setting, 
#it will ensure that three default permissions 
#add, change and delete – are created for each Django model defined in one of installed applications.
#when below is executed  
$ python manage.py migrate


#For example - for app_label 'foo' and a model named 'Bar', 
#to test for basic permissions you should use: NOte : 
1.add: user.has_perm('foo.add_bar')
2.change: user.has_perm('foo.change_bar')
3.delete: user.has_perm('foo.delete_bar')
#Note app_label comes from Model, Meta OPTIONS 
Options.app_label
    If a model is defined outside of an application in INSTALLED_APPS, 
    it must declare which app it belongs to:
    Else, app_lable comes from manage.py startapp 'myapp', then   app_label = 'myapp'
    If you want to represent a model with the format app_label.object_name or app_label.model_name 
    you can use model._meta.label or model._meta.label_lower respectively.

#These permissions can be added/deleted from admin consoles for each User, for User group 



##django.contrib.auth.models.Group
#A generic way of categorizing users so you can apply permissions, or some other label, to those users. 
#A user can belong to any number of groups.

#A user in a group automatically has the permissions granted to that group. 
#For example, if the group Site editors has the permission 'can_edit_home_page', 
#any user in that group will have that permission.


##Programmatically creating permissions
#While custom permissions can be defined within a model’s Meta class, you can also create permissions directly. 
#Note permissions are "<app label>.<permission codename>"
Options.permissions
    Extra permissions to enter into the permissions table when creating this object. 
    Add, delete and change permissions are automatically created for each model. 
    This example specifies an extra permission, can_deliver_pizzas:
    permissions = (("can_deliver_pizzas", "Can deliver pizzas"),)
    This is a list or tuple of 2-tuples in the format (permission_code, human_readable_permission_name).
Options.default_permissions
    Defaults to ('add', 'change', 'delete'). 
    You may customize this list, for example, by setting this to an empty list 
    if your app doesn’t require any of the default permissions. 
    It must be specified on the model before the model is created by migrate in order 
    to prevent any omitted permissions from being created.


#OR,create the 'can_publish' permission for a BlogPost model in myapp:
from myapp.models import BlogPost
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType #django.contrib.contenttypes in INSTALLED_APPS

content_type = ContentType.objects.get_for_model(BlogPost)  #content_type is a Model  
permission = Permission.objects.create(
    codename='can_publish',
    name='Can Publish Posts',
    content_type=content_type,
)

#The permission can then be assigned to a User via its user_permissions attribute 
#or to a Group via its 'permissions' attribute.
#User objects have two many-to-many fields: 
#groups and user_permissions. 
#User objects can access their related objects in the same way as any other Django model:
myuser.groups.set([group_list])
myuser.groups.add(group, group, ...)
myuser.groups.remove(group, group, ...)
myuser.groups.clear()
myuser.user_permissions.set([permission_list])
myuser.user_permissions.add(permission, permission, ...)
myuser.user_permissions.remove(permission, permission, ...)
myuser.user_permissions.clear()
#OR via group 
group.permissions.set([permission_list])
group.permissions.add(permission, permission, ...)
group.permissions.remove(permission, permission, ...)
group.permissions.clear()
        
#And then check via User 
myuser.has_perm(perm, obj=None)
myuser.has_perms(perm_list, obj=None)

##Permission caching
#The ModelBackend caches permissions on the user object after the first time they need to be fetched for a permissions check. 
#If you are adding permissions and checking them immediately afterward, in a test or view for example, 
#the easiest solution is to re-fetch the user from the database

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from myapp.models import BlogPost
def user_gains_perms(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # any permission check will cache the current set of permissions
    user.has_perm('myapp.change_blogpost')
    content_type = ContentType.objects.get_for_model(BlogPost)
    permission = Permission.objects.get(
        codename='change_blogpost',
        content_type=content_type,
    )
    user.user_permissions.add(permission)
    # Checking the cached permission set
    user.has_perm('myapp.change_blogpost')  # False
    # Request new instance of User
    # Be aware that user.refresh_from_db() won't clear the cache.
    user = get_object_or_404(User, pk=user_id)
    # Permission cache is repopulated from the database
    user.has_perm('myapp.change_blogpost')  # True
    ...




###Authenticating users
#checks username, password against each authentication backend, 
#and returns a User object if the credentials are valid for a backend. 
#if a backend raises PermissionDenied, it returns None. 

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.



def logout_view(request):
    logout(request)
    # Redirect to a success page.

 

##Limiting access to logged-in users
from django.conf import settings
from django.shortcuts import redirect
def my_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # ...
#or display an error message:
from django.shortcuts import render
def my_view(request):
    if not request.user.is_authenticated:
        return render(request, 'myapp/login_error.html')
    # ...
    
#OR , use The login_required decorator
#use django.contrib.admin.views.decorators.staff_member_required() if STAFF(not superuser) is required 
login_required(redirect_field_name='next', login_url=None)
    login_required() does the following:
    1.If the user isn’t logged in, redirect to settings.LOGIN_URL, 
      passing the current absolute path in the query string . Example: /accounts/login/?next=/polls/3/.
    2.If the user is logged in, execute the view normally. 
      The view code is free to assume the user is logged in.

#Example 
from django.contrib.auth.decorators import login_required
@login_required
def my_view(request):
    #request.user is now logged in 
    

#By default, the path that the user should be redirected to upon successful authentication 
#is stored in a query string parameter called "next" or use  redirect_field_name parameter in login_required
#And customize login template as well, since the template context variable would also use redirect_field_name as its key rather than "next" (the default).

@login_required(redirect_field_name='my_redirect_field')
def my_view(request):
    ...
    
#login_required() also takes an optional login_url parameter for redirecting to login view (instead of settings.LOGIN_URL
@login_required(login_url='/accounts/login/')
def my_view(request):
    ...
    
#then urls.py:  Note path should be equal to login_url or settings.LOGIN_URL    
from django.contrib.auth import views as auth_views
path('accounts/login/', auth_views.LoginView.as_view()),



##Class based Access control 
#https://ccbv.co.uk/projects/Django/1.9/django.contrib.auth.mixins/UserPassesTestMixin/
class django.contrib.auth.mixins import AccessMixin
    Abstract CBV mixin that gives access mixins the same customizable functionality.
    Attributes 
        login_url = None 	AccessMixin
        permission_denied_message = '' 	AccessMixin
        raise_exception = False 	AccessMixin
        redirect_field_name = 'next' 	AccessMixin 


class django.contrib.auth.mixins.LoginRequiredMixin
    CBV mixin which verifies that the current user is authenticated.
    Ancestors (MRO)
        LoginRequiredMixin
        AccessMixin
    Attributes 
        login_url = None 	AccessMixin
        permission_denied_message = '' 	AccessMixin
        raise_exception = False 	AccessMixin
        redirect_field_name = 'next' 	AccessMixin


class django.contrib.auth.mixins.PermissionRequiredMixin
    CBV mixin which verifies that the current user has all specified permissions.
    Ancestors (MRO)
        PermissionRequiredMixin
        AccessMixin
    Attributes
        login_url = None 	
        permission_denied_message = '' 	
        permission_required = None 	 #String name of permssions or tuple pf permission strings 
        raise_exception = False 	
        redirect_field_name = 'next' 	
    Methods 
        def get_permission_required(self):
            """
            Override this method to override the permission_required attribute.
            Must return an iterable.
            """
            if self.permission_required is None:
                raise ImproperlyConfigured(
                    '{0} is missing the permission_required attribute. Define {0}.permission_required, or override '
                    '{0}.get_permission_required().'.format(self.__class__.__name__)
                )
            if isinstance(self.permission_required, six.string_types):
                perms = (self.permission_required, )
            else:
                perms = self.permission_required
            return perms
        def has_permission(self):
            """
            Override this method to customize the way permissions are checked.
            """
            perms = self.get_permission_required()
            return self.request.user.has_perms(perms)    
            
            

class django.contrib.auth.mixins.UserPassesTestMixin
    CBV Mixin that allows you to define a test function which must return True
    if the current user can access the view.
    Ancestors (MRO)
        UserPassesTestMixin
        AccessMixin
    Attributes
        login_url = None 	            AccessMixin
        permission_denied_message = '' 	AccessMixin
        raise_exception = False 	    AccessMixin
        redirect_field_name = 'next' 	AccessMixin
    Methods
        def test_func(self):
            raise NotImplementedError(
                '{0} is missing the implementation of the test_func() method.'.format(self.__class__.__name__)
            )
            
            
##LoginRequiredMixin
#If a view is using this mixin, all requests by non-authenticated users will be redirected to the login page 
#or shown an HTTP 403 Forbidden error, depending on the raise_exception parameter.

from django.contrib.auth.mixins import LoginRequiredMixin
class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    #implement get(self, request, *args, **kwargs) etc if any HTTP is required 
    #
    
    
##Limiting access to logged-in users that pass a test
#Option-1 
from django.shortcuts import redirect
def my_view(request):
    if not request.user.email.endswith('@example.com'):
        return redirect('/login/?next=%s' % request.path)
    # ...
    
#OR use 'user_passes_test' which redirects to login_url or settings.LOGIN_URL when test_func returns True 
#user_passes_test() takes a required argument: a callable that takes a User object and returns True if the user is allowed to view the page. 
#Note that user_passes_test() does not automatically check that the User is not anonymous( call user.is_authenticated to know that)

def email_check(user):
    return user.email.endswith('@example.com')
    
@user_passes_test(email_check)
def my_view(request):
    ...

#With login_url
@user_passes_test(email_check, login_url='/login/')
def my_view(request):
    ...
    
#OR use UserPassesTestMixin
from django.contrib.auth.mixins import UserPassesTestMixin
class MyView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.email.endswith('@example.com')
        
        
        
##Stacking UserPassesTestMixin
#Due to the way UserPassesTestMixin is implemented, you cannot stack them in inheritance list. 
#The following does NOT work:
#If TestMixin1 calls super() and take that result into account, TestMixin1 wouldn’t work standalone anymore.
class TestMixin1(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.email.endswith('@example.com')
class TestMixin2(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.username.startswith('django')
class MyView(TestMixin1, TestMixin2, View):
    ...
    
    


##The permission_required decorator
permission_required(perm, login_url=None, raise_exception=False)
#permission names take the form "<app label>.<permission codename>" (i.e. polls.can_vote for a permission on a model in the polls application).
#login_url defaults to settings.LOGIN_URL
#If the raise_exception parameter is given, the decorator will raise PermissionDenied, prompting the 403 (HTTP Forbidden) view instead of redirecting to the login page.

#Example 
from django.contrib.auth.decorators import permission_required
@permission_required('polls.can_vote')
def my_view(request):
    ...

#OR 
from django.contrib.auth.decorators import permission_required
@permission_required('polls.can_vote', login_url='/loginpage/')
def my_view(request):
    ...
    
    
#can be stacked with login_required, reccomended 
from django.contrib.auth.decorators import login_required, permission_required
@login_required
@permission_required('polls.can_vote', raise_exception=True)
def my_view(request):
    ...


#Or USe The PermissionRequiredMixin mixin
#can override get_permission_required():list_of_perms and or has_permission():Trie/False

from django.contrib.auth.mixins import PermissionRequiredMixin
class MyView(PermissionRequiredMixin, View):
    permission_required = 'polls.can_vote'
    # Or multiple of permissions:
    permission_required = ('polls.can_open', 'polls.can_edit')
    



       
    
###Django Angular 
#check - https://github.com/jrief/django-angular

#OR basic idea is to seperate Frontend and Backend
#Develop frontend in any framework 
#for backend use rest or Django-rest framework and frontend call django-rest implementations 
#check http://www.django-rest-framework.org/





###*** Example - Django blog using Django packages 

#Better to create virtualenv and virtualenvwrapper
#virtualenv is a tool to create isolated Python environments
    
$ pip install virtualenv

##Then use virtualenvwrapper (easy usage of virtualenv in windows) to provide a dedicated environment for each Django project 
#https://pypi.org/project/virtualenvwrapper-win/

$ pip install virtualenvwrapper  #unix 
$ pip install virtualenvwrapper-win

#create a virtual environment for your project:
$ mkvirtualenv simpleblog   --no-site-packages 
#stored in %USERPROFILE%\Envs
#or set WORKON_HOME=some_loacation where it would be stored 

#The virtual environment will be activated automatically 
#or in new command prompt 
$ workon simpleblog

#other commands 
lsvirtualenv
    List all of the enviornments stored in WORKON_HOME.
rmvirtualenv <name>
    Remove the environment <name>.
deactivate
    Deactivate the working virtualenv and switch back to the default system Python.
add2virtualenv <full or relative path>
    If a virtualenv environment is active, appends <path> to virtualenv_path_extensions.pth inside the environment’s site-packages, 
    which effectively adds <path> to the environment’s PYTHONPATH
cdproject
    If a virtualenv environment is active and a projectdir has been defined, 
    change the current working directory to active virtualenv’s project directory
cdsitepackages
    If a virtualenv environment is active, change the current working directory to the active virtualenv’s site-packages directory
cdvirtualenv
    If a virtualenv environment is active, change the current working directory to the active virtualenv base directory.
lssitepackages
    If a virtualenv environment is active, list that environment’s site-packages
mkproject
    If the environment variable PROJECT_HOME is set, 
    create a new project directory in PROJECT_HOME and a virtualenv in WORKON_HOME. 
    The project path will automatically be associated with the virtualenv on creation.
setprojectdir <full or relative path>
    If a virtualenv environment is active, define <path> as project directory containing the source code
toggleglobalsitepackages
    If a virtualenv environment is active, toggle between having the global site-packages in the PYTHONPATH or just the virtualenv’s site-packages.
whereis <file>
    Returns the locations (on %PATH%) that contain an executable file. 
virtualenvwrapper
    Print a list of commands and their descriptions as basic help output


#To create requirements.txt from existng environment 
$ pip freeze > requirements.txt

#Install requirements.txt in new dir 
$ cd <<DIR>>/MyProject/
$ workon simpleblog
$ pip install -r requirements.txt 




###Simple blog usin zinnia
#https://djangopackages.org/packages/p/django-plugins/

$ mkvirtualenv simpleblog   --no-site-packages 

#Creating other file 
$ mkdir simpleblog 
$ cd simpleblog 
$ workon simpleblog 
$ pip install Django==2.0.6
#https://github.com/drager/django-simple-blog
$ pip install django-blog-zinnia
#start project 
$ django-admin startproject myblog 

#compact the dir structure such that it measures below 
#create static and templates dir under this 
#dir structure 
.
└── simpleblog
    ├── manage.py
    └── myblog
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
        
        
        
##Update Settings.py 

#additional locations the staticfiles app will traverse
STATICFILES_DIRS = (
   os.path.join(BASE_DIR, "static/"),   
   )
   
#mywonstuff 
TEMPLATES[0]['DIRS'].append(os.path.join(BASE_DIR, 'templates'))

   
#for register zinnia module 
INSTALLED_APPS += [ 'django.contrib.humanize', 'django.contrib.sites', 'django_comments',
  'mptt',
  'tagging',
  'zinnia',
]
SITE_ID = 1
TEMPLATES[0]['OPTIONS']['context_processors']+= [
    'django.template.context_processors.i18n',
    'zinnia.context_processors.version',  # Optional
]


##Update urls.py 

from django.conf.urls import url

urlpatterns += [
    url(r'^weblog/', include('zinnia.urls')),
    url(r'^comments/', include('django_comments.urls')),
 ]


#then 
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver 8000 
#http://127.0.0.1:8000/weblog    

#Change domain from www.example.com to new from http://127.0.0.1:8000/admin/sites/site/
#Change Heading from Zinnia;s weblog to Myweblog 
#copy zinnia module/templates/zinnia/skeleton.html to myblog/templates/zinnia/skeleton.html 
#update 

#check api  http://docs.django-blog-zinnia.com/en/develop/getting-started/overview.html




##Updating wsgi.py using this virtualenv 
import os
import sys
import site

#site:This module is automatically imported during initialization
#addsitedir: Add a directory to sys.path and process its .pth files.
# Add the site-packages of the chosen virtualenv to work with
#$WORKON_HOME/simpleblog/Lib/site-packages
#find out exact dir 
sitedir = os.path.expanduser("~/Envs/simpleblog/Lib/site-packages")
site.addsitedir(sitedir)  #C:\Users\das\Envs\simpleblog\Lib\site-packages

# Add the app's directory to the PYTHONPATH
app_dir = r"D:\Desktop\PPT\python\OtherPython\Django\code\recent\simpleblog\myblog"
sys.path.append(app_dir)
sys.path.append(os.path.join(app_dir, 'myblog'))  #where settings.py exists 

# Activate your virtual env
activate_env = os.path.expanduser("~/Envs/simpleblog/Scripts/activate_this.py") #C:\Users\das\Envs\simpleblog\Scripts

#python2.7 
#execfile(activate_env, dict(__file__=activate_env))
#python3 
with open(activate_env) as f:
    code = compile(f.read(), activate_env, 'exec')
    exec(code, dict(__file__=activate_env))


from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblog.settings")
application = get_wsgi_application()