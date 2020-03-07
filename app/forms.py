from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.forms import ModelForm, forms
from django.contrib.auth.models import User
from django.db import models
from app.models import *
from django import forms


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', "password1", "password2")


class LoginUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User


class AddCommentForm(forms.Form):
    message = forms.CharField(max_length=140)
    user = forms.HiddenInput()
    tweet = forms.HiddenInput()


class SendMessageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    sender = forms.HiddenInput()
    receiver = forms.ChoiceField(choices=User.objects.all())