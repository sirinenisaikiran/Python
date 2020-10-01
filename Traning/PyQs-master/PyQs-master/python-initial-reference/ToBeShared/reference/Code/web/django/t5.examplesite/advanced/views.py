from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail, get_connection
from django.core.mail.backends.console import EmailBackend
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import StreamingHttpResponse 


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


import mimetypes 
import os.path

from .forms import *
from .models import * 


def contact(request):    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':        
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:            
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['ndas1971@gmail.com']
            if cc_myself:
                recipients.append(sender)            
            send_mail(subject, message, sender, recipients )
            return HttpResponseRedirect(reverse('thanks'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
    
def thanks(request):
    return HttpResponse("email sent")

    
@login_required(login_url='/advanced/login/')  # beginning / is must, reverse('login') -> gives error!! 
def document_list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = form.cleaned_data['docfile'])
            newdoc.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('document-lists'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    # Render list page with the documents and the form
    return render(request, 'upload_list.html',  {'documents': documents, 'form': form}  )


    
def download(request, pk=1):
    # Handle file download
    document    = Document.objects.get(pk = pk)    
    file_full_path = os.path.join(settings.MEDIA_ROOT, document.docfile.name)
    filename = os.path.basename(file_full_path)
    response = StreamingHttpResponse(document.docfile, content_type=mimetypes.guess_type(file_full_path)[0]) 
    response['Content-Disposition'] = "attachment; filename={0}".format(filename)
    response['Content-Length'] = os.path.getsize(file_full_path) 
    return response
    
    
    
    
def signup(request):
    # Handle file upload
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = create_user(username=form.cleaned_data['user'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            # Redirect to login page 
            return HttpResponseRedirect('%s?next=%s' % (reverse('login'), reverse('document-lists')) )
    else:
        form = SignupForm() # A empty, unbound form    
    # Render list page with the documents and the form
    return render(request, 'registration/signup.html',  {'form': form} )


 

    
def create_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    return user



    
    
