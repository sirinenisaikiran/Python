from django.forms import ModelForm
from .models import *
from django import forms
'''
#Not required as we have used CreateView 
class AuthorForm(ModelForm):    
    class Meta:
        model = Author
        fields = ['name', 'title', 'birth_date']
        widgets = {
            'name': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
'''       
        

class BookForm(ModelForm):
    def clean(self):      
        '''additional validation'''
        cleaned_data = super(BookForm, self).clean()
        name = cleaned_data.get("name")        
        if len(name) < 2:            
                raise forms.ValidationError("Name Length Error")
    class Meta:
        model = Book
        fields = ['name', 'authors']
        widgets = {
            'name': forms.Textarea(attrs={'cols': 80, 'rows':2}),
        }
        
  