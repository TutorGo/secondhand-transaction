from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
# Create your views here.
from .forms import LoginForm

class Login(LoginView):
    template_name = 'member/login.html'
    authentication_form = LoginForm
    redirect_field_name = 'main'

def facebook_login(request):
    pass