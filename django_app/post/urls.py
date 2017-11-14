from django.conf.urls import url
from .views import SellListView, AjaxSell, ajax_detail
from . import views

app_name = 'post'
urlpatterns = [
    url(r'^sell/$', SellListView.as_view(), name="sell_page"),
    url(r'^ajax/sell/$', AjaxSell.as_view(), name="ajax_sell"),
    url(r'^sell/(?P<post_id>[0-9]+)/$', views.ajax_detail)
]