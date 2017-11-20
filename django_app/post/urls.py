from django.conf.urls import url
from .views import SellListView, AjaxSell, AjaxDetail, PostRegister
from . import views

app_name = 'post'
urlpatterns = [
    url(r'^sell/$', SellListView.as_view(), name="sell_page"),
    url(r'^ajax/sell/$', AjaxSell.as_view(), name="ajax_sell"),
    url(r'^sell/(?P<post_id>[0-9]+)/$', AjaxDetail.as_view()),
    url(r'^register/$', PostRegister.as_view(), name='post_register')
    # url(r'^register/$', views.register, name='post_register')
]