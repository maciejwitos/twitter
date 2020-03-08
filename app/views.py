from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django.views import View
from app.forms import RegisterUserForm, AddCommentForm, SendMessageForm, NewTweetForm
from app.models import *
from django.http import HttpResponse


class Dashboard(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        tweets = Tweet.objects.all()
        print(request.POST.get('tweet_name'))
        add_comment = AddCommentForm(request.POST, initial={'user': request.user,
                                                            'tweet': request.GET.get('tweet_name')})
        return render(request, 'dashboard.html', {'tweets': tweets,
                                                  'add_comment': add_comment})

    def post(self, request):
        add_comment = AddCommentForm(request.POST, initial={'user': request.user,
                                                            'tweet': request.POST.get('tweet_name')})
        print(request.POST.get('tweet_name'))
        if add_comment.is_valid():
            add_comment.save()
            return redirect('/dashboard/')
        return redirect('/dashboard')


class UserView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        tweets = Tweet.objects.filter(user=id)
        return render(request, 'user.html', {
            'tweets': tweets})


class AddCommentView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = AddCommentForm(request.GET, initial={'tweet': request.GET.get('tweet_name'),
                                                     'message': request.GET.get('message'),
                                                     'user': request.GET.get('user')})
        if form.is_valid():
            form.save()
        return redirect(f'/user/{request.user.pk}/')


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


class Received(LoginRequiredMixin, View):
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
        form = SendMessageForm(initial={'sender': request.user})
        return render(request, 'new_message.html', {'form': form})

    def post(self, request):
        form = SendMessageForm(request.POST, initial={'sender': request.user})
        if form.is_valid():
            form.save()
            return redirect('/received/')
        return redirect('/dashboard/')


class Settings(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'settings.html')


class NewTweet(View):

    def get(self, request):
        form = NewTweetForm(initial={'user': request.user})
        return render(request, 'new_tweet.html', {'form': form})

    def post(self, request):
        form = NewTweetForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            form.save()
            return redirect(f'/user/{request.user.pk}')
        return redirect(f'/new_tweet/')


class DeleteTweet(View):

    def get(self, request, id):
        tweet = Tweet.objects.get(id=id)
        tweet.delete()
        return redirect(f'/user/{request.user.pk}')
