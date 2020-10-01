from django.conf.urls import url, include 
from . import views

#after dummy/
urlpatterns = [    
    url(r'^(\w+)/$',  views.index),    #views 's index method has 2nd arg as (\w+)
] 