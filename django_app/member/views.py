from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.contrib.auth import login as django_login
# Create your views here.
from member.utils.socials_exception import DebugTokenException, GetAccessTokenException, NaverGetAccessTokenException
from .forms import LoginForm
import requests

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

        print(result)
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

    code = request.GET.get('code')
    print(request)

    def get_access_token(code):

        access_token_url = 'https://nid.naver.com/oauth2.0/token'

        access_token_params = {
            'grant_type': 'authorization_cod',
            'client_id': settings.NAVER_APP_ID,
            'client_secret': settings.NAVER_SECRET_KEY,
            'code': code
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
        header = {"Authorization" : user_info_header}
        response = requests.get(user_info_url, headers=header)
        result = response.json()

        print(result)


    access_token = get_access_token(code)
    get_user_info(access_token['access_token'])

class Logout(LogoutView):
    def get(self, request, *args, **kwargs):
        return redirect('main')