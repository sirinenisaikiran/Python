from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def api_root():
	return 'Welcome'

@app.route('/articles')
def api_articles():
	return 'List of ' + url_for('api_articles')

@app.route('/articles/<articleid>')
def api_article(articleid):
	return 'You are reading ' + articleid

if __name__ == '__main__':
	app.run()

'''
curl http://127.0.0.1:5000/
curl http://127.0.0.1:5000/articles
curl http://127.0.0.1:5000/articles/2


Note:
Other converter 
@app.route('/articles/<int:articleid>')
@app.route('/articles/<float:articleid>')
@app.route('/articles/<path:articleid>')

The default is string which accepts any text without slashes.
'''