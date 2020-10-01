from app import app  #from __init__.py's app variable 

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Nobody'}
    return '''
<html>
    <head>
        <title>Home Page</title>
    </head>
    <body>
        <h1>Hello, ''' + user['username'] + '''!</h1>
    </body>
</html>'''