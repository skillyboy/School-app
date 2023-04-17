from django.contrib.auth import models
from schoolapp.models import Message, Wishlist
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import fields
from django.forms import ModelForm

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email','password1','password2',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control'}),
        }
        
class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ('thecontent',)
        
        
    
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('value','forum')
       
    
    
