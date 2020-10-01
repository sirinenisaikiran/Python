from app import app  #from __init__.py's app variable 

from flask import jsonify

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Nobody'}
    resp = jsonify(user)
    resp.status_code = 200
    return resp