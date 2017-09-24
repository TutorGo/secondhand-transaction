from django.conf import settings

def facebook_info(request):
    context = {
        'facebook_app_id': settings.FACEBOOK_APP_ID,
        'site_url': settings.SITE_URL,
    }
    return context

def naver_info(request):
    context = {
        'naver_app_id': settings.NAVER_APP_ID
    }
    return context