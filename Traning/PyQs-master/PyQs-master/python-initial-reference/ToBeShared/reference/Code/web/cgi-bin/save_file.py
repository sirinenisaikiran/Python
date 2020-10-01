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
    