import re
from django import forms 
from  django.core.exceptions import ValidationError
from django.contrib.auth.models import User
def notnumber(value):
    for i in value:
        if i.isdigit():
            raise ValidationError('Name must not contain numbers')

def existalready(value):
    existing=User.objects.all()
    j=0
    for users in existing:          
                if (str(users)==str(value)):
                   raise ValidationError('Username already exist')     
def password_correct(value):
     special=0
     num=0
     up_c=0
     lo_c=0
     special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
     for i in value:
            if(i.isupper()):
               up_c+=1
            if(i.isdigit()):
                 num+=1
            if(i.islower()):
                 lo_c+=1
            if not(special_char.search(i) == None):
                 special+=1
     if not(special>0 and num>0 and up_c>0 and lo_c>0):
          raise ValidationError(f'Must contain a uppercase,lowercase,numeral and special character')
class RegistrationForm(forms.Form):
    username=forms.CharField(max_length=30,validators=[existalready])
    password=forms.CharField(max_length=30,validators=[password_correct])
    ConfirmPassword=forms.CharField(max_length=30,validators=[password_correct])
    firstname=forms.CharField(max_length=30,validators=[notnumber])
    lastname=forms.CharField(max_length=30, validators=[notnumber])

class LoginForm(forms.Form):
    username=forms.CharField(max_length=30)
    password=forms.CharField(max_length=30)