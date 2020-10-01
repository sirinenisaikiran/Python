from django.conf.urls import url, include 

from . import views


urlpatterns = [        
    url(r'^book-create/',  views.create_book, name="modelex-book-create"),  
    url(r'^author-create/',  views.AuthorCreate.as_view(), name="modelex-author-create"), 
    url(r'^books/',  views.latest_books , name="modelex-books-list"),
   url(r'^authors/',  views.latest_authors , name="modelex-authors-list"),
]