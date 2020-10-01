'''
$ pip install gevent 

'''

from gevent.pywsgi import WSGIServer
from myblog.wsgi import application as app

http_server = WSGIServer(('127.0.0.1', 8000), app)
http_server.serve_forever()