import re
from email.utils import parseaddr
from django import forms
from django.contrib import messages
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm
from member.models import MyUser
from django.utils.translation import ugettext, ugettext_lazy as _

MyUser = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=40, widget=forms.TextInput \
        (attrs={'placeholder': 'Email', 'class': 'login-email'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput \
        (attrs={'placeholder': 'Password', 'class': 'login-password'}))

    error_messages = {
        'invalid_login': _(
            "ID or PW incorrect"
        ),
        'inactive': _("ID or PW incorrect"),
    }


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput \
        (attrs={'placeholder': 'password', 'class': 'signup-password'}))
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput \
        (attrs={'placeholder': 'confirm passowrd', 'class': 'signup-password'}))

    class Meta:
        model = MyUser
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'email@example.com', 'class': 'signup-email'}),
            'nickname': forms.TextInput(attrs={'placeholder': 'nickname', 'class': 'signup-nickname'}),
        }
        fields = (
            'email',
            'nickname',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        m = re.match(email_pattern, email)
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_("이미 존재하는 email 입니다."))
        if m:
            return email
        else:
            raise forms.ValidationError(_("email 형식이 아닙니다."))


class NicknameChangeForm(forms.Form):
    nickname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'mat-input'}))

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if MyUser.objects.filter(nickname=nickname):
            raise forms.ValidationError(_("이미 존재하는 nickname 입니다."))
        return nickname


class UserPasswordChangeForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class':'mat-input'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'mat-input'}),
    )

class EmailInputForm(forms.Form):
    email = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'mat-input'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        m = re.match(email_pattern, email)
        if not MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_("존재하는 않는 email 입니다."))
        elif not MyUser.objects.get(email=email).user_type == 'g':
            raise forms.ValidationError(_("일반 회원가입 회원만 가능 합니다"))
        if m:
            return email
        else:
            raise forms.ValidationError(_("email 형식이 아닙니다."))
