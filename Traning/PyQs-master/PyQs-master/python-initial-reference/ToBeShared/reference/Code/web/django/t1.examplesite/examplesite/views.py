from django.views.generic.base import TemplateView
import os 

class MyView(TemplateView):

    template_name = "environ.html"

    def get_context_data(self, **kwargs):
        context = super(MyView, self).get_context_data(**kwargs)
        context['objects'] = os.environ
        return context

from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world")
    
from django.shortcuts import render

import logging
log = logging.getLogger(__name__)

def index2(request, id, url):
    query = request.GET.dict()
    log.debug("GET " + str(request.GET))
    return render(request, 'index.html', {'id': id, 'queries':query})
    
from django.http import HttpResponseRedirect  
from django.urls  import reverse
def hello(request):
    return HttpResponseRedirect(reverse('index'))