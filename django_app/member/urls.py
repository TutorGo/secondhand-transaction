from django.conf.urls import url
from .views import Login, facebook_login, naver_login, Logout, SignUpView, member_information, MyPostListView, \
    ChangeNicknameView, PasswordChangeInputEmail, PasswordChangeView
from . import views

app_name = 'member'
urlpatterns = [
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^facebook_login/$', facebook_login, name='facebook_login'),
    url(r'^naver_login/$', naver_login, name='naver_login'),
    url(r'^member_information/$', views.member_information, name='member_information'),
    url(r'^member_information/mypost/$', MyPostListView.as_view(), name='my_post'),
    url(r'^change/nickname/$', ChangeNicknameView.as_view(), name='nickname_change'),
    url(r'^password_change/input_email/$', PasswordChangeInputEmail.as_view(), name='input_email'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^password/change/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordChangeView.as_view(), name='password_change'),
]