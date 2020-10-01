"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]


#customization starts here 
from django.conf import settings 
import os
from django.conf.urls.static import static

#myownstuff 
from django.views.generic import TemplateView

urlpatterns += [path('', TemplateView.as_view(template_name="myblog/index.html") ),]



#simpleblog 
#run python manage.py migrate 

from django.conf.urls import url

urlpatterns += [
    url(r'^weblog/', include('zinnia.urls')),
    url(r'^comments/', include('django_comments.urls')),
 ]

##If using with GEVENT as wsgi automatically shuts off static file serving 
#note static only works in debug=True
#STATIC_ROOT = os.path.join(BASE_DIR, "static/") #or some path  
#python manage.py collectstatic 
#

if 'GEVENT' in os.environ:
    static_root = settings.STATIC_ROOT #shortcut  #
    urlpatterns += static(settings.STATIC_URL, document_root=static_root)
