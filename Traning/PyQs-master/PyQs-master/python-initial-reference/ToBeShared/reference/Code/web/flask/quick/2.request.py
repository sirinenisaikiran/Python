from flask import Flask, url_for
app = Flask(__name__)

from flask import request

@app.route('/hello')
def api_hello():
	if 'name' in request.args:
		return 'Hello ' + request.args['name']
	else:
		return 'Hello John Doe'

if __name__ == '__main__':
	app.run()

'''
curl -v http://127.0.0.1:5000/hello
curl -v  http://127.0.0.1:5000/hello?name=Luis


'''
'''
request.path             /page.html
request.script_root      /myapplication
request.base_url         http://www.example.com/myapplication/page.html
request.url              http://www.example.com/myapplication/page.html?x=y
request.url_root         http://www.example.com/myapplication/
    
    
request.args
    the key/value pairs in the URL query string
request.form
    the key/value pairs in the body, from a HTML post form, or JavaScript request that isn't JSON encoded
request.files
    the files in the body, which Flask keeps separate from form. 
    HTML forms must use enctype=multipart/form-data or files will not be uploaded.
request.values
    combined args and form, preferring args if keys overlap
request.json
    for application/json, it is python object 
request.data 
    Contains the incoming request data as string in case it came with a mimetype Flask does not handle.

All of these are MultiDict instances. You can access values using eg for .form 
request.form['name']
    use indexing if you know the key exists
request.form.get('name')
    use get if the key might not exist
request.form.getlist('name')
    use getlist if the key is sent multiple times and you want a list of values. 
    get only returns the first value.
request.get_json(force=True) 
    if set to True the mimetype is ignored., 
    so it won't return None for requests that don't have application/json set in the contentType header

'''