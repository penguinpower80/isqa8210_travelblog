from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserAccountForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, help_text='Required')
    last_name = forms.CharField(max_length=20, help_text='Required')
    email = forms.EmailField(max_length=60, help_text='Required')

    class Meta(UserCreationForm.Meta):
        model = User

        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
