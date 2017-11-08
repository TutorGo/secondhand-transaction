from django.conf.urls import url
from .views import sell_page
from . import views

app_name = 'post'
urlpatterns = [
    url(r'^sell/$', views.sell_page, name="sell_page"),
    url(r'^ajax/sell/$', views.ajax_sell, name="ajax_sell")
]