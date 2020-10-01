from flask import Flask, url_for
from flask import request
from flask import json
from flask import Response
from flask import jsonify


app = Flask(__name__)

from functools import wraps

def check_auth(username, password):
    return username == 'admin' and password == 'secret'


def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'
    resp.status_code = 401
    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization #Authorization: Basic YWRtaW46c2VjcmV0MjM=
        if not auth: 
            return authenticate()
        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/secrets')
@requires_auth
def api_hello():
    return "Shhh this is top secret spy stuff!"


if __name__ == '__main__':
    app.run()

'''
curl -v -u "admin:secret" http://127.0.0.1:5000/secrets
#not auth
curl -v -u "admin:secret23" http://127.0.0.1:5000/secrets

Note 
Flask uses a MultiDict to store the headers. 
To present clients with multiple possible authentication schemes 
it is possible to simply add more WWW-Authenticate lines to the header

resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'
resp.headers.add('WWW-Authenticate', 'Bearer realm="Example"')

'''