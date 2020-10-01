from django.conf.urls import url
from django.views.generic import TemplateView

from . import views 

urlpatterns = [ 
        url(r'^ajax/add/$', views.add_todo),
        url(r'^ajax/more/$', views.more_todo),
        url(r'', TemplateView.as_view(template_name='ajaxapp/index.html')),
]
