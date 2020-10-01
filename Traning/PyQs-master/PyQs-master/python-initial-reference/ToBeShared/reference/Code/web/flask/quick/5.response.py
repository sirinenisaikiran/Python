from flask import Flask, url_for
from flask import request
from flask import json
app = Flask(__name__)

from flask import Response
from flask import jsonify

'''
Default Flask error messages can be overwritten using 
either the @error_handler decorator or
app.error_handler_spec[None][404] = not_found
'''
@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/users/<userid>', methods = ['GET'])
def api_users(userid):
    users = {'1':'john', '2':'steve', '3':'bill'}
    
    if userid in users:
        return jsonify({userid:users[userid]})
    else:
        return not_found()


@app.route('/hello', methods = ['GET'])
def api_hello():
    data = {
        'hello'  : 'world',
        'number' : 3
    }
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    #or 
    resp = jsonify(data)
    resp.status_code = 200
    resp.headers['Link'] = 'http://luisrei.com'
    return resp
    

if __name__ == '__main__':
    app.run()

'''
curl -v http://127.0.0.1:5000/hello
curl -v http://127.0.0.1:5000/users/2 
curl -v http://127.0.0.1:5000/users/10

OR

>>> import requests
>>> r = requests.get("http://127.0.0.1:5000/hello")
>>> r.json()
{'hello': 'world', 'number': 3}

'''