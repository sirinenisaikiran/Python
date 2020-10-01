"""examplesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from .views import MyView, index, index2
from . import views
from django.conf.urls import include 
from django.urls import include, path  
from django.conf import settings 
import os
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^$', views.index, name='index'),  
    url(r'^hello2/(?P<id>\d+)', views.index2, kwargs={'url': 'index'}, name = "views_index"), 
    url(r'hello/$', views.hello),
    
    url(r'^dummy/', include('dummy.urls')),
    
    url(r'^about/$', TemplateView.as_view(template_name="about.html")),
    url(r'^environ/$', MyView.as_view()),
]
#for debug_toolbar 
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
    
##If using with GEVENT as wsgi automatically shuts off static file serving 
if 'GEVENT' in os.environ:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
