from flask import Flask
app = Flask(__name__)
from app import routes  #should be last as routes module needs above app variable 
