#! C:/Python35/python.exe -u 

#-u is must for opening stdin in unbuffered mode 

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

import os, sys , os.path
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
    
   
     

if 'REQUEST_METHOD'  in os.environ and os.environ['REQUEST_METHOD'].upper() == 'POST':
    #print(html % (sys.stdin.read(),))
    main = ""
    for i in range(2):
        while True:
            chunk = sys.stdin.read(10000)
            if not chunk: break
            main += chunk 
    print(main)
else:
    print(html % (string,))
    