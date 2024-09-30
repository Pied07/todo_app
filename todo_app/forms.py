from django import forms
from .models import Task_Model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class Task_Form(forms.ModelForm):
    class Meta:
        model = Task_Model
        fields = ['task_name']
        widgets = {
            'task_name': forms.TextInput(attrs={
                'placeholder':'Add New Task',
                'class':'form-control'
            })
        }

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    class Meta:
        model = User
        fields = ['username','password1','password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Enter Username','id':'username'}))
    password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'placeholder':'Enter Password','id':'password'}))