from django.db import models

# Create your models here.

class Book(models.Model):                   #two field  
    name = models.CharField(max_length=50)
    pub_date = models.DateField()	
    email = models.EmailField(null=True, blank=True)
    def __str__(self):             
        return self.name
