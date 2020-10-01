'''
WSGI is a synchronous interface, while Tornado’s concurrency model is based on single-threaded 
asynchronous execution. This means that running a WSGI app with Tornado’s WSGIContainer 
is less scalable than running the same app in a multi-threaded WSGI server like gunicorn 
or uwsgi. Use WSGIContainer only when there are benefits to combining Tornado 
and WSGI in the same process that outweigh the reduced scalability
'''
'''
$ pip install tornado 

'''
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from examplesite.wsgi import application as app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
IOLoop.instance().start()

