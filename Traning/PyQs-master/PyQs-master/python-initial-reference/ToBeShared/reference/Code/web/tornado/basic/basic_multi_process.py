import tornado.options
import logging
import tornado.ioloop
import tornado.web
import signal

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])
    
#Due to the Python GIL (Global Interpreter Lock), 
#it is necessary to run multiple Python processes to take full advantage of multi-CPU machines. 
#Typically it is best to run one process per CPU.

#note this requires unix as it uses os.fork 
def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8888)
    server.start(0)  # forks one process per cpu
    IOLoop.current().start()    


if __name__ == "__main__":
    ## to enable logging , start with 'python basic_multi_process.py --logging=info'
    # check other options eg log file prefix, rotation etc 
    #https://www.tornadoweb.org/en/stable/_modules/tornado/log.html#LogFormatter
    tornado.options.parse_command_line()      
    # In Python, signals are always handled by the main thread. 
    # If the IOLoop is run from the main thread, it will block it when server is idle 
    # and waiting for IO. 
    # As a result, all signals will be pending on the thread to wake up. 
    # So, press  crtl+c and then refresh browser 
    main()
        