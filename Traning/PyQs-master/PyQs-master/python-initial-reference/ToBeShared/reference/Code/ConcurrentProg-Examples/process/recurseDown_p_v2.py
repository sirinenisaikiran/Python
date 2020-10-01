import multiprocessing  
import requests,time,urllib.parse
import os.path ,sys,bs4
import functools

#You can't pass normal multiprocessing.Lock objects to Pool methods, 
#because they can't be pickled	
#now each process can access lock 
def init(lock):
    global printLck
    printLck = lock

#debug print 
def printD(debug,*args, **kargs):
    if debug:
        with printLck:
            print(multiprocessing.current_process().name,*args, **kargs)

#without query etc 
def getBaseDomain(url):
    u = urllib.parse.urlsplit(url)
    #reset query and fragment 
    return urllib.parse.urlunsplit( (u.scheme, u.netloc,u.path,'','') )
    
def getFileName(url):
    u = urllib.parse.urlsplit(url)
    return u.path[u.path.rfind("/")+1:]  #might '' or actual path 
    
def getAllLinks( temp, baseDomain,debug=True):
    url,page = temp
    soup = bs4.BeautifulSoup(page, "html.parser")  
    raw_links = [link.get('href') for link in soup.find_all('a')]
    def process_each(link):
        fullUrl = urllib.parse.urljoin(url,link)
        return fullUrl if baseDomain in fullUrl else ''
    result = [ process_each(link)  for link in raw_links if process_each(link) ]
    printD(debug, printLck, ": parsed: ", result)
    return result

def load(url, sleep=0.1,debug=True, dir=r".", createFile=True):
    time.sleep(sleep)
    printD(debug, printLck, ": starting download ",url)
    conn = requests.get(url)  
    fileName = getFileName(url)
    if createFile and fileName:
        #create files 
        #might fail 
        try:
            with open(os.path.normpath(os.path.join(dir,fileName)), "wt") as f:
                f.write(conn.text)
        except Exception as ex :
            printD(debug, printLck, ":", str(ex)) 
    return [url, conn.text]
    


    
if __name__ == '__main__':
    baseUrl = sys.argv[1] if len(sys.argv) >= 2 else "http://ss64.com/bash/"
    basedomain = getBaseDomain(baseUrl)
    masterSetWithLinks = set()
    #create global printLck for sharing 
    pLck = multiprocessing.RLock() #only child process can access it 
    executor = multiprocessing.Pool(processes=10, initializer=init, initargs=(pLck,))
    
    #other vars 
    sleep = 0.1
    debug = True
    dir = r"./download"
    createFile = True
    maxDepth = 1 
    HACK = True
    
    #executor part 
    fut = executor.apply_async(load,(baseUrl,) , dict(sleep=sleep,debug=debug, dir=dir, createFile=createFile) )
    url, html = fut.get(timeout=None) #blocks 
    #parse and get all links 
    urls = executor.apply_async(getAllLinks,( (url, html), basedomain,debug) )
    urls = urls.get(timeout=None)
    #update master set 
    masterSetWithLinks.update(set(urls))
    
    ###Hack start - to download only 20 
    hackMaxDownload = 20
    if HACK:
        urls = urls[:hackMaxDownload]
    ###Hack -end 
    
    #fire maps 
    fnload = functools.partial(load, sleep=sleep,debug=debug, dir=dir, createFile=createFile)
    fnlinks = functools.partial(getAllLinks, baseDomain=basedomain, debug=debug)
    depth = 0
    while depth < maxDepth:
        #res = [ (url,page),...]
        res = executor.map(fnload, urls) #blocks 
        #get all pages 
        #res = [ [links], [links] ]        
        res = executor.map(fnlinks, res) #can take only one arg, hence tuple would be passed 
        #flatten 
        res = [item for sublist in res for item in sublist]
        #take only diff 
        urls = list(set(res) - masterSetWithLinks)
        masterSetWithLinks.update(set(res))
        depth += 1
        if debug:  #can not call printD as Rlock can not be accessed here 
            print("next depth:",depth, urls ) 
    executor.close()
    executor.join()