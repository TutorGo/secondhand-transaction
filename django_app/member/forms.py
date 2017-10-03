from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from member.models import MyUser
from django.utils.translation import ugettext, ugettext_lazy as _

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=20, widget=forms.TextInput(\
                                attrs={'placeholder': 'Email', 'class': 'login-email'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput\
                                (attrs={'placeholder': 'Password', 'class': 'login-password'}))

    error_messages = {
        'invalid_login': _(
            "ID or PW incorrect"
        ),
        'inactive': _("ID or PW incorrect"),
    }



class SignUpForm(UserCreationForm):
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    class Meta:
        model = MyUser
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'email을 입력하시오'}),
            'nickname': forms.TextInput(attrs={'placeholder': '별명을 입력하시오'}),
        }
        fields = (
            'email',
            'nickname',
        )
