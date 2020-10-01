from django import forms
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    
    


class DocumentForm(forms.Form):
    docfile = forms.FileField( label='Select a file' )
    
    
##Signup form
from django.contrib.auth.password_validation  import password_validators_help_text_html, validate_password

class SignupForm(forms.Form):
    user = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, help_text= password_validators_help_text_html())
    again_password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        user = cleaned_data.get("user")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        user_obj = User(username=user, password=password, email=email)
        validate_password(password, user_obj)
        if self.user_exists(user): 
            self.add_error('user', "User exists!!")
        
    def user_exists(self, username):
        user_count = User.objects.filter(username=username).count()
        if user_count == 0:
            return False
        return True