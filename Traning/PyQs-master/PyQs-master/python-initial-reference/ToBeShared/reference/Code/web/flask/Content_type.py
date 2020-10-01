
from flask import Flask, render_template, make_response
app = Flask(__name__)

@app.route('/user/xml')
def user_xml():
    resp = make_response(render_template('xml/user.html', username='Ryan'))
    resp.headers['Content-type'] = 'text/xml; charset=utf-8'
    return resp



@app.route('/hello')
def hello():

    headers={ 'content-type':'text/plain' ,'location':'http://www.stackoverflow'}
    response = make_response('<h1>hello world</h1>',301)
    response.headers = headers
    return response

#case two:

@app.route('/hello')
def hello():

    headers={ 'content-type':'text/plain' ,'location':'http://www.stackoverflow.com'}
    return '<h1>hello world</h1>',301,headers


import json # 
@app.route('/search/<keyword>')
def search(keyword):

    result = Book.search_by_keyword(keyword)
    return json.dumps(result),200,{'content-type':'application/json'}


from flask import jsonify
@app.route('/search/<keyword>')
def search(keyword):

    result = Book.search_by_keyword(keyword)
    return jsonify(result)
    
    
if __name__ == '__main__':
    app.run()