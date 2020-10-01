import threading, concurrent.futures  #in Py2, must do, pip install futures
import requests,time,urllib.parse
import os.path ,sys,bs4
import functools
#from promise import Promise #does not work in py3!!
from async_promises import Promise

#debug print 
def printD(debug,printLck, *args, **kargs):
    if debug:
        with printLck:
            print(threading.current_thread().getName(),*args, **kargs)

#without query etc 
def getBaseDomain(url):
    u = urllib.parse.urlsplit(url)
    #reset query and fragment 
    return urllib.parse.urlunsplit( (u.scheme, u.netloc,u.path,'','') )
    
def getFileName(url):
    u = urllib.parse.urlsplit(url)
    return u.path[u.path.rfind("/")+1:]  #might '' or actual path 
    
def getAllLinks(url, page, baseDomain,printLck, debug=True):
    soup = bs4.BeautifulSoup(page, "html.parser")  
    raw_links = [link.get('href') for link in soup.find_all('a')]
    def stripHash(url, hash='#'):
        return url.split(hash)[0]
    def process_each(link):
        fullUrl = urllib.parse.urljoin(url,link)
        return stripHash(fullUrl) if baseDomain in fullUrl else ''
    result = [ process_each(link)  for link in raw_links if process_each(link) ]
    printD(debug, printLck, ": parsed: ", result)
    return result

def load(url, printLck, sleep=0.1,debug=True, dir=r".", createFile=True):
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
    
def runOne_v1(loadFn, parseFn, url): #returns list of all links 
    def actualOp(resolve, reject):
        def submit():
            _ , html = loadFn(url)
            links = parseFn(url,html)
            return links 
        try:            
            resolve(submit()) #asynchronous !!!
        except Exception as ex:
            reject(ex)
    return Promise(actualOp)
    
#below way does not work - why???
def runOne_v2(loadFn, parseFn, url): #returns list of all links 
    def submit():
        _ , html = loadFn(url)
        links = parseFn(url,html)
        return links 
    try:
        return Promise.resolve(submit())
    except Exception as ex:
        Promise.reject(ex)

    
def success(lnks, pLck, masterSetWithLinks,debug):
    with pLck:
        deltaLnks = set(lnks) - masterSetWithLinks
        masterSetWithLinks.update(set(lnks))
        #printD(debug, pLck, "Updated master set :", len(deltaLnks) , len(masterSetWithLinks)) 
    return list(deltaLnks)
    
def flatten(array):
	res = []
	for ele in array:
		if type(ele) is list:
			res += flatten(ele)
		else:
			res.append(ele)
	return res
    
def runAll(loadFn, parseFn, urls,  pLck,  masterSetWithLinks, HACK=False, debug=False, maxDepth=100,curDepth=-1):
    ###Hack start - to download only 20 
    hackMaxDownload = 20
    if HACK:
         urls = urls[:hackMaxDownload]
    ###Hack -end 
    printD(debug, pLck, ":next depth:",curDepth+1, urls ) 
    if curDepth < maxDepth:
        for url in urls:
            runOne_v1(loadFn, parseFn, url)\
                .then(lambda lnks: success(lnks, pLck, masterSetWithLinks,debug), \
                      lambda ex: ex) \
                .then(lambda deltaUrls: runAll(loadFn, parseFn, deltaUrls,pLck,masterSetWithLinks, HACK,debug,maxDepth,curDepth+1) , \
                      lambda ex: ex) \
                .catch(lambda ex: print(ex))
        
    
if __name__ == '__main__':
    baseUrl = sys.argv[1] if len(sys.argv) >= 2 else "http://ss64.com/bash/"
    basedomain = getBaseDomain(baseUrl)
    masterSetWithLinks = set()
    pLck = threading.RLock()
    #other vars 
    sleep = 0.1
    debug = True
    dir = r"./download"
    createFile = True
    maxDepth = 1 
    HACK = True
    #code    
    fnload = functools.partial(load, printLck=pLck, sleep=sleep,debug=debug, dir=dir, createFile=createFile)
    fnlinks = functools.partial(getAllLinks, baseDomain=basedomain, printLck=pLck, debug=debug)

    runAll(fnload, fnlinks, [baseUrl], pLck,masterSetWithLinks,HACK,debug,maxDepth)
    
    

