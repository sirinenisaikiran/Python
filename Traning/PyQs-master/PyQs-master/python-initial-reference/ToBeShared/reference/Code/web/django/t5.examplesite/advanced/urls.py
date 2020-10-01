from django.conf.urls import url, include 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

#after advanced/

urlpatterns = [        
    url(r'^contact/',  views.contact, name="contact"),  
    
    url(r'^signup/',  views.signup, name = 'signup'),  
    url(r'^login/',  auth_views.login,  {'template_name': 'registration/login.html'}, name = 'login'),  
    url(r'^logout/',  auth_views.logout,{'template_name': 'registration/logout.html'}, name = 'logout'), 
    
    url(r'^list/$', views.document_list, name='document-lists'),
    url(r'^documents/(?P<pk>\d+)/$', views.download , name = 'documents-download'),
    
    url(r'^thanks/',  views.thanks, name='thanks'),     
] 