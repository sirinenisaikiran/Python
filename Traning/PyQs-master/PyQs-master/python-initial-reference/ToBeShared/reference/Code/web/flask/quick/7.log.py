from flask import Flask, url_for
from flask import request
from flask import json
from flask import Response

app = Flask(__name__)

import logging
file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

@app.route('/hello', methods = ['GET'])
def api_hello():
    app.logger.info('informing you that im processing a request')
    app.logger.warning('warning you that im processing a request')
    app.logger.error('screaming bloody murder!')
    
    return "check your logs\n"
    

if __name__ == '__main__':
    app.run()

'''
curl -v  http://127.0.0.1:5000/hello


Note:
Activating pretty (HTML) debug messages during development can be done simply by passing an argument
app.run(debug=True)


'''