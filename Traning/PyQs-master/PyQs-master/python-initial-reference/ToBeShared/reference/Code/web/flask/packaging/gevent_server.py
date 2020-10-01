from gevent.pywsgi import WSGIServer
from flaskr import app

#http_server = WSGIServer(('127.0.0.1', 5000), app)
http_server = WSGIServer(('localhost', 5000), app, keyfile='key.pem', certfile='cert.pem')
http_server.serve_forever()