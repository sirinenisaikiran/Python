from flask import render_template
from app import app
from flask import request


'''
1.If a rule ends with a slash and is requested without a slash by the user, 
  the user is automatically redirected to the same page with a trailing slash attached.
2.If a rule does not end with a trailing slash 
  and the user requests the page with a trailing slash, 
  a 404 not found is raised.
'''

@app.route('/')
@app.route('/index/')
def index():
    user = {'username': 'Nobody'}
    return render_template('index.html', title='Home', user=user) #Jinja2 template engine

    
@app.route('/index/for/')
def index1():
    user = {'username': 'Nobody'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('indexFor.html', title='Home', user=user, posts=posts)
    
#both routes are required to get optional params
@app.route('/index/if/')
@app.route('/index/if/<username>')
def index2(username=None):
    user = {'username': username if username else "Nobody"}
    
    return render_template('indexIf.html', title='Home', user=user) #Jinja2 template engine

@app.route('/index/inher/') 
@app.route('/index/inher/<string:username>')
def index3(username=None):
    user = {'username': username if username else "Nobody"}
    dct = dict(query_string=request.query_string, url=request.url)
    #to get one param, request.args.get('param')
    print(dct)
    return render_template('indexInher.html', title='Home', user=user) #Jinja2 template engine

#Send json 
from flask import jsonify
from flask import Response

@app.route('/summary')
def summary():
    d = {'data':'OK'}
    return jsonify(d)
    
#Send file 
@app.route("/get-file")
def get_file():
    def generator(filename="text.txt"):
        #open file and return file object 
        #else 
            yield "Firstline\n"
            yield "2ndline\n"
    return Response(generator(), mimetype="text/plain",  headers={"Content-Disposition":"attachment;filename=test.txt"})
    