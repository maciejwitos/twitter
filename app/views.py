from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from app.forms import RegisterUserForm, SendMessageForm, NewTweetForm
from app.models import *



''' ################# MAINS VIEW ######################'''

'''
Dashboard with all tweets from database
'''

class Dashboard(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        tweets = Tweet.objects.all()
        return render(request, 'dashboard.html', {'tweets': tweets})


'''View with all yours tweets'''


class UserView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        tweets = Tweet.objects.filter(user=id)
        return render(request, 'user.html', {'tweets': tweets})


''' ################# COMMENTS ######################'''


'''Adding comments view, you can add'''


class AddCommentView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request):
        user = User.objects.get(id=request.POST.get('user'))
        tweet = Tweet.objects.get(id=request.POST.get('tweet'))
        message = request.POST.get('message')
        next = request.POST.get('next')

        if user and tweet and message:
            Comment.objects.create(tweet=tweet,
                                   message=message,
                                   user=user)
        return redirect(next)


''' ################# USERS ######################'''


'''Register user view'''

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


'''Deletion user confirmation view'''


class DeleteUserConfirm(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'delete_user.html')


'''Deletion user view'''


class DeleteUser(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        user = User.objects.get(id=request.user.pk)
        user.delete()
        return redirect('/login/')


'''User details view'''


class UserDetails(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'user_details.html')


''' User settings view'''


class Settings(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'settings.html')


''' ################# MESSAGES ######################'''


'''Received emails'''


class Received(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        received = Message.objects.filter(receiver=request.user.pk)
        return render(request, 'received.html', {'received': received})


'''Sent emails'''


class Sent(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        sent = Message.objects.filter(sender=request.user.pk)
        return render(request, 'sent.html', {'sent': sent})


'''New message form'''


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


''' ################# TWEET ######################'''

'''Create new Tweet form'''


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


'''Delete tweet form'''


class DeleteTweet(View):

    def get(self, request, id):
        tweet = Tweet.objects.get(id=id)
        tweet.delete()
        return redirect(f'/user/{request.user.pk}')
