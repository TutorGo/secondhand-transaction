import string
import random
from django.conf import settings

def facebook_info(request):
    context = {
        'facebook_app_id': settings.FACEBOOK_APP_ID,
        'site_url': settings.SITE_URL,
    }
    return context

# 사이트 위조 공격을 막기 위한 state 생성기
def state_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def naver_info(request):
    # state 생성
    state = state_generator()
    context = {
        'naver_app_id': settings.NAVER_APP_ID,
        'state': state
    }
    return context
