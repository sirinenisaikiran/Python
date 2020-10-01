from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from  django.urls import reverse, reverse_lazy


from .forms import *
from .models import *


'''
def create_author(request):   

    # if this is a POST request we need to process the form data
    if request.method == 'POST':      
        # create a form instance and populate it with data from the request:
        form = AuthorForm(request.POST)
        log.debug("POST " + str(request.POST))
        # check whether it's valid:
        if form.is_valid():            
            form.save(commit=True)           
            return HttpResponseRedirect(reverse('modelex-authors-list'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AuthorForm()
    return render(request, 'create.html', {'form': form, 'create_string': 'modelex-author-create'})
'''    

#default value: template_name_suffix =  '_form' , 
#default template_name to be 'modelform/templates/modelform/author_form.html'.
from django.views.generic.edit import CreateView
from django.utils import timezone
class AuthorCreate(CreateView):
    model = Author   
    success_url = reverse_lazy('modelex-authors-list')  # _lazy is must else ImproperlyConfigured error 
    fields = ['name', 'title', 'birth_date']    
    
    def get_context_data(self, **kwargs):
        ''' Any context var for form '''
        context = super(AuthorCreate, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #Do some addl activity, super class saves it in database 
        return super(AuthorCreate, self).form_valid(form)

    
    
def create_book(request):  
    # if this is a POST request we need to process the form data
    if request.method == 'POST':      
        # create a form instance and populate it with data from the request:
        form = BookForm(request.POST)        
        # check whether it's valid:
        if form.is_valid():           
            form.save(commit=True)           
            return HttpResponseRedirect(reverse('modelex-books-list'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = BookForm()
    return render(request, 'create.html', {'form': form, 'create_string': 'modelex-book-create'})
  
    
def latest_books(request):    
    book_list = Book.objects.prefetch_related('authors').all()
    return render(request, 'list.html', {'book_list': book_list})

def latest_authors(request):   
    a_list = Author.objects.prefetch_related('book_set').all()
    return render(request, 'list_a.html', {'a_list': a_list})
    
