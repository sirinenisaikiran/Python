from django.shortcuts import render

# Create your views here.

from .models import Book

def latest_books(request):
	book_list = Book.objects.order_by('-pub_date')
	return render(request, 'books/latest_books.html', {'book_list': book_list})

    
from django.views.generic.list import ListView
from django.utils import timezone

from .models import Book

class BookListView(ListView):

    model = Book
    template_name = "books/booklist.html"

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

