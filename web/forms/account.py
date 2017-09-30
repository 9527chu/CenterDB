from django import forms
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = UsernameField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class RegistForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=16, min_length=6)
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=6)
