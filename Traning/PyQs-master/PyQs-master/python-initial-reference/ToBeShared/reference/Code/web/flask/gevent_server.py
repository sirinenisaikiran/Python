from gevent.pywsgi import WSGIServer
from rest import app

http_server = WSGIServer(('127.0.0.1', 5000), app)
http_server.serve_forever()