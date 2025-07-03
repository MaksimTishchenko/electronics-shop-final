from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]

class ProfileForm(UserChangeForm):
    email = forms.EmailField()
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "avatar"]