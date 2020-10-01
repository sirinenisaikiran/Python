import tornado.options, tornado.ioloop, tornado.web, tornado.escape, tornado.iostream, tornado.gen
import logging
import os,  uuid, shutil
import mimetypes

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world and earth")
        
        
class MainHandler2(tornado.web.RequestHandler):
    def get(self):
        self.write('<a href="%s">link to story 1</a>' %
                   self.reverse_url("story", "1"))  #'story' comes from URL, name , become /story/1

class StoryHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self, story_id):
        self.write("this is story %s" % story_id)

        
#The main entry point for a handler subclass is a method named 
#after the HTTP method being handled: get(), post() ...
#render() loads a Template by name and renders it with the given arguments
#write() is used for non-template-based output; it accepts strings, bytes, and dictionaries 
#(dicts will be encoded as JSON).
class JsonHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.args = None 
        if self.request.headers.get('Content-Type',"Unknown") == 'application/json':
            self.args = tornado.escape.json_decode(self.request.body)
        # Access self.args directly instead of using self.get_argument.
    def get_name(self, name):
        #to search both query or body 
        # RequestHandler.get_argument(name: str, default: Union[None, str, RAISE] = RAISE, strip: bool = True) -> Optional[str]
        # RequestHandler.get_arguments(name: str, strip: bool = True) -> List[str]
        #to search query 
        # RequestHandler.get_query_argument(name: str, default: Union[None, str, RAISE] = RAISE, strip: bool = True) => Optional[str][source]
        # RequestHandler.get_query_arguments(name: str, strip: bool = True) => List[str]
        #to search body 
        # RequestHandler.get_body_argument(name: str, default: Union[None, str, RAISE] = RAISE, strip: bool = True) => Optional[str][source]
        # RequestHandler.get_body_arguments(name: str, strip: bool = True) => List[str]
        res = name 
        if not name:
            if self.args:
                res = self.args.get('name',"Jane Doe")
            elif self.get_query_argument('name', None):
                res = self.get_query_argument('name')
        return res or "Jane Doe"
        
    def get(self, name=None):
        obj = {'name': self.get_name(name), 'age': 200}
        self.set_status(200) 
        self.write(obj)
        
        
class XMLHandler(tornado.web.RequestHandler):
    def get(self, name):
        obj = "<data><name>%s</name><age>%d</age></data>" %(name, 20)
        self.add_header("Content-Type", "application/xml; charset=UTF-8")
        self.write(obj)

    
#In templates, followings are available
#    escape: alias for tornado.escape.xhtml_escape
#    xhtml_escape: alias for tornado.escape.xhtml_escape
#    url_escape: alias for tornado.escape.url_escape
#    json_encode: alias for tornado.escape.json_encode
#    squeeze: alias for tornado.escape.squeeze
#    linkify: alias for tornado.escape.linkify
#    datetime: the Python datetime module
#    handler: the current RequestHandler object
#    request: alias for handler.request
#    current_user: alias for handler.current_user
#    locale: alias for handler.locale
#    _: alias for handler.locale.translate
#    static_url: alias for handler.static_url
#    xsrf_form_html: alias for handler.xsrf_form_html
#    reverse_url: alias for Application.reverse_url
#    All entries from the ui_methods and ui_modules Application settings
#    Any keyword arguments passed to render or render_string
    
# Tornado templates support control statements and expressions. 
# Control statements are surrounded by {% and %}, e.g. {% if len(items) > 2 %}. 
# Expressions are surrounded by {{ and }}, e.g. {{ items[0] }}.

# Control statements more or less map exactly to Python statements. 
# We support if, for, while, and try, all of which are terminated with {% end %}. 
# We also support template inheritance using the extends and block statements

# Expressions can be any Python expression, including function calls. Te
    
class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        #RequestHandler.render_string(template_name: str, **kwargs) -> bytes
        #could have used self.write(html_string) but to support xsrf use below 
        self.render("env_get.html", url=self.reverse_url("myform"))
                   
    def post(self):
        #for list, use RequestHandler.get_body_arguments(name: str, strip: bool = True) -> List[str]
        envp = self.get_body_argument("envp","all").upper()
        env_dict = os.environ
        if os.environ.get(envp, "notfound") != "notfound":
            env_dict = { envp : os.environ.get(envp,"notfound") }        
        self.render("env.html", envs=env_dict)   
        
        
#Login 
#The currently authenticated user is available in every request handler 
#as self.current_user, and in every template as current_user. 
#By default, current_user is None.

#To implement user authentication in your application, 
#you need to override the get_current_user() method in your request handlers 
#to determine the current user based on, e.g., the value of a cookie. 

#Third party authentication
#https://www.tornadoweb.org/en/stable/guide/security.html#third-party-authentication

# RequestHandler.set_secure_cookie(name: str, value: Union[str, bytes], 
#     expires_days: int = 30, version: int = None, **kwargs) -> None
# RequestHandler.get_secure_cookie(name: str, value: str = None, 
#     max_age_days: int = 31, min_version: int = None) => Optional[bytes]

# Note that the expires_days parameter sets the lifetime of the cookie in the browser, 
# but is independent of the max_age_days parameter to get_secure_cookie.
 
# By default, Tornado’s secure cookies expire after 30 days. 
# To change this, use the expires_days keyword argument to set_secure_cookie 
# and the max_age_days argument to get_secure_cookie. 
# These two values are passed separately so that you may 
# e.g. have a cookie that is valid for 30 days for most purposes, 
# but for certain sensitive actions (such as changing billing information) 
# you use a smaller max_age_days when reading the cookie.

def check_auth(username, password):
    return username == 'admin' and password == 'secret'

class SecureBaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class LoginHandler(SecureBaseHandler):
    def get(self):
        self.render("login.html", url=self.application.settings['login_url'])

    def post(self):
        name = self.get_argument("name", None)
        password = self.get_argument("password", None)        
        if check_auth(name, password):
            self.set_secure_cookie("user", name)
            self.redirect(self.get_argument("next", None) or self.reverse_url("secure_site") )
        else:
             self.redirect(self.application.settings['login_url'])

        
# If a request goes to a method with tornado.web.authenticated decorator, 
# and the user is not logged in, they will be redirected to login_url

# If you decorate post() methods with the authenticated decorator, 
# and the user is not logged in, the server will send a 403 response. 
# The @authenticated decorator is simply shorthand for
# if not self.current_user: self.redirect()
# Note, it appends ?next=self.request.uri

class SecureMainHandler(SecureBaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)
        
"""
To use with requests 


import requests

URL = 'http://localhost:8888/login'

client = requests.session()

# Retrieve the CSRF token first
getr = client.get(URL)  # sets cookie
from bs4 import BeautifulSoup
soup = BeautifulSoup(getr.text, 'html.parser')

#if with cookies 
if 'csrftoken' in client.cookies:
    # Django 1.6 and up
    csrftoken = client.cookies['csrftoken']
else:
    # older versions
    csrftoken = client.cookies['csrf']
login_data = dict(username=EMAIL, password=PASSWORD, csrfmiddlewaretoken=csrftoken, next='/')

#if with page meta holds the CSRF token
csrf_token = soup.select_one('meta[name="csrf-token"]')['content']

#if with header 
csrf_token = getr.headers.get('X-Xsrf-Token',None) or getr.headers['X-CSRFToken']

#in our case 
csrftoken = soup.find('input', dict(name='_xsrf'))['value']
#or 
csrftoken = client.cookies['_xsrf']

login_data = dict(name='admin', password='secret', _xsrf=csrftoken )
r = client.post(URL, data=login_data, params=dict(next='/secure'), headers=dict(Referer=URL))

"""
        
##Upload and download 
class UploadPOSTHandler(tornado.web.RequestHandler):
    def initialize(self, upload_path):
        self.upload_path = upload_path
    def get(self):
        self.render("upload.html")
    def post(self):
        try:
            fileinfo = self.request.files['file'][0]
        except:
            self.redirect(self.reverse_url("upload_normal"))
            return
        try:
            with open(os.path.join(self.upload_path, fileinfo["filename"]), 'wb') as fh:
                fh.write(fileinfo['body'])
            logging.info("%s uploaded %s, saved as %s",
                         str(self.request.remote_ip),
                         str(fileinfo['filename']),
                         fileinfo["filename"])
        except IOError as e:
            logging.error("Failed to write file due to IOError %s", str(e))
        
        self.redirect(self.reverse_url("download", fileinfo['filename']))

        
#Download 
class DownloadHandler(tornado.web.RequestHandler):
    def initialize(self, upload_path):
        self.upload_path = upload_path
    async def get(self, filename):
        # chunk size to read
        chunk_size = 1024 * 1024 * 1 # 1 MiB
        mtype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        self.set_header("Content-Disposition", 'attachment; filename="%s"' %(filename,) )
        self.set_header("Content-Type", mtype )        
        with open(os.path.join(self.upload_path,filename), 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                try:
                    self.write(chunk) # write the cunk to response
                    await self.flush() # flush the current chunk to socket
                except tornado.iostream.StreamClosedError:
                    # this means the client has closed the connection
                    # so break the loop
                    break
                finally:
                    # deleting the chunk is very important because 
                    # if many clients are downloading files at the 
                    # same time, the chunks in memory will keep 
                    # increasing and will eat up the RAM
                    del chunk
                    # pause the coroutine so other handlers can run
                    await tornado.gen.sleep(0.000000001) # 1 nanosecond        
        
        
        
#for large file 
MAX_STREAMED_SIZE = 1024 * 1024 * 1024

# Tornado does not currently  support streaming multi-part uploads. 
# This means that uploads you wish to stream must be simple PUTs, 
# instead of a POST that mixes the uploaded data with other form fields like _xsrf. 
# To use XSRF protection in this scenario you must pass the XSRF token via an HTTP header 
# (X-Xsrf-Token/X-CSRFToken) instead of via a form field. 
# Unfortunately this is incompatible with non-javascript web form uploads; 
# you must have a client capable of setting arbitrary HTTP headers


@tornado.web.stream_request_body
class UploadLargePOSTHandler(tornado.web.RequestHandler):
    def initialize(self, upload_path):
        self.bytes_read = 0
        self.upload_path = upload_path
        self.temp_filename = uuid.uuid4().hex
        
    def prepare(self):
        self.request.connection.set_max_body_size(MAX_STREAMED_SIZE)        
        
    #The regular HTTP method (post, put, etc) will be called 
    #after the entire body has been read.    
    def data_received(self, chunk):
        self.bytes_read += len(chunk)
        #store in temp file 
        with open(os.path.join(self.upload_path, self.temp_filename), 'ab') as fw:
            fw.write(chunk)

    def post(self):
        try:
            fileinfo = self.request.files['file'][0]
        except:
            self.redirect(self.reverse_url("upload_large"))
            return
        try:
            #copy from temp file to correct file 
            import shutil
            with open(os.path.join(self.upload_path, filename), 'wb') as fw:
                with open(os.path.join(self.upload_path, self.temp_filename), 'rb') as fr:
                    shutil.copyfileobj(fr, fw) 
            #remove self.temp_filename
            os.rm(os.path.join(self.upload_path, self.temp_filename))
        except IOError as e:
            logging.error("Failed to write file due to IOError %s", str(e))
        
        self.write("OK")
    def get(self):
        self.render("notsupported.html")
        
#DB 
"""
#check for DB lib in aio-libs eg aiopg, aiomysql etc 
#many other libs in aio-libs
#or 
you can turn synchronous calls into asynchronous ones by wrapping 
them in run_in_executor. For example:

async def fetchall_async(conn, query):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, lambda: conn.cursor().execute(query).fetchall())
   
#OR using tornado

async def fetchall_async(conn, query):
    return await tornado.ioloop.IOLoop.current().run_in_executor(
        None, lambda conn, query: conn.cursor().execute(query).fetchall(), conn, query)
    
#Then using 
async def some_task():
    ...
    students = await fetchall_async(conn, "select * from students")
    
    
#For our case, we would use 
$ pip install aiosqlite

"""
import aiosqlite


class NoResult(Exception):
    pass
        
class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db
    def row_to_obj(self, row, cur):
        obj = tornado.util.ObjectDict()
        for val, desc in zip(row, cur.description):
            obj[desc[0]] = val #first one is name 
        return obj        
        
    async def query(self, stmt, *args):
        async with aiosqlite.connect(self.db) as db:
            db.row_factory = aiosqlite.Row 
            async with db.execute(stmt, args) as cur:
                #in python3.6, https://www.python.org/dev/peps/pep-0530/#implementation
                #return [self.row_to_obj(row, cur) async for row in cur.fetchall()]
                return [self.row_to_obj(row, cur) for row in await cur.fetchall()]
                
    async def queryone(self, stmt, *args):
        results = await self.query(stmt, *args)
        if len(results) >= 0 :
            return results[0] 
        else:
            raise NoResult("No result")
            
async def maybe_create_tables(dbpath):   
    async with aiosqlite.connect(dbpath) as db:
        try:
            async with db.execute("SELECT COUNT(*) FROM people LIMIT 1") as cursor:
                await cursor.fetchone()
        except :                
            await db.execute("""create table if not exists people (name string, age int)""")
            await db.execute("""insert into people values(?,?) """, ('xyz',20))
            await db.execute("""insert into people values(?,?) """, ('abc',20))
            await db.commit()

        
class DBHandler(BaseHandler):
    async def get(self, name=None):
        try:
            if not name:
                people = await self.query(
                    "SELECT * FROM people"
                )
                obj = {'all': people}
            else:
                entries = await self.queryone(
                    "SELECT * FROM people where name=?", name
                )
                #find age , each row is dict because of db.row_factory = aiosqlite.Row
                obj = {'name': name, 'age': entries['age']}
        except Exception as ex:
            obj={'message': str(ex)}
        self.write(obj) #only accepts bytes, unicode, and dict objects
        
"""
Urls 
http://localhost:8888/
http://localhost:8888/static/hello.html 
http://localhost:8888/some.txt
http://localhost:8888/main 
http://localhost:8888/story/2

http://localhost:8888/helloj/das
http://localhost:8888/helloj/ with json  "{\"name\": \"dasn\"}"
http://localhost:8888/helloj/
http://localhost:8888/helloj/?name=dasq

http://localhost:8888/hellox/das

http://localhost:8888/env

http://localhost:8888/secure
http://localhost:8888/login   with admin/secret

http://localhost:8888/upload
http://localhost:8888/upload_large
http://localhost:8888/download/data.jpg

http://localhost:8888/db/
http://localhost:8888/db/abc 

"""



def make_app(dbpath):
    settings = {
    #This setting will automatically make all requests that start with /static/ serve from that static directory
    #automatically serve /robots.txt and /favicon.ico from the static directory (even though they don’t start with the /static/ prefix)
    #To use /static/images/logo.png, use <img src="{{ static_url("images/logo.png") }}"/></div>,
    # It uses cacheing , to disable, use static_hash_cache=False
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": True,
    #templates 
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),
    #file upload 
    "upload_path": os.path.join(os.path.dirname(__file__), "uploads"),
    }
    return tornado.web.Application([
        (r"/", MainHandler),
        #static file can be served directly by below with url /some.txt , note below is regex group
        (r"/(some\.txt)", tornado.web.StaticFileHandler, dict(path=settings['static_path']) ),
        
        tornado.web.url(r"/main", MainHandler2),
        #db goes to StoryHandler.__init__ 
        #regex group goes to StoryHandler.get(story_id)
        tornado.web.url(r"/story/([0-9]+)", StoryHandler, dict(db=None), name="story"),
        
        #handlinh json
        (r"/helloj/(\w*)", JsonHandler),
        #XML
        (r"/hellox/(\w+)", XMLHandler),
        #form 
        tornado.web.url(r"/env", MyFormHandler, name="myform"),
        
        #login 
        (r"/login", LoginHandler),
        tornado.web.url(r"/secure", SecureMainHandler, name="secure_site"),
        
        #upload 
        tornado.web.url(r"/upload", UploadPOSTHandler, dict(upload_path=settings['upload_path']), name="upload_normal"),
        tornado.web.url(r"/upload_large", UploadLargePOSTHandler, dict(upload_path=settings['upload_path']), name="upload_large"),
        tornado.web.url(r"/download/(.+)", DownloadHandler, dict(upload_path=settings['upload_path']), name="download"),
        
        #db 
        tornado.web.url(r"/db/(.*)", DBHandler, dict(db=dbpath), name="db"),
        
    ],    **settings
    )
    
    
#for debug true , it has to be module 
#debug=True) #autoreload=True,compiled_template_cache=False:,static_hash_cache=False,serve_traceback=True:
#does not work as intended in windows 

if __name__ == "__main__":
    ## to enable logging , start with 'python basic.py --logging=info'
    # check other options eg log file prefix, rotation etc 
    #https://www.tornadoweb.org/en/stable/_modules/tornado/log.html#LogFormatter
    tornado.options.parse_command_line()
    dbpath = "tornado.db"
    application =  make_app(dbpath)
    application.listen(8888)
    
    # In Python, signals are always handled by the main thread. 
    # If the IOLoop is run from the main thread, it will block it when server is idle 
    # and waiting for IO. 
    # As a result, all signals will be pending on the thread to wake up. 
    # So, press  crtl+c and then refresh browser or install below callback 
    tornado.ioloop.PeriodicCallback( lambda:None, 1000 , jitter=0.1).start()   
    #add db creation in IOLoop
    tornado.ioloop.IOLoop.current().spawn_callback(maybe_create_tables, dbpath)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:  #for crtl+c 
        logging.getLogger("tornado.general").info("Exiting")
        tornado.ioloop.IOLoop.current().stop()

    
        
"""
#using asyncio (arguments are like requests)

aiohttp.ClientSession(cookies=None, headers=None, read_timeout=None, conn_timeout=None)
    request(method, url, *, params=None, data=None, json=None, cookies=None, 
            headers=None,proxy=None, proxy_auth=None, timeout=sentinel, 
            ssl=None, proxy_headers=None)
        cookies, headers are dict 
        params ,for query params 
        data , for form data 
        json , any python object (then dont use data)
        proxy  ,URL 
        proxy_auth ,aiohttp.BasicAuth(login, password='', encoding='latin1')
        ssl=False , dont use certificates verification 
        ssl=ssl_context, with certs, https://docs.python.org/3/library/ssl.html#ssl.SSLContext 
        timeout , If float is passed it is a total timeout or aiohttp.ClientTimeout(*, total=None, connect=None, sock_connect, sock_read=None)
Response 
    cookies
    headers
    status 
    content_type
    coroutine text()
    coroutine json()
    coroutine read()
    content aiohttp.StreamReader
    
    
#code 
import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        print(html)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(url="http://localhost:8888/"))



"""