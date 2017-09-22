from django.conf.urls import url
from .views import Login
app_name = 'member'
urlpatterns = [
    url('^login/$', Login.as_view(),name='login')
]