from flask import Flask,jsonify,request

app = Flask(__name__)


@app.route('/')
@app.route('/json', methods = ['POST'])
def index():
    user = {'username': 'Nobody'}
    if 'Content-Type' in request.headers and  request.headers['Content-Type'] == 'application/json':
        user["username"] =request.json["username"]
    resp = jsonify(user)
    resp.status_code = 200
    return resp
    
@app.route('/html')
def html():
    return '''
    <html> <body><h1>Hello Das</h1></body></html>
    '''
    
if __name__ == '__main__':
	app.run()

'''
curl -v http://127.0.0.1:5000/
curl -v http://127.0.0.1:5000/html
curl -v -H "Content-type: application/json" -X GET http://127.0.0.1:5000/ -d "{\"username\":\"MyName\"}"
curl -v -H "Content-type: application/json" -X POST http://127.0.0.1:5000/json -d "{\"username\":\"MyName\"}"

#OR 
import requests, json 
data = {"username": "Das"}
headers = {'Content-type': 'application/json'}
r = requests.post("http://127.0.0.1:5000/json", data=json.dumps(data),headers=headers)
>>> r.json()
{'username': 'Das'}
>>>






































'''