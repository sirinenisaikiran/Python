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

    


if __name__ == "__main__":
    ## to enable logging , start with 'python basic.py --logging=info'
    # check other options eg log file prefix, rotation etc 
    #https://www.tornadoweb.org/en/stable/_modules/tornado/log.html#LogFormatter
    tornado.options.parse_command_line()  
    application =  make_app()
    application.listen(8888)
    
    # In Python, signals are always handled by the main thread. 
    # If the IOLoop is run from the main thread, it will block it when server is idle 
    # and waiting for IO. 
    # As a result, all signals will be pending on the thread to wake up. 
    # So, press  crtl+c and then refresh browser or install below callback 
    tornado.ioloop.PeriodicCallback( lambda:None, 1000 ).start()      
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:  #for crtl+c 
        logging.getLogger("tornado.general").info("Exiting")
        tornado.ioloop.IOLoop.current().stop()
        