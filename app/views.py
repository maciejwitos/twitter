from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django.views import View
from app.forms import RegisterUserForm, AddCommentForm, SendMessageForm
from app.models import *
from django.http import HttpResponse


class Dashboard(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        tweets = Tweet.objects.all()
        add_comment = AddCommentForm()
        return render(request, 'dashboard.html', {'tweets': tweets,
                                                  'add_comment': add_comment})

    def post(self, request):
        add_comment = AddCommentForm(request.POST)
        if add_comment.is_valid():
            Comment.objects.create(message=add_comment.cleaned_data['message'],
                                   tweet=add_comment.cleaned_data['tweet.name'],
                                   user=request.user)
            return redirect('/dashboard/')
        return redirect('/dashboard')


class RegisterView(View):

    def get(self, request):
        form = RegisterUserForm()
        return render(request, 'register_user.html', {'form': form})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(username=form.cleaned_data['email'],
                                     password=form.cleaned_data['password1'],
                                     email=form.cleaned_data['email'])
            user = authenticate(request,
                                username=form.cleaned_data['email'],
                                password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('/dashboard/')
        return redirect('/register_user/')


class UserView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        tweets = Tweet.objects.filter(user=id)
        add_comment = AddCommentForm()
        return render(request, 'user.html', {'tweets': tweets,
                                             'add_comment': add_comment})

    def post(self, request, id):

        add_comment = AddCommentForm(request.POST)
        if add_comment.is_valid():
            Comment.objects.create(message=add_comment.cleaned_data['message'],
                                   tweet=add_comment.cleaned_data['tweet.name'],
                                   user=request.user)
            return redirect(f'/user/{id}')
        return redirect(f'/user/{id}')


class DeleteUserConfirm(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'delete_user.html')


class DeleteUser(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        user = User.objects.get(id=request.user.pk)
        user.delete()
        return redirect('/login/')


class UserDetails(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'user_details.html')


class Received(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self, request):
        received = Message.objects.filter(receiver=request.user.pk)
        return render(request, 'received.html', {'received': received})


class Sent(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        sent = Message.objects.filter(sender=request.user.pk)
        return render(request, 'sent.html', {'sent': sent})



class SendMessage(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = SendMessageForm()
        return render(request, 'new_message.html', {'form': form})

    def post(self, request):
        form = SendMessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(text=form.cleaned_data['text'],
                                   sender=request.user,
                                   receiver=form.cleaned_data['receiver'])
            return redirect('/messages/')
        return redirect('/dashboard/')


class Settings(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'settings.html')
