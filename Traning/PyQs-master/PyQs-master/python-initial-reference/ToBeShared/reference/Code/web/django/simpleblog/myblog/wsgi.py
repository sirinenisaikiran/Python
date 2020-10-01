"""
WSGI config for myblog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""


import os
import sys
import site

#site:This module is automatically imported during initialization
#addsitedir: Add a directory to sys.path and process its .pth files.
# Add the site-packages of the chosen virtualenv to work with
#$WORKON_HOME/simpleblog/Lib/site-packages
#find out exact dir 
sitedir = os.path.expanduser("~/Envs/simpleblog/Lib/site-packages")
site.addsitedir(sitedir)  #C:\Users\das\Envs\simpleblog\Lib\site-packages

# Add the app's directory to the PYTHONPATH
app_dir = r"D:\Desktop\PPT\python\OtherPython\Django\code\recent\simpleblog"
sys.path.append(app_dir)
sys.path.append(os.path.join(app_dir, 'myblog'))  #where settings.py exists 

# Activate your virtual env

activate_env = os.path.expanduser("~/Envs/simpleblog/Scripts/activate_this.py") #C:\Users\das\Envs\simpleblog\Scripts

#python2.7 
#execfile(activate_env, dict(__file__=activate_env))
#python3 
with open(activate_env) as f:
    code = compile(f.read(), activate_env, 'exec')
    exec(code, dict(__file__=activate_env))




from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblog.settings")

application = get_wsgi_application()
