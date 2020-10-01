from flask import Flask, url_for
from flask import request
app = Flask(__name__)

from flask import json

@app.route('/messages', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data
    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)
    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('dummy', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"
    else:
        return "415 Unsupported Media Type ;)"

if __name__ == '__main__':
	app.run()

'''
curl -v -H "Content-type: application/json" -X POST http://127.0.0.1:5000/messages -d "{\"message\":\"Hello Data\"}"
curl -v -H "Content-type: application/octet-stream" -X POST http://127.0.0.1:5000/messages --data-binary "@var.txt"


Note:
Accessing the HTTP headers is done using the request.headers dictionary ("dictionary-like object") 
and the request data using the request.data string. 
As a convenience, if the mimetype is application/json, 
request.json will contain the parsed JSON.

Flask can handle files POSTed via an HTML form using request.files dict 
and curl can simulate that behavior with the -F flag(enctype="multipart/form-data)

request.args is dict for URL KEY for GET 
for POST and application/x-www-form-urlencoded, use request.form as dict 
for post and 'application/json'  , use request.json or request.get_json() which json coverted to py obj 
for post and 'text/plain', use request.data

for POST and in curl 
curl -d 'uuid=admin&password=admin' -X POST 
'''