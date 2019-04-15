from django.db import models
from django.contrib import auth
# Create your models here.
class User(auth.models.User, auth.models.PermissionsMixin):
    #this is the built in User class
    #we will inherit from it
    def __str__(self):
        #just gives the object the name of the user
        return self.first_name + ' '+ self.last_name
