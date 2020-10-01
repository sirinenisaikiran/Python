from urllib.request import urlopen
url = "http://accionlabs.com/company/leadership-team/executive-leadership-team/index.html"
html = urlopen(url)
from bs4 import BeautifulSoup
soup = BeautifulSoup(html)
for res in soup.findAll('img'):
  print(res.get('src'))
  # list_var = url.split('/')
  # resource = urlopen(list_var[0]+"//"+list_var[2]+res.get('src'))
  # output = open(res.get('src’).split(‘/‘)[-1],”wb")
  # output.write(resource.read())
  # output.close()