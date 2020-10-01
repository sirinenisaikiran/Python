from aiohttp import web
import aiohttp.web, aiohttp_jinja2, aiohttp_session
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import logging
import os,  uuid, shutil, asyncio , functools
import mimetypes, jinja2
from bs4 import BeautifulSoup
import lxml.etree # not used directly
import base64
from cryptography import fernet
from html import escape as html_escape
import multidict, urllib.parse
import aiosqlite
import aiohttp_csrf

routes = web.RouteTableDef()
logging.basicConfig(level=logging.DEBUG)

async def reverse_url(request, id, *args, **kwargs):
    """
    id is route name 
    args= query string eg "a=b"
    kwargs = path arg        
    """
    if args and kwargs:
        return request.app.router[id].url_for(**kwargs).with_query(*args)
    if args:
        return request.app.router[id].url_for().with_query(*args)
    if kwargs:
        return request.app.router[id].url_for(**kwargs)
    else:
        return request.app.router[id].url_for()
    
def debug_log_all(request):  
    q = [ request.headers.get('Referer', "NOReferer"),
          request.url, 
          request.path_qs, #The URL including PATH_INFO and the query string
          request.path, #The URL including PATH INFO without the host or scheme
          request.raw_path,  #path may be URL-encoded 
          request.query_string,
          str(request.query),  #A multidict with all the variables in the query string.
          str(request.headers),  #A case-insensitive multidict proxy with all headers
          str(request.cookies), #A multidict of all request’s cookies.
          str(list(request.keys())),
        ] 
    logging.debug(str(q))
    
@routes.get('/')
async def home(request):
    return web.Response(text= """
        <html><body>
        <h1 id="some1" class="some">Hello there!!</h1>
        <h1 id="some2" class="some">Hello there!!</h1>
        </body></html>    
        """, content_type="text/html") 
        
        
'''
url = request.app.router['user-info'].url_for(user='john_doe')
url_with_qs = url.with_query("a=b")
assert url_with_qs == '/john_doe/info?a=b'
'''

@routes.get('/main')   
def main_handler2(request):
    return web.Response(text= '<a href="%s">link to story 1</a>' %
                   request.app.router['story'].url_for(story_id="1"), content_type="text/html") 
                   
                   
@routes.get('/story/{story_id:\d+}', name='story')
def story_handler(request):
        return web.Response(text= 'this is story %s' % request.match_info['story_id'])
        
        
#template 
#Handlers should be coroutines accepting self only and returning response object 
#as regular web-handler. Request object can be retrieved by View.request property.
@routes.view('/env', name="env")
class MyFormHandler(aiohttp.web.View):
    def reverse_url(self, id, *args, **kwargs):
        """
        id is route name 
        args= query string eg "a=b"
        kwargs = path arg        
        """
        if args and kwargs:
            return self.request.app.router[id].url_for(**kwargs).with_query(*args)
        else:
            return self.request.app.router[id].url_for()
        if args:
            return self.request.app.router[id].url_for().with_query(*args)
        if kwargs:
            return self.request.app.router[id].url_for(**kwargs)
        
        
    @aiohttp_jinja2.template("env_get.html")
    async def get(self):
        #RequestHandler.render_string(template_name: str, **kwargs) -> bytes
        #could have used self.write(html_string) but to support xsrf use below 
        return dict(url= await reverse_url(self.request, "env"))
                 
    @aiohttp_jinja2.template("env.html")                 
    async def post(self):
        posts = await self.request.post()
        logging.debug(str(posts))
        envp = posts.get("envp","all").upper()
        env_dict = os.environ
        if os.environ.get(envp, "notfound") != "notfound":
            env_dict = { envp : os.environ.get(envp,"notfound") } 
        #logging.debug(str(env_dict))
        return dict(envs=env_dict.copy())  

'''
from jinja2 import * 
import os 
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(['html', 'xml'])
)
t = env.get_template('base.html')

s = t.render(envs=os.environ)


'''        
#Json,XML 

@routes.get('/helloj/{name:.*}') 
async def handle_json(request):
    def get_name(request,jdata):
        qname = request.query.get("name", None)
        jname = jdata.get("name", None)
        pname = request.match_info.get('name', None) # could be empty 
        logging.debug("qname<%s> jname<%s>/jdata<%s> pname<%s>" % (qname,jname,jdata,pname,))
        res = pname 
        if not res:
            if not jname:
                res = qname 
            else:
                res = jname 
        return res or "Jane Doe"
    name = get_name(request, await request.json() if request.body_exists else {} )
    data = {'name': name}
    return web.json_response(data)

@routes.get('/hellox/{name:.*}') 
async def handle_json(request):
    def name_xml(request,text):
        if request.headers.get('Content-Type', "other") == 'application/xml':
            soup = BeautifulSoup(text, 'xml')
            name = soup.find("name")
            return name.text if name else None 
        return None             
    def get_name(request, text):
        qname = request.query.get("name", None)
        xname = name_xml(request, text)
        pname = request.match_info.get('name', None)
        logging.debug("qname<%s> xname<%s>/text<%s> pname<%s>" % (qname,xname,text,pname,))
        res = pname 
        if not res:
            if not xname:
                res = qname 
            else:
                res = xname 
        return res or "Jane Doe"
    name = get_name(request, await request.text() if request.body_exists else {} )
    return web.Response(text= """
        <data><name>%s</name><age>%d</age></data>            
        """ %(name, 200), content_type="application/xml")
        
#login     
@aiohttp.web.middleware
async def current_user_middleware(request, handler):
    session = await aiohttp_session.get_session(request)
    request['current_user'] = session['current_user'] if 'current_user' in session else None
    resp = await handler(request)
    return resp


@routes.view('/login', name="login")
class LoginHandler(aiohttp.web.View):        
    def check_auth(self, username, password):
        return username == 'admin' and password == 'secret'
        
    def handle_post_query(self, url):
        charset =  self.request.charset or 'utf-8'
        posts = multidict.MultiDict()
        o = urllib.parse.urlparse(url)
        posts.extend(urllib.parse.parse_qsl(
                        qs=o.query,
                        keep_blank_values=True,
                        encoding=charset))
        return posts
        
    @aiohttp_jinja2.template("login.html")
    async def get(self):
        return dict(url=await reverse_url(self.request, "login"))

    async def post(self):        
        #debug_log_all(self.request)
        posts = await self.request.post()
        name = posts.get("name",None)
        password = posts.get("password", None) 
        if self.check_auth(name, password):
            session = await aiohttp_session.get_session(self.request)
            session['current_user'] = name 
            #aiohttp does not handle post query!!, so below hack 
            post_query = self.handle_post_query(self.request.headers['Referer'])
            #logging.debug(str(post_query))
            location = post_query.get("next", None) or (await reverse_url(self.request,"secure_site")) 
            raise aiohttp.web.HTTPFound(location=location) # redirect via raise
        else:
            location = await reverse_url(self.request, "login")
            raise aiohttp.web.HTTPFound(location=location) # redirect via raise 
            
    
def requires_auth(func):
    async def decorated(self, *args, **kwargs):
        request = None 
        try:
            request = self.request
        except:
            request = self
        us = request['current_user']
        if not us : 
            location = await reverse_url(request, "login", "next=%s" %(request.rel_url,))
            raise aiohttp.web.HTTPFound(location=location)  #method name ?next=curr
        if asyncio.iscoroutinefunction(func):
            coro = func
        else:
            coro = asyncio.coroutine(func)
        res = await coro(request, *args, **kwargs)
        return res
    return decorated
    
    
@routes.view('/secure', name="secure_site")
class SecureMainHandler(aiohttp.web.View):
    @requires_auth
    async def get(self):
        name = "ok" # html_escape(self.request['current_user'])
        return web.Response(text="Hello, " + name)  
        
        
@routes.get('/logout')        
@requires_auth
async def logout(request):
    session = await aiohttp_session.get_session(request)
    session['current_user'] = None 
    return web.Response(text="loggedout")       

        
#DB         
class NoResult(Exception):
    pass
        
class DBApi:
    def __init__(self, db):
        self.db = db
    def row_to_obj(self, row, cur):
        obj = {}
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
            
async def maybe_create_tables(app):   
    logging.debug("DBPATH=%s" % (app['dbpath'], ))
    async with aiosqlite.connect(app['dbpath']) as db:
        try:
            async with db.execute("SELECT COUNT(*) FROM people LIMIT 1") as cursor:
                await cursor.fetchone()
        except :                
            await db.execute("""create table if not exists people (name string, age int)""")
            await db.execute("""insert into people values(?,?) """, ('xyz',20))
            await db.execute("""insert into people values(?,?) """, ('abc',20))
            await db.commit()

            
@routes.view("/db/{name:.*}", name="db")    
class DBHandler(aiohttp.web.View):
    async def get(self):
        name = self.request.match_info.get('name', None)
        try:
            if not name:
                people = await DBApi(app['dbpath']).query(
                    "SELECT * FROM people"
                )
                obj = {'all': people}
            else:
                entries = await DBApi(app['dbpath']).queryone(
                    "SELECT * FROM people where name=?", name
                )
                #find age , each row is dict because of db.row_factory = aiosqlite.Row
                obj = {'name': name, 'age': entries['age']}
        except Exception as ex:
            obj={'message': str(ex)}
        return web.json_response(obj)    
        
        
        
    
#Upload and download 
#CSRF 
async def setup_csrf(app):
    csrf_policy = aiohttp_csrf.policy.FormPolicyWithMultipart(app['FORM_FIELD_NAME'])
    csrf_storage = aiohttp_csrf.storage.CookieStorage(app['COOKIE_NAME'])
    aiohttp_csrf.setup(app, policy=csrf_policy, storage=csrf_storage)
    
    
@routes.view("/upload", name="upload")  
class UploadPOSTHandler(aiohttp.web.View):
    @aiohttp_csrf.csrf_protect
    @aiohttp_jinja2.template("upload.html")
    async def get(self):
        token = await aiohttp_csrf.generate_token(self.request)
        return dict(token_name=self.request.app['FORM_FIELD_NAME'], token=token)
        
    @aiohttp_csrf.csrf_protect
    async def post(self):   
        debug_log_all(self.request)
        reader = await self.request.multipart()
        # reader.next() will `yield` the fields of your form
        #so for other form fields 
        # field = await reader.next()
        # assert field.name == 'name'
        # name = await field.read(decode=True) #get value 
        # in our case 'file'
        field = await reader.next()
        assert field.name == 'file'
        filename = field.filename
        # You cannot rely on Content-Length if transfer is chunked.
        size = 0
        try:
            with open(os.path.join(self.request.app['upload_path'], filename), 'wb') as f:
                while True:
                    chunk = await field.read_chunk()  # 8192 bytes by default.
                    if not chunk:
                        break
                    size += len(chunk)
                    f.write(chunk)
        except IOError as e:
            logging.error("Failed to write file due to IOError %s", str(e))            
        location = await reverse_url(self.request, "download", filename=filename)
        raise aiohttp.web.HTTPFound(location=location)
        #return web.Response(text='{} sized of {} successfully stored'.format(filename, size))
      

        
#Download 
@routes.view("/download/{filename}", name="download")  
class DownloadHandler(aiohttp.web.View):
    async def get(self):
        filename = self.request.match_info.get('filename', "default_name")
        # chunk size to read
        chunk_size = 1024 * 1024 * 8 # 8 MiB
        mtype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        headers = {}
        headers["Content-Disposition"] = 'attachment; filename="%s"' %(filename,) 
        headers["Content-Type"] =  mtype
        response = web.StreamResponse(status=200,reason='OK',headers=headers )    
        await response.prepare(self.request)  #start the response 
        with open(os.path.join(self.request.app['upload_path'],filename), 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                try:
                    await response.write(chunk) # write the cunk to response
                    await response.drain() # flush the current chunk to socket
                except Exception:
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
                    await asyncio.sleep(0.000000001) # 1 nanosecond        
            await response.write_eof()
            return response


    

#CRTL+C handling 
#note loop once started , would check only any event in main thread 
#so crtl+c would be processed only when events reach to loop 
#iether by one browser url or via below method 

async def call_periodic(app, sleep, func):
    while True:
        func()
        await asyncio.sleep(sleep)

        
async def start_background_tasks(app,sleep, func):
    app['periodic'] = app.loop.create_task(call_periodic(app,sleep, func)) #every 5 seconds 


async def cleanup_background_tasks(app):
    app['periodic'].cancel()
    await app['periodic']

    
if __name__ == '__main__':
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": b'CvkgfR6WATWuWnJPLJWrcWHslRW9893sNPwl1Ko7qhk=', #fernet.Fernet.generate_key()
        'template_path': os.path.join(os.path.dirname(__file__), "templates"),
        "upload_path": os.path.join(os.path.dirname(__file__), "uploads"),
        'dbpath' : os.path.join(os.path.dirname(__file__), "people.db"),
        'FORM_FIELD_NAME' : '_csrf_token',
        'COOKIE_NAME' : 'csrf_token',
        }
    app = web.Application()
    #update static , now view function can access, request.app['key']
    for k, v in settings.items():
        app[k] = v 
    #session middleware must be first 
    secret_key = base64.urlsafe_b64decode(app['cookie_secret'])
    aiohttp_session.setup(app, EncryptedCookieStorage(secret_key))
    #then other middle ware 
    app.middlewares.append(current_user_middleware)
    #add routes 
    app.add_routes(routes)
    #static file 
    app.add_routes([web.static('/static', app['static_path']), ])
    #jinja setup , adds middleware 
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(app['template_path']))
    
    #signals
    app.on_startup.append(functools.partial(start_background_tasks, sleep=5, func=lambda:None))
    app.on_startup.append(maybe_create_tables)
    app.on_cleanup.append(cleanup_background_tasks)
    #csrf setup 
    app.on_startup.append(setup_csrf)
    
    web.run_app(app) 
    
'''
Urls 
http://localhost:8080/
http://localhost:8080/static/hello.html 

http://localhost:8080/main 
http://localhost:8080/story/2

http://localhost:8080/env

http://localhost:8080/helloj/das
http://localhost:8080/helloj/ with json  "{\"name\": \"dasn\"}"
http://localhost:8080/helloj/
http://localhost:8080/helloj/?name=dasq

http://localhost:8080/hellox/das
http://localhost:8080/hellox/ with <name>das</name> & application/xml


http://localhost:8080/secure
http://localhost:8080/login   with admin/secret
http://localhost:8080/logout

http://localhost:8080/upload
http://localhost:8080/download/data.jpg

http://localhost:8080/db/
http://localhost:8080/db/abc 


#CSRF implementation 
https://github.com/asvetlov/aiohttp-csrf/tree/init
'''
