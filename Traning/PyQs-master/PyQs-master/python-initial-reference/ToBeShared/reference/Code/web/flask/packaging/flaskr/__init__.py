from flask import Flask
app = Flask(__name__)
from . import quick_server  #should be last as routes module needs above app variable 
