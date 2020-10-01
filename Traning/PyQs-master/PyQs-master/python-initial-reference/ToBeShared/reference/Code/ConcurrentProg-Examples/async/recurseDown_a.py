import threading, concurrent.futures  #in Py2, must do, pip install futures
import urllib.parse
import os.path ,sys,bs4
import functools,time
import asyncio, aiohttp

#debug print 
def printD(debug,*args, **kargs):
    if debug:
        print(threading.current_thread().getName(),*args, **kargs)

#without query etc 
def getBaseDomain(url):
    u = urllib.parse.urlsplit(url)
    #reset query and fragment 
    return urllib.parse.urlunsplit( (u.scheme, u.netloc,u.path,'','') )
    
def getFileName(url):
    u = urllib.parse.urlsplit(url)
    return u.path[u.path.rfind("/")+1:]  #might '' or actual path 
    
async def get(session, url, *args, **kwargs):  
    async with session.get(url, *args, **kwargs ) as resp:
        return (await resp.text())
    
def getAllLinks(url, page, baseDomain, debug=True):
    soup = bs4.BeautifulSoup(page, "html.parser")  
    raw_links = [link.get('href') for link in soup.find_all('a')]
    def process_each(link):
        fullUrl = urllib.parse.urljoin(url,link)
        return fullUrl if baseDomain in fullUrl else ''
    result = [ process_each(link)  for link in raw_links if process_each(link) ]
    printD(debug, ": parsed: ", result)
    return result
    
async def load(url, session, sleep=0.1,debug=True, dir=r".", createFile=True):
    await asyncio.sleep(sleep)
    printD(debug,  ": starting download ",url)
    page = await get(session, url)
    fileName = getFileName(url)
    if createFile and fileName:
        #create files 
        #might fail 
        try:
            with open(os.path.normpath(os.path.join(dir,fileName)), "wt") as f:
                f.write(page)
        except Exception as ex :
            printD(debug, ":", str(ex)) 
    return [url, page]
    
async def runOne(loadFn, parseFn, url,session): #returns list of all links 
    _ , html = await loadFn(url,session)
    links = parseFn(url,html)
    return links 
    
    
async def run(baseUrl,sleep,debug,dir,createFile,maxDepth,executor,loop,HACK):
    basedomain = getBaseDomain(baseUrl)
    masterSetWithLinks = set()
    
    fnload = functools.partial(load, sleep=sleep,debug=debug, dir=dir, createFile=createFile)
    fnlinks = functools.partial(getAllLinks, baseDomain=basedomain, debug=debug)
 
    #parse and get all links 
    async with aiohttp.ClientSession() as session:
        urls = await runOne(fnload, fnlinks, baseUrl,session)
    #update master set 
    masterSetWithLinks.update(set(urls))
    
    ###Hack start - to download only 20 
    hackMaxDownload = 20
    if HACK:
        urls = urls[:hackMaxDownload]
    ###Hack -end 
    
    #loop
    depth = 0
    async with aiohttp.ClientSession() as session:
        while depth < maxDepth:
            fut = asyncio.gather(*[runOne(fnload, fnlinks, url,session) for url in urls])
            res = await asyncio.wait_for(fut,None) #list of list 
            #flatten 
            res = [item for sublist in res for item in sublist]
            urls = list(set(res) - masterSetWithLinks)
            masterSetWithLinks.update(set(res))
            depth += 1
            printD(debug, ":next depth:",depth, urls ) 

    
    
if __name__ == '__main__':
    baseUrl = sys.argv[1] if len(sys.argv) >= 2 else "http://ss64.com/bash/"

    #other vars 
    sleep = 0.1
    debug = True
    dir = r"./download"
    createFile = True
    maxDepth = 1 
    HACK = True
    
    #loop part 
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    loop = asyncio.get_event_loop()
    loop.set_default_executor(executor)
    result = loop.run_until_complete(run(baseUrl,sleep,debug,dir,createFile,maxDepth,executor,loop,HACK))
    executor.shutdown() 