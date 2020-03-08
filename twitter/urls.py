"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

from app.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', Dashboard.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login_user.html')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/')),
    path('accounts/profile/', Dashboard.as_view()),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html')),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html')),
    path('user/<int:id>/', UserView.as_view()),
    path('user/details/', UserDetails.as_view()),
    path('received/', Received.as_view()),
    path('sent/', Sent.as_view()),
    path('send_message/', SendMessage.as_view()),
    path('delete_confirm/', DeleteUserConfirm.as_view(), name='delete_account'),
    path('delete_account/', DeleteUser.as_view()),
    path('settings/', Settings.as_view(), name='settings'),
    path('change_username/', Dashboard.as_view(), name='change_username'),
    path('change_email/', Dashboard.as_view(), name='change_email'),
    path('new_tweet/', NewTweet.as_view()),
    path('delete_tweet/<int:id>/', DeleteTweet.as_view()),
    path('add_comment/', AddCommentView.as_view(), name='add-comment')

]
