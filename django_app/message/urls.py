from django.conf.urls import url

from message.views import SendMessage, MyReceiveMessage, MySendMessage, DetailMessage, DeleteMessage

app_name = 'message'
urlpatterns = [
    url(r'^send/$', SendMessage.as_view(), name='send_message'),
    url(r'^see/receive/$',MyReceiveMessage.as_view(), name='my_receive_message'),
    url(r'^see/send/$', MySendMessage.as_view(), name='my_send_message'),
    url(r'^detail/(?P<pk>[0-9]+)/$', DetailMessage.as_view(), name='detail_message'),
    url(r'^delete/(?P<message_pk>[0-9]+)/$', DeleteMessage.as_view(), name='delete_message')

]