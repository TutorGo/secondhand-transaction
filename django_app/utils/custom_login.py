from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages

class CustomRequiredLogin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif not request.user.is_email_verification:
            messages.error(request, "이메일 인증 하세요")
            return render(request, 'base/main.html')
        return super(CustomRequiredLogin, self).dispatch(request, *args, **kwargs)
