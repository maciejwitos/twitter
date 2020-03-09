from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.forms import ModelForm
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


class SendMessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'text']
        widgets = {'text': forms.Textarea(attrs={'cols': 80, 'rows': 7}),
                   'sender': forms.HiddenInput()}


class NewTweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ['message', 'user']
        widgets = {'user': forms.HiddenInput()}