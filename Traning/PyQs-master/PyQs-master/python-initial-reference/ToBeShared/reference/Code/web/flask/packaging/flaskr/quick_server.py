from flask import Flask, request, jsonify, render_template
import json , os 


'''
#configmodule.py 
class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True
    ASSETS_DEBUG = True
    DATABASE = 'teamprojet_db'
    print('THIS APP IS IN DEBUG MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    DATABASE = 'teamprojet_prod_db'

#Or do 
set YOURAPPLICATION_SETTINGS=\path\to\settings.cfg
#\path\to\settings.cfg
DEBUG = False
SECRET_KEY = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'

#then 
app = Flask(__name__)
app.config.from_object('configmodule.ProductionConfig')
app.config.from_envvar('YOURAPPLICATION_SETTINGS')

#or for development , defaults to production.
$ set FLASK_ENV=development
$ python filename.py 
#Once Debugger enabled and an error happens during a request you will see a detailed traceback instead of a general “internal server error”. 
#DEBUGGER PIN is for security feature 
#above sets below 
import os
if os.environ['ENV'] == 'prod':
    config = ProductionConfig()
else:
    config = DevelopmentConfig()
'''

#app = Flask(__name__)
from flaskr import app

@app.route("/env", methods=['GET','POST'])#http://127.0.0.1:5000/env
def env():
    if request.method == 'POST':
        envp = request.form.get('envp', 'all').upper()
        env_dict = os.environ
        if os.environ.get(envp, "notfound") != "notfound":
            env_dict = { envp : os.environ.get(envp,"notfound") }
        return render_template("env.html", 
            envs=env_dict)
    else:
        return """
            <html><body>
            <form action="/env" method="post">
              Put Variable name :<br>
              <input type="text" name="envp" value="ALL">
              <br><br>
              <input type="submit" value="Submit">
            </form> 
            </body></html>
        """
    
@app.route("/")#http://127.0.0.1:5000/
def home():
    return """
        <html><body><h1 id="some" class="some">Hello there!!</h1></body></html>
    """
#OR  
# from flask import Response
# r = Response(response="<a>ok</a>", status=200, mimetype="application/xml")
# r.headers["Content-Type"] = "text/xml; charset=utf-8"
# return r
    
@app.route("/helloj") #http://127.0.0.1:5000/helloj
@app.route("/helloj/<string:name>") #default is strig, can put int as well 
def helloj(name="jane doe"):
    final_name = request.args.get("name", name)
    obj = { "name":final_name}
    resp = jsonify(obj)
    resp.status_code = 200
    return resp
    
@app.route("/json") #http://127.0.0.1:5000/json
#@app.route("/json", methods=["POST"])
def server():
    import os.path 
    filename = os.path.join(app.root_path, 'example.json')
    with open(filename, "rt") as f:
        obj = json.load(f)
    resp = jsonify(obj)
    resp.status_code = 200
    return resp
    

@app.route('/index', methods=['POST']) #http://127.0.0.1:5000/index
def index():
    user = { 'username': 'Nobody', 'age': 20}
    #https://flask.palletsprojects.com/en/1.1.x/logging/
    #default info  or set as import logging;app.logger.setLevel(logging.ERROR)
    app.logger.info('json=%s', str(request.json))
    if 'Content-Type' in request.headers and request.headers['Content-Type'].lower() == 'application/json':
        user['username'] = request.json.get('username', "Nobody")
    resp = jsonify(user)
    resp.status_code = 200 
    return resp 
    
#Logins 
from flask import Flask, session, redirect, url_for, escape, request, flash
#In order to use sessions you have to set a secret key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

'''
url_for('name of the function of the route','parameters (if required)')

#template, under  static/jquery.min.js, static/style.css
<script src="{{ url_for('static', filename='jquery.min.js') }}"></script>
<link rel=stylesheet type=text/css href="{{ url_for('static', filename='style.css') }}">

#or 
@app.route('/questions/<int:question_id>'):    #int has been used as a filter that only integer will be passed in the url otherwise it will give a 404 error
def find_question(question_id):  
    return ('you asked for question{0}'.format(question_id))

template 
<a href = {{ url_for('find_question' ,question_id=1) }}>Question 1</a>
'''
def check_auth(username, password):
    return username == 'admin' and password == 'secret'



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None 
    if request.method == 'POST':
        if check_auth(request.form['username'], request.form['pass']):
            session['username'] = request.form['username']
            flash('You were successfully logged in')
            next = request.args.get("next", "secret")
            return redirect(url_for(next))
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)
    
     
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))  #method name 
    
    

from functools import wraps
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session : 
            curr = request.endpoint  #get endpoint value 
            return redirect(url_for('login', next=curr))  #method name ?next=curr
        return f(*args, **kwargs)
    return decorated
    
@app.route("/secret", endpoint="secret")#http://127.0.0.1:5000/secret, sendpoint must be method name as we would use it with url_for
@requires_auth
def secret():
    return render_template('secret.html')
    
#db 
import sqlite3
from flask import g  
#g is global object behaves like dict , same lifetime as an application context
# g can be used without app.app_context()

DATABASE = os.path.join(app.root_path,'database.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/db') #http://127.0.0.1:5000/db
def db():
    cur = get_db().cursor()
    cur.execute("""create table if not exists people (name string, age int)""")
    cur.execute("""insert into people values(?,?) """, ('xyz',20))
    cur.execute("""insert into people values(?,?) """, ('abc',20))
    get_db().commit()
    q = cur.execute("""select * from people""")
    result = list(q.fetchall())
    return str(result) 
    
#Upload_download 
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(app.root_path,'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET', 'POST']) #http://127.0.0.1:5000/upload
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file.filename:
            filename = secure_filename(file.filename) #normalizes the file path 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
    
from flask import send_from_directory
#mimetype: str

#as_attachment: bool, attachment_filename:str, mimetype: str
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)    

if __name__ == '__main__':
    app.run()
    
    
'''
curl -v -H "Content-Type:application/json" -X POST http://127.0.0.1:5000/index -d "{\"username\":\"Das\"}"

import requests
import json
user={'username': 'Das'}
headers= {'Content-Type':"application/json"}
r = requests.post("http://127.0.0.1:5000/index", data=json.dumps(user), headers=headers)
>>> r.json()
{'username': 'Das'}

>>> import subprocess
>>> import shlex
>>> args = shlex.split(r'curl -v -H "Content-Type:application/json" -X POST http://127.0.0.1:5000/index -d "{\"username\":\"Das\"}"')
>>> args
['curl', '-v', '-H', 'Content-Type:application/json', '-X', 'POST', 'http://127.0.0.1:5000/index', '-d', '{"username":"Das"}']
obj = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
>>> obj.stdout.read()
'{\n  "username": "Das"\n}\n'
>>> obj.stderr.read()
'''