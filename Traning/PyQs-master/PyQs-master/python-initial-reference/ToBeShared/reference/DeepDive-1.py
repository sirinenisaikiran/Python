#Contents 
Re Expression 
Advanced Sorting 
Web Page & CGI Programming
Web Server Gateway Interface (WSGI)
Database Access
SMTP & Emailing
CSV handling - std module 
xml.etree.ElementTree — The ElementTree XML API (same in Py3.x and Py2.7)
HTML Handling 
HTTP automation 
*Apache requests 
XML Processing - Use BeautifulSoup for HTML/XML processing
*Module Json 
*Python Standard Library – datetime
Scrapy
CSS Reference 
XPATH reference 
#**************************************************
###Re Expression 
##match() vs search()
#re.match() checks for a match only at the beginning 
#of the string, 
#while re.search() checks for a match anywhere in the string 


>>> re.match("c", "abcdef")    # No match
>>> re.search("c", "abcdef")   # Match
<_sre.SRE_Match object at ...>


#Regular expressions beginning with '^' can be used 
#with search() to restrict the match at the beginning of the string:


>>> re.match("c", "abcdef")    # No match
>>> re.search("^c", "abcdef")  # No match
>>> re.search("^a", "abcdef")  # Match
<_sre.SRE_Match object at ...>


#in MULTILINE mode match() only matches 
#at the beginning of the string, 
#whereas using search() with a regular expression 
#beginning with '^' will match at the beginning of each line.


>>> re.match('X', 'A\nB\nX', re.MULTILINE)  # No match
>>> re.search('^X', 'A\nB\nX', re.MULTILINE)  # Match
<_sre.SRE_Match object at ...>

##sub with repl as function 
#it is called for every non-overlapping occurrence of pattern. 
#The function takes a single match object argument, 
#and returns the replacement string


def dashrepl(matchobj):
    if matchobj.group(0) == '-': return ' '
    else: return '-'
>>> re.sub('-{1,2}', dashrepl, 'pro----gram-files')
'pro--gram files'


##Flags 
re.DEBUG        Display debug information about compiled expression.
re.I            re.IGNORECASE
re.L            re.LOCALE, Make \w, \W, \b, \B, \s and \S dependent on the current locale.
re.M            re.MULTILINE  ^,$ for each newline 
re.S            re.DOTALL   . matches newline 
re.X            re.VERBOSE

a = re.compile(r"""\d +  # the integral part
                   \.    # the decimal point
                   \d *  # some fractional digits""", re.X)
b = re.compile(r"\d+\.\d*")



##Match Object 
match = re.search(pattern, string)
if match:
    process(match)
    
#meaning of group 
>>> m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
>>> m.group(0)       # The entire match
'Isaac Newton'
>>> m.group(1)       # The first parenthesized subgroup.
'Isaac'
>>> m.group(2)       # The second parenthesized subgroup.
'Newton'
>>> m.group(1, 2)    # Multiple arguments give us a tuple.
('Isaac', 'Newton')





###Advanced Sorting 
from operator import itemgetter, attrgetter

student_tuples = [
        ('john', 'A', 15),
        ('jane', 'B', 12),
        ('dave', 'B', 10),
    ]
>>> sorted(student_tuples, key=lambda student: student[2])   # sort by age
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

#OR 
>>> sorted(student_tuples, key=itemgetter(2))
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

#for object 

>>> class Student:
            def __init__(self, name, grade, age):
                self.name = name
                self.grade = grade
                self.age = age
            def __repr__(self):
                return repr((self.name, self.grade, self.age))



>>> student_objects = [
        Student('john', 'A', 15),
        Student('jane', 'B', 12),
        Student('dave', 'B', 10),
    ]
>>> sorted(student_objects, key=lambda student: student.age)   # sort by age
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

#OR 

>>> sorted(student_objects, key=attrgetter('age'))
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]


#for multiple key , use below 

>>> sorted(student_tuples, key=itemgetter(1,2))
[('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]



>>> sorted(student_objects, key=attrgetter('grade', 'age'))
[('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]


#The operator.methodcaller() function makes method calls 
#with fixed parameters for each object being sorted. 

>>> from operator import methodcaller
>>> messages = ['critical!!!', 'hurry!', 'standby', 'immediate!!']
>>> sorted(messages, key=methodcaller('count', '!')) #calls str.count('!')
['standby', 'hurry!', 'immediate!!', 'critical!!!']












###Database Access

#Module-sqllit , standard package
from sqlite3 import connect

conn = connect(r'D:/temp.db')
curs = conn.cursor()
curs.execute('create table if not exists emp (who, job, pay)')

prefix = 'insert into emp values '
curs.execute(prefix + "('Bob', 'dev', 100)")
curs.execute(prefix + "('Sue', 'dev', 120)")
conn.commit()
curs.execute("select * from emp where pay > 100")
for (who, job, pay) in curs.fetchall():
		print(who, job, pay)

result = curs.execute("select who, pay from emp")
result.fetchone()

query = "select * from emp where job = ?"
curs.execute(query, ('dev',)).fetchall()
conn.close()

#bulk insert 
import sqlite3
conn = connect(r'D:/temp.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")



# Larger example that inserts many records at a time
purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
curs.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

conn.commit()
conn.close()
#Other reference - http://pythoncentral.io/advanced-sqlite-usage-in-python/




$ sqlite3 sample.db
SQLite version 3.19.1 2017-05-24 13:08:33
Enter ".help" for usage hints.
sqlite> .tables
emp
sqlite> .schema emp
sqlite> select * from emp;


###*** Mysql 
#https://dev.mysql.com/downloads/connector/python/




#Creation 
import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'employees'

TABLES = {}
TABLES['employees'] = (
    "CREATE TABLE `employees` ("
    "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ENGINE=InnoDB")

TABLES['departments'] = (
    "CREATE TABLE `departments` ("
    "  `dept_no` char(4) NOT NULL,"
    "  `dept_name` varchar(40) NOT NULL,"
    "  PRIMARY KEY (`dept_no`), UNIQUE KEY `dept_name` (`dept_name`)"
    ") ENGINE=InnoDB")

TABLES['salaries'] = (
    "CREATE TABLE `salaries` ("
    "  `emp_no` int(11) NOT NULL,"
    "  `salary` int(11) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`,`from_date`), KEY `emp_no` (`emp_no`),"
    "  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) "
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['dept_emp'] = (
    "CREATE TABLE `dept_emp` ("
    "  `emp_no` int(11) NOT NULL,"
    "  `dept_no` char(4) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`),"
    "  KEY `dept_no` (`dept_no`),"
    "  CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`) "
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
    "  CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`) "
    "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['dept_manager'] = (
    "  CREATE TABLE `dept_manager` ("
    "  `dept_no` char(4) NOT NULL,"
    "  `emp_no` int(11) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`,`dept_no`),"
    "  KEY `emp_no` (`emp_no`),"
    "  KEY `dept_no` (`dept_no`),"
    "  CONSTRAINT `dept_manager_ibfk_1` FOREIGN KEY (`emp_no`) "
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
    "  CONSTRAINT `dept_manager_ibfk_2` FOREIGN KEY (`dept_no`) "
    "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['titles'] = (
    "CREATE TABLE `titles` ("
    "  `emp_no` int(11) NOT NULL,"
    "  `title` varchar(50) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date DEFAULT NULL,"
    "  PRIMARY KEY (`emp_no`,`title`,`from_date`), KEY `emp_no` (`emp_no`),"
    "  CONSTRAINT `titles_ibfk_1` FOREIGN KEY (`emp_no`)"
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")
    


cnx = mysql.connector.connect(user='scott', password='password',
                              host='127.0.0.1',
                              database='employees')
                              
cursor = cnx.cursor()



def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)


for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

        
from datetime import date, datetime, timedelta

tomorrow = datetime.now().date() + timedelta(days=1)

add_employee = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")
add_salary = ("INSERT INTO salaries "
              "(emp_no, salary, from_date, to_date) "
              "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

# Insert new employee
cursor.execute(add_employee, data_employee)
emp_no = cursor.lastrowid

# Insert salary information
data_salary = {
  'emp_no': emp_no,
  'salary': 50000,
  'from_date': tomorrow,
  'to_date': date(9999, 1, 1),
}
cursor.execute(add_salary, data_salary)

# Make sure data is committed to the database
cnx.commit()
        
        
query = ("SELECT first_name, last_name, hire_date FROM employees "
         "WHERE hire_date BETWEEN %s AND %s")

hire_start = datetime.date(1999, 1, 1)
hire_end = datetime.date(1999, 12, 31)

cursor.execute(query, (hire_start, hire_end))

for (first_name, last_name, hire_date) in cursor:
  print("{}, {} was hired on {:%d %b %Y}".format(
    last_name, first_name, hire_date))
        
cursor.close()



# Get two buffered cursors
curA = cnx.cursor(buffered=True)
curB = cnx.cursor(buffered=True)

# Query to get employees who joined in a period defined by two dates
query = (
  "SELECT s.emp_no, salary, from_date, to_date FROM employees AS e "
  "LEFT JOIN salaries AS s USING (emp_no) "
  "WHERE to_date = DATE('9999-01-01')"
  "AND e.hire_date BETWEEN DATE(%s) AND DATE(%s)")

# UPDATE and INSERT statements for the old and new salary
update_old_salary = (
  "UPDATE salaries SET to_date = %s "
  "WHERE emp_no = %s AND from_date = %s")
insert_new_salary = (
  "INSERT INTO salaries (emp_no, from_date, to_date, salary) "
  "VALUES (%s, %s, %s, %s)")

# Select the employees getting a raise
curA.execute(query, (date(2000, 1, 1), date(2000, 12, 31)))

# Iterate through the result of curA
for (emp_no, salary, from_date, to_date) in curA:

  # Update the old and insert the new salary
  new_salary = int(round(salary * Decimal('1.15')))
  curB.execute(update_old_salary, (tomorrow, emp_no, from_date))
  curB.execute(insert_new_salary,
               (emp_no, tomorrow, date(9999, 1, 1,), new_salary))

  # Commit the changes
  cnx.commit()


cnx.close()
    
  
    
###Executing stored proceedure - mysql 
result_args = cursor.callproc(proc_name, args=())

#Result sets produced by the stored procedure are automatically fetched 
#and stored as MySQLCursorBuffered instances. For more information about using these result sets, see stored_results(). 



#Example 
CREATE PROCEDURE multiply(IN pFac1 INT, IN pFac2 INT, OUT pProd INT)
BEGIN
  SET pProd := pFac1 * pFac2;
END
#python code 
args = (5, 6, 0) # 0 is to hold value of the OUT parameter pProd
>>> cursor.callproc('multiply', args)
('5', '6', 30L)

#OR  with parameter types to be specified. 
#specify a parameter as a two-item tuple consisting of the parameter value and type.
CREATE PROCEDURE sp1(IN pStr1 VARCHAR(20), IN pStr2 VARCHAR(20),
                     OUT pConCat VARCHAR(100))
BEGIN
  SET pConCat := CONCAT(pStr1, pStr2);
END;
#code 
args = ('ham', 'eggs', (0, 'CHAR'))
result_args = cursor.callproc('sp1', args)
print(result_args[2])

#If you are using sqlalchemy, then 

def call_procedure(function_name, params):
    engine = create_engine('mysql://scott:tiger@localhost/test')
    connection = engine.raw_connection()
    try:
       cursor = connection.cursor()
       cursor.callproc(function_name, params)
       results = list(cursor.fetchall())
       cursor.close()
       connection.commit()
       return results
    finally:
       connection.close()
#usage 
call_procedure("my_procedure", ['x', 'y', 'z'])









###SMTP & Emailing


#Mail handling using smtplib and poplib
#to use google access, make it less secure https://www.google.com/settings/security/lesssecureapps

#Sending a mail
1. Create a message using email.mime.text.MIMEText
2. Create smptp object via SMTP and sendmail()

#example:
import smtplib
import email.utils
from email.mime.text import MIMEText
import getpass

# Create the message
msg = MIMEText('This is the body of the message.')
msg['To'] = email.utils.formataddr(('Recipient', 'ndas1971@gmail.com'))
msg['From'] = email.utils.formataddr(('Author', 'ndas1971@gmail.com'))
msg['Subject'] = 'Simple test message'


server = smtplib.SMTP('smtp.gmail.com', 587)  
server.set_debuglevel(True) # show communication with the server
try:
    # identify ourselves, prompting server for supported features
	server.ehlo()
	# If we can encrypt this session, do it
	if server.has_extn('STARTTLS'):
		server.starttls()
		server.ehlo() # re-identify ourselves over TLS connection
	
	p = getpass.getpass()
	server.login('ndas1971@gmail.com', p)
	server.sendmail('ndas1971@gmail.com', ['ndas1971@gmail.com',], msg.as_string())
finally:
    server.quit()

#For multiple recipants
recipients = ['john.doe@example.com', 'john.smith@example.co.uk']
msg['To'] = ", ".join(recipients)
s.sendmail(sender, recipients, msg.as_string())
#check many examples
#https://docs.python.org/3/library/email-examples.html

##Download message using poplib 
#server mmust support POP3



import getpass, poplib
import email
from io import StringIO   # for py2.x cStringIO
from email.generator import Generator


user = 'ndas1971@gmail.com' 

Mailbox = poplib.POP3_SSL('pop.gmail.com', '995') 
Mailbox.user(user) 

p = getpass.getpass()

Mailbox.pass_(p) 
numMessages = len(Mailbox.list()[1])

#(numMsgs, totalSize) = Mailbox.stat()
print(" No of messages=%s" % numMessages )
for i in range(5):
	msg = Mailbox.retr(i+1)[1]
	f_msg = email.message_from_bytes(b"\n".join(msg))   #in py2.x, use _string 
	for header in [ 'subject', 'to', 'from' ]:
		print('%-8s: %s' % (header.upper(), f_msg[header]))
	print("\n")

# complete message

num = int(input("Input msg # for seeing complete message>"))
msg = Mailbox.retr(num+1)[1]
c_msg = email.message_from_bytes(b"\n".join(msg))  #in py2.x, use _string 
fp = StringIO()
g = Generator(fp, mangle_from_=False, maxheaderlen=60)
g.flatten(c_msg)
text = fp.getvalue()
print(text)

Mailbox.quit()





###CSV handling - std module 

#csv.reader(csvfile, dialect='excel', **fmtparams)
#Each row read from the csv file is returned as a list of strings. 
#No automatic data type conversion is performed unless the QUOTE_NONNUMERIC format option is specified 
#(in which case unquoted fields are transformed into floats).

csvreader.next()
csvreader.line_num

#newline='' , pass newline directly without translation to reader/write process 

import csv
with open('eggs.csv', newline='',) as csvfile:
    r = csv.reader(csvfile, delimiter=',',quoting=csv.QUOTE_NONNUMERIC)
    for row in r:
        print(':'.join(row))
Spam, Spam, Spam, Spam, Spam, Baked Beans
Spam, Lovely Spam, Wonderful Spam

#csv.writer(csvfile, dialect='excel', **fmtparams)
#csvwriter.writerow(row)
#csvwriter.writerows(rows)
#DictWriter.writeheader()


import csv
with open('eggs1.csv', 'w', newline='') as csvfile:
    w = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
    w.writerow(['Spam'] * 5 + ['Baked Beans'])
    w.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

#For handling header etc - use manually 

import csv
dict1 = {}

with open("test.csv", "rb") as infile:
    reader = csv.reader(infile)
    headers = next(reader)[1:]
    for row in reader:
        dict1[row[0]] = {key: int(value) for key, value in zip(headers, row[1:])}
        
#data 
,col1,col2,col3
row1,23,42,77
row2,25,39,87
row3,48,67,53
row4,14,48,66





###xml.etree.ElementTree — The ElementTree XML API (same in Py3.x and Py2.7)
#std module 
 
#Example: country_data.xml file 
  
<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>


#code 
import xml.etree as etree


import xml.etree.ElementTree as ET
tree = ET.parse('example.xml')
root = tree.getroot()

print(ET.tostring(root))  #give element 

#Or directly from a string:
root = ET.fromstring(country_data_as_string)

#Every element has a tag and a dictionary of attributes

>>> root.tag
'data'
>>> root.attrib
{}


#It also has children nodes over which we can iterate

for child in root:
    print(child.tag, child.attrib)
...
country {'name': 'Liechtenstein'}
country {'name': 'Singapore'}
country {'name': 'Panama'}


#Children are nested, 
#access specific child nodes by index:

>>> root[0][1].text

#Finding interesting elements

#use Element.iter()
#any tag can be given, then it would return list of those 
for neighbor in root.iter('neighbor'):
		print(neighbor.attrib)

#Use Element.findall() finds only elements with a tag which are direct children of the current element. 
#Element.find() finds the first child with a particular tag, 
#Element.text accesses the element’s text content. 
#Element.get() accesses the element’s attributes


for country in root.findall('country'):
		rank = country.find('rank').text
		name = country.get('name')
		print(name, rank)

##XPath support - limited support via findall() and find()
#findall always return list of ELement 
#find always return single Element 

import xml.etree.ElementTree as ET

# Top-level elements
root.findall(".")

# All 'neighbor' grand-children of 'country' children of the top-level
# elements
root.findall("./country/neighbor")

# Nodes with name='Singapore' that have a 'year' child
root.findall(".//year/..[@name='Singapore']")
ET.tostring(x[0])

# 'year' nodes that are children of nodes with name='Singapore'
root.findall(".//*[@name='Singapore']/year")

# All 'neighbor' nodes that are the second child of their parent
root.findall(".//neighbor[2]")

#Modifying an XML File
#to update attribute,  use Element.set()
#to update text, just assign to text 

for rank in root.iter('rank'):
		new_rank = int(rank.text) + 1
		rank.text = str(new_rank)
		rank.set('updated', 'yes')

tree.write('output.xml')


#remove elements using Element.remove(). 

>>> for country in root.findall('country'):
		rank = int(country.find('rank').text)
		if rank > 50:
			root.remove(country)

>>> tree.write('output.xml')

#Building XML documents
#Creation
#Element(tag, attrib={})
#SubElement(parent, tag, attrib={})
import xml.etree.ElementTree as ET
a = ET.Element('a')
b = ET.SubElement(a, 'b', attrib=dict(count="1")) #attrib must be string 
b.text = "hello"
ET.dump(a)

#Parsing XML with Namespaces
#If the XML input has namespaces, 
#tags and attributes with prefixes in the form prefix:sometag 
#get expanded to {uri}sometag where the prefix is replaced by the full URI.
#Also, if there is a default namespace, that full URI gets prepended to all of the non-prefixed tags

<?xml version="1.0"?>
<actors xmlns:fictional="http://characters.example.com"
        xmlns="http://people.example.com">
    <actor>
        <name>John Cleese</name>
        <fictional:character>Lancelot</fictional:character>
        <fictional:character>Archie Leach</fictional:character>
    </actor>
    <actor>
        <name>Eric Idle</name>
        <fictional:character>Sir Robin</fictional:character>
        <fictional:character>Gunther</fictional:character>
        <fictional:character>Commander Clement</fictional:character>
    </actor>
</actors>


#Option-1 

root = fromstring(xml_text)
for actor in root.findall('{http://people.example.com}actor'):
    name = actor.find('{http://people.example.com}name')
    print(name.text)
    for char in actor.findall('{http://characters.example.com}character'):
        print(' |-->', char.text)


#Option-2

ns = {'real_person': 'http://people.example.com',
      'role': 'http://characters.example.com'}

for actor in root.findall('real_person:actor', ns):
    name = actor.find('real_person:name', ns)
    print(name.text)
    for char in actor.findall('role:character', ns):
        print(' |-->', char.text)


		


###HTML Handling 
#Below methods has method is either "xml", "html" or "text" (default is "xml"). 
xml.etree.ElementTree.tostring(element, encoding="us-ascii", method="xml")
xml.etree.ElementTree.tostringlist(element, encoding="us-ascii", method="xml")
class xml.etree.ElementTree.ElementTree(element=None, file=None)
    write(file, encoding="us-ascii", xml_declaration=None, default_namespace=None, method="xml")


#html file 
<html>
    <head>
        <title>Example page</title>
    </head>
    <body>
        <p>Moved to <a href="http://example.org/">example.org</a>
        or <a href="http://example.com/">example.com</a>.</p>
    </body>
</html>

#example 

from xml.etree.ElementTree import ElementTree
tree = ElementTree()
tree.parse("index.xhtml")
#<Element 'html' at 0xb77e6fac>
p = tree.find("body/p")     # Finds first occurrence of tag p in body
links = list(p.iter("a"))   # Returns list of all links
links
#[<Element 'a' at 0xb77ec2ac>, <Element 'a' at 0xb77ec1cc>]
for i in links:             # Iterates through all found links
    i.attrib["target"] = "blank"

tree.write("output.xhtml")



###*Module Json 
#JSON (JavaScript Object Notation) specified by RFC 7159 

# to and from file 
json.dump(obj, fp, skipkeys=False, ensure_ascii=True, check_circular=True, 
   allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw)
#fp is opened as fp = open(filename, "w")
#indent is string which is used for indentation

json.load(fp, cls=None, object_hook=None, parse_float=None, parse_int=None, 
    parse_constant=None, object_pairs_hook=None, **kw)
#fp is opened as fp = open(filename, "r")
#parse_type, if specified, will be called with the string of every JSON 'type' to be decoded


#To and from string  
json.dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, 
    allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw)

json.loads(s, encoding=None, cls=None, object_hook=None, parse_float=None, 
    parse_int=None, parse_constant=None, object_pairs_hook=None, **kw)
    
#Jason syntax 
JSON data is written as - "name":value pairs, eg -  "firstName":"John"
name is in double quote
JSON values can be:
    A number (integer or floating point)
    A string (in double quotes)
    A Boolean (true or false)
    An array (in square brackets with , as separator )
    An object (in curly braces with "name":value)
    null


#The file type for JSON files is ".json"
#The MIME type for JSON text is "application/json"
#No comment is allowed  even with /* */, // or #
#Only one root element or object is allowed, no multiple root elements 

#conversion table
#Python			JSON
dict 			object 
list, tuple 	array 
str 			string 
int, float,     int,float
True 			true 
False 			false 
None 			null 

#Note, separators=(',', ': ') as default if indent is not None.
#The json module always produces str objects, not bytes objects
#Keys in key/value pairs of JSON are always of the type str. 
#When a dictionary is converted into JSON, all the keys of the dictionary are coerced to strings
#That is, loads(dumps(x)) != x if x has non-string keys.
 

#Example file: example.json  
[
 { "empId: 1, "details": 
                        {                       
                          "firstName": "John",
                          "lastName": "Smith",
                          "isAlive": true,
                          "age": 25,
                          "salary": 123.5,
                          "address": {
                            "streetAddress": "21 2nd Street",
                            "city": "New York",
                            "state": "NY",
                            "postalCode": "10021-3100"
                          },
                          "phoneNumbers": [
                            {
                              "type": "home",
                              "number": "212 555-1234"
                            },
                            {
                              "type": "office",
                              "number": "646 555-4567"
                            },
                            {
                              "type": "mobile",
                              "number": "123 456-7890"
                            }
                          ],
                          "children": [],
                          "spouse": null
                        }
  } , { "empId: 20, "details": 
                            {                       
                              "firstName": "Johns",
                              "lastName": "Smith",
                              "isAlive": true,
                              "age": 25,
                              "salary": 123.5,
                              "address": {
                                "streetAddress": "21 2nd Street",
                                "city": "New York",
                                "state": "NY",
                                "postalCode": "10021-3100"
                              },
                              "phoneNumbers": [
                                {
                                  "type": "home",
                                  "number": "212 555-1234"
                                },
                                {
                                  "type": "office",
                                  "number": "646 555-4567"
                                },
                                {
                                  "type": "mobile",
                                  "number": "123 456-7890"
                                }
                              ],
                              "children": [],
                              "spouse": null
                            }
    }
]

#Example reading file 
import json 
import pprint 
fp = open("data/example.json", "r")
obj = json.load(fp)
fp.close()
pprint.pprint(obj)  #check size 
[{'details': {'address': {'city': 'New York',
                          'postalCode': '10021-3100',
                          'state': 'NY',
                          'streetAddress': '21 2nd Street'},
              'age': 25,
              'children': [],
              'firstName': 'John',
              'isAlive': True,
              'lastName': 'Smith',
              'phoneNumbers': [{'number': '212 555-1234', 'type': 'home'},
                               {'number': '646 555-4567', 'type': 'office'},
                               {'number': '123 456-7890', 'type': 'mobile'}],
              'salary': 123.5,
              'spouse': None},
  'empId': 1},
 {'details': {'address': {'city': 'New York',
                          'postalCode': '10021-3100',
                          'state': 'NY',
                          'streetAddress': '21 2nd Street'},
              'age': 25,
              'children': [],
              'firstName': 'Johns',
              'isAlive': True,
              'lastName': 'Smith',
              'phoneNumbers': [{'number': '212 555-1234', 'type': 'home'},
                               {'number': '646 555-4567', 'type': 'office'},
                               {'number': '123 456-7890', 'type': 'mobile'}],
              'salary': 123.5,
              'spouse': None},
  'empId': 20}]

#manipulations 
len(obj)        #2
type(obj)       #<class 'list'>
type(obj[0])    #<class 'dict'>
with open("data/example1.json", "w") as fp1:
    json.dump(obj, fp1, indent='\t')
  
#Obj is array , all array manipulations can be used 
[emp['details']['address']['state']   for emp in obj if emp['empId'] > 10] 








###*Python Standard Library – datetime
import datetime
dir(datetime)
dir(datetime.date)
dir(datetime.time)
dir(datetime.datetime)
dir(datetime.timedelta)


##here timestamp is as returned by time.time()
classmethod date.today()
classmethod date.fromtimestamp(timestamp)
classmethod date.fromordinal(ordinal) # ordinal, where January 1 of year 1 has ordinal 1

classmethod datetime.today()
classmethod datetime.now(tz=None)
classmethod datetime.utcnow()


classmethod datetime.fromtimestamp(timestamp, tz=None)
classmethod datetime.utcfromtimestamp(timestamp)

#combining date and time 
classmethod datetime.combine(date, time)

instancemethod timedelta.total_seconds()
instancemethod date.weekday(), datetime.weekday()  #0 is Monday
instancemethod datetime.date()  #returns date 
instancemethod datetime.time()  #returns time


class datetime.timedelta([days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])
class datetime.date(year, month, day) #month, day 1 based, hr, min, sec are zero based
class datetime.datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
class datetime.time([hour[, minute[, second[, microsecond[, tzinfo]]]]])

# +, -, *(by int), /(by int) operations are valid between two timedelta
# timedelta can be added or subtraced to date or datetime , but not time

# difference of two dates or datetimes  is timedelata
# date, time, datetime, timedelta are comparable
# no arithmatic operations are supported for two time 

# date.timetuple() or datetime.timetuple() returns time.struct_time(as returned by time.localtime())
# date.ctime(), datetime.ctime, date or time or datetime.strftime(format) returns string
# classmethod datetime.strptime(date_string, format) converts string to datetime

#years before 1900 cannot be used with strftime()
date.strftime("%A %d. %B %Y")
datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
datetime.strftime("%A, %d. %B %Y %I:%M%p")
#format
%d 	    Day of the month as a zero-padded decimal number. 	01, 02, ..., 31 	 
%m 	    Month as a zero-padded decimal number. 	01, 02, ..., 12 	 
%y 	    Year without century as a zero-padded decimal number. 	00, 01, ..., 99 	 
%Y 	    Year with century as a decimal number. 	1970, 1988, 2001, 2013 	 
%H 	    Hour (24-hour clock) as a zero-padded decimal number. 	00, 01, ..., 23 	 
%M 	    Minute as a zero-padded decimal number. 	00, 01, ..., 59 	 
%S 	    Second as a zero-padded decimal number. 	00, 01, ..., 59 	(3)

%a 	    Weekday as locale’s abbreviated name. 	
            Sun, Mon, ..., Sat (en_US);
            So, Mo, ..., Sa (de_DE)
%A 	    Weekday as locale’s full name. 	
            Sunday, Monday, ..., Saturday (en_US);
            Sonntag, Montag, ..., Samstag (de_DE)
%b 	    Month as locale’s abbreviated name. 	
            Jan, Feb, ..., Dec (en_US);
            Jan, Feb, ..., Dez (de_DE)
%B 	    Month as locale’s full name. 	
            January, February, ..., December (en_US);
            Januar, Februar, ..., Dezember (de_DE)

%w 	    Weekday as a decimal number, where 0 is Sunday and 6 is Saturday. 	0, 1, ..., 6 	 
%I 	    Hour (12-hour clock) as a zero-padded decimal number. 	01, 02, ..., 12 	 
%p 	    Locale’s equivalent of either AM or PM. 	
            AM, PM (en_US);
            am, pm (de_DE)
%f 	    Microsecond as a decimal number, zero-padded on the left. 	000000, 000001, ..., 999999 	(4)
%z 	    UTC offset in the form +HHMM or -HHMM (empty string if the the object is naive). 	(empty), +0000, -0400, +1030 	(5)
%Z 	    Time zone name (empty string if the object is naive). 	(empty), UTC, EST, CST 	 
%j 	    Day of the year as a zero-padded decimal number. 	001, 002, ..., 366 	 
%U 	    Week number of the year (Sunday as the first day of the week) as a zero padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0. 	00, 01, ..., 53 	(6)
%W 	    Week number of the year (Monday as the first day of the week) as a decimal number. All days in a new year preceding the first Monday are considered to be in week 0. 	00, 01, ..., 53 	(6)
%c 	    Locale’s appropriate date and time representation. 	
            Tue Aug 16 21:30:00 1988 (en_US);
            Di 16 Aug 21:30:00 1988 (de_DE)
%x 	    Locale’s appropriate date representation. 	
            08/16/88 (None);
            08/16/1988 (en_US);
            16.08.1988 (de_DE)
%X 	    Locale’s appropriate time representation. 	
            21:30:00 (en_US);
            21:30:00 (de_DE)
%% 	    A literal '%' character. 	%

#Example
>>> import os
>>> s = os.stat("regex.py")
>>> s.st_mtime
1425968214.7254572
>>> import datetime
>>> dt = datetime.datetime.fromtimestamp(s.st_mtime)
>>> str(dt)
'2015-03-10 11:46:54.725457'
>>> delta = datetime.timedelta(days=1)
>>> delta
datetime.timedelta(1)
>>> import time
>>> fd = dt + delta
>>> nt = time.mktime(fd.timetuple())
>>> nt
1426054614.0
>>> os.utime("regex.py", (nt,nt))


>>> from datetime import timedelta
>>> year = timedelta(days=365)
>>> another_year = timedelta(weeks=40, days=84, hours=23, minutes=50, seconds=600)  # adds up to 365 days
>>> year.total_seconds()
31536000.0
>>> year == another_year
True
>>> ten_years = 10 * year
>>> ten_years, ten_years.days // 365
(datetime.timedelta(3650), 10)
>>> nine_years = ten_years - year
>>> nine_years, nine_years.days // 365
(datetime.timedelta(3285), 9)
>>> three_years = nine_years // 3;
>>> three_years, three_years.days // 365
(datetime.timedelta(1095), 3)
>>> abs(three_years - ten_years) == 2 * three_years + year
True

>>> import time
>>> from datetime import date
>>> today = date.today()
>>> today
datetime.date(2007, 12, 5)
>>> today == date.fromtimestamp(time.time())
True
>>> my_birthday = date(today.year, 6, 24)
>>> if my_birthday < today:
        my_birthday = my_birthday.replace(year=today.year + 1)
>>> my_birthday
datetime.date(2008, 6, 24)
>>> time_to_birthday = abs(my_birthday - today)
>>> time_to_birthday.days
202
>>> my_birthday.isoformat()
'2002-03-11'
>>> d.strftime("%d/%m/%y")
'11/03/02'
>>> my_birthday.strftime("%A %d. %B %Y")
'Monday 11. March 2002'
>>> 'The {1} is {0:%d}, the {2} is {0:%B}.'.format(my_birthday, "day", "month")
'The day is 11, the month is March.'

>>> from datetime import datetime, date, time
>>> # Using datetime.combine()
>>> d = date(2005, 7, 14)
>>> t = time(12, 30)
>>> datetime.combine(d, t)
datetime.datetime(2005, 7, 14, 12, 30)
>>> # Using datetime.now() or datetime.utcnow()
>>> datetime.now()   
datetime.datetime(2007, 12, 6, 16, 29, 43, 79043)   # GMT +1
>>> datetime.utcnow()   
datetime.datetime(2007, 12, 6, 15, 29, 43, 79060)
>>> # Using datetime.strptime()
>>> dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
>>> dt
datetime.datetime(2006, 11, 21, 16, 30)
>>> # Using datetime.timetuple() to get tuple of all attributes
>>> tt = dt.timetuple()
>>> for it in tt:   
...     print it
...
2006    # year
11      # month
21      # day
16      # hour
30      # minute
0       # second
1       # weekday (0 = Monday)
325     # number of days since 1st January
-1      # dst - method tzinfo.dst() returned None
>>> # Date in ISO format
>>> ic = dt.isocalendar()
>>> for it in ic:   
...     print it
...
2006    # ISO year
47      # ISO week
2       # ISO weekday
>>> # Formatting datetime
>>> dt.strftime("%A, %d. %B %Y %I:%M%p")
'Tuesday, 21. November 2006 04:30PM'
>>> 'The {1} is {0:%d}, the {2} is {0:%B}, the {3} is {0:%I:%M%p}.'.format(dt, "day", "month", "time")
'The day is 21, the month is November, the time is 04:30PM.'




###HTTP automation 
#Automating HTTP using urllib, urllib2 and httplib
#Py2.x - urllib and urllib2 , renamed in Python 3 to urllib.request, urllib.parse, and urllib.error. 
#Py3.x urllib.request.urlopen() is equivalent to urllib2.urlopen() and urllib.urlopen() has been removed
#Use apache requests for high level API

•urllib.request for opening and reading URLs for file, ftp and http, raises urllib.error
•urllib.parse for parsing URLs
•urllib.robotparser for parsing robots.txt files

#urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)
provide data (must be in bytes) for http POST, use urllib.parse.urlencode({k:v,..})

#example - read() gives in bytes

import urllib.request
with urllib.request.urlopen('http://www.python.org/') as f:
	print(f.read(100).decode('utf-8'))  #can use read() and readline() or can be used as iterator

#Py2.7 
import urllib2
response = urllib2.urlopen('http://python.org/')
html = response.read()
#OR
import urllib2
req = urllib2.Request('http://www.voidspace.org.uk')
response = urllib2.urlopen(req)
the_page = response.read()


#get method
import urllib.request
import urllib.parse
params = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
url = "http://www.musi-cal.com/cgi-bin/query?%s" % params
with urllib.request.urlopen(url) as f:
	print(f.read().decode('utf-8'))

#Py2.7
import urllib2
import urllib
data = {}
data['name'] = 'Somebody Here'
data['location'] = 'Northampton'
data['language'] = 'Python'
url_values = urllib.urlencode(data)
print url_values  # The order may differ. 
#name=Somebody+Here&language=Python&location=Northampton
url = 'http://www.example.com/example.cgi'
full_url = url + '?' + url_values
data = urllib2.urlopen(full_url)
the_page = data.read()





# POST method 
import urllib.request
import urllib.parse
data = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
data = data.encode('ascii')
with urllib.request.urlopen("http://requestb.in/xrbl82xr", data) as f:
	print(f.read().decode('utf-8'))


#py2.7 
import urllib
import urllib2

url = 'http://www.someserver.com/cgi-bin/register.cgi'
values = {'name' : 'Michael Foord',
          'location' : 'Northampton',
          'language' : 'Python' }

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()

#parse method
from urllib.parse import urlparse
o = urlparse('http://www.cwi.nl:80/%7Eguido/Python.html')
>> o
ParseResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
            params='', query='', fragment='')
o.scheme
'http'
o.port
80
o.geturl()
'http://www.cwi.nl:80/%7Eguido/Python.html'

#Other methods 
urllib.parse.quote(string, safe='/', encoding=None, errors=None)
Replace special characters in string using the %xx escape.
Example: quote('/El Niño/') yields '/El%20Ni%C3%B1o/'.

urllib.parse.quote_plus(string, safe='', encoding=None, errors=None)
Like quote(), but also replace spaces by plus signs
as required for quoting HTML form values when building up a query string to go into a URL
Example: quote_plus('/El Niño/') yields '%2FEl+Ni%C3%B1o%2F'.

urllib.parse.unquote(string, encoding='utf-8', errors='replace')
Replace %xx escapes by their single-character equivalent

urllib.parse.unquote_plus(string, encoding='utf-8', errors='replace')
Like unquote(), but also replace plus signs by spaces


#Py2.x httplib module has been renamed to http.client in Python 3
#don't use directly, urllib.request uses httplib to handle URLs that use HTTP and HTTPS
#use 'pip3 install requests' and use requests package in real code




###*Apache requests 
$ pip install requests 

##MAIn API 
requests.request(method, url, **kwargs)
    Constructs and sends a Request.
    Parameters:
        method -- method for the new Request object.
        url -- URL for the new Request object.
        params -- (optional) Dictionary or bytes to be sent in the query string for the Request.
        data -- (optional) Dictionary or list of tuples [(key, value)] (will be form-encoded), bytes, or file-like object to send in the body of the Request.
        json -- (optional) json data to send in the body of the Request.
        headers -- (optional) Dictionary of HTTP Headers to send with the Request.
        cookies -- (optional) Dict or CookieJar object to send with the Request.
        files -- (optional) Dictionary of 'name': file-like-objects (or {'name': file-tuple}) for multipart encoding upload. file-tuple can be a 2-tuple ('filename', fileobj), 3-tuple ('filename', fileobj, 'content_type') or a 4-tuple ('filename', fileobj, 'content_type', custom_headers), where 'content-type' is a string defining the content type of the given file and custom_headers a dict-like object containing additional headers to add for the file.
        auth -- (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
        timeout (float or tuple) -- (optional) How many seconds to wait for the server to send data before giving up, as a float, or a (connect timeout, read timeout) tuple.
        allow_redirects (bool) -- (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to True.
        proxies -- (optional) Dictionary mapping protocol to the URL of the proxy.
        verify -- (optional) Either a boolean, in which case it controls whether we verify the server's TLS certificate, or a string, in which case it must be a path to a CA bundle to use. Defaults to True.
        stream -- (optional) if False, the response content will be immediately downloaded.
        cert -- (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    Returns:
        Response object
        >>> dir(requests.Response)
        ['__attrs__', '__bool__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', 
        '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', 
        '__init__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__nonzero__', '__reduce__', 
        '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', 
        '__weakref__', 'apparent_encoding', 'close', 'content', 'is_permanent_redirect', 'is_redirect', 
        'iter_content', 'iter_lines', 'json', 'links', 'next', 'ok', 'raise_for_status', 'text']

#example
import requests
r = requests.get("http://www.yahoo.com")
r.text
r.status_code   # status code
r.headers  		# dict object

#With HTTPs
>>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'), verify=False) #Requests could verify SSL certificates for https requests automatically and it sets verify=True as default.
>>> r.status_code
200
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> r.encoding
'utf-8'
>>> r.text
u'{"type":"User"...'
>>> r.json()
{u'private_gists': 419, u'total_private_repos': 77, ...}


#with proxy 
p1 = 'http://proxy_username:proxy_password@proxy_server.com:port'
p2 = 'https://proxy_username:proxy_password@proxy_server.com:port'
proxy = {'http': p1, 'https':p2}
r = requests.get(site, proxies=proxy, auth=('site_username', 'site_password')) #Site basic authentication 



##RESTful API
r = requests.post(site)
r = requests.put("site/put")
r = requests.delete("site/delete")
r = requests.head("site/get")
r = requests.options("site/get")


##Get - use 'params'
import requests 
payload1 = {'key1': 'value1', 'key2': 'value2'}
r = requests.get("http://httpbin.org/get", params=payload1)
print(r.url)  #http://httpbin.org/get?key2=value2&key1=value1
r.headers
r.text
r.json()  # it's a python dict

#For Request debugging,
>>> r.request.url
'http://httpbin.org/forms/post?delivery=12&topping=onion&custtel=123&comments=ok&custname=das&custemail=ok%40com&size=small'
>>> r.request.headers
{'Content-Length': '0', 'User-Agent': 'Mozilla/5.0', 'Connection': 'keep-alive', 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate'}
>>> r.request.body


##POST, use 'data'
headers = {'User-Agent': 'Mozilla/5.0'}
payload = {'custname':'das', 'custtel': '123', 'custemail' : 'ok@com', 'size':'small',  'topping':'bacon',  'topping': 'onion',  'delivery':'12', 'comments': 'ok'}
r = requests.post("http://httpbin.org/post", data=payload, headers=headers)
r.text
r.headers
r.json()

r.request.headers
r.request.body #custname=das&custtel=123&custemail=ok@com&size=small&topping=bacon&topping=onion&delivery=12&comments=ok

##Content
r.text
r.content  # as bytes
r.json()  # json content

##Example to handle image Py3
#Install Pillow from http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow , for py2, http://www.pythonware.com/products/pil/

from PIL import Image
from io import BytesIO   
i = Image.open(BytesIO(r.content))



##Download file 
url = 'http://google.com/favicon.ico'
r = requests.get(url, allow_redirects=True)
open('google.ico', 'wb').write(r.content)



##Custom Headers and body 
import json
payload = {'some': 'data'}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(payload), headers=headers)

##POST a Multipart-Encoded File
files = {'file': open('report.xls', 'rb')}
r = requests.post(url, files=files)


##Streaming file 
#"Requests automatically decompresses gzip-encoded responses" 
#but .raw does not handle decoding
import requests
import shutil

def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return local_filename
#for decoding, use 
def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush() 
    return local_filename


##Cookies
#get
r.cookies['example_cookie_name']

#or sending
cookies = dict(cookies_are='working')
r = requests.get(url, cookies=cookies)

##Or persisting across session
s = requests.Session()
s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get("http://httpbin.org/cookies")
r.text # contains cookies from first access


##Example:
import requests
headers = {'User-Agent': 'Mozilla/5.0'}
payload = {'username':'niceusername','pass':'123456'}

session = requests.Session()
session.post('https://admin.example.com/login.php',headers=headers,data=payload)
# the session instance holds the cookie. So use it to get/post later.
# e.g. session.get('https://example.com/profile')



##Example - Form conatins

<textarea id="text" class="wikitext" name="text" cols="80" rows="20">
This is where your edited text will go
</textarea>
<input type="submit" id="save" name="save" value="Submit changes">

#Code:
import requests
from bs4 import BeautifulSoup

url = "http://www.someurl.com"

username = "your_username"
password = "your_password"

session = requests.Session()
session.auth = (username, password)
response = session.get(url, verify=False)

# Getting the text of the page from the response data       
page = BeautifulSoup(response.text)

# Finding the text contained in a specific element, for instance, the 
# textarea element that contains the area where you would write a forum post
txt = page.find('textarea', id="text").string

# Finding the value of a specific attribute with name = "version" and 
# extracting the contents of the value attribute
tag = page.find('input', attrs = {'name':'version'})
ver = tag['value']

# Changing the text to whatever you want
txt = "Your text here, this will be what is written to the textarea for the post"

# construct the POST request
form_data = {
    'save' : 'Submit changes'
    'text' : txt
} 

post = session.post(url,data=form_data,verify=False)


###Http-Auth
$ pip install requests_oauthlib requests_kerberos 

>>> from requests.auth import HTTPBasicAuth
>>> requests.get('https://api.github.com/user', auth=HTTPBasicAuth('user', 'pass'))
<Response [200]>
#OR
>>> requests.get('https://api.github.com/user', auth=('user', 'pass'))
<Response [200]>



>>> from requests.auth import HTTPDigestAuth
>>> url = 'http://httpbin.org/digest-auth/auth/user/pass'
>>> requests.get(url, auth=HTTPDigestAuth('user', 'pass'))
<Response [200]>

#OAuth-1 
#https://requests-oauthlib.readthedocs.io/en/latest/oauth1_workflow.html
>>> import requests
>>> from requests_oauthlib import OAuth1

>>> url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
>>> auth = OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET',
                'USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')

>>> requests.get(url, auth=auth)
<Response [200]>

#OAuth 2 and OpenID Connect Authentication
#https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#web-application-flow

# Credentials you get from registering a new application
client_id = '<the id you get from google>.apps.googleusercontent.com'
client_secret = '<the secret you get from google>'
redirect_uri = 'https://your.registered/callback'

# OAuth endpoints given in the Google API documentation
authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_url = "https://www.googleapis.com/oauth2/v4/token"
scope = [
 "https://www.googleapis.com/auth/userinfo.email",
 "https://www.googleapis.com/auth/userinfo.profile"]


from requests_oauthlib import OAuth2Session
google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

# Redirect user to Google for authorization
authorization_url, state = google.authorization_url(authorization_base_url,
    # offline for refresh token
    # force to always make user click authorize
    access_type="offline", prompt="select_account")
print 'Please go here and authorize,', authorization_url

# Get the authorization verifier code from the callback url
redirect_response = raw_input('Paste the full redirect URL here:')

# Fetch the access token
google.fetch_token(token_url, client_secret=client_secret,
        authorization_response=redirect_response)

# Fetch a protected resource, i.e. user profile
r = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
print r.content

#Kerbos 
#https://github.com/requests/requests-kerberos
>>> import requests
>>> from requests_kerberos import HTTPKerberosAuth, REQUIRED
>>> kerberos_auth = HTTPKerberosAuth(mutual_authentication=REQUIRED, sanitize_mutual_error_response=False)
>>> r = requests.get("https://windows.example.org/wsman", auth=kerberos_auth)

#With explicit principal
>>> import requests
>>> from requests_kerberos import HTTPKerberosAuth, REQUIRED
>>> kerberos_auth = HTTPKerberosAuth(principal="user@REALM")
>>> r = requests.get("http://example.org", auth=kerberos_auth)
...



###XML Processing - Use BeautifulSoup for HTML/XML processing
#no xpath, but css select 
$ pip install BeautifulSoup4
$ pip install requests

#code 
#main attributes of a soup element - .name(for tag) .attrs(for attrib), .text (for text)
# tag['one_attrib'] gives attributes value 
from bs4 import BeautifulSoup
import requests

r  = requests.get("http://www.yahoo.com")
data = r.text

soup = BeautifulSoup(data, "html.parser")
print(soup.prettify())
#extracting all the text from a page:
print(soup.get_text())

#finding all 
#Signature: find_all(name=None, attrs={}, recursive=True, text=None, limit=None **kwargs)
#specify the name of the Tag and any attributes you want the Tag to have.
#name can be a string(inc tag), a regular expression, a list, a function, or the value True.
#The value of a key-value pair in the 'attrs' map can be a string, a list of strings, 
#a regular expression object, or a callable that takes a string and returns whether or not the string matches for some custom definition of 'matches'. 

for link in soup.find_all('a'):  # tag <a href=".."
		print(link.get('href'))	 # Attribute href


##Parser 
#lxml 
#from http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml

#html5lib 
$ pip install html5lib

BeautifulSoup(markup, "html.parser") #default
BeautifulSoup(markup, "lxml")  #very fast 
BeautifulSoup(markup, "lxml-xml")  #only xml parser
BeautifulSoup(markup, "xml")
BeautifulSoup(markup, "html5lib") #creates valid HTML5, •Extremely lenient, very slow


    
##	tag becomes attributes of soup object
soup = BeautifulSoup('<html><body><p class="title">data</p><p class="title">data</p></body></html>', 'html.parser')
#Only first P 
soup.html
soup.html.body.p
soup.html.body.text #or .string
soup.html.body.attrs  #{'class': ['title']}
soup.html.body.name
soup.html.body.p['class']
soup.body
soup.body.attrs
soup.p.text  		# can get all nested .p directly 
#to get all P 
list(soup.html.body.children) #[<p class="title">data</p>, <p class="title">data</p>]
soup.get_text()  
soup.html.name
soup.p.parent.name

##Tag 
soup = BeautifulSoup('<b id="boldest">Extremely bold</b>')
tag = soup.b
type(tag)
# <class 'bs4.element.Tag'>
tag.name
# u'b'
#modify 
tag.name = "blockquote"
tag
# <blockquote id="boldest">Extremely bold</blockquote>

##Attributes like dict 
tag.has_attr('id') #True 
tag['id']
# u'boldest'
tag.attrs
# {u'id': 'boldest'}
#add, remove, and modify a tag’s attributes
tag['id'] = 'verybold'
tag['another-attribute'] = 1
tag
# <b another-attribute="1" id="verybold"></b>

del tag['id']
del tag['another-attribute']
tag
# <b></b>

tag['id']
# KeyError: 'id'
print(tag.get('id'))
# None

##multivalued attribute
# Beautiful Soup presents the value(s) of a multi-valued attribute as a list:

css_soup = BeautifulSoup('<p class="body strikeout"></p>')
css_soup.p['class']
# ["body", "strikeout"]

css_soup = BeautifulSoup('<p class="body"></p>')
css_soup.p['class']
# ["body"]

#for non multivalued, does not convert to list 
id_soup = BeautifulSoup('<p id="my id"></p>')
id_soup.p['id']
# 'my id'


#turn a tag back into a string, multiple attribute values are consolidated:
rel_soup = BeautifulSoup('<p>Back to the <a rel="index">homepage</a></p>')
rel_soup.a['rel']
# ['index']
rel_soup.a['rel'] = ['index', 'contents']
print(rel_soup.p)
# <p>Back to the <a rel="index contents">homepage</a></p>

#use `get_attribute_list to get a value that’s always a list
id_soup.p.get_attribute_list('id') # ['my id']

#for XML, there are no multi-valued attributes:
xml_soup = BeautifulSoup('<p class="body strikeout"></p>', 'xml')
xml_soup.p['class']
# u'body strikeout'

##A string corresponds to  text within a tag
#NavigableString supports most of the features of Navigating the tree and Searching the tree
tag.string
# u'Extremely bold'
type(tag.string)
# <class 'bs4.element.NavigableString'>



##	Pretty-printing
print(soup.prettify())

##Non-pretty printing
print(str(soup))

##Navigating using tag names - other than tags become soup's attributes 
.contents and .children
#A tag’s children are available in a LIST called .contents
#The .contents and .children attributes only consider a tag’s direct children
#Instead of getting as a list, iterate over a tag’s children using the .children generator:
for child in title_tag.children:
    print(child)

    
.descendants
#The .descendants attribute iterates over all of a tag’s children, recursively: 
#its direct children, the children of its direct children, and so on
for child in head_tag.descendants:
    print(child)

.string
#If a tag has only one NavigableString as child
#or tag has one child tag who has another the NavigableString child 
#that is  .string, else it is NOne 

.strings and stripped_strings
#If there’s more than one thing inside a tag, 
# Use the .strings generator or .stripped_strings generator(whitespace removed)
for string in soup.strings:
    print(repr(string))


.parent
#an element’s parent
title_tag = soup.title
title_tag
# <title>The Dormouse's story</title>
title_tag.parent
# <head><title>The Dormouse's story</title></head>
#The title string itself has a parent: the <title> tag that contains it:
title_tag.string.parent
# <title>The Dormouse's story</title>
html_tag = soup.html
type(html_tag.parent)
# <class 'bs4.BeautifulSoup'>
print(soup.parent)
# None


.parents
#iterate over all of an element’s parents 


.next_sibling and .previous_sibling
#navigate to one sibling (elements that are on the same level of the parse tree)
#Example 
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
#Note  .next_sibling of the first <a> tag is not second <a> tag. 
#But actually, it’s a string: the comma and newline that separate the first <a> tag from the second:
link = soup.a
link
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
link.next_sibling
# u',\n'

#The second <a> tag is actually the .next_sibling of the comma:
link.next_sibling.next_sibling
# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>



.next_siblings and .previous_siblings
#iterate all siblings


.next_element and .previous_element
#next or previous element , might not be equivalent to siblings 

.next_elements and .previous_elements
#iterate all elements



s = """<html>
 <head>
  <title>
   Page title
  </title>
 </head>
 <body>
  <p id="firstpara" align="center">
   This is paragraph
   <b>
    one
   </b>
   .
  </p>
  <p id="secondpara" align="blah">
   This is paragraph
   <b>
    two
   </b>
   .
  </p>
 </body>
</html>"""
soup = BeautifulSoup(s)

##	Searching the string
find_all(tag_name, attrs, recursive, text, limit, **kwargs)  #returns list 
find(name, attrs, recursive, string, **kwargs) #returns first element
#The find_all() method looks through a tag’s descendants and retrieves all descendants in a list 
#specify the name of the Tag and any attributes you want the Tag to have.
#name can be a string(inc tag), a regular expression, a list, a function, or the value True.
#The value of a key-value pair in the 'attrs' map can be a string, a list of strings, 
#a regular expression object, or a callable that takes a string and returns whether or not the string matches for some custom definition of 'matches'. The
#The keyword arguments impose restrictions on the attributes of a tag. 


##Using - name 
#String 
#This code finds all the <B> Tags in the document:
soup.findAll('b')
# [<b>one</b>, <b>two</b>]

#RE 
#This code finds all the tags whose names start with B:
import re
tagsStartingWithB = soup.findAll(re.compile('^b'))
[tag.name for tag in tagsStartingWithB]
# [u'body', u'b', u'b']

#list or a dictionary. 
#find all the <TITLE> and all the <P> tags. 
soup.findAll(['title', 'p'])
# [<title>Page title</title>, 
#  <p id="firstpara" align="center">This is paragraph <b>one</b>.</p>, 
#  <p id="secondpara" align="blah">This is paragraph <b>two</b>.</p>]

soup.findAll({'title' : True, 'p' : True})
# [<title>Page title</title>, 
#  <p id="firstpara" align="center">This is paragraph <b>one</b>.</p>, 
#  <p id="secondpara" align="blah">This is paragraph <b>two</b>.</p>]


#True 
#which matches every tag with a name: that is, it matches every tag.
allTags = soup.findAll(True)
[tag.name for tag in allTags]
[u'html', u'head', u'title', u'body', u'p', u'b', u'p', u'b']


#Callable 
#which takes a Tag object as its only argument, and returns a boolean. 
#This code finds the tags that have two, and only two, attributes:
soup.findAll(lambda tag: len(tag.attrs) == 2)
# [<p id="firstpara" align="center">This is paragraph <b>one</b>.</p>, 
#  <p id="secondpara" align="blah">This is paragraph <b>two</b>.</p>]

#This code finds the tags that have one-character names and no attributes:
soup.findAll(lambda tag: len(tag.name) == 1 and not tag.attrs)
# [<b>one</b>, <b>two</b>]



##Using **kwargs
#The keyword arguments impose restrictions on the attributes of a tag. 
#value of keyword can be same like for name arg 

#This simple example finds all the tags with attribs 'align' and it's value 'center'
soup.findAll(align="center")
# [<p id="firstpara" align="center">This is paragraph <b>one</b>.</p>]

#RE 
soup.findAll(id=re.compile("para$"))
# [<p id="firstpara" align="center">This is paragraph <b>one</b>.</p>,
#  <p id="secondpara" align="blah">This is paragraph <b>two</b>.</p>]

#List 
soup.findAll(align=["center", "blah"])
# [<p id="firstpara" align="center">This is paragraph <b>one</b>.</p>,
#  <p id="secondpara" align="blah">This is paragraph <b>two</b>.</p>]

#Callable 
soup.findAll(align=lambda value : value and len(value) < 5)
# [<p id="secondpara" align="blah">This is paragraph <b>two</b>.</p>]

#True and None
#True matches a tag that has any value for the given attribute, 
#and None matches a tag that has no value for the given attribute
soup.findAll(align=True)
# [<p id="firstpara" align="center">This is paragraph <b>one</b>.</p>,
#  <p id="secondpara" align="blah">This is paragraph <b>two</b>.</p>]

[tag.name for tag in soup.findAll(align=None)]
# [u'html', u'head', u'title', u'body', u'b', u'b']

#What if you have a document with a tag that defines an attribute called name? 
#or a Python reserved word like for as a keyword argument.
#Use attrs
#attrs is a dictionary that acts  like the **kwargs, 
#ie can take string, RE, list of String and callable 

soup.findAll(id=re.compile("para$"))
# [<p id="firstpara" align="center">This is paragraph <b>one</b>.</p>,
#  <p id="secondpara" align="blah">This is paragraph <b>two</b>.</p>]

soup.findAll(attrs={'id' : re.compile("para$")})
# [<p id="firstpara" align="center">This is paragraph <b>one</b>.</p>,
#  <p id="secondpara" align="blah">This is paragraph <b>two</b>.</p>]

#with name as attribute (conflicts because find_all has name one of it's arg)
from BeautifulSoup import BeautifulStoneSoup
xml = '<person name="Bob"><parent rel="mother" name="Alice">'
xmlSoup = BeautifulStoneSoup(xml)

xmlSoup.findAll(name="Alice")
# []

xmlSoup.findAll(attrs={"name" : "Alice"})
# [parent rel="mother" name="Alice"></parent>]


##Searching by CSS class - special use of 'string' as attrs arg 
soup.find("tagName", attrs={ "class" : "cssClass" }), 
#OR  pass a string for attrs instead of a dictionary. 
#The string will be used to restrict the CSS class.

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup("""Bob's <b>Bold</b> Barbeque Sauce now available in 
                        <b class="hickory">Hickory</b> and <b class="lime">Lime</a>""")

soup.find("b", { "class" : "lime" })
# <b class="lime">Lime</b>

soup.find("b", "hickory")
# <b class="hickory">Hickory</b>

##text is an argument that lets you search for NavigableString objects instead of Tags. 
#Its value can be a string, a regular expression, a list or dictionary, True or None, 
#or a callable that takes a NavigableString object as its argument
#If you use text, then any values you give for name and the keyword arguments are ignored.

soup.findAll(text="one")
# [u'one']
soup.findAll(text=u'one')
# [u'one']

soup.findAll(text=["one", "two"])
# [u'one', u'two']

soup.findAll(text=re.compile("paragraph"))
# [u'This is paragraph ', u'This is paragraph ']

soup.findAll(text=True)
# [u'Page title', u'This is paragraph ', u'one', u'.', u'This is paragraph ', 
#  u'two', u'.']

soup.findAll(text=lambda x: len(x) < 12)
# [u'Page title', u'one', u'.', u'two', u'.']


##recursive is a boolean argument (defaulting to True) 
#which tells Beautiful Soup whether to go all the way down the parse tree, 
#or whether to only look at the immediate children of the Tag or the parser object.

[tag.name for tag in soup.html.findAll()]
# [u'head', u'title', u'body', u'p', u'b', u'p', u'b']

[tag.name for tag in soup.html.findAll(recursive=False)]
# [u'head', u'body']


##Setting limit argument lets to stop the search once Beautiful Soup finds a certain number of matches. 
#If there are a thousand tables in your document, but you only need the fourth one, pass in 4 to limit 
#By default, there is no limit.

soup.findAll('p', limit=1)
# [<p id="firstpara" align="center">This is paragraph <b>one</b>.</p>]

soup.findAll('p', limit=100)
# [<p id="firstpara" align="center">This is paragraph <b>one</b>.</p>, 
#  <p id="secondpara" align="blah">This is paragraph <b>two</b>.</p>]


##Calling a tag is like calling findall
#If you call the parser object or a Tag like a function, 
#then you can pass in all of findall's arguments and it's the same as calling findall. 

soup(text=lambda x: len(x) < 12)
# [u'Page title', u'one', u'.', u'two', u'.']

soup.body('p', limit=1)
# [<p id="firstpara" align="center">This is paragraph <b>one</b>.</p>]


##Special handling of Some attributes, 
#like the data-* attributes in HTML 5, can not be used 
data_soup = BeautifulSoup('<div data-foo="value">foo!</div>')
data_soup.find_all(data-foo="value")
# SyntaxError: keyword can't be an expression
#use as 
data_soup.find_all(attrs={"data-foo": "value"})
# [<div data-foo="value">foo!</div>]

#special handling of class attribute(use class_)
#you can pass class_ a string, a regular expression, a function, or True:
soup.find_all("a", class_="sister")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.find_all(class_=re.compile("itl"))
# [<p class="title"><b>The Dormouse's story</b></p>]

def has_six_characters(css_class):
    return css_class is not None and len(css_class) == 6

soup.find_all(class_=has_six_characters)

#Maching any of class value 
css_soup = BeautifulSoup('<p class="body strikeout"></p>')
css_soup.find_all("p", class_="strikeout")
# [<p class="body strikeout"></p>]
css_soup.find_all("p", class_="body")
# [<p class="body strikeout"></p>]

#or full value in exact order 
css_soup.find_all("p", class_="body strikeout")
# [<p class="body strikeout"></p>]
#not in other order
css_soup.find_all("p", class_="strikeout body")
# []

#or use css selector where order does not matter 
css_soup.select("p.strikeout.body")
# [<p class="body strikeout"></p>]
#or use attrs 
soup.find_all("a", attrs={"class": "sister"})





##Other find methods - Usage is similar 
find_parents(name, attrs, text, limit, **kwargs)
find_parent(name, attrs, text, **kwargs)

find_next_siblings(name, attrs, text, limit, **kwargs)
find_next_sibling(name, attrs, text, **kwargs)

find_previous_siblings(name, attrs, text, limit, **kwargs)
find_previous_sibling(name, attrs, text, **kwargs)

find_all_next(name, attrs, text, limit, **kwargs)
find_next(name, attrs, text, **kwargs)

find_all_previous(name, attrs, text, limit, **kwargs)
find_previous(name, attrs, text, **kwargs)


##CSS Selector (supports a subset of CSS3)
select( selector, _candidate_generator=None, limit=None)

#Example 
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>"""
soup = BeautifulSoup(html_doc, 'html.parser')


#find tags:
soup.select("title")
# [<title>The Dormouse's story</title>]
soup.select("p:nth-of-type(3)")
# [<p class="story">...</p>]


#Find tags beneath other tags:
soup.select("body a")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie"  id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
soup.select("html head title")
# [<title>The Dormouse's story</title>]

#Find tags directly beneath other tags:
soup.select("head > title")
# [<title>The Dormouse's story</title>]

soup.select("p > a")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie"  id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.select("p > a:nth-of-type(2)")
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]

soup.select("p > #link1")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

soup.select("body > a")
# []

#Find the siblings of tags:
soup.select("#link1 ~ .sister")
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie"  id="link3">Tillie</a>]

soup.select("#link1 + .sister")
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]


#Find tags by CSS class:
soup.select(".sister")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.select("[class~=sister]")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]


#Find tags by ID:
soup.select("#link1")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

soup.select("a#link2")
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]

#Find tags that match any selector from a list of selectors:
soup.select("#link1,#link2") # [<a class=”sister” href=”http://example.com/elsie” id=”link1”>Elsie</a>, # <a class=”sister” href=”http://example.com/lacie” id=”link2”>Lacie</a>]

#Test for the existence of an attribute:
soup.select('a[href]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

#Find tags by attribute value:
soup.select('a[href="http://example.com/elsie"]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

soup.select('a[href^="http://example.com/"]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.select('a[href$="tillie"]')
# [<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.select('a[href*=".com/el"]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]


#Match language codes:
multilingual_soup.select('p[lang|=en]')
# [<p lang="en">Hello</p>,
#  <p lang="en-us">Howdy, y'all</p>,
#  <p lang="en-gb">Pip-pip, old fruit</p>]


#Find only the first tag that matches a selector:
soup.select_one(".sister")
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>




##Changing tag names and attributes
soup = BeautifulSoup('<b class="boldest">Extremely bold</b>')
tag = soup.b

tag.name = "blockquote"
tag['class'] = 'verybold'
tag['id'] = 1
tag
# <blockquote class="verybold" id="1">Extremely bold</blockquote>

del tag['class']
del tag['id']
tag
# <blockquote>Extremely bold</blockquote>



##Modifying .string
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup)

tag = soup.a
tag.string = "New link text."
tag
# <a href="http://example.com/">New link text.</a>

##append()
#append to a tag’s contents
soup = BeautifulSoup("<a>Foo</a>")
soup.a.append("Bar")
soup
# <html><head></head><body><a>FooBar</a></body></html>
soup.a.contents
# [u'Foo', u'Bar']

#to add a string to a document
soup = BeautifulSoup("<b></b>")
tag = soup.b
tag.append("Hello")
new_string = NavigableString(" there")
tag.append(new_string)
tag
# <b>Hello there.</b>
tag.contents
# [u'Hello', u' there']


##to create a comment or some other subclass of NavigableString
from bs4 import Comment
new_comment = Comment("Nice to see you.")
tag.append(new_comment)
tag
# <b>Hello there<!--Nice to see you.--></b>
tag.contents
# [u'Hello', u' there', u'Nice to see you.']


##to create a whole new tag
soup = BeautifulSoup("<b></b>")
original_tag = soup.b

new_tag = soup.new_tag("a", href="http://www.example.com")
original_tag.append(new_tag)
original_tag
# <b><a href="http://www.example.com"></a></b>

new_tag.string = "Link text."
original_tag
# <b><a href="http://www.example.com">Link text.</a></b>

##insert()
#insert at whatever numeric position you say.
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup)
tag = soup.a

tag.insert(1, "but did not endorse ")
tag
# <a href="http://example.com/">I linked to but did not endorse <i>example.com</i></a>
tag.contents
# [u'I linked to ', u'but did not endorse', <i>example.com</i>]



##insert_before() and insert_after()
#inserts a tag or string immediately before/after something else in the parse tree:
soup = BeautifulSoup("<b>stop</b>")
tag = soup.new_tag("i")
tag.string = "Don't"
soup.b.string.insert_before(tag)
soup.b
# <b><i>Don't</i>stop</b>


soup.b.i.insert_after(soup.new_string(" ever "))
soup.b
# <b><i>Don't</i> ever stop</b>
soup.b.contents
# [<i>Don't</i>, u' ever ', u'stop']



##clear()
#removes the contents of a tag:
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup)
tag = soup.a

tag.clear()
tag
# <a href="http://example.com/"></a>


##extract()
#removes a tag or string from the tree
#returns the tag or string that was extracted:
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup)
a_tag = soup.a

i_tag = soup.i.extract()

a_tag
# <a href="http://example.com/">I linked to</a>

i_tag
# <i>example.com</i>

print(i_tag.parent)
None

#two parse trees
my_string = i_tag.string.extract()
my_string
# u'example.com'

print(my_string.parent)
# None
i_tag
# <i></i>



##decompose()
#removes a tag from the tree, then completely destroys it and its contents:
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup)
a_tag = soup.a

soup.i.decompose()

a_tag
# <a href="http://example.com/">I linked to</a>



##replace_with()
# removes a tag or string from the tree, and replaces it with the tag or string of your choice:
#returns the tag or string that was replaced
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup)
a_tag = soup.a

new_tag = soup.new_tag("b")
new_tag.string = "example.net"
a_tag.i.replace_with(new_tag)

a_tag
# <a href="http://example.com/">I linked to <b>example.net</b></a>

##wrap()
#wraps an element in the tag you specify. 
#It returns the new wrapper:
soup = BeautifulSoup("<p>I wish I was bold.</p>")
soup.p.string.wrap(soup.new_tag("b"))
# <b>I wish I was bold.</b>

soup.p.wrap(soup.new_tag("div")
# <div><p><b>I wish I was bold.</b></p></div>


##unwrap()
# opposite of wrap(). 
#It replaces a tag with whatever’s inside that tag. 
#returns the tag that was replaced.
#It’s good for stripping out markup:
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup)
a_tag = soup.a

a_tag.i.unwrap()
a_tag
# <a href="http://example.com/">I linked to example.com</a>



##use Unicode, Dammit without using Beautiful Soup. 
#It’s useful to guess correct encoding of the text 

from bs4 import UnicodeDammit
dammit = UnicodeDammit("Sacr\xc3\xa9 bleu!")
print(dammit.unicode_markup)
# Sacré bleu!
dammit.original_encoding
# 'utf-8'


#Unicode, Dammit’s guesses will get a lot more accurate 
#if you install the chardet or cchardet Python libraries. 

#or can pass few our estimates 
dammit = UnicodeDammit("Sacr\xe9 bleu!", ["latin-1", "iso-8859-1"])
print(dammit.unicode_markup)
# Sacré bleu!
dammit.original_encoding
# 'latin-1'


#use Unicode, Dammit to convert Microsoft smart quotes to HTML or XML entities:
markup = b"<p>I just \x93love\x94 Microsoft Word\x92s smart quotes</p>"

UnicodeDammit(markup, ["windows-1252"], smart_quotes_to="html").unicode_markup
# u'<p>I just &ldquo;love&rdquo; Microsoft Word&rsquo;s smart quotes</p>'

UnicodeDammit(markup, ["windows-1252"], smart_quotes_to="xml").unicode_markup
# u'<p>I just &#x201C;love&#x201D; Microsoft Word&#x2019;s smart quotes</p>'


#to convert Microsoft smart quotes to ASCII quotes:
UnicodeDammit(markup, ["windows-1252"], smart_quotes_to="ascii").unicode_markup
# u'<p>I just "love" Microsoft Word\'s smart quotes</p>'

#Beautiful Soup prefers the default behavior, 
#which is to convert Microsoft smart quotes to Unicode characters along with everything else:
UnicodeDammit(markup, ["windows-1252"]).unicode_markup
# u'<p>I just \u201clove\u201d Microsoft Word\u2019s smart quotes</p>'


##Inconsistent encodings
#Sometimes a document is mostly in UTF-8, 
#but contains Windows-1252 characters such as  Microsoft smart quotes. 


snowmen = (u"\N{SNOWMAN}" * 3)
quote = (u"\N{LEFT DOUBLE QUOTATION MARK}I like snowmen!\N{RIGHT DOUBLE QUOTATION MARK}")
doc = snowmen.encode("utf8") + quote.encode("windows_1252")
#messy display 
print(doc)
# ????I like snowmen!?
print(doc.decode("windows-1252"))
# â˜ƒâ˜ƒâ˜ƒ“I like snowmen!”

#use UnicodeDammit.detwingle() 
new_doc = UnicodeDammit.detwingle(doc)
print(new_doc.decode("utf8"))
# ???“I like snowmen!”


##Copying Beautiful Soup objects
import copy
p_copy = copy.copy(soup.p)
print p_copy
# <p>I want <b>pizza</b> and more <b>pizza</b>!</p>

print soup.p == p_copy
# True

print soup.p is p_copy
# False

##Comparing objects for equality
#content checking 
markup = "<p>I want <b>pizza</b> and more <b>pizza</b>!</p>"
soup = BeautifulSoup(markup, 'html.parser')
first_b, second_b = soup.find_all('b')
print first_b == second_b
# True

print first_b.previous_element == second_b.previous_element
# False

##Parsing only part of a document - use SoupStrainer
from bs4 import SoupStrainer

only_a_tags = SoupStrainer("a")

only_tags_with_id_link2 = SoupStrainer(id="link2")

def is_short_string(string):
    return len(string) < 10

only_short_strings = SoupStrainer(string=is_short_string)


html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

print(BeautifulSoup(html_doc, "html.parser", parse_only=only_a_tags).prettify())
# <a class="sister" href="http://example.com/elsie" id="link1">
#  Elsie
# </a>
# <a class="sister" href="http://example.com/lacie" id="link2">
#  Lacie
# </a>
# <a class="sister" href="http://example.com/tillie" id="link3">
#  Tillie
# </a>

print(BeautifulSoup(html_doc, "html.parser", parse_only=only_tags_with_id_link2).prettify())
# <a class="sister" href="http://example.com/lacie" id="link2">
#  Lacie
# </a>

print(BeautifulSoup(html_doc, "html.parser", parse_only=only_short_strings).prettify())
# Elsie
# ,
# Lacie
# and
# Tillie
# ...
#


#You can also pass a SoupStrainer into any of the methods covered in Searching the tree. 
soup = BeautifulSoup(html_doc)
soup.find_all(only_short_strings)
# [u'\n\n', u'\n\n', u'Elsie', u',\n', u'Lacie', u' and\n', u'Tillie',
#  u'\n\n', u'...', u'\n']





###*Web Scraping using Scrapy 

$ pip install scrapy

#Install pywin32 from https://sourceforge.net/projects/pywin32/files/pywin32/


###Scrapy - Archiecture 
#Diagram 
https://doc.scrapy.org/en/latest/topics/architecture.html#data-flow

##The data flow in Scrapy is controlled by the execution engine, 
1.The Engine gets the initial Requests to crawl from the Spider.
2.The Engine schedules the Requests in the Scheduler 
  and asks for the next Requests to crawl.
3.The Scheduler returns the next Requests to the Engine.
4.The Engine sends the Requests to the Downloader, 
  passing through the Downloader Middlewares 
5.Once the page finishes downloading the Downloader generates a Response 
  (with that page) and sends it to the Engine, passing through the Downloader Middlewares 
6.The Engine receives the Response from the Downloader 
  and sends it to the Spider for processing, passing through the Spider Middleware 
7.The Spider processes the Response and returns scraped items 
  and new Requests (to follow) to the Engine, passing through the Spider Middleware 
8.The Engine sends processed items to Item Pipelines, 
  then send processed Requests to the Scheduler and asks for possible next Requests to crawl.
9.The process repeats (from step 1) until there are no more requests from the Scheduler.

    








###*Scrapy -  projects 


$ scrapy startproject quotesproject

#Check all files generated 
quotesproject
+-- quotesproject
¦   +-- __init__.py
¦   +-- __pycache__
¦   +-- items.py
¦   +-- middlewares.py
¦   +-- pipelines.py
¦   +-- settings.py
¦   +-- spiders
¦       +-- __init__.py
¦       +-- __pycache__
+-- scrapy.cfg



#Requests are scheduled and processed asynchronously

#CSS -> ::text , ::attr('attribute') css pseudo selector returns text and attribute value 
#XPATH -> text() and @attribute 

#Create below files 
#spiders/toscrape-xpath.py : for spider name toscrape-xpath
import scrapy

#derive from Spider 
class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = [                          #one by one, each URL is downloaded
        'http://quotes.toscrape.com/',
    ]

    #and parsed by below function 
    #response is instance of scrapy.http.Response
    #parse must return dict of items or a Request, which would be followed 
    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
                'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
                'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            }

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        #callback by default is self.parse, hence can be omitted 
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)




#spiders/toscrape-css.py : for spider name toscrape-css
import scrapy


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").extract_first(),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags > a.tag::text").extract()
            }

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        #alternate form of following 
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)


##Alternate form of following 

#pass a selector to response.follow instead of a string
for href in response.css('li.next a::attr(href)'):
    yield response.follow(href, callback=self.parse)


#For <a> elements , response.follow uses their href attribute automatically
for a in response.css('li.next a'):
    yield response.follow(a, callback=self.parse)



##Execution 
# use --nolog  for no log output 
$ cd quotesproject
$ scrapy crawl toscrape-css
$ scrapy crawl toscrape-xpath -o quotes.json


###Scrapy - Example - without Creating project 


#change the export format (XML or CSV, for example) or the storage backend (FTP or Amazon S3, for example).
$ scrapy runspider quotesproject\spiders\toscrape-css.py -o quotes1.json
$ scrapy runspider quotesproject\spiders\toscrape-css.py -o quotes1.csv
$ scrapy runspider quotesproject\spiders\toscrape-css.py -o quotes1.xml



###Scrapy - Multiple callbacks and following links

# + Sign:
#It is Adjacent sibling combinator. 
#It combines two sequences of simple selectors having the same parent 
#and the second one must come IMMEDIATELY after the first.

import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('.author + a::attr(href)'):
            yield response.follow(href, self.parse_author)

        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }


###Scrapy - Using spider arguments
$ scrapy crawl quotes -o quotes-humor.json -a tag=humor

#arguments for option -a 
#are passed to the Spider’s __init__ method 
#and become spider attributes by default

#'tag' becomes one attribute of Spider 

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    
    #Alternate form of start_urls 
    #start_request must yield Request object or returns list of those 
    #The default implementation generates Request(url, dont_filter=True) for each url in start_urls.
    #called only once 
    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None) #gets from command line 
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


###*Scrapy - commandline 
#https://doc.scrapy.org/en/latest/topics/commands.html


$ scrapy -h


##Create a new spider in the current folder or in the current project’s spiders folder, 

#csvfeed parses csv file , xmlfeed parses xml file 

$ scrapy genspider -l
Available templates:
  basic
  crawl
  csvfeed
  xmlfeed

$ scrapy genspider example example.com
Created spider 'example' using template 'basic'

$ scrapy genspider -t crawl scrapyorg scrapy.org
Created spider 'scrapyorg' using template 'crawl'




###Scrapy - Spider Details 

class scrapy.spiders.Spider 
    It just provides a default start_requests() implementation 
    which sends requests from the start_urls spider attribute 
    and calls the spider’s method parse for each of the resulting responses.

    name
        A string which defines the name for this spider.
    allowed_domains
       An optional list of strings containing domains 
       that this spider is allowed to crawl.         
    start_urls
        A list of URLs where the spider will begin to crawl from      
    custom_settings
        A dictionary of settings specific to this spider     
    logger
        Python logger created with the Spider’s name  
    start_requests()
        This method must return an iterable with the first Requests to crawl for this spider.
    parse(response)
        This is the default callback used by Scrapy to process downloaded responses, 
    log(message[, level, component])
        Wrapper that sends a log message through the Spider’s logger    
    closed(reason)
        Called when the spider closes.    
    

##Spider Generic Spiders - CrawlSpider
#inherited from Spider 

#Example uses below 
#myproject.items module:

import scrapy
class TestItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()



class scrapy.spiders.CrawlSpider
    for crawling regular websites, 
    it provides a mechanism for following links by defining a set of rules. 
    
    rules
        Which is a list of one (or more) Rule objects.    
    parse_start_url(response)
        This method is called for the start_urls responses. 
        It allows to parse the initial responses 
        and must return either an Item object, 
        a Request object, or an iterable containing any of them.

class scrapy.spiders.Rule(link_extractor, callback=None, 
        cb_kwargs=None, follow=None, process_links=None, 
        process_request=None)

    link_extractor is a Link Extractor object 
    which defines how links will be extracted from each crawled page.

    When writing crawl spider rules, avoid using 'parse' as callback, 
    since the CrawlSpider uses the parse method itself to implement its logic   
   
    callback is a callable or a string (in which case a method from the spider object with that name will be used) 
    to be called for each link extracted with the specified link_extractor. 
    
    This callback receives a response as its first argument 
    and must return a list containing Item and/or Request objects 
    (or any subclass of them).
    
    cb_kwargs is a dict containing the keyword arguments to be passed to the callback function.

    follow is a boolean which specifies if links should be followed 
    from each response extracted with this rule. 
    
    If callback is None follow defaults to True, 
    otherwise it defaults to False.

    process_links is a callable, or a string (in which case a method from the spider object with that name will be used) 
    which will be called for each list of links extracted 
    from each response using the specified link_extractor. 
    This is mainly used for filtering purposes.

    process_request is a callable, or a string (in which case a method from the spider object with that name will be used) 
    which will be called with every request extracted by this rule, 
    and must return a request or None (to filter out the request).
    
    
##Link Extractors
#The default link extractor is LinkExtractor/LxmlLinkExtractor:

from scrapy.linkextractors import LinkExtractor

class scrapy.linkextractors.lxmlhtml.LxmlLinkExtractor(allow=(), deny=(),
    allow_domains=(), deny_domains=(), deny_extensions=None, 
    restrict_xpaths=(), restrict_css=(), tags=('a', 'area'), 
    attrs=('href', ), canonicalize=False, unique=True, 
    process_value=None, strip=True)
    
    allow (a regular expression (or list of)) 
        a single regular expression (or list of regular expressions) 
        that the (absolute) urls must match in order to be extracted. 
        If not given (or empty), it will match all links.
    deny (a regular expression (or list of)) 
        a single regular expression (or list of regular expressions) 
        that the (absolute) urls must match in order to be excluded 
        (ie. not extracted). 
        It has precedence over the allow parameter. 
        If not given (or empty) it won’t exclude any links.
    allow_domains (str or list) 
        a single value or a list of string containing domains 
        which will be considered for extracting the links
    deny_domains (str or list)
        a single value or a list of strings containing domains 
        which won’t be considered for extracting the links
    deny_extensions (list)
        a single value or list of strings containing extensions 
        that should be ignored when extracting links. 
        If not given, it will default to the IGNORED_EXTENSIONS list defined in the scrapy.linkextractors package.
    restrict_xpaths (str or list) 
        an XPath (or list of XPath’s) which defines regions 
        inside the response where links should be extracted from. 
        If given, only the text selected by those XPath will be scanned for links. 
    restrict_css (str or list)
        a CSS selector (or list of selectors) 
        which defines regions inside the response where links should be extracted from. 
        Has the same behaviour as restrict_xpaths.
    tags (str or list) 
        a tag or a list of tags to consider when extracting links. 
        Defaults to ('a', 'area').
    attrs (list)
        an attribute or list of attributes which should be considered 
        when looking for links to extract 
        (only for those tags specified in the tags parameter). 
        Defaults to ('href',)
    strip (boolean) 
            whether to strip whitespaces from extracted attributes. 
    process_value (callable) 
        a function which receives each value extracted 
        from the tag and attributes scanned 
        and can modify the value and return a new one, 
        or return None to ignore the link altogether. 
        If not given, process_value defaults to lambda x: x
        
        For example, to extract links from this code:
        <a href="javascript:goToPage('../other/page.html'); return false">Link text</a>
        def process_value(value):
            m = re.search("javascript:goToPage\('(.*?)'", value)
            if m:
                return m.group(1)


 

##CrawlSpider - Example 

#myproject.items module:

import scrapy

class TestItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()


#spider code 
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = scrapy.Item()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item

        
    
##Other Generic Spider 
#https://doc.scrapy.org/en/latest/topics/spiders.html#xmlfeedspider

class scrapy.spiders.XMLFeedSpider
    XMLFeedSpider is designed for parsing XML feeds by iterating 
    through them by a certain node name. 

class scrapy.spiders.CSVFeedSpider
    This spider is very similar to the XMLFeedSpider, 
    except that it iterates over rows, instead of nodes. 
    The method that gets called in each iteration is parse_row().

class scrapy.spiders.SitemapSpider
    SitemapSpider allows you to crawl a site by discovering the URLs using Sitemaps.
    It supports nested sitemaps and discovering sitemap urls from robots.txt.





###Scrapy - Request objects
#Request objects are generated in the spiders 
#and pass across the system until they reach the Downloader, 
#which executes the request and returns a Response object 
#which travels back to the spider that issued the request.



class scrapy.http.Request(url[, callback, method='GET', 
        headers, body, cookies, meta, encoding='utf-8', 
        priority=0, dont_filter=False, errback, flags])

    url (string) 
        the URL of this request
    callback (callable) 
        the function that will be called with the response of this request 
    method (string)
        the HTTP method of this request. Defaults to 'GET'.
    meta (dict) 
        the initial values for the Request.meta attribute. 
        If given, the dict passed in this parameter will be shallow copied.
        The Request.meta attribute can contain any arbitrary data, but there are some special keys recognized by Scrapy and its built-in extensions.
        https://doc.scrapy.org/en/latest/topics/request-response.html#topics-request-meta
    body (str or unicode) 
        the request body
    headers (dict) 
        the headers of this request. 
        The dict values can be strings (for single valued headers) 
        or lists (for multi-valued headers). 


##Using a dict as cookies 

request_with_cookies = Request(url="http://www.example.com",
                               cookies={'currency': 'USD', 'country': 'UY'})

##Using a list of dicts:

request_with_cookies = Request(url="http://www.example.com",
                               cookies=[{'name': 'currency',
                                        'value': 'USD',
                                        'domain': 'example.com',
                                        'path': '/currency'}])

#By Default 
#When some site returns cookies (in a response) 
#those are stored in the cookies for that domain 
#and will be sent again in future requests. 

#to avoid  merging with existing cookies 
#set dont_merge_cookies key to True in the Request.meta

request_with_cookies = Request(url="http://www.example.com",
                               cookies={'currency': 'USD', 'country': 'UY'},
                               meta={'dont_merge_cookies': True})


##Request.meta - Passing additional data to callback functions

def parse_page1(self, response):
    return scrapy.Request("http://www.example.com/some_page.html",
                          callback=self.parse_page2)

def parse_page2(self, response):
    # this would log http://www.example.com/some_page.html
    self.logger.info("Visited %s", response.url)

#to get a user defined value to parse_page2
#use the Request.meta 

#example of how to pass an item using this mechanism, 
#to populate different fields from different pages:

def parse_page1(self, response):
    item = MyItem()
    item['main_url'] = response.url
    request = scrapy.Request("http://www.example.com/some_page.html",
                             callback=self.parse_page2)
    request.meta['item'] = item
    yield request

def parse_page2(self, response):
    item = response.meta['item']
    item['other_url'] = response.url
    yield item

    
##Using errbacks to catch exceptions in request processing
#The errback of a request is a function that will be called 
#when an exception is raise while processing it.


import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class ErrbackSpider(scrapy.Spider):
    name = "errback_example"
    start_urls = [
        "http://www.httpbin.org/",              # HTTP 200 expected
        "http://www.httpbin.org/status/404",    # Not found error
        "http://www.httpbin.org/status/500",    # server issue
        "http://www.httpbin.org:12345/",        # non-responding host, timeout expected
        "http://www.httphttpbinbin.org/",       # DNS error expected
    ]

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_httpbin,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)

    def parse_httpbin(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        # do something useful here...

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)


##Request subclasses - FormRequest
        
class scrapy.http.FormRequest(url[, formdata, ...])
    classmethod from_response(response[, formname=None, formid=None, 
    formnumber=0, formdata=None, formxpath=None, formcss=None, 
    clickdata=None, dont_click=False, ...]) 
        Returns a new FormRequest object with its form field values 
        pre-populated with those found in the HTML <form> element 
        contained in the given response


##Using FormRequest to send data via HTTP POST

return [FormRequest(url="http://www.example.com/post/action",
                    formdata={'name': 'John Doe', 'age': '27'},
                    callback=self.after_post)]

##Using FormRequest.from_response() to simulate a user login
#It is usual for web sites to provide pre-populated form fields 
#through <input type="hidden"> elements, 
#such as session related data or authentication tokens (for login pages).

#When scraping, you’ll want these fields to be automatically pre-populated 
#and only override a couple of them, 
#such as the user name and password. 


import scrapy

class LoginSpider(scrapy.Spider):
    name = 'example.com'
    start_urls = ['http://www.example.com/users/login.php']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'john', 'password': 'secret'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return

        # continue scraping with authenticated session...

        
        
        
###Scrapy - Response objects

class scrapy.http.Response(url[, status=200, headers=None, 
    body=b'', flags=None, request=None])

    url
        A string containing the URL of the response.
        This attribute is read-only. 
        To change the URL of a Response use replace().
    status
        An integer representing the HTTP status of the response. 
        Example: 200, 404.
    headers
        A dictionary-like object which contains the response headers. 
        Values can be accessed using get() to return the first header value with the specified name 
        or getlist() to return all header values with the specified name. 
        For example, this call will give you all cookies in the headers:
        response.headers.getlist('Set-Cookie')
    body
        The body of this Response. 
        Response.body is always a bytes object. 
        If you want the unicode version use TextResponse.text 
        (only available in TextResponse and subclasses).   
    request
        The Request object that generated this response.
    meta
        A shortcut to the Request.meta attribute of the Response.request object 
        (ie. self.request.meta).        
    flags
        A list that contains flags for this response. 
        Flags are labels used for tagging Responses. 
        For example: ‘cached’, ‘redirected‘, etc. 
        And they’re shown on the string representation of the Response (__str__ method) 
    copy()
    replace([url, status, headers, body, request, flags, cls])
        Returns a Response object with the same members, 
        except for those members given new values 
        by whichever keyword arguments are specified. 
        The attribute Response.meta is copied by default.
    urljoin(url)
        Constructs an absolute url by combining the Response’s url 
        with a possible relative url.
        This is a wrapper over urlparse.urljoin
        urlparse.urljoin(response.url, url)
    follow(url, callback=None, method='GET', headers=None, 
        body=None, cookies=None, meta=None, encoding='utf-8', 
        priority=0, dont_filter=False, errback=None)
        Return a Request instance to follow a link url. 
        It accepts the same arguments as Request.__init__ method, 
        but url can be a relative URL or a scrapy.link.Link object, 
        or absolute URL.
        TextResponse provides a follow() method which supports selectors 
        in addition to absolute/relative URLs and Link objects.

        
##Response subclasses - TextResponse

class scrapy.http.TextResponse(url[, encoding[, ...]])
    TextResponse objects adds encoding capabilities to the base Response class, 
    which is meant to be used only for binary data, 
    such as images, sounds or any media file.
    
    text
        Response body, as unicode.
        The same as response.body.decode(response.encoding), 
        but the result is cached after the first call, 
    encoding
        A string with the encoding of this response.
        this is resolved automatically 
    selector 
        A Selector instance using the response as target
    xpath(query)
        A shortcut to TextResponse.selector.xpath(query):
        response.xpath('//p')
    css(query)
        A shortcut to TextResponse.selector.css(query):
        response.css('p')
    follow(url, callback=None, method='GET', headers=None, body=None, 
        cookies=None, meta=None, encoding=None, priority=0, 
        dont_filter=False, errback=None)
        Return a Request instance to follow a link url. 
        It accepts the same arguments as Request.__init__ method, 
        but url can be not only an absolute URL, but also
            a relative URL;
            a scrapy.link.Link object (e.g. a link extractor result);
            an attribute Selector (not SelectorList) 
            - e.g. response.css('a::attr(href)')[0] 
            or response.xpath('//img/@src')[0].
            a Selector for <a> or <link> element, 
            e.g. response.css('a.my_link')[0].


class scrapy.http.HtmlResponse(url[, ...])
    The HtmlResponse class is a subclass of TextResponse 
    which adds encoding auto-discovering support by looking 
    into the HTML meta http-equiv attribute. 

class scrapy.http.XmlResponse(url[, ...])
    The XmlResponse class is a subclass of TextResponse 
    which adds encoding auto-discovering support by looking 
    into the XML declaration line

    
##Response type is auto resolved 
#from_headers
({'Content-Type': ['text/html; charset=utf-8']}, HtmlResponse),
({'Content-Type': ['application/octet-stream'], 'Content-Disposition': ['attachment; filename=data.txt']}, TextResponse),
({'Content-Type': ['text/html; charset=utf-8'], 'Content-Encoding': ['gzip']}, Response),

#From body 
('\x03\x02\xdf\xdd\x23', Response),
('Some plain text\ndata with tabs\t and null bytes\0', TextResponse),
('<html><head><title>Hello</title></head>', HtmlResponse),
('<?xml version="1.0" encoding="utf-8"', XmlResponse),

#from file name 
('data.bin', Response),
('file.txt', TextResponse),
('file.xml.gz', Response),
('file.xml', XmlResponse),
('file.html', HtmlResponse),
('file.unknownext', Response),

            

    
###Scrapy- Selectors
#do not use the HtmlXPathSelector anymore,
#Use Selector which includes methods for both xpath() and css(). 



class scrapy.selector.Selector(response=None, text=None, type=None)
    response is an HtmlResponse or an XmlResponse object
    text is a unicode string or utf-8 encoded text if response is not given 
    type defines the selector type, it can be "html", "xml" or None (default).
    If type is None, the selector automatically chooses the best type based on response type 
    xpath(query)
        Find nodes matching the xpath query 
        and return the result as a SelectorList instance 
    css(query)
        Apply the given CSS selector and return a SelectorList instance.
    extract()
        Serialize 
        and return the matched nodes as a list of unicode strings. 
    re(regex)
        Apply the given regex 
        and return a list of unicode strings with the matches.
    register_namespace(prefix, uri)
        Register the given namespace to be used in this Selector. 
        Without registering namespaces you can’t select or extract data from non-standard namespaces. 
        See examples below.
    remove_namespaces()
        Remove all namespaces, 
        allowing to traverse the document using namespace-less xpaths. 

class scrapy.selector.SelectorList
    The SelectorList class is a subclass of the builtin list class
    xpath(query)
        Call the .xpath() method for each element in this list 
        and return their results flattened as another SelectorList.
    css(query)
        Call the .css() method for each element in this list 
        and return their results flattened as another SelectorList.
    extract()
        Call the .extract() method for each element in this list 
        and return their results flattened, as a list of unicode strings.
    re()
        Call the .re() method for each element in this list 
        and return their results flattened, as a list of unicode strings.




##Quick example 
##Summary 
sel = Selector(html_response)

#Select all <h1> elements from an HTML response body, 
#returning a list of Selector objects (ie. a SelectorList object):

sel.xpath("//h1")

#Extract the text of all <h1> elements from an HTML response body, 
#returning a list of unicode strings:

sel.xpath("//h1").extract()         # this includes the h1 tag
sel.xpath("//h1/text()").extract()  # this excludes the h1 tag

#Iterate over all <p> tags and print their class attribute:

for node in sel.xpath("//p"):
    print node.xpath("@class").extract()



##Selector examples on XML response

sel = Selector(xml_response)

#Select all <product> elements from an XML response body, 
#returning a list of Selector objects (ie. a SelectorList object):

sel.xpath("//product")

#Extract all prices from a Google Base XML feed 
#which requires registering a namespace:

sel.register_namespace("g", "http://base.google.com/ns/1.0")
sel.xpath("//g:price").extract()

        
        

###*Scrapy selectors are built over the lxml library
#It automatically chooses the best parsing rules (XML vs HTML) based on input type:

>>> from scrapy.selector import Selector
>>> from scrapy.http import HtmlResponse

##Constructing from text:

>>> body = '<html><body><span>good</span></body></html>'
>>> Selector(text=body).xpath('//span/text()').extract()
[u'good']

##Constructing from response:

>>> response = HtmlResponse(url='http://example.com', body=body)
>>> Selector(response=response).xpath('//span/text()').extract()
[u'good']

#response objects expose a selector on .selector attribute
>>> response.selector.xpath('//span/text()').extract()
[u'good']

##Using selectors
#from below 
    http://doc.scrapy.org/en/latest/_static/selectors-sample1.html

#HTML code:
<html>
 <head>
  <base href='http://example.com/' />
  <title>Example website</title>
 </head>
 <body>
  <div id='images'>
   <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' /></a>
   <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
   <a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>
   <a href='image4.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' /></a>
   <a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>
  </div>
 </body>
</html>

$ scrapy shell http://doc.scrapy.org/en/latest/_static/selectors-sample1.html

>>> response.selector.xpath('//title/text()')
[<Selector (text) xpath=//title/text()>]

#or directly 
>>> response.xpath('//title/text()')
[<Selector (text) xpath=//title/text()>]
>>> response.css('title::text')
[<Selector (text) xpath=//title/text()>]

#can be chained 
>>> response.css('img').xpath('@src').extract()
[u'image1_thumb.jpg',
 u'image2_thumb.jpg',
 u'image3_thumb.jpg',
 u'image4_thumb.jpg',
 u'image5_thumb.jpg']

#To actually extract the textual data
>>> response.xpath('//title/text()').extract()
[u'Example website']

#to extract only first matched element
>>> response.xpath('//div[@id="images"]/a/text()').extract_first()
u'Name: My image 1 '

#It returns None if no element was found:
>>> response.xpath('//div[@id="not-exists"]/text()').extract_first() is None
True

#A default return value can be provided as an argument
>>> response.xpath('//div[@id="not-exists"]/text()').extract_first(default='not-found')
'not-found'

#CSS selectors can select text or attribute nodes using CSS3 pseudo-elements:
>>> response.css('title::text').extract()
[u'Example website']

>>> response.xpath('//base/@href').extract()
[u'http://example.com/']

>>> response.css('base::attr(href)').extract()
[u'http://example.com/']

>>> response.xpath('//a[contains(@href, "image")]/@href').extract()
[u'image1.html',
 u'image2.html',
 u'image3.html',
 u'image4.html',
 u'image5.html']

>>> response.css('a[href*=image]::attr(href)').extract()
[u'image1.html',
 u'image2.html',
 u'image3.html',
 u'image4.html',
 u'image5.html']

>>> response.xpath('//a[contains(@href, "image")]/img/@src').extract()
[u'image1_thumb.jpg',
 u'image2_thumb.jpg',
 u'image3_thumb.jpg',
 u'image4_thumb.jpg',
 u'image5_thumb.jpg']

>>> response.css('a[href*=image] img::attr(src)').extract()
[u'image1_thumb.jpg',
 u'image2_thumb.jpg',
 u'image3_thumb.jpg',
 u'image4_thumb.jpg',
 u'image5_thumb.jpg']

##Nesting selectors

>>> links = response.xpath('//a[contains(@href, "image")]')
>>> links.extract()
[u'<a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg"></a>',
 u'<a href="image2.html">Name: My image 2 <br><img src="image2_thumb.jpg"></a>',
 u'<a href="image3.html">Name: My image 3 <br><img src="image3_thumb.jpg"></a>',
 u'<a href="image4.html">Name: My image 4 <br><img src="image4_thumb.jpg"></a>',
 u'<a href="image5.html">Name: My image 5 <br><img src="image5_thumb.jpg"></a>']

>>> for index, link in enumerate(links):
        args = (index, link.xpath('@href').extract(), link.xpath('img/@src').extract())
        print 'Link number %d points to url %s and image %s' % args

Link number 0 points to url [u'image1.html'] and image [u'image1_thumb.jpg']
Link number 1 points to url [u'image2.html'] and image [u'image2_thumb.jpg']
Link number 2 points to url [u'image3.html'] and image [u'image3_thumb.jpg']
Link number 3 points to url [u'image4.html'] and image [u'image4_thumb.jpg']
Link number 4 points to url [u'image5.html'] and image [u'image5_thumb.jpg']

##Using selectors with regular expressions
#you can’t construct nested .re() calls.

>>> response.xpath('//a[contains(@href, "image")]/text()').re(r'Name:\s*(.*)')
[u'My image 1',
 u'My image 2',
 u'My image 3',
 u'My image 4',
 u'My image 5']

#to extract just the first matching string:

>>> response.xpath('//a[contains(@href, "image")]/text()').re_first(r'Name:\s*(.*)')
u'My image 1'

##Working with relative XPaths

#use an XPath that starts with /, 
#that XPath will be absolute to the document 

#to extract all <p> elements inside <div> elements. 
#First, you would get all <div> elements:
>>> divs = response.xpath('//div')

#then below is wrong 
>>> for p in divs.xpath('//p'):  # this is wrong - gets all <p> from the whole document
        print p.extract()

#correct way is 
>>> for p in divs.xpath('.//p'):  # extracts all <p> inside
...     print p.extract()

#to extract all direct <p> children:
>>> for p in divs.xpath('p'):
        print p.extract()

##Variables in XPath expressions

>>> # `$val` used in the expression, a `val` argument needs to be passed
>>> response.xpath('//div[@id=$val]/a/text()', val='images').extract_first()
u'Name: My image 1 '

#to find the “id” attribute of a <div> tag containing five <a> children (here we pass the value 5 as an integer):

>>> response.xpath('//div[count(a)=$cnt]/@id', cnt=5).extract_first()
u'images'






##Using EXSLT extensions
prefix 	namespace 	                            usage
re 	    http://exslt.org/regular-expressions 	regular expressions
set 	http://exslt.org/sets 	                set manipulation

##Using EXSLT extensions - Regular expressions

#when XPath’s starts-with() or contains() are not sufficient
#use re::test()

#Example selecting links in list item with a “class” attribute ending with a digit:

>>> from scrapy import Selector
>>> doc = """
    <div>
        <ul>
            <li class="item-0"><a href="link1.html">first item</a></li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-inactive"><a href="link3.html">third item</a></li>
            <li class="item-1"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
    """
>>> sel = Selector(text=doc, type="html")
>>> sel.xpath('//li//@href').extract()
[u'link1.html', u'link2.html', u'link3.html', u'link4.html', u'link5.html']
>>> sel.xpath('//li[re:test(@class, "item-\d$")]//@href').extract()
[u'link1.html', u'link2.html', u'link4.html', u'link5.html']
>>>

##Using EXSLT extensions - Set operations

#for excluding parts of a document tree before extracting text elements

#Example extracting microdata with groups of itemscopes and corresponding itemprops:

>>> doc = """
    <div itemscope itemtype="http://schema.org/Product">
    <span itemprop="name">Kenmore White 17" Microwave</span>
    <img src="kenmore-microwave-17in.jpg" alt='Kenmore 17" Microwave' />
    <div itemprop="aggregateRating"
        itemscope itemtype="http://schema.org/AggregateRating">
    Rated <span itemprop="ratingValue">3.5</span>/5
    based on <span itemprop="reviewCount">11</span> customer reviews
    </div>
    
    <div itemprop="offers" itemscope itemtype="http://schema.org/Offer">
        <span itemprop="price">$55.00</span>
        <link itemprop="availability" href="http://schema.org/InStock" />In stock
    </div>
    
    Product description:
    <span itemprop="description">0.7 cubic feet countertop microwave.
    Has six preset cooking categories and convenience features like
    Add-A-Minute and Child Lock.</span>
    
    Customer reviews:
    
    <div itemprop="review" itemscope itemtype="http://schema.org/Review">
        <span itemprop="name">Not a happy camper</span> -
        by <span itemprop="author">Ellie</span>,
        <meta itemprop="datePublished" content="2011-04-01">April 1, 2011
        <div itemprop="reviewRating" itemscope itemtype="http://schema.org/Rating">
        <meta itemprop="worstRating" content = "1">
        <span itemprop="ratingValue">1</span>/
        <span itemprop="bestRating">5</span>stars
        </div>
        <span itemprop="description">The lamp burned out and now I have to replace
        it. </span>
    </div>
    
    <div itemprop="review" itemscope itemtype="http://schema.org/Review">
        <span itemprop="name">Value purchase</span> -
        by <span itemprop="author">Lucas</span>,
        <meta itemprop="datePublished" content="2011-03-25">March 25, 2011
        <div itemprop="reviewRating" itemscope itemtype="http://schema.org/Rating">
        <meta itemprop="worstRating" content = "1"/>
        <span itemprop="ratingValue">4</span>/
        <span itemprop="bestRating">5</span>stars
        </div>
        <span itemprop="description">Great microwave for the price. It is small and
        fits in my apartment.</span>
    </div>
    ...
    </div>
    """
>>> sel = Selector(text=doc, type="html")
>>> for scope in sel.xpath('//div[@itemscope]'):
        print "current scope:", scope.xpath('@itemtype').extract()
        props = scope.xpath('''
                    set:difference(./descendant::*/@itemprop,
                                    .//*[@itemscope]/*/@itemprop)''')
        print "    properties:", props.extract()
        print

current scope: [u'http://schema.org/Product']
    properties: [u'name', u'aggregateRating', u'offers', u'description', u'review', u'review']

current scope: [u'http://schema.org/AggregateRating']
    properties: [u'ratingValue', u'reviewCount']

current scope: [u'http://schema.org/Offer']
    properties: [u'price', u'availability']

current scope: [u'http://schema.org/Review']
    properties: [u'name', u'author', u'datePublished', u'reviewRating', u'description']

current scope: [u'http://schema.org/Rating']
    properties: [u'worstRating', u'ratingValue', u'bestRating']

current scope: [u'http://schema.org/Review']
    properties: [u'name', u'author', u'datePublished', u'reviewRating', u'description']

current scope: [u'http://schema.org/Rating']
    properties: [u'worstRating', u'ratingValue', u'bestRating']





##Good practice - Using text nodes in a condition
#to use the text content as argument to an XPath string function, 
#avoid using .//text() and use just . instead.

#the expression .//text() yields a collection of text elements – a node-set. 
#And when a node-set is converted to a string eg with contains() or starts-with(), 
#it results in the text for the first element only.


>>> from scrapy import Selector
>>> sel = Selector(text='<a href="#">Click here to go to the <strong>Next Page</strong></a>')


>>> sel.xpath('//a//text()').extract() # take a peek at the node-set
[u'Click here to go to the ', u'Next Page']
>>> sel.xpath("string(//a[1]//text())").extract() # convert it to string
[u'Click here to go to the ']

#A node converted to a string, 
#however, puts together the text of itself plus of all its descendants:

>>> sel.xpath("//a[1]").extract() # select the first node
[u'<a href="#">Click here to go to the <strong>Next Page</strong></a>']
>>> sel.xpath("string(//a[1])").extract() # convert it to string
[u'Click here to go to the Next Page']

#using the .//text() node-set won’t select anything in this case:

>>> sel.xpath("//a[contains(.//text(), 'Next Page')]").extract()
[]

#But using the . to mean the node, works:

>>> sel.xpath("//a[contains(., 'Next Page')]").extract()
[u'<a href="#">Click here to go to the <strong>Next Page</strong></a>']







##Good practice - Beware of the difference between //node[1] and (//node)[1]

#//node[1] selects all the nodes occurring first under their respective parents.
#(//node)[1] selects all the nodes in the document, and then gets only the first of them.

>>> from scrapy import Selector
>>> sel = Selector(text="""
        <ul class="list">
            <li>1</li>
            <li>2</li>
            <li>3</li>
        </ul>
        <ul class="list">
            <li>4</li>
            <li>5</li>
            <li>6</li>
        </ul>""")
>>> xp = lambda x: sel.xpath(x).extract()

#This gets all first <li> elements under whatever it is its parent:

>>> xp("//li[1]")
[u'<li>1</li>', u'<li>4</li>']

#And this gets the first <li> element in the whole document:

>>> xp("(//li)[1]")
[u'<li>1</li>']

#This gets all first <li> elements under an <ul> parent:

>>> xp("//ul/li[1]")
[u'<li>1</li>', u'<li>4</li>']

#this gets the first <li> element under an <ul> parent in the whole document:

>>> xp("(//ul/li)[1]")
[u'<li>1</li>']



##Good practice - When querying by class, consider using CSS

#Because an element can contain multiple CSS classes, 
#the XPath way to select elements by class is complex

*[contains(concat(' ', normalize-space(@class), ' '), ' someclass ')]

#Good solution is 
>>> from scrapy import Selector
>>> sel = Selector(text='<div class="hero shout"><time datetime="2014-07-23 19:00">Special date</time></div>')
>>> sel.css('.shout').xpath('./time/@datetime').extract() #note relative XPATH
[u'2014-07-23 19:00']



##Good practice - Remove namespaces


$ scrapy shell https://github.com/blog.atom

# selecting all <link> objects 
#(because the Atom XML namespace is obfuscating those nodes):

>>> response.xpath("//link")
[]

#Good solution 
>>> response.selector.remove_namespaces()
>>> response.xpath("//link")
[<Selector xpath='//link' data=u'<link xmlns="http://www.w3.org/2005/Atom'>,
 <Selector xpath='//link' data=u'<link xmlns="http://www.w3.org/2005/Atom'>,
 ...

##Good practice - Get all texts under a tag 

sel = Selector(text='<a href="#">Click here to go to the <strong>Next Page</strong></a>')

#to get the entire text using: 
text_content = sel.xpath("//a[1]//text()").extract()
# which results [u'Click here to go to the ', u'Next Page']
' '.join(text_content)
 

#OR Use html2text 

import scrapy
import html2text


class WikiSpider(scrapy.Spider):
    name = "wiki_spider"
    allowed_domains = ["www.wikipedia.org"]
    start_urls = ["http://en.wikipedia.org/wiki/Python_(programming_language)"]

    def parse(self, response):
        hxs = response.selector 
        sample = hxs.xpath("//div[@id='mw-content-text']/p[1]").extract()[0]
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        print(converter.handle(sample)) #Python 3 print syntax

        
        

   
   
###*Scrapy - Items
#https://doc.scrapy.org/en/latest/topics/items.html    

#Scrapy spiders can return the extracted data as Python dicts or Item class 

#Item objects are simple containers used to collect the scraped data

##Declaring Items


import scrapy

class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)



>>> product = Product(name='Desktop PC', price=1000)
>>> print product
Product(name='Desktop PC', price=1000)

>>> product['name']
Desktop PC
>>> product.get('name')
Desktop PC

>>> product['price']
1000

>>> product['last_updated']
Traceback (most recent call last):
    ...
KeyError: 'last_updated'

>>> product.get('last_updated', 'not set')
not set

>>> product['lala'] # getting unknown field
Traceback (most recent call last):
    ...
KeyError: 'lala'

>>> product.get('lala', 'unknown field')
'unknown field'

>>> 'name' in product  # is name field populated?
True

>>> 'last_updated' in product  # is last_updated populated?
False

>>> 'last_updated' in product.fields  # is last_updated a declared field?
True

>>> 'lala' in product.fields  # is lala a declared field?
False


>>> product['last_updated'] = 'today'
>>> product['last_updated']
today

>>> product['lala'] = 'test' # setting unknown field
Traceback (most recent call last):
    ...
KeyError: 'Product does not support field: lala'

##Accessing all populated values

#To access all populated values, just use the typical dict API:

>>> product.keys()
['price', 'name']

>>> product.items()
[('price', 1000), ('name', 'Desktop PC')]

#Copying items:

>>> product2 = Product(product)
>>> print product2
Product(name='Desktop PC', price=1000)

>>> product3 = product2.copy()
>>> print product3
Product(name='Desktop PC', price=1000)

#Creating dicts from items:

>>> dict(product) # create a dict from all populated values
{'price': 1000, 'name': 'Desktop PC'}

#Creating items from dicts:

>>> Product({'name': 'Laptop PC', 'price': 1500})
Product(price=1500, name='Laptop PC')

>>> Product({'name': 'Laptop PC', 'lala': 1500}) # warning: unknown field in dict
Traceback (most recent call last):
    ...
KeyError: 'Product does not support field: lala'



##Extending Items
#to add more fields or to change some metadata for some fields


class DiscountedProduct(Product):
    discount_percent = scrapy.Field(serializer=str)
    discount_expiration_date = scrapy.Field()

    
    
###*Item Loaders
#a mechanism for populating scraped Items

#for items 
import scrapy

class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)

#the Item Loader 
from scrapy.loader import ItemLoader
from myproject.items import Product

#in parse method , Returns Item
#Note parse can return dict or Item or Request to follow
def parse(self, response):
    l = ItemLoader(item=Product(), response=response)
    l.add_xpath('name', '//div[@class="product_name"]')
    l.add_xpath('name', '//div[@class="product_title"]')
    l.add_xpath('price', '//p[@id="price"]')
    l.add_css('stock', 'p#stock')
    l.add_value('last_updated', 'today') # you can also use literal values
    return l.load_item()
    
    
##Item Loaders - Input and Output processors

#An Item Loader contains one input processor 
#and one output processor for each (item) field.

#Note ItemLoader has below default processor for all item field
    default_input_processor = Identity()
    default_output_processor = Identity()
    
#Note: processors are just callable objects(with 1st arg as Iterator)
#which are called with the data to be parsed, 
#and return a parsed value


#for example - 
l = ItemLoader(Product(), some_selector)
l.add_xpath('name', xpath1) # (1)
l.add_xpath('name', xpath2) # (2)
l.add_css('name', css) # (3)
l.add_value('name', 'test') # (4)
return l.load_item() # (5)

#1,2,3,4 are the places where input processors of 'name' are called with extracted values
#and returned values from input processors are appended one after another in a list 

#Step (5) - appended list is passed through the output processor 
#and value from output processor is assigned to Product.name 





##Item Loaders - Declaring input/output processors of Item Loaders


#OPTION-1 : Create a new Class 
#input processors are declared using the _in suffix 
#output processors are declared using the _out suffix

#declare a default input/output processors 
#using the ItemLoader.default_input_processor 
#and ItemLoader.default_output_processor attributes.


from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class ProductLoader(ItemLoader):

    default_output_processor = TakeFirst()

    name_in = MapCompose(unicode.title)  #in py3, use str.title 
    name_out = Join()

    price_in = MapCompose(unicode.strip)

    # ...

##OPTION-2 :  Declare them in Item definition 
import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

def filter_price(value):
    if value.isdigit():
        return value

class Product(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(remove_tags, filter_price),
        output_processor=TakeFirst(),
    )

>>> from scrapy.loader import ItemLoader
>>> il = ItemLoader(item=Product())
>>> il.add_value('name', [u'Welcome to my', u'<strong>website</strong>'])
>>> il.add_value('price', [u'&euro;', u'<span>1000</span>'])
>>> il.load_item()
{'name': u'Welcome to my website', 'price': u'1000'}

##The precedence order, for both input and output processors
1.Item Loader field-specific attributes: field_in and field_out (most precedence)
2.Field metadata (input_processor and output_processor key)
3.Item Loader defaults: ItemLoader.default_input_processor() and ItemLoader.default_output_processor() (least precedence)



##Item Loaders - Item Loader Context
#dict of arbitrary key/values as 2nd arg of processor function 
#which is shared among all input and output processors in the Item Loader

#For example, a processors function parse_length 
#which receives a text value and extracts a length from it:

def parse_length(text, loader_context):
    unit = loader_context.get('unit', 'm')
    # ... length parsing code goes here ...
    return parsed_length


#to modify Item Loader context values:
#1. By modifying the currently active Item Loader context (context attribute):
loader = ItemLoader(product)
loader.context['unit'] = 'cm'

#2.On Item Loader instantiation (the keyword arguments of Item Loader constructor are stored in the Item Loader context):
loader = ItemLoader(product, unit='cm')

#3.On Item Loader declaration, for those input/output processors that support instantiating them with an Item Loader context. MapCompose is one of them:
class ProductLoader(ItemLoader):
    length_out = MapCompose(parse_length, unit='cm')

    
    
    
    
##Item Loaders - Available built-in processors
class scrapy.loader.processors.Identity
    It returns the original values unchanged
    does not Accept item loader context 
    >>> from scrapy.loader.processors import Identity
    >>> proc = Identity()
    >>> proc(['one', 'two', 'three'])
    ['one', 'two', 'three']

class scrapy.loader.processors.TakeFirst
    Returns the first non-null/non-empty value from the values received
    does not Accept item loader context 
    >>> from scrapy.loader.processors import TakeFirst
    >>> proc = TakeFirst()
    >>> proc(['', 'one', 'two', 'three'])
    'one'

class scrapy.loader.processors.Join(separator=u' ')    
    Returns the values joined with the separator given in the constructor, which defaults to 
    does not Accept item loader context 
    >>> from scrapy.loader.processors import Join
    >>> proc = Join()
    >>> proc(['one', 'two', 'three'])
    u'one two three'
    >>> proc = Join('<br>')
    >>> proc(['one', 'two', 'three'])
    u'one<br>two<br>three'

class scrapy.loader.processors.Compose(*functions, **default_loader_context)
    each input value of this processor is passed to the first function, 
    and the result of that function is passed to the second function, 
    and so on
    Accepts item loader context 
    >>> from scrapy.loader.processors import Compose
    >>> proc = Compose(lambda v: v[0], str.upper)
    >>> proc(['hello', 'world'])
    'HELLO'

class scrapy.loader.processors.MapCompose(*functions, **default_loader_context)
    Same as Compose, but for Iterable, ie juxtaposition of function 
    >>> def filter_world(x):
            return None if x == 'world' else x
    ...
    >>> from scrapy.loader.processors import MapCompose
    >>> proc = MapCompose(filter_world, unicode.upper)
    >>> proc([u'hello', u'world', u'this', u'is', u'scrapy'])
    [u'HELLO, u'THIS', u'IS', u'SCRAPY']

class scrapy.loader.processors.SelectJmes(json_path) 
    Queries the value using the json path provided to the constructor and returns the output.
   
    >>> from scrapy.loader.processors import SelectJmes, Compose, MapCompose
    >>> proc = SelectJmes("foo") #for direct use on lists and dictionaries
    >>> proc({'foo': 'bar'})
    'bar'
    >>> proc({'foo': {'bar': 'baz'}})
    {'bar': 'baz'}

    Working with Json:

    >>> import json
    >>> proc_single_json_str = Compose(json.loads, SelectJmes("foo"))
    >>> proc_single_json_str('{"foo": "bar"}')
    u'bar'
    >>> proc_json_list = Compose(json.loads, MapCompose(SelectJmes('foo')))
    >>> proc_json_list('[{"foo":"bar"}, {"baz":"tar"}]')
    [u'bar']
    
    
    

##Item Loaders - Nested Loaders

#When parsing related values from a subsection of a document, 
#it can be useful to create nested loaders. 

#Example -extracting details from a footer of a page 
<footer>
    <a class="social" href="http://facebook.com/whatever">Like Us</a>
    <a class="social" href="http://twitter.com/whatever">Follow Us</a>
    <a class="email" href="mailto:whatever@example.com">Email Us</a>
</footer>

#Without nested loaders, 
#specify the full xpath (or css) for each value 
loader = ItemLoader(item=Item())
# load stuff not in the footer
loader.add_xpath('social', '//footer/a[@class = "social"]/@href')
loader.add_xpath('email', '//footer/a[@class = "email"]/@href')
loader.load_item()

#OR create a nested loader with the footer selector 
#and add values relative to the footer

loader = ItemLoader(item=Item())
# load stuff not in the footer
footer_loader = loader.nested_xpath('//footer')
footer_loader.add_xpath('social', 'a[@class = "social"]/@href')
footer_loader.add_xpath('email', 'a[@class = "email"]/@href')
# no need to call footer_loader.load_item()
loader.load_item()


#Example - How To Remove White Space in Scrapy Spider Data

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.utils.markup import replace_escape_chars
from ccpstore.items import Greenhouse

class GreenhouseSpider(BaseSpider):
    name = "greenhouse"
    allowed_domains = ["domain.com"]
    start_urls = [
        "http://www.domain.com",
    ]
    def parse(self, response):
        items = []
        l = ItemLoader(item=Greenhouse(), response=response)
        l.default_input_processor = MapCompose(lambda v: v.split(), replace_escape_chars)
        l.default_output_processor = Join()
        l.add_xpath('title', '//h1/text()')
        l.add_xpath('usage', '//li[@id="ctl18_ctl00_rptProductAttributes_ctl00_liItem"]/text()')
        l.add_xpath('repeat', '//li[@id="ctl18_ctl00_rptProductAttributes_ctl02_liItem"]/text()')
        l.add_xpath('direction', '//li[@id="ctl18_ctl00_rptProductAttributes_ctl03_liItem"]/text()')
        items.append(l.load_item())
        yield items        


##Item Loaders - ItemLoader objects

class scrapy.loader.ItemLoader([item, selector, response, ]**kwargs)
    item (Item object) – The item instance to populate using subsequent calls to add_xpath(), add_css(), or add_value().
    selector (Selector object) – The selector to extract data from, when using the add_xpath() (resp. add_css()) or replace_xpath() (resp. replace_css()) method.
    response (Response object) – The response used to construct the selector using the default_selector_class, unless the selector argument is given, in which case this argument is ignored.


    get_value(value, *processors, **kwargs)
        Process the given value by the given processors 
        and keyword arguments.        
        re (str or compiled regex) – 
            a regular expression to use for extracting data 
            from the given value using extract_regex() method, 
            applied before processors
        >>> from scrapy.loader.processors import TakeFirst
        >>> loader.get_value(u'name: foo', TakeFirst(), unicode.upper, re='name: (.+)')
        'FOO'

    add_value(field_name, value, *processors, **kwargs)
        Process and then add the given value for the given field.
        The value is first passed through get_value() 
        by giving the processors and kwargs, 
        and then passed through the field input processor 
        and its result appended to the data collected for that field. 
        
        If the field already contains collected data, 
        the new data is added.

        The given field_name can be None, 
        in which case values for multiple fields may be added. 
        And the processed value should be a dict 
        with field_name mapped to values.

        loader.add_value('name', u'Color TV')
        loader.add_value('colours', [u'white', u'blue'])
        loader.add_value('length', u'100')
        loader.add_value('name', u'name: foo', TakeFirst(), re='name: (.+)')
        loader.add_value(None, {'name': u'foo', 'sex': u'male'})

    replace_value(field_name, value, *processors, **kwargs)
        Similar to add_value() 
        but replaces the collected data with the new value 
        instead of adding it.

    #Other similar methods 
    get_xpath(xpath, *processors, **kwargs)    
    add_xpath(field_name, xpath, *processors, **kwargs)
    replace_xpath(field_name, xpath, *processors, **kwargs)
    get_css(css, *processors, **kwargs)
    add_css(field_name, css, *processors, **kwargs)
    replace_css(field_name, css, *processors, **kwargs)
     
    #Other methods 
    load_item()
    nested_xpath(xpath)
    nested_css(css)
    get_collected_values(field_name)
    get_output_value(field_name)
    get_input_processor(field_name)
    get_output_processor(field_name)


###*Scrapy - Scrapy shell

$ scrapy shell <url>

# local file system 
$ scrapy shell ./path/to/file.html
$ scrapy shell ../other/path/to/file.html
$ scrapy shell /absolute/path/to/file.html

# File URI
scrapy shell file:///absolute/path/to/file.html

##Available Shortcuts
shelp() - print a help with the list of available objects and shortcuts
fetch(url[, redirect=True]) - fetch a new response from the given URL and update all related objects accordingly. You can optionaly ask for HTTP 3xx redirections to not be followed by passing redirect=False
fetch(request) - fetch a new response from the given request and update all related objects accordingly.
view(response) - open the given response in your local web browser, for inspection. This will add a <base> tag to the response body in order for external links (such as images and style sheets) to display properly. Note, however, that this will create a temporary file in your computer, which won’t be removed automatically.

##Available Scrapy objects in shell 
crawler - the current Crawler object.
spider - the Spider which is known to handle the URL, or a Spider object if there is no spider found for the current URL
request - a Request object of the last fetched page. You can modify this request using replace() or fetch a new request (without leaving the shell) using the fetch shortcut.
response - a Response object containing the last fetched page
settings - the current Scrapy settings

##Example 

$ scrapy shell 'http://scrapy.org' --nolog

[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x7f07395dd690>
[s]   item       {}
[s]   request    <GET http://scrapy.org>
[s]   response   <200 https://scrapy.org/>
[s]   settings   <scrapy.settings.Settings object at 0x7f07395dd710>
[s]   spider     <DefaultSpider 'default' at 0x7f0735891690>
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
[s]   fetch(req)                  Fetch a scrapy.Request and update local objects
[s]   shelp()           Shell help (print this help)
[s]   view(response)    View response in a browser


>>> response.xpath('//title/text()').extract_first()
'Scrapy | A Fast and Powerful Scraping and Web Crawling Framework'

>>> fetch("http://reddit.com")

>>> response.xpath('//title/text()').extract()
['reddit: the front page of the internet']

>>> request = request.replace(method="POST")

>>> fetch(request)

>>> response.status
404

>>> from pprint import pprint

>>> pprint(response.headers)
{'Accept-Ranges': ['bytes'],
 'Cache-Control': ['max-age=0, must-revalidate'],
 'Content-Type': ['text/html; charset=UTF-8'],
 'Date': ['Thu, 08 Dec 2016 16:21:19 GMT'],
 'Server': ['snooserv'],
 'Set-Cookie': ['loid=KqNLou0V9SKMX4qb4n; Domain=reddit.com; Max-Age=63071999; Path=/; expires=Sat, 08-Dec-2018 16:21:19 GMT; secure',
                'loidcreated=2016-12-08T16%3A21%3A19.445Z; Domain=reddit.com; Max-Age=63071999; Path=/; expires=Sat, 08-Dec-2018 16:21:19 GMT; secure',
                'loid=vi0ZVe4NkxNWdlH7r7; Domain=reddit.com; Max-Age=63071999; Path=/; expires=Sat, 08-Dec-2018 16:21:19 GMT; secure',
                'loidcreated=2016-12-08T16%3A21%3A19.459Z; Domain=reddit.com; Max-Age=63071999; Path=/; expires=Sat, 08-Dec-2018 16:21:19 GMT; secure'],
 'Vary': ['accept-encoding'],
 'Via': ['1.1 varnish'],
 'X-Cache': ['MISS'],
 'X-Cache-Hits': ['0'],
 'X-Content-Type-Options': ['nosniff'],
 'X-Frame-Options': ['SAMEORIGIN'],
 'X-Moose': ['majestic'],
 'X-Served-By': ['cache-cdg8730-CDG'],
 'X-Timer': ['S1481214079.394283,VS0,VE159'],
 'X-Ua-Compatible': ['IE=edge'],
 'X-Xss-Protection': ['1; mode=block']}
>>>

##Invoking the shell from spiders to inspect responses
#Use inspect_response

import scrapy


class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = [
        "http://example.com",
        "http://example.org",
        "http://example.net",
    ]

    def parse(self, response):
        # We want to inspect one specific response.
        if ".org" in response.url:
            from scrapy.shell import inspect_response
            inspect_response(response, self)

        # Rest of parsing code.

#run the spider

2014-01-23 17:48:31-0400 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://example.com> (referer: None)
2014-01-23 17:48:31-0400 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://example.org> (referer: None)
[s] Available Scrapy objects:
[s]   crawler    <scrapy.crawler.Crawler object at 0x1e16b50>
...

>>> response.url
'http://example.org'

>>> response.xpath('//h1[@class="fn"]')
[]

#open the response in web browser 
#and see if it’s the response you were expecting:

>>> view(response)
True

#hit Ctrl-D (or Ctrl-Z in Windows) to exit the shell 
#and resume the crawling:

>>> ^D
2014-01-23 17:50:03-0400 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://example.net> (referer: None)
...




###*Scrapy - Item Pipeline

#After an item has been scraped by a spider, 
#it is sent to the Item Pipeline 
#which processes it through several components that are executed sequentially.

#Typical uses of item pipelines are:
    cleansing HTML data
    validating scraped data (checking that the items contain certain fields)
    checking for duplicates (and dropping them)
    storing the scraped item in a database

##Writing your own item pipeline

#Each item pipeline is a Python class 
#that must implement the following method
#and must add its class to the ITEM_PIPELINES setting

process_item(self, item, spider)   
        item (Item object or a dict) – the item scraped
        spider (Spider object) – the spider which scraped the item
        must either: 
            return a dict with data, 
            return an Item (or any descendant class) object, 
            return a Twisted Deferred 
            or raise DropItem exception. 
        Dropped items are no longer processed by further pipeline components.

#Additionally, they may also implement the following methods:
open_spider(self, spider)
    This method is called when the spider is opened.
    spider (Spider object) – the spider which was opened

close_spider(self, spider)
    This method is called when the spider is closed.
    spider (Spider object) – the spider which was closed

from_crawler(cls, crawler)
    If present, this classmethod is called 
    to create a pipeline instance from a Crawler. 
    It must return a new instance of the pipeline. 
    Crawler object provides access to all Scrapy core components like settings and signals; 
    it is a way for pipeline to access them 
    and hook its functionality into Scrapy.
    Parameters:	crawler (Crawler object) – crawler that uses this pipeline


##Example - Price validation and dropping items with no prices


from scrapy.exceptions import DropItem

class PricePipeline(object):

    vat_factor = 1.15

    def process_item(self, item, spider):
        if item['price']:
            if item['price_excludes_vat']:
                item['price'] = item['price'] * self.vat_factor
            return item
        else:
            raise DropItem("Missing price in %s" % item)

##Example - Write items to a JSON file
#stores all scraped items (from all spiders) into a single items.jl file, 
#containing one item per line serialized in JSON format:

import json

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


##Example - Duplicates filter
#looks for duplicate items, and drops those items 
#that were already processed. 

#for example our items have a unique id, 
#but our spider returns multiples items with the same id:

from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item

##Activating an Item Pipeline component
#add its class to the ITEM_PIPELINES setting, 

#The integer values determine the order in which they run: 
#items go through from lower valued to higher valued classes. 
#It’s customary to define these numbers in the 0-1000 range.

#in settings.py 

ITEM_PIPELINES = {
    'myproject.pipelines.PricePipeline': 300,
    'myproject.pipelines.JsonWriterPipeline': 800,
}



###Scrapy - Serialization formats
#For serializing the scraped data, 
#the feed exports use the Item exporters. 
        JSON
        JSON lines
        CSV
        XML

#OR extend the supported format through the FEED_EXPORTERS setting.

JSON

        FEED_FORMAT: json
        Exporter used: JsonItemExporter        

JSON lines

        FEED_FORMAT: jsonlines
        Exporter used: JsonLinesItemExporter

CSV

        FEED_FORMAT: csv
        Exporter used: CsvItemExporter
        To specify columns to export and their order use FEED_EXPORT_FIELDS. Other feed exporters can also use this option, but it is important for CSV because unlike many other export formats CSV uses a fixed header.

XML

        FEED_FORMAT: xml
        Exporter used: XmlItemExporter

Pickle

        FEED_FORMAT: pickle
        Exporter used: PickleItemExporter

Marshal

        FEED_FORMAT: marshal
        Exporter used: MarshalItemExporter
        
##Settings for for configuring the feed exports:
•FEED_URI (mandatory)
•FEED_FORMAT
•FEED_STORAGES
•FEED_EXPORTERS
•FEED_STORE_EMPTY
•FEED_EXPORT_ENCODING
•FEED_EXPORT_FIELDS
•FEED_EXPORT_INDENT



##Storages
#To define where to store the feed using a URI 
#(through the FEED_URI setting). 

#The feed exports supports multiple storage backend types 
#which are defined by the URI scheme.
    Local filesystem
    FTP
    S3 (requires botocore or boto)
    Standard output

##Storage URI parameters
#parameters that get replaced when the feed is being created. 
    %(time)s - gets replaced by a timestamp when the feed is being created
    %(name)s - gets replaced by the spider name

#Any other named parameter gets replaced 
#by the spider attribute of the same name. 

#For example, %(site_id)s would get replaced by the 
#spider.site_id attribute the moment the feed is being created.

#Example 
#Store in FTP using one directory per spider:
    ftp://user:password@ftp.example.com/scraping/feeds/%(name)s/%(time)s.json
#Store in S3 using one directory per spider:
    s3://mybucket/scraping/feeds/%(name)s/%(time)s.json


##Local filesystem(default)
#The feeds are stored in the local filesystem.
        URI scheme: file
        Example URI: file:///tmp/export.csv
        Required external libraries: none

##FTP
#The feeds are stored in a FTP server.
        URI scheme: ftp
        Example URI: ftp://user:pass@ftp.example.com/path/to/export.csv
        Required external libraries: none

#Standard output
#The feeds are written to the standard output of the Scrapy process.
        URI scheme: stdout
        Example URI: stdout:
        Required external libraries: none




###*Scrapy - Settings


##Option-1 : Command line options 

$ scrapy crawl myspider -s LOG_FILE=scrapy.log

##Option-2 : Settings per-spider
class MySpider(scrapy.Spider):
    name = 'myspider'

    custom_settings = {
        'SOME_SETTING': 'some value',
    }

##Option-3 : Project settings module
    adding or changing the settings in the project/settings.py 

##Option-4 : Default settings per-command
#Each Scrapy tool command can have its own default settings, 
#are specified in the default_settings attribute of the command class.


##Option-5 : Default global settings
#located in the scrapy.settings.default_settings module 
#Ref:
#https://doc.scrapy.org/en/latest/topics/settings.html#topics-settings-ref



##How to access settings
#In a spider, the settings are available through self.settings:

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['http://example.com']

    def parse(self, response):
        print("Existing settings: %s" % self.settings.attributes.keys())


        
        
        
###*Scrapy - Logging       
#use self.logger in Spider 

import scrapy

class MySpider(scrapy.Spider):

    name = 'myspider'
    start_urls = ['https://scrapinghub.com']

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)

#That logger is created using the Spider’s name,
#or override that 

import logging
import scrapy

logger = logging.getLogger('mycustomlogger')

class MySpider(scrapy.Spider):

    name = 'myspider'
    start_urls = ['https://scrapinghub.com']

    def parse(self, response):
        logger.info('Parse function called on %s', response.url)

        
        
##Logging settings
    LOG_FILE
    LOG_ENABLED
    LOG_ENCODING
    LOG_LEVEL
    LOG_FORMAT
    LOG_DATEFORMAT
    LOG_STDOUT
    LOG_SHORT_NAMES
    
    
##Command-line options
    --logfile FILE
        Overrides LOG_FILE

    --loglevel/-L LEVEL
        Overrides LOG_LEVEL

    --nolog
        Sets LOG_ENABLED to False

        
        
###Scrapy - Sending e-mail


from scrapy.mail import MailSender
mailer = MailSender()
#OR 
mailer = MailSender.from_settings(settings)

#to send an e-mail (without attachments):
mailer.send(to=["someone@example.com"], subject="Some subject", body="Some body", cc=["another@example.com"])

##Mail settings
MAIL_FROM
    Default: 'scrapy@localhost'
    Sender email to use (From: header) for sending emails.
MAIL_HOST
    Default: 'localhost'
    SMTP host to use for sending emails.
MAIL_PORT
    Default: 25
    SMTP port to use for sending emails.
MAIL_USER
    Default: None
    User to use for SMTP authentication. 
    If disabled no SMTP authentication will be performed.
MAIL_PASS
    Default: None
    Password to use for SMTP authentication, along with MAIL_USER.
MAIL_TLS
    Default: False
    Enforce using STARTTLS. STARTTLS is a way to take an existing insecure connection, and upgrade it to a secure connection using SSL/TLS.
MAIL_SSL
    Default: False
    Enforce connecting using an SSL encrypted connection


###Scrapy - Telnet Console

#Scrapy comes with a built-in telnet console 
#for inspecting and controlling a Scrapy running process. 

#The telnet console is a regular python shell running inside the Scrapy process

#The telnet console listens in the TCP port defined in the TELNETCONSOLE_PORT setting, which defaults to 6023. To access the console you need to type:

$ telnet localhost 6023
>>>

##Available variables in the telnet console
#a regular Python shell running inside the Scrapy process, 
#so you can do anything from it including importing new modules, etc.

#Also comes with some default variables defined for convenience:
#Ref:
#https://doc.scrapy.org/en/latest/topics/telnetconsole.html#available-variables-in-the-telnet-console




##Console - View engine status, use est()

$ telnet localhost 6023
>>> est()
Execution engine status

time()-engine.start_time                        : 8.62972998619
engine.has_capacity()                           : False
len(engine.downloader.active)                   : 16
engine.scraper.is_idle()                        : False
engine.spider.name                              : followall
engine.spider_is_idle(engine.spider)            : False
engine.slot.closing                             : False
len(engine.slot.inprogress)                     : 16
len(engine.slot.scheduler.dqs or [])            : 0
len(engine.slot.scheduler.mqs)                  : 92
len(engine.scraper.slot.queue)                  : 0
len(engine.scraper.slot.active)                 : 0
engine.scraper.slot.active_size                 : 0
engine.scraper.slot.itemproc_size               : 0
engine.scraper.slot.needs_backout()             : False

##Console - Pause, resume and stop the Scrapy engine

#To pause:

$ telnet localhost 6023
>>> engine.pause()
>>>

#To resume:

$ telnet localhost 6023
>>> engine.unpause()
>>>

#To stop:

$ telnet localhost 6023
>>> engine.stop()
Connection closed by foreign host.




###Scrapy - Scrapy with BeautifulSoup


from bs4 import BeautifulSoup
import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = (
        'http://www.example.com/',
    )

    def parse(self, response):
        # use lxml to get decent HTML parsing speed
        soup = BeautifulSoup(response.text, 'lxml')
        yield {
            "url": response.url,
            "title": soup.h1.string
        }




###Scrapy - Debugging Spiders


import scrapy
from myproject.items import MyItem

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = (
        'http://example.com/page1',
        'http://example.com/page2',
        )

    def parse(self, response):
        # collect `item_urls`
        for item_url in item_urls:
            yield scrapy.Request(item_url, self.parse_item)

    def parse_item(self, response):
        item = MyItem()
        # populate `item` fields
        # and extract item_details_url
        yield scrapy.Request(item_details_url, self.parse_details, meta={'item': item})

    def parse_details(self, response):
        item = response.meta['item']
        # populate more `item` fields
        return item


##Parse Command
#The most basic way of checking the output of spider is 
#to use the parse command. 

#It allows to check the behaviour of different parts of the spider at the method level. 


$ scrapy parse --spider=myspider -c parse_item -d 2 <item_url>
[ ... scrapy log lines crawling example.com spider ... ]

>>> STATUS DEPTH LEVEL 2 <<<
# Scraped Items  ------------------------------------------------------------
[{'url': <item_url>}]

# Requests  -----------------------------------------------------------------
[]

#Using the --verbose or -v option we can see the status at each depth level:

$ scrapy parse --spider=myspider -c parse_item -d 2 -v <item_url>
[ ... scrapy log lines crawling example.com spider ... ]

>>> DEPTH LEVEL: 1 <<<
# Scraped Items  ------------------------------------------------------------
[]

# Requests  -----------------------------------------------------------------
[<GET item_details_url>]


>>> DEPTH LEVEL: 2 <<<
# Scraped Items  ------------------------------------------------------------
[{'url': <item_url>}]

# Requests  -----------------------------------------------------------------
[]

#Checking items scraped from a single start_url, can also be easily achieved using:

$ scrapy parse --spider=myspider -d 3 'http://example.com/page1'



##Debugging using Scrapy Shell


from scrapy.shell import inspect_response

def parse_details(self, response):
    item = response.meta.get('item', None)
    if item:
        # populate more `item` fields
        return item
    else:
        inspect_response(response, self)


##Debugging using Open in browser


from scrapy.utils.response import open_in_browser

def parse_details(self, response):
    if "item name" not in response.body:
        open_in_browser(response)


##Debugging using Logging


def parse_details(self, response):
    item = response.meta.get('item', None)
    if item:
        # populate more `item` fields
        return item
    else:
        self.logger.warning('No item received for %s', response.url)


        
###Scrapy - check other help 
https://doc.scrapy.org/en/latest/topics/firefox.html
https://doc.scrapy.org/en/latest/topics/firebug.html      
     

###Scrapy - Deploying to a Scrapyd Server
#Scrapyd is an open source application to run Scrapy spiders. 
#It provides a server with HTTP API, 
#capable of running and monitoring Scrapy spiders.
#Ref:
#https://scrapyd.readthedocs.io/en/latest/deploy.html

   
###Scrapy - Deploy them toScrapy Cloud
$ pip install shub
$ shub login
Insert your Scrapinghub API Key: <API_KEY>

# Deploy the spider to Scrapy Cloud
$ shub deploy

# Schedule the spider for execution
$ shub schedule blogspider 
Spider blogspider scheduled, watch it running here:
https://app.scrapinghub.com/p/26731/job/1/8

# Retrieve the scraped data
$ shub items 26731/1/8
{"title": "Improved Frontera: Web Crawling at Scale with Python 3 Support"}
{"title": "How to Crawl the Web Politely with Scrapy"}



###Scrapy - AutoThrottle extension
#This is an extension for automatically throttling crawling speed 
#based on load of both the Scrapy server and the website for  crawling.

#The settings used to control the AutoThrottle extension are:
    AUTOTHROTTLE_ENABLED
    AUTOTHROTTLE_START_DELAY
    AUTOTHROTTLE_MAX_DELAY
    AUTOTHROTTLE_TARGET_CONCURRENCY
    AUTOTHROTTLE_DEBUG
    CONCURRENT_REQUESTS_PER_DOMAIN
    CONCURRENT_REQUESTS_PER_IP
    DOWNLOAD_DELAY
    
    

###Scrapy - Spider Middleware

#The spider middleware is a framework of hooks into Scrapy’s spider processing mechanism 
#where you can plug custom functionality to process the responses 
#that are sent to Spiders for processing 
#and to process the requests and items that are generated from spiders.


##Activating a spider middleware
#add it to the SPIDER_MIDDLEWARES setting

SPIDER_MIDDLEWARES = {
    'myproject.middlewares.CustomSpiderMiddleware': 543,
}



##Spider Middleware - Built-in spider middleware reference

class scrapy.spidermiddlewares.depth.DepthMiddleware
    for tracking the depth of each Request inside the site being scraped. 
    It can be used to limit the maximum depth to scrape or things like that.
    Settings:
        DEPTH_LIMIT - The maximum depth that will be allowed to crawl for any site. If zero, no limit will be imposed.
        DEPTH_STATS - Whether to collect depth stats.
        DEPTH_PRIORITY - Whether to prioritize the requests based on their depth.


class scrapy.spidermiddlewares.httperror.HttpErrorMiddleware
    Filter out unsuccessful (erroneous) HTTP responses 
    so that spiders don’t have to deal with them, 
    which (most of the time) imposes an overhead, 
    consumes more resources, and makes the spider logic more complex.
    
    For example, if you want your spider to handle 404 responses 
    class MySpider(CrawlSpider):
        handle_httpstatus_list = [404]
    
    The handle_httpstatus_list key of Request.meta can also be used 
    to specify which response codes to allow on a per-request basis. 
    You can also set the meta key handle_httpstatus_all to True 
    if you want to allow any response code for a request.


class scrapy.spidermiddlewares.offsite.OffsiteMiddleware
    Filters out Requests for URLs outside the domains covered by the spider.
    This middleware filters out every request 
    whose host names aren’t in the spider’s allowed_domains attribute. 
    All subdomains of any domain in the list are also allowed. 
    E.g. the rule www.example.org will also allow bob.www.example.org 
    but not www2.example.com nor example.com.

   

class scrapy.spidermiddlewares.urllength.UrlLengthMiddleware
    Filters out requests with URLs longer than URLLENGTH_LIMIT
    Settings:
        URLLENGTH_LIMIT - The maximum URL length to allow for crawled URLs.









###Scrapy - Downloader Middleware

#The downloader middleware is a framework of hooks 
#into Scrapy’s request/response processing. 
#used for globally altering Scrapy’s requests and responses.


##Activating a downloader middleware
#add it to the DOWNLOADER_MIDDLEWARES setting,

DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.CustomDownloaderMiddleware': 543,
}

#to disable a built-in middleware , make it None 
#(the ones defined in DOWNLOADER_MIDDLEWARES_BASE and enabled by default) you must define it in your project’s DOWNLOADER_MIDDLEWARES setting and assign None as its value. For example, if you want to disable the user-agent middleware:

DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.CustomDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

#Also note that some middlewares may need to be enabled 
#through a particular setting. 


##Built-in downloader middleware reference


class scrapy.downloadermiddlewares.cookies.CookiesMiddleware
    This middleware enables working with sites that require cookies, 
    such as those that use sessions. 
    It keeps track of cookies sent by web servers, 
    and send them back on subsequent requests (from that spider), 
    just like web browsers do.
    Settings:
    COOKIES_ENABLED
    COOKIES_DEBUG
    

class scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware
    This middleware sets all default requests headers 
    specified in the DEFAULT_REQUEST_HEADERS setting.

    

class scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware
    This middleware sets the download timeout for requests specified 
    in the DOWNLOAD_TIMEOUT setting 
    or download_timeout spider attribute.


class scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware
    This middleware authenticates all requests generated 
    from certain spiders using Basic access authentication 
    (aka. HTTP auth).

    To enable HTTP authentication from certain spiders, 
    set the http_user and http_pass attributes of those spiders.

    from scrapy.spiders import CrawlSpider
    
    class SomeIntranetSiteSpider(CrawlSpider):
        http_user = 'someuser'
        http_pass = 'somepass'
        name = 'intranet.example.com'

        # .. rest of the spider code omitted ...



class scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware
    This middleware sets the HTTP proxy to use for requests, 
    by setting the proxy meta value for Request objects.
    Like the Python standard library modules urllib and urllib2, 
    it obeys the following environment variables:
        http_proxy
        https_proxy
        no_proxy
    You can also set the meta key proxy per-request, 
    to a value like http://some_proxy_server:port 
    or http://username:password@some_proxy_server:port. 
    Keep in mind this value will take precedence over http_proxy/https_proxy environment variables, and it will also ignore no_proxy environment variable.



class scrapy.downloadermiddlewares.redirect.RedirectMiddleware
    This middleware handles redirection of requests based 
    on response status.
    The urls which the request goes through (while being redirected) 
    can be found in the redirect_urls Request.meta key.
    Settings:
        REDIRECT_ENABLED
        REDIRECT_MAX_TIMES

    If Request.meta has dont_redirect key set to True, 
    the request will be ignored by this middleware.

    If you want to handle some redirect status codes in your spider, 
    you can specify these in the handle_httpstatus_list spider attribute.

    For example, if you want the redirect middleware to ignore 301 and 302 responses 
    (and pass them through to your spider) you can do this:

    class MySpider(CrawlSpider):
        handle_httpstatus_list = [301, 302]

    The handle_httpstatus_list key of Request.meta 
    can also be used to specify which response codes to allow on a per-request basis. 
    You can also set the meta key handle_httpstatus_all to True 
    if you want to allow any response code for a request.        



class scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware
    This middleware handles redirection of requests based 
    on meta-refresh html tag.
    Settings:
        METAREFRESH_ENABLED
        METAREFRESH_MAXDELAY
    This middleware obey REDIRECT_MAX_TIMES setting, 
    dont_redirect and redirect_urls request meta keys 
    as described for RedirectMiddleware
    


class scrapy.downloadermiddlewares.retry.RetryMiddleware
    A middleware to retry failed requests 
    that are potentially caused by temporary problems 
    such as a connection timeout or HTTP 500 error.
    Settings:
        RETRY_ENABLED
        RETRY_TIMES
        RETRY_HTTP_CODES
    If Request.meta has dont_retry key set to True, 
    the request will be ignored by this middleware.


class scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware
    This middleware filters out requests forbidden by the robots.txt exclusion standard.
    Ensure ROBOTSTXT_OBEY setting is enabled.
    If Request.meta has dont_obey_robotstxt key set to True 
    the request will be ignored by this middleware 
    even if ROBOTSTXT_OBEY is enabled.



class scrapy.downloadermiddlewares.useragent.UserAgentMiddleware
    Middleware that allows spiders to override the default user agent.
    To override the default user agent, 
    spiders user_agent attribute must be set.



class scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware
    Middleware that finds ‘AJAX crawlable’ page variants 
    based on meta-fragment html tag. 
    Ref: https://developers.google.com/webmasters/ajax-crawling/docs/getting-started for more info.

  




###CSS Reference 
#Selector 			Example 		Description
.class 				.intro 			Selects all elements with class="intro" 
#id 				#firstname 		Selects the element with id="firstname" 
* 					* 				Selects all elements 
element 			p 				Selects all <p> elements 
element,element 	div, p 			Selects all <div> elements and all <p> elements 
element element 	div p 			Selects all <p> elements inside <div> elements 
element>element 	div > p 		Selects all <p> elements where the parent is a <div> element 
element+element 	div + p 		Selects all <p> elements that are placed immediately after <div> elements 
element1~element2 	p ~ ul 			Selects every <ul> element that are preceded by a <p> element 
[attribute] 		[target] 		Selects all elements with a target attribute 
[attribute=value] 	[target=_blank] Selects all elements with target="_blank" 
[attribute~=value] 	[title~=flower] Selects all elements with a title attribute containing the word "flower" 
[attribute|=value] 	[lang|=en] 		Selects all elements with a lang attribute value starting with "en" 
[attribute^=value] 	a[href^="https"] Selects every <a> element whose href attribute value begins with "https" 
[attribute$=value] 	a[href$=".pdf"] Selects every <a> element whose href attribute value ends with ".pdf" 
[attribute*=value] 	a[href*="w3schools"] Selects every <a> element whose href attribute value contains the substring "w3schools" 
:active 			a:active 		Selects the active link 
::after 			p::after 		Insert something after the content of each <p> element 
::before 			p::before 		Insert something before the content of each <p> element 
:checked 			input:checked 	Selects every checked <input> element 
:disabled 			input:disabled 	Selects every disabled <input> element 
:empty 				p:empty 		Selects every <p> element that has no children (including text nodes) 
:enabled 			input:enabled 	Selects every enabled <input> element 
:first-child 		p:first-child 	Selects every <p> element that is the first child of its parent 
::first-letter 		p::first-letter Selects the first letter of every <p> element 
::first-line 		p::first-line 	Selects the first line of every <p> element 
:first-of-type 		p:first-of-type Selects every <p> element that is the first <p> element of its parent 
:focus 				input:focus 	Selects the input element which has focus 
:in-range 			input:in-range 	Selects input elements with a value within a specified range 
:invalid 			input:invalid 	Selects all input elements with an invalid value 
:last-child 		p:last-child 	Selects every <p> element that is the last child of its parent 
:last-of-type 		p:last-of-type 	Selects every <p> element that is the last <p> element of its parent 
:link 				a:link 			Selects all unvisited links 
:not(selector) 		:not(p) 		Selects every element that is not a <p> element  
:nth-child(n) 		p:nth-child(2) 	Selects every <p> element that is the second child of its parent 
:nth-last-child(n) 	p:nth-last-child(2) Selects every <p> element that is the second child of its parent, counting from the last child 
:nth-last-of-type(n) p:nth-last-of-type(2) Selects every <p> element that is the second <p> element of its parent, counting from the last child 
:nth-of-type(n) 	p:nth-of-type(2) Selects every <p> element that is the second <p> element of its parent 
:only-of-type 		p:only-of-type 	Selects every <p> element that is the only <p> element of its parent 
:only-child 		p:only-child 	Selects every <p> element that is the only child of its parent 
:optional 			input:optional 	Selects input elements with no "required" attribute 
:out-of-range 		input:out-of-range Selects input elements with a value outside a specified range 
:required 			input:required Selects input elements with the "required" attribute specified 
:root 				:root 			Selects the document's root element 
::selection 		::selection 	Selects the portion of an element that is selected by a user   
:target 			#news:target  	Selects the current active #news element (clicked on a URL containing that anchor name) 3 
:valid 				input:valid 	Selects all input elements with a valid value 
:visited 			a:visited 		Selects all visited links 


###CSS Reference - Difference of  space, <, +, ~

<div id="container">            
   <p>First</p>
    <div>
        <p>Child Paragraph</p>
    </div>
   <p>Second</p>
   <p>Third</p>      
</div>

 
##Space: It is the descendant selector. all tags(any level) under one tag 

div#container p{
font-weight:bold;
}
#It will target all p tags within container div. 
#(First Child Paragraph Second Third)



## > Sign: elements which are DIRECT children of a particular element.
#all tags(only first level) under one tag 
div#container > p {
  border: 1px solid black;
}
#It will target all P element which are direct children of container div,
#not children of child div.
#(First Second Third)


 

## + Sign:It is Adjacent sibling combinator.
#one tag immediatly with another tag(same level) 
#selectors having the same parent 
#and the second one must come IMMEDIATELY after the first.


div + p {  
   color: green;  
} 
#(Second , note immediate p after <div></div> 
#as they have to be siblings )

 
##~ Sign:It is general sibling combinator 
##one tag with another tag(same level) (does not need to be immediate)
#the second selector does NOT have to immediately follow the first one
#It will select all elements that is preceded by the former selector.

div ~ p{
background-color:blue;
} 
#(Second Third, note any p after <div></div> as they have to be siblings)


###CSS Reference- Difference among Attribute selector 

##The [attribute] selector 
#is used to select elements with a specified attribute.

#Example selects all <a> elements with a target attribute
a[target] {
    background-color: yellow;
} 


##The [attribute="value"] selector 
#is used to select elements with a specified attribute and value.

#Example - selects all <a> elements with a target="_blank" attribute
a[target="_blank"] { 
    background-color: yellow;
} 


##The [attribute~="value"] selector 
#is used to select elements with an attribute value 
#containing a specified word(has to be word ie separated by space)

#Example - selects all elements with a title attribute 
#that contains a space-separated list of words, one of which is "flower":
[title~="flower"] {
    border: 5px solid yellow;
}


##The [attribute|="value"] selector 
#is used to select elements with the specified attribute 
#starting with the specified word (ie space after)
#either alone, like class="top", 
#or followed by a hyphen( - ), like class="top-text"


##[attribute^="value"] , [attribute$="value"] , [attribute*="value"]
#is used to select elements whose attribute value 
#begins/ends/contains with a specified string(might not be word)
[class*="te"] {
    background: yellow;
}


###CSS Refernce -  Pseudo elements(:: CSS3 but : in CSS2) and pseudo-classes (:)
selector::pseudo-element {
    property:value;
}

selector:pseudo-class {
    property:value;
}

###CSS Refernce -  All CSS Pseudo Elements
::after         p::after        Insert something after the content of each <p> element 
::before        p::before       Insert something before the content of each <p> element 
::first-letter  p::first-letter Selects the first letter of each <p> element 
::first-line    p::first-line   Selects the first line of each <p> element 
::selection     p::selection    Selects the portion of an element that is selected by a user 


###CSS Refernce -  All CSS Pseudo Classes

#a:hover MUST come after a:link and a:visited in the CSS definition 
#a:active MUST come after a:hover in the CSS definition 

:visited        a:visited       Selects all visited links 
:link           a:link          Selects all unvisited links 
:hover          a:hover         Selects links on mouse over 
:active         a:active        Selects the active link 

#Example 
/* unvisited link */
a:link {
    color: #FF0000;
}

/* visited link */
a:visited {
    color: #00FF00;
}

/* mouse over link */
a:hover {
    color: #FF00FF;
}

/* selected link */
a:active {
     color: #0000FF;
} 

##CSS Pseudo Classes - Others 
:empty          p:empty         Selects every <p> element that has no children 
:lang(language) p:lang(it)      Selects every <p> element with a lang attribute value starting with "it" 
:not(selector)  :not(p)         Selects every element that is not a <p> element 
:root           root            Selects the document's root element 
:target         #news:target    Selects the current active #news element (clicked on a URL containing that anchor name) 

##CSS Pseudo Classes - Form elements 
:checked        input:checked   Selects every checked <input> element 
:disabled       input:disabled  Selects every disabled <input> element 
:enabled        input:enabled   Selects every enabled <input> element 
:focus          input:focus     Selects the <input> element that has focus 
:invalid        input:invalid   Selects all <input> elements with an invalid value 
:optional       input:optional  Selects <input> elements with no "required" attribute 
:required       input:required  Selects <input> elements with a "required" attribute specified 
:valid          input:valid     Selects all <input> elements with a valid value 
:read-only      input:read-only Selects <input> elements with a "readonly" attribute specified 

:in-range       input:in-range      Selects <input> elements with a value within a specified range 
:out-of-range   input:out-of-range  Selects <input> elements with a value outside a specified range 
:read-write     input:read-write    Selects <input> elements with no "readonly" attribute 

#:in-range, :out-of-range selector only works for elements with range limitations, 
#such as input elements with min and max attributes



##CSS Pseudo Classes - Child selections 
:last-child     p:last-child    Selects every <p> elements that is the last child of its parent 
:first-child    p:first-child   Selects every <p> elements that is the first child of its parent 

:last-of-type   p:last-of-type  Selects every <p> element that is the last <p> element of its parent 
:first-of-type  p:first-of-type Selects every <p> element that is the first <p> element of its parent 

:only-of-type   p:only-of-type  Selects every <p> element that is the only <p> element of its parent 
:only-child     p:only-child    Selects every <p> element that is the only child of its parent 

#n can be a number, a keyword, or a formula.
:nth-child(n)           p:nth-child(2)          Selects every <p> element that is the second child of its parent 
:nth-last-child(n)      p:nth-last-child(2)     Selects every <p> element that is the second child of its parent, counting from the last child 
:nth-last-of-type(n)    p:nth-last-of-type(2)   Selects every <p> element that is the second <p> element of its parent, counting from the last child 
:nth-of-type(n)         p:nth-of-type(2)        Selects every <p> element that is the second <p> element of its parent 

#Odd and even are keywords that can be used to match child elements 
#whose index is odd or even (the index of the first child is 1).

p:nth-child(odd) {
     background: red;
}

p:nth-child(even) {
     background: blue;
} 

#Using a formula (a*n + b). 
#a represents a cycle size(can be negative to denote from last), 
#n is a counter (starts at 0), 
#and b is an offset value.

p:nth-child(3n+0) {
     background: red;
} 




###XPATh Reference 

#If the path starts with the slash / , 
#then it represents an absolute path to the required element.
/AAA
/AAA/CCC
/AAA/DDD/BBB

#If the path starts with // 
#then all elements in the document which fulfill following criteria are selected.
//BBB
//DDD/BBB


#The star * selects all elements located by preceeding path
/AAA/CCC/DDD/*
/*/*/*/BBB
//*


#Expresion in square brackets can further specify an element. 
#A number in the brackets gives the position of the element in the selected set. 
#The function last() selects the last element in the selection.
/AAA/BBB[1]
/AAA/BBB[last()]


#Attributes are specified by @ prefix.
//@id
//BBB[@id]
//BBB[@name]
//BBB[@*]
//BBB[not(@*)]

#Values of attributes can be used as selection criteria. 
#Function normalize-space removes leading and trailing spaces 
#and replaces sequences of whitespace characters by a single space.
//BBB[@id='b1']
//BBB[@name='bbb']
//BBB[normalize-space(@name)='bbb']

#Function count() counts the number of selected elements
//*[count(BBB)=2]
//*[count(*)=2]
//*[count(*)=3]


#Function name() returns name of the element, 
#the starts-with function returns true if the first argument string starts with the second argument string, 
#the contains function returns true if the first argument string contains the second argument string.
//*[name()='BBB']
//*[starts-with(name(),'B')]
//*[contains(name(),'C')]

#The string-length function returns the number of characters in the string. 
#You must use &lt; as a substitute for < and &gt; as a substitute for > .
//*[string-length(name()) = 3]
//*[string-length(name()) < 3]
//*[string-length(name()) > 3]

#Several paths can be combined with | separator.
//CCC | //BBB
/AAA/EEE | //BBB
/AAA/EEE | //DDD/CCC | /AAA | //BBB


##child axis
#The child axis contains the children of the context node. 
#The child axis is the default axis and it can be omitted.
/AAA
/child::AAA
/AAA/BBB
/child::AAA/child::BBB
/child::AAA/BBB


##Descendant axis
#The descendant axis contains the descendants of the context node; 
#a descendant is a child or a child of a child and so on; 
#thus the descendant axis never contains attribute or namespace nodes
/descendant::*
/AAA/BBB/descendant::*
//CCC/descendant::*
//CCC/descendant::DDD

##Parent axis
#The parent axis contains the parent of the context node, if there is one.
# It can be abbreviated as two periods (..).
//DDD/parent::*


##Ancestor axis
#The ancestor axis contains the ancestors of the context node; 
#the ancestors of the context node consist of the parent of context node 
#and the parent's parent and so on; 
#thus, the ancestor axis will always include the root node, unless the context node is the root node.
/AAA/BBB/DDD/CCC/EEE/ancestor::*
//FFF/ancestor::*

##Following-sibling axis
#The following-sibling axis contains all the following siblings of the context node.
/AAA/BBB/following-sibling::*
//CCC/following-sibling::*

##Preceding-sibling axis
#The preceding-sibling axis contains all the preceding siblings of the context node
/AAA/XXX/preceding-sibling::*
//CCC/preceding-sibling::*

##Following axis
#The following axis contains all nodes in the same document 
#as the context node that are after the context node in document order, 
#excluding any descendants and excluding attribute nodes and namespace nodes.
/AAA/XXX/following::*
//ZZZ/following::*

##Preceding axis
#The preceding axis contains all nodes in the same document 
#as the context node that are before the context node in document order,
#excluding any ancestors and excluding attribute nodes and namespace nodes
/AAA/XXX/preceding::*
//GGG/preceding::*

##Descendant-or-self axis
#The descendant-or-self axis contains the context node 
#and the descendants of the context node
/AAA/XXX/descendant-or-self::*
//CCC/descendant-or-self::*

##Ancestor-or-self axis
#The ancestor-or-self axis contains the context node 
#and the ancestors of the context node; 
#thus, the ancestor-or-self axis will always include the root node.
/AAA/XXX/DDD/EEE/ancestor-or-self::*
//GGG/ancestor-or-self::*

##Orthogonal axes
#The ancestor, descendant, following, preceding 
#and self axes partition a document (ignoring attribute and namespace nodes): 
#they do not overlap and together they contain all the nodes in the document.
//GGG/ancestor::*
//GGG/descendant::*
//GGG/following::*
//GGG/preceding::*
//GGG/self::*
//GGG/ancestor::* | //GGG/descendant::* | //GGG/following::* | //GGG/preceding::* | //GGG/self::*

##Numeric operations
#The div operator performs floating-point division, 
#the mod operator returns the remainder from a truncating division. 
#The floor function returns the largest (closest to positive infinity) number that is not greater than the argument and that is an integer.
#The ceiling function returns the smallest (closest to negative infinity) number that is not less than the argument and that is an integer.
//BBB[position() mod 2 = 0 ]
//BBB[ position() = floor(last() div 2 + 0.5) or position() = ceiling(last() div 2 + 0.5) ]
//CCC[ position() = floor(last() div 2 + 0.5) or position() = ceiling(last() div 2 + 0.5) ]

###XPATh Reference - Example - *S* means selected 
#http://www.zvon.org/comp/r/tut-XPath_1.html
/AAA
     <AAA>  *S*
          <BBB/>
          <CCC/>
          <BBB/>
          <BBB/>
          <DDD>
               <BBB/>
          </DDD>
          <CCC/>
     </AAA> *S*
 
/AAA/CCC

     <AAA>
          <BBB/>
          <CCC/> *S*
          <BBB/>
          <BBB/>
          <DDD>
               <BBB/>
          </DDD>
          <CCC/> *S*
     </AAA>
 
/AAA/DDD/BBB

     <AAA>
          <BBB/>
          <CCC/>
          <BBB/>
          <BBB/>
          <DDD>
               <BBB/> *S*
          </DDD>
          <CCC/>
     </AAA> 
     
     
//BBB

     <AAA>
          <BBB/>    *S*
          <CCC/>
          <BBB/>    *S*
          <DDD>
               <BBB/>   *S*
          </DDD>
          <CCC>
               <DDD>
                    <BBB/>  *S*
                    <BBB/> *S*
               </DDD>
          </CCC>
     </AAA>
 
//DDD/BBB

     <AAA>
          <BBB/>
          <CCC/>
          <BBB/>
          <DDD>
               <BBB/> *S*
          </DDD>
          <CCC>
               <DDD>
                    <BBB/> *S*
                    <BBB/> *S*
               </DDD>
          </CCC>
     </AAA>     
     
/AAA/CCC/DDD/*

     <AAA>
          <XXX>
               <DDD>
                    <BBB/>
                    <BBB/>
                    <EEE/>
                    <FFF/>
               </DDD>
          </XXX>
          <CCC>
               <DDD>
                    <BBB/> *S*
                    <BBB/> *S*
                    <EEE/> *S*
                    <FFF/> *S*
               </DDD>
          </CCC>
          <CCC>
               <BBB>
                    <BBB>
                         <BBB/>
                    </BBB>
               </BBB>
          </CCC>
     </AAA>
 
/*/*/*/BBB
Select all elements BBB which have 3 ancestors

     <AAA>
          <XXX>
               <DDD>
                    <BBB/> *S*
                    <BBB/> *S*
                    <EEE/>
                    <FFF/>
               </DDD>
          </XXX>
          <CCC>
               <DDD>
                    <BBB/> *S*
                    <BBB/> *S*
                    <EEE/>
                    <FFF/>
               </DDD>
          </CCC>
          <CCC>
               <BBB>
                    <BBB> *S*
                         <BBB/>
                    </BBB>
               </BBB>
          </CCC>
     </AAA>
 
//*
Select all elements

     <AAA>                      *S*
          <XXX>                 *S*
               <DDD>            *S*
                    <BBB/>      *S*
                    <BBB/>      *S*
                    <EEE/>      *S*
                    <FFF/>      *S*
               </DDD>           *S*
          </XXX>                *S*
          <CCC>                 *S*
               <DDD>            *S*
                    <BBB/>      *S*
                    <BBB/>      *S*
                    <EEE/>      *S*
                    <FFF/>      *S*
               </DDD>           *S*
          </CCC>                *S*
          <CCC>                 *S*
               <BBB>            *S*
                    <BBB>       *S*
                         <BBB/> *S*
                    </BBB>      *S*
               </BBB>           *S*
          </CCC>                *S*
     </AAA> 

     
/AAA/BBB[1]
Select the first BBB child of element AAA

     <AAA>
          <BBB/> *S*
          <BBB/>
          <BBB/>
          <BBB/>
     </AAA>
 
/AAA/BBB[last()]
Select the last BBB child of element AAA

     <AAA>
          <BBB/>
          <BBB/>
          <BBB/>
          <BBB/> *S*
     </AAA> 

//@id
Select all attributes @id

     <AAA>
          <BBB id = "b1" *S*/>
          <BBB id = "b2" *S*/>
          <BBB name = "bbb"/>
          <BBB/>
     </AAA>
 
//BBB[@id]
Select BBB elements which have attribute id

     <AAA>
          <BBB id = "b1"/> *S*
          <BBB id = "b2"/> *S*
          <BBB name = "bbb"/>
          <BBB/>
     </AAA>
 
//BBB[@name]
Select BBB elements which have attribute name

     <AAA>
          <BBB id = "b1"/>
          <BBB id = "b2"/>
          <BBB name = "bbb"/> *S*
          <BBB/>
     </AAA>
 
//BBB[@*]
Select BBB elements which have any attribute

     <AAA>
          <BBB id = "b1"/> *S*
          <BBB id = "b2"/> *S*
          <BBB name = "bbb"/> *S*
          <BBB/>
     </AAA>
 
//BBB[not(@*)]
Select BBB elements without an attribute

     <AAA>
          <BBB id = "b1"/>
          <BBB id = "b2"/>
          <BBB name = "bbb"/>
          <BBB/> *S*
     </AAA> 

//BBB[@id='b1']
Select BBB elements which have attribute id with value b1

     <AAA>
          <BBB id = "b1"/> *S*
          <BBB name = " bbb "/>
          <BBB name = "bbb"/>
     </AAA>
 
//BBB[@name='bbb']
Select BBB elements which have attribute name with value 'bbb'

     <AAA>
          <BBB id = "b1"/>
          <BBB name = " bbb "/>
          <BBB name = "bbb"/> *S*
     </AAA>
 
//BBB[normalize-space(@name)='bbb']
Select BBB elements which have attribute name with value bbb, leading and trailing spaces are removed before comparison

     <AAA>
          <BBB id = "b1"/>
          <BBB name = " bbb "/> *S*
          <BBB name = "bbb"/> *S*
     </AAA> 

//*[count(BBB)=2]
Select elements which have two children BBB

     <AAA>
          <CCC>
               <BBB/>
               <BBB/>
               <BBB/>
          </CCC>
          <DDD> *S*
               <BBB/>
               <BBB/>
          </DDD> *S*
          <EEE>
               <CCC/>
               <DDD/>
          </EEE>
     </AAA>
 
//*[count(*)=2]
Select elements which have 2 children

     <AAA>
          <CCC>
               <BBB/>
               <BBB/>
               <BBB/>
          </CCC>
          <DDD> *S*
               <BBB/>
               <BBB/>
          </DDD> *S*
          <EEE> *S*
               <CCC/>
               <DDD/>
          </EEE> *S*
     </AAA>
 
//*[count(*)=3]
Select elements which have 3 children

     <AAA> *S*
          <CCC> *S*
               <BBB/>
               <BBB/>
               <BBB/>
          </CCC> *S*
          <DDD>
               <BBB/>
               <BBB/>
          </DDD>
          <EEE>
               <CCC/>
               <DDD/>
          </EEE>
     </AAA>  *S*

//*[name()='BBB']
Select all elements with name BBB, equivalent with //BBB

     <AAA>
          <BCC>
               <BBB/> *S*
               <BBB/> *S*
               <BBB/> *S*
          </BCC>
          <DDB>
               <BBB/> *S*
               <BBB/> *S*
          </DDB>
          <BEC>
               <CCC/>
               <DBD/>
          </BEC>
     </AAA>
 
//*[starts-with(name(),'B')]
Select all elements name of which starts with letter B

     <AAA>
          <BCC> *S*
               <BBB/> *S*
               <BBB/> *S*
               <BBB/> *S*
          </BCC> *S*
          <DDB>
               <BBB/> *S*
               <BBB/> *S*
          </DDB>
          <BEC> *S*
               <CCC/>
               <DBD/>
          </BEC> *S*
     </AAA>
 
//*[contains(name(),'C')]
Select all elements name of which contain letter C

     <AAA>
          <BCC> *S*
               <BBB/>
               <BBB/>
               <BBB/>
          </BCC> *S*
          <DDB>
               <BBB/>
               <BBB/>
          </DDB>
          <BEC> *S*
               <CCC/> *S*
               <DBD/>
          </BEC> *S*
     </AAA> 

//*[string-length(name()) = 3]
Select elements with three-letter name

     <AAA> *S*
          <Q/>
          <SSSS/>
          <BB/>
          <CCC/> *S*
          <DDDDDDDD/>
          <EEEE/>
     </AAA> *S*
 
//*[string-length(name()) < 3]
Select elements name of which has one or two characters

     <AAA>
          <Q/> *S*
          <SSSS/>
          <BB/> *S*
          <CCC/>
          <DDDDDDDD/>
          <EEEE/>
     </AAA>
 
//*[string-length(name()) > 3]
Select elements with name longer than three characters

     <AAA>
          <Q/>
          <SSSS/> *S*
          <BB/>
          <CCC/>
          <DDDDDDDD/> *S*
          <EEEE/> *S*
     </AAA> 

//CCC | //BBB
Select all elements CCC and BBB

     <AAA>
          <BBB/> *S*
          <CCC/> *S*
          <DDD>
               <CCC/> *S*
          </DDD>
          <EEE/>
     </AAA>
 
/AAA/EEE | //BBB
Select all elements BBB and elements EEE which are children of root element AAA

     <AAA>
          <BBB/> *S*
          <CCC/>
          <DDD>
               <CCC/>
          </DDD>
          <EEE/> *S*
     </AAA>
 
/AAA/EEE | //DDD/CCC | /AAA | //BBB
Number of combinations is not restricted

     <AAA> *S*
          <BBB/> *S*
          <CCC/>
          <DDD>
               <CCC/> *S*
          </DDD>
          <EEE/> *S*
     </AAA>  *S*

/AAA
Equivalent of /child::AAA

     <AAA> *S*
          <BBB/>
          <CCC/>
     </AAA> *S*
 
/child::AAA
Equivalent of /AAA

     <AAA> *S*
          <BBB/>
          <CCC/>
     </AAA> *S*
 
/AAA/BBB
Equivalent of /child::AAA/child::BBB

     <AAA>
          <BBB/> *S*
          <CCC/>
     </AAA>
 
/child::AAA/child::BBB
Equivalent of /AAA/BBB

     <AAA>
          <BBB/> *S*
          <CCC/>
     </AAA>
 
/child::AAA/BBB
Both possibilities can be combined

     <AAA>
          <BBB/> *S*
          <CCC/>
     </AAA> 
/descendant::*
Select all descendants of document root and therefore all elements

     <AAA>                               *S*
          <BBB>                          *S*
               <DDD>                     *S*
                    <CCC>                *S*
                         <DDD/>          *S*
                         <EEE/>          *S*
                    </CCC>               *S*
               </DDD>                    *S*
          </BBB>                         *S*
          <CCC>                          *S*
               <DDD>                     *S*
                    <EEE>                *S*
                         <DDD>           *S*
                              <FFF/>     *S*
                         </DDD>          *S*
                    </EEE>               *S*
               </DDD>                    *S*
          </CCC>                         *S*
     </AAA>                              *S*
 
/AAA/BBB/descendant::*
Select all descendants of /AAA/BBB

     <AAA>
          <BBB>
               <DDD> *S*
                    <CCC> *S*
                         <DDD/> *S*
                         <EEE/> *S*
                    </CCC> *S*
               </DDD> *S*
          </BBB>
          <CCC>
               <DDD>
                    <EEE>
                         <DDD>
                              <FFF/>
                         </DDD>
                    </EEE>
               </DDD>
          </CCC>
     </AAA>
 
//CCC/descendant::*
Select all elements which have CCC among its ancestors

     <AAA>
          <BBB>
               <DDD>
                    <CCC>
                         <DDD/> *S*
                         <EEE/> *S*
                    </CCC>
               </DDD>
          </BBB>
          <CCC>
               <DDD> *S*
                    <EEE> *S*
                         <DDD> *S*
                              <FFF/> *S*
                         </DDD> *S*
                    </EEE> *S*
               </DDD> *S*
          </CCC>
     </AAA>
 
//CCC/descendant::DDD
Select elements DDD which have CCC among its ancestors

     <AAA>
          <BBB>
               <DDD>
                    <CCC>
                         <DDD/> *S*
                         <EEE/>
                    </CCC>
               </DDD>
          </BBB>
          <CCC>
               <DDD> *S*
                    <EEE>
                         <DDD> *S*
                              <FFF/>
                         </DDD> *S*
                    </EEE>
               </DDD> *S*
          </CCC>
     </AAA> 

//DDD/parent::*
Select all parents of DDD element

     <AAA>
          <BBB> *S*
               <DDD>
                    <CCC> *S*
                         <DDD/>
                         <EEE/>
                    </CCC> *S*
               </DDD>
          </BBB> *S*
          <CCC> *S*
               <DDD>
                    <EEE> *S*
                         <DDD>
                              <FFF/>
                         </DDD>
                    </EEE> *S*
               </DDD>
          </CCC> *S*
     </AAA> 
/AAA/BBB/DDD/CCC/EEE/ancestor::*
Select all elements given in this absolute path

     <AAA> *S*
          <BBB> *S*
               <DDD> *S*
                    <CCC> *S*
                         <DDD/>
                         <EEE/>
                    </CCC> *S*
               </DDD> *S*
          </BBB> *S*
          <CCC>
               <DDD>
                    <EEE>
                         <DDD>
                              <FFF/>
                         </DDD>
                    </EEE>
               </DDD>
          </CCC>
     </AAA> *S*
 
//FFF/ancestor::*
Select ancestors of FFF element

     <AAA> *S*
          <BBB>
               <DDD>
                    <CCC>
                         <DDD/>
                         <EEE/>
                    </CCC>
               </DDD>
          </BBB>
          <CCC> *S*
               <DDD> *S*
                    <EEE> *S*
                         <DDD> *S*
                              <FFF/>
                         </DDD> *S*
                    </EEE> *S*
               </DDD> *S*
          </CCC> *S*
     </AAA>  *S*
/AAA/BBB/following-sibling::*

     <AAA>
          <BBB>
               <CCC/>
               <DDD/>
          </BBB>
          <XXX> *S*
               <DDD>
                    <EEE/>
                    <DDD/>
                    <CCC/>
                    <FFF/>
                    <FFF>
                         <GGG/>
                    </FFF>
               </DDD>
          </XXX> *S*
          <CCC> *S*
               <DDD/>
          </CCC> *S*
     </AAA>
 
//CCC/following-sibling::*

     <AAA>
          <BBB>
               <CCC/>
               <DDD/> *S*
          </BBB>
          <XXX>
               <DDD>
                    <EEE/>
                    <DDD/>
                    <CCC/>
                    <FFF/> *S*
                    <FFF> *S*
                         <GGG/>
                    </FFF> *S*
               </DDD>
          </XXX>
          <CCC>
               <DDD/>
          </CCC>
     </AAA> 
/AAA/XXX/preceding-sibling::*

     <AAA>
          <BBB> *S*
               <CCC/>
               <DDD/>
          </BBB> *S*
          <XXX>
               <DDD>
                    <EEE/>
                    <DDD/>
                    <CCC/>
                    <FFF/>
                    <FFF>
                         <GGG/>
                    </FFF>
               </DDD>
          </XXX>
          <CCC>
               <DDD/>
          </CCC>
     </AAA>
 
//CCC/preceding-sibling::*

     <AAA>
          <BBB> *S*
               <CCC/>
               <DDD/>
          </BBB> *S*
          <XXX> *S*
               <DDD> 
                    <EEE/> *S*
                    <DDD/> *S*
                    <CCC/>
                    <FFF/>
                    <FFF>
                         <GGG/>
                    </FFF>
               </DDD>
          </XXX> *S*
          <CCC>
               <DDD/>
          </CCC>
     </AAA> 
/AAA/XXX/following::*

     <AAA>
          <BBB>
               <CCC/>
               <ZZZ>
                    <DDD/>
                    <DDD>
                         <EEE/>
                    </DDD>
               </ZZZ>
               <FFF>
                    <GGG/>
               </FFF>
          </BBB>
          <XXX>
               <DDD>
                    <EEE/>
                    <DDD/>
                    <CCC/>
                    <FFF/>
                    <FFF>
                         <GGG/>
                    </FFF>
               </DDD>
          </XXX>
          <CCC> *S*
               <DDD/> *S*
          </CCC> *S*
     </AAA>
 
//ZZZ/following::*

     <AAA>
          <BBB>
               <CCC/>
               <ZZZ>
                    <DDD/>
                    <DDD>
                         <EEE/>
                    </DDD>
               </ZZZ>
               <FFF> *S*
                    <GGG/> *S*
               </FFF> *S*
          </BBB>
          <XXX>                  *S*
               <DDD>             *S*
                    <EEE/>       *S*
                    <DDD/>       *S*
                    <CCC/>       *S*
                    <FFF/>       *S*
                    <FFF>        *S*
                         <GGG/>  *S*
                    </FFF>       *S*
               </DDD>            *S*
          </XXX>                 *S*
          <CCC>                  *S*
               <DDD/>            *S*
          </CCC>                 *S*
     </AAA> 
/AAA/XXX/preceding::*

     <AAA>
          <BBB> *S*
               <CCC/> *S*
               <ZZZ> *S*
                    <DDD/> *S*
               </ZZZ> *S*
          </BBB> *S*
          <XXX>
               <DDD>
                    <EEE/>
                    <DDD/>
                    <CCC/>
                    <FFF/>
                    <FFF>
                         <GGG/>
                    </FFF>
               </DDD>
          </XXX>
          <CCC>
               <DDD/>
          </CCC>
     </AAA>
 
//GGG/preceding::*

     <AAA>
          <BBB> *S*
               <CCC/> *S*
               <ZZZ> *S*
                    <DDD/> *S*
               </ZZZ> *S*
          </BBB> *S*
          <XXX>
               <DDD>
                    <EEE/> *S*
                    <DDD/> *S*
                    <CCC/> *S*
                    <FFF/> *S*
                    <FFF>
                         <GGG/>
                    </FFF>
               </DDD>
          </XXX>
          <CCC>
               <DDD/>
          </CCC>
     </AAA> 
/AAA/XXX/descendant-or-self::*

     <AAA>
          <BBB>
               <CCC/>
               <ZZZ>
                    <DDD/>
               </ZZZ>
          </BBB>
          <XXX>                  *S*
               <DDD>             *S*
                    <EEE/>       *S*
                    <DDD/>       *S*
                    <CCC/>       *S*
                    <FFF/>       *S*
                    <FFF>        *S*
                         <GGG/>  *S*
                    </FFF>       *S*
               </DDD>            *S*
          </XXX>                 *S*
          <CCC>
               <DDD/>
          </CCC>
     </AAA>
 
//CCC/descendant-or-self::*

     <AAA>
          <BBB>
               <CCC/> *S*
               <ZZZ>
                    <DDD/>
               </ZZZ>
          </BBB>
          <XXX>
               <DDD>
                    <EEE/>
                    <DDD/>
                    <CCC/> *S*
                    <FFF/>
                    <FFF>
                         <GGG/>
                    </FFF>
               </DDD>
          </XXX>
          <CCC> *S*
               <DDD/> *S*
          </CCC> *S*
     </AAA> 
     
/AAA/XXX/DDD/EEE/ancestor-or-self::*

     <AAA>*S*
          <BBB>
               <CCC/>
               <ZZZ>
                    <DDD/>
               </ZZZ>
          </BBB>
          <XXX>*S*
               <DDD>*S*
                    <EEE/>*S*
                    <DDD/>
                    <CCC/>
                    <FFF/>
                    <FFF>
                         <GGG/>
                    </FFF>
               </DDD>*S*
          </XXX>*S*
          <CCC>
               <DDD/>
          </CCC>
     </AAA>*S*
 
//GGG/ancestor-or-self::*

     <AAA>*S*
          <BBB>
               <CCC/>
               <ZZZ>
                    <DDD/>
               </ZZZ>
          </BBB>
          <XXX>*S*
               <DDD>*S*
                    <EEE/>
                    <DDD/>
                    <CCC/>
                    <FFF/>
                    <FFF>*S*
                         <GGG/>*S*
                    </FFF>*S*
               </DDD>*S*
          </XXX>*S*
          <CCC>
               <DDD/>
          </CCC>
     </AAA> *S*
     
//GGG/ancestor::*

     <AAA>*S*
          <BBB>
               <CCC/>
               <ZZZ/>
          </BBB>
          <XXX>*S*
               <DDD>*S*
                    <EEE/>
                    <FFF>*S*
                         <HHH/>
                         <GGG>
                              <JJJ>
                                   <QQQ/>
                              </JJJ>
                              <JJJ/>
                         </GGG>
                         <HHH/>
                    </FFF>*S*
               </DDD>*S*
          </XXX>*S*
          <CCC>
               <DDD/>
          </CCC>
     </AAA>*S*
 
//GGG/descendant::*

     <AAA>
          <BBB>
               <CCC/>
               <ZZZ/>
          </BBB>
          <XXX>
               <DDD>
                    <EEE/>
                    <FFF>
                         <HHH/>
                         <GGG>
                              <JJJ>*S*
                                   <QQQ/>*S*
                              </JJJ>*S*
                              <JJJ/>*S*
                         </GGG>
                         <HHH/>
                    </FFF>
               </DDD>
          </XXX>
          <CCC>
               <DDD/>
          </CCC>
     </AAA>
 
//GGG/following::*

     <AAA>
          <BBB>
               <CCC/>
               <ZZZ/>
          </BBB>
          <XXX>
               <DDD>
                    <EEE/>
                    <FFF>
                         <HHH/>
                         <GGG>
                              <JJJ>
                                   <QQQ/>
                              </JJJ>
                              <JJJ/>
                         </GGG>
                         <HHH/>*S*
                    </FFF>
               </DDD>
          </XXX>
          <CCC>*S*
               <DDD/>*S*
          </CCC>*S*
     </AAA>
 
//GGG/preceding::*

     <AAA>
          <BBB>*S*
               <CCC/>*S*
               <ZZZ/>*S*
          </BBB>*S*
          <XXX>
               <DDD>
                    <EEE/>
                    <FFF>
                         <HHH/>*S*
                         <GGG>
                              <JJJ>
                                   <QQQ/>
                              </JJJ>
                              <JJJ/>
                         </GGG>
                         <HHH/>
                    </FFF>
               </DDD>
          </XXX>
          <CCC>
               <DDD/>
          </CCC>
     </AAA>
 
//GGG/self::*
# It can be abbreviated as a single period (.).
     <AAA>
          <BBB>
               <CCC/>
               <ZZZ/>
          </BBB>
          <XXX>
               <DDD>
                    <EEE/>
                    <FFF>
                         <HHH/>
                         <GGG>*S*
                              <JJJ>
                                   <QQQ/>
                              </JJJ>
                              <JJJ/>
                         </GGG>*S*
                         <HHH/>
                    </FFF>
               </DDD>
          </XXX>
          <CCC>
               <DDD/>
          </CCC>
     </AAA>
 
//GGG/ancestor::* | //GGG/descendant::* | //GGG/following::* | //GGG/preceding::* | //GGG/self::*

     <AAA>                                      *S*   
          <BBB>                                 *S*
               <CCC/>                           *S*
               <ZZZ/>                           *S*
          </BBB>                                *S*
          <XXX>                                 *S*
               <DDD>                            *S*
                    <EEE/>                      *S*
                    <FFF>                       *S*
                         <HHH/>                 *S*
                         <GGG>               *S*
                              <JJJ>             *S*
                                   <QQQ/>       *S*
                              </JJJ>            *S*
                              <JJJ/>            *S*
                         </GGG>            *S*
                         <HHH/>                 *S*
                    </FFF>                      *S*
               </DDD>                           *S*
          </XXX>                                *S*
          <CCC>                                 *S*
               <DDD/>                           *S*
          </CCC>                                *S*
     </AAA>                                     *S*
     
//BBB[position() mod 2 = 0 ]
Select even BBB elements

     <AAA>
          <BBB/>
          <BBB/> *S*
          <BBB/>
          <BBB/> *S*
          <BBB/>
          <BBB/> *S*
          <BBB/>
          <BBB/> *S*
          <CCC/>
          <CCC/>
          <CCC/>
     </AAA>
 
//BBB[ position() = floor(last() div 2 + 0.5) or position() = ceiling(last() div 2 + 0.5) ]
Select middle BBB element(s)

     <AAA>
          <BBB/>
          <BBB/>
          <BBB/>
          <BBB/> *S*
          <BBB/> *S*
          <BBB/>
          <BBB/>
          <BBB/>
          <CCC/>
          <CCC/>
          <CCC/>
     </AAA>
 
//CCC[ position() = floor(last() div 2 + 0.5) or position() = ceiling(last() div 2 + 0.5) ]
Select middle CCC element(s)

     <AAA>
          <BBB/>
          <BBB/>
          <BBB/>
          <BBB/>
          <BBB/>
          <BBB/>
          <BBB/>
          <BBB/>
          <CCC/>
          <CCC/> *S*
          <CCC/>
     </AAA> 
     

