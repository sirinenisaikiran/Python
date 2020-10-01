from aiohttp import web

async def handle(request):
    text = "Hello, World"
    #Response(*, body=None, status=200, reason=None, text=None, headers=None, content_type=None, charset=None, zlib_executor_size=sentinel, zlib_executor=None)
    return web.Response(text=text) 
    
async def post_handler(request):
    #GET data 
    #methods: getall(key[, default]), get(key[, default]), key in d
    gets = list(request.query.items())
    #post BODY  
    #posts = await request.post() #methods: getall(key[, default]), get(key[, default]), key in d
    #text body 
    #posts = await requests.text()
    #json body 
    posts = await request.json() #python obj
    #Query String , .path, .query_string
    q = [ request.path_qs, #The URL including PATH_INFO and the query string
          request.path, #The URL including PATH INFO without the host or scheme
          request.raw_path,  #path may be URL-encoded 
          request.query_string,
          str(request.query),  #A multidict with all the variables in the query string.
          str(request.headers),  #A case-insensitive multidict proxy with all headers
          str(request.cookies), #A multidict of all request’s cookies.
        ]
    #Method 
    m = [request.method, request.content_type  , request.host, request.remote]
    #data 
    data = dict(query=gets, json=posts, q=q, m=m)
    return web.json_response(data)
    
async def handle_json(request):
    name = request.match_info.get('name', "Anonymous") # from PATH template 
    data = {'name': name}
    return web.json_response(data)

app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/{name}', handle_json)
app.router.add_post('/post', post_handler)             
               
#aiohttp.web.run_app(app, *, host=None, port=None, path=None, sock=None, shutdown_timeout=60.0, ssl_context=None, print=print, backlog=128, access_log_class=aiohttp.helpers.AccessLogger, access_log_format=aiohttp.helpers.AccessLogger.LOG_FORMAT, access_log=aiohttp.log.access_logger, handle_signals=True, reuse_address=None, reuse_port=None)               
web.run_app(app) 
#http://localhost:8080/
#http://localhost:8080/das
#http://localhost:8080/post?name=das 
#or with post json 
'''
import aiohttp
import asyncio
import json 

async def fetch(session, url):    
    data = dict(name='das')
    headers = {'Content-Type': 'application/json'}
    #for json,  post(url,json=data)
    #for query, .get(url, params=query_dict)
    #for post data , post(url, data=post_dict)
    async with session.post(url,data=json.dumps(data), headers=headers) as response:
        # rsp.text() or rsp.text(encoding='windows-1251'), resp.read() for binary body 
        return await response.json()  

async def main(loop):
    timeout = aiohttp.ClientTimeout(total=60.0)
    #timeout can be part of .get, .post etc 
    async with aiohttp.ClientSession(loop=loop, timeout=timeout) as session:
        result = await fetch(session, 'http://localhost:8080/post?name=das')
    return result

async def cookie():
    #ClientSession may be used for sharing cookies between multiple requests:
    async with aiohttp.ClientSession() as session:
        await session.get('http://httpbin.org/cookies/set?my_cookie=my_value')
        filtered = session.cookie_jar.filter_cookies('http://httpbin.org')
        assert filtered['my_cookie'].value == 'my_value'
        async with session.get('http://httpbin.org/cookies') as r:
            json_body = await r.json()
            assert json_body['cookies']['my_cookie'] == 'my_value'
            assert resp.headers['Content-Type'] == 'application/json'

async def few_info():
    async with aiohttp.ClientSession() as session:
        resp = await session.get('http://example.com/some/redirect/')
        assert resp.status == 200
        assert resp.url == URL('http://example.com/some/other/url/')
        assert len(resp.history) == 1
        assert resp.history[0].status == 301
        assert resp.history[0].url == URL('http://example.com/some/redirect/')            

async def download_large(filename, chunk_size=1024*1024):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.github.com/events') as resp:    
            with open(filename, 'wb') as fd:
                while True:
                    chunk = await resp.content.read(chunk_size)
                    if not chunk:
                        break
                    fd.write(chunk)

async def send_file():
    async with aiohttp.ClientSession() as session:
        url = 'http://httpbin.org/post'
        data = aiohttp.FormData()
        data.add_field('file',
                       open('report.xls', 'rb'),
                       filename='report.xls',
                       content_type='application/vnd.ms-excel')
        await session.post(url, data=data)    

async def send_large_file():
    async with aiohttp.ClientSession() as session:
        with open('report.xls', 'rb') as f:
           await session.post('http://httpbin.org/post', data=f)  
        #or chain 
        resp = await session.get('http://python.org')
        await session.post('http://httpbin.org/post', data=resp.content)

async def proxy():
    async with aiohttp.ClientSession() as session:
        proxy_auth = aiohttp.BasicAuth('user', 'pass')
        async with session.get("http://python.org",
                               proxy="http://proxy.com",
                               proxy_auth=proxy_auth) as resp:
            print(resp.status)   

loop = asyncio.get_event_loop()
result = loop.run_until_complete(main(loop))
# Zero-sleep to allow underlying connections to close
loop.run_until_complete(asyncio.sleep(0)) #for SSL, use 0.250
loop.close()

#SSL 
#By default aiohttp uses strict checks for HTTPS protocol. 
#Certification checks can be relaxed by setting ssl to False:

r = await session.get('https://example.com', ssl=False)

#or with sslContext 
import ssl 
sslcontext = ssl.create_default_context( cafile='/path/to/ca-bundle.crt')
r = await session.get('https://example.com', ssl=sslcontext)

#with self signed 
sslcontext = ssl.create_default_context( cafile='/path/to/ca-bundle.crt')
sslcontext.load_cert_chain('/path/to/client/public/device.pem',
                           '/path/to/client/private/device.key')
r = await session.get('https://example.com', ssl=sslcontext)


'''