from app import app  #from __init__.py's app variable 

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"