import requests
import time
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, ListView

from post.models import Post
from utils.custom_login import CustomRequiredLogin
from utils.socials_exception import DebugTokenException, GetAccessTokenException, NaverGetAccessTokenException
from .forms import LoginForm, SignUpForm
from .tokens import account_activation_token
from .tasks import email_send

User = get_user_model()


class Login(LoginView):
    template_name = 'member/login.html'
    authentication_form = LoginForm
    redirect_field_name = 'main'

def facebook_login(request):
    # facebook 로그인 버튼을 누르면 code를 반환한다.
    code = request.GET.get('code')

    def get_access_token(code):
        # access_token을 받아올 url
        access_token_url = 'https://graph.facebook.com/v2.10/oauth/access_token'

        # access_token에 요청을 보내고 다시 돌아올 url 설정 request.path이 리퀘스트를 받은 url을 반환한다 ex)/member/facebook_login/
        redirect_uri = '{}{}'.format(
            settings.SITE_URL,
            request.path
        )

        # access_token 요청하기 위해서는 페이스북 앱 id, 리다이렉트할 url, 페이스북 앱 secret key, code가 필요하다
        access_token_params = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': redirect_uri,
            'client_secret': settings.FACEBOOK_SECRET_KEY,
            'code': code,
        }
        # requests로 access_token_url에 params로 access_token_params으로 요청
        response = requests.get(
            access_token_url,
            params=access_token_params
        )

        result = response.json()
        if 'access_token' in result:
            return result['access_token']
        elif 'error' in result:
            return result['error']['message']

    # 토큰을 디버그 하는 함수
    def debug_access_token(access_token):

        app_access_token = '{}|{}'.format(
            settings.FACEBOOK_APP_ID,
            settings.FACEBOOK_SECRET_KEY
        )

        debug_token_url = 'https://graph.facebook.com/debug_token'

        debug_token_params = {
            'input_token': access_token,
            'access_token': app_access_token
        }

        response = requests.get(debug_token_url, params=debug_token_params)

        result = response.json()

        if 'error' in result:
            raise DebugTokenException(result)
        else:
            return result

    # 오류를 출력하고 이점 URL로 리다이렉트
    def error_message_and_redirect_referer():
        error_message = 'Facebook login error'
        messages.error(request, error_message)

        # 이전 URL 로 리다이렉트
        return redirect(request.META['HTTP_REFERER'])

    # 유저 정보를 받아오는 함수
    def get_user_info(user_id, token):
        # user_id 를 url로 넣으면 user의 기본 정보만 들고 올 수 있음
        url_user_info = 'https://graph.facebook.com/v2.9/{user_id}'.format(user_id=user_id)
        url_user_info_params = {
            'access_token': token,
            'fields': ','.join([
                'id',
                'name',
                'email',
            ])
        }
        response = requests.get(url_user_info, params=url_user_info_params)
        result = response.json()
        return result

    if not code:
        return error_message_and_redirect_referer()

    try:
        access_token = get_access_token(code)
        debug_result = debug_access_token(access_token)
        print(debug_result)
        user_info = get_user_info(user_id=debug_result['data']['user_id'], token=access_token)
        user = User.objects.get_or_create_facebook_user(user_info)

        django_login(request, user)
        return redirect('main')
    except GetAccessTokenException as e:
        print(e.code)
        print(e.message)
        return error_message_and_redirect_referer()
    except DebugTokenException as e:
        print(e.code)
        print(e.message)
        return error_message_and_redirect_referer()


def naver_login(request):
    '''
    1. https://developers.naver.com/main/ 내 에플리케이션 등록 클릭
    2. 애플리케이션 등록을 눌리고 앱이름 설정 사용 API 네아로(네이버 아이디 로그인)클릭
    3. 추가 권한 설정
    4. 환경 추가 에서 pc웹
    5. 서비스 URL 의 설명에는 도메인만 적으라고 하지만  http://localhost:8000 다 적어줘야함
    6. Callback URL도 http://localhost:8000/member/naver_login 설정
    '''
    code = request.GET.get('code')
    print(request)

    def get_access_token(code):

        access_token_url = 'https://nid.naver.com/oauth2.0/token'

        access_token_params = {
            'grant_type': 'authorization_code',
            'client_id': settings.NAVER_APP_ID,
            'client_secret': settings.NAVER_SECRET_KEY,
            'code': code,
        }

        response = requests.get(access_token_url, access_token_params)

        result = response.json()
        if 'error' in result:
            raise NaverGetAccessTokenException(result)
        else:
            return result

    def get_user_info(access_token):

        user_info_header = "Bearer " + access_token
        user_info_url = "https://openapi.naver.com/v1/nid/me"
        header = {"Authorization": user_info_header}
        response = requests.get(user_info_url, headers=header)
        result = response.json()

        return result

        # 오류를 출력하고 이점 URL로 리다이렉트

    def error_message_and_redirect_referer():
        error_message = 'Facebook login error'
        messages.error(request, error_message)

        # 이전 URL 로 리다이렉트
        return redirect(request.META['HTTP_REFERER'])

    try:
        access_token = get_access_token(code)
        user_info = get_user_info(access_token['access_token'])
        user = User.objects.get_or_create_naver_user(user_info)
        django_login(request, user)
        return redirect('main')
    except NaverGetAccessTokenException as e:
        print(e.error)
        print(e.error_description)
        return error_message_and_redirect_referer()


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'member/signup.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_email_verification = False
        user.save()
        current_site = get_current_site(self.request)
        subject = 'Activate your blog account.'
        message = render_to_string('member/acc_active_email.html', {
            'user': user, 'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        # user.email_user(subject, message)
        toemail = user.email
        email_send(subject, message, toemail)
        return HttpResponse('메일을 확인해서 인증해주세요.')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_verification = True
        user.save()
        django_login(request, user)
        return HttpResponse('인증이 완료되었습니다. 게시판 사용이 가능합니다')
    else:
        return HttpResponse('Activation link is invalid!')


def member_information(request):
    return render(request, 'member/member_information.html')


class Logout(LogoutView):
    def get(self, request, *args, **kwargs):
        return redirect('main')


class MyPostListView(CustomRequiredLogin, ListView):
    login_url = 'member:login'
    model = Post
    template_name = 'member/mypost.html'

    def get_queryset(self):
        my_post = Post.objects.filter(author=self.request.user)
        return my_post

