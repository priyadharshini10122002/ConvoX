from django.forms import ModelForm
from .models import Rooom,User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields= ['name','username','email','password1','password2']

class RooomForm(ModelForm):
    class Meta:
        model=Rooom
        fields='__all__'
        exclude=['host','participants']


class UserForm(ModelForm):
    class Meta:
        model=User
        fields = ['name','avatar','username','email','bio']