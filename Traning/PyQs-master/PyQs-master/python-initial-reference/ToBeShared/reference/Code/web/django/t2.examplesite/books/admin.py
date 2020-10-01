from django.contrib import admin

# Register your models here.

from .models import Book 


class BookAdmin(admin.ModelAdmin):
	fields = ['pub_date', 'name', 'email']  # reorder

admin.site.register(Book, BookAdmin)  
