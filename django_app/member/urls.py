from django.conf.urls import url
from .views import Login, facebook_login, naver_login

app_name = 'member'
urlpatterns = [
    url('^login/$', Login.as_view(),name='login'),
    url('^facebook_login/$', facebook_login, name='facebook_login'),
    url('^naver_login/$', naver_login, name='naver_login')
]