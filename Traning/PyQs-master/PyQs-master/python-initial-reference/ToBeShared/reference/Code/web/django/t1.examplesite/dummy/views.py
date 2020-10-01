from django.http import HttpResponse
def index(request, name):           #comes from url's (\w+)
    return HttpResponse("Hello " + name)