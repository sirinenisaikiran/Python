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


