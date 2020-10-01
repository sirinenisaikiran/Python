'''
$ pip install gunicorn
$ gunicorn --bind 0.0.0.0:8000  -w 4 rest:app

#Guicorn works in unix only 

#Alternate is waitress 
$ pip install waitress

# Listen on both IPv4 and IPv6 on port 8041
waitress-serve --listen=*:8041 rest:app

# Listen on only IPv4 on port 8041
waitress-serve --port=8041 rest:app 

#OR 

from waitress import serve
serve(wsgiapp, listen='*:8080')

'''
from examplesite.wsgi import application as app
from waitress import serve
serve(app, host='0.0.0.0', port=8080)