from django.conf.urls import url
from .views import Login, facebook_login, naver_login, Logout, SignUpView
from . import views

app_name = 'member'
urlpatterns = [
    url('^login/$', Login.as_view(), name='login'),
    url('^logout/$', Logout.as_view(), name='logout'),
    url('^signup/$', SignUpView.as_view(), name='signup'),
    url('^facebook_login/$', facebook_login, name='facebook_login'),
    url('^naver_login/$', naver_login, name='naver_login'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]