from django.conf.urls import url
from .views import PostListView, AjaxSell, AjaxDetail, PostRegister, PostUpdate
from . import views

app_name = 'post'
urlpatterns = [
    url(r'^sell/$', PostListView.as_view(), name="sell_page"),
    url(r'^buy/$', PostListView.as_view(), name="buy_page"),
    url(r'^load/$', AjaxSell.as_view(), name="ajax_sell"),
    url(r'^detail/(?P<post_id>[0-9]+)/$', AjaxDetail.as_view()),
    url(r'^update/(?P<pk>[0-9]+)/$', PostUpdate.as_view(), name='post_update'),
    # url(r'^update/(?P<pk>[0-9]+)/$', views.post_update, name='post_update'),
    url(r'^register/$', PostRegister.as_view(), name='post_register')
]