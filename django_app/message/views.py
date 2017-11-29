from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect, Http404

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView

from message.forms import MessageForm
from message.models import Message

MyUser = get_user_model()


class SendMessage(CreateView):
    login_url = 'member:login'
    template_name = 'message/message.html'
    form_class = MessageForm
    success_url = reverse_lazy('message:my_send_message')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        nickname = self.request.GET.get('nickname', "")
        recipient = MyUser.objects.get(nickname=nickname)
        form.instance.recipient = recipient
        if self.request.GET.get('nickname', ""):
            ValidationError("닉네임이 존재하지 않습니다.")
        return super(SendMessage, self).form_valid(form)


class MyReceiveMessage(ListView):
    model = Message
    template_name = 'message/my_message.html'
    context_object_name = 'messages'
    paginate_by = 2

    def get_queryset(self):
        messages = Message.objects.filter(Q(recipient=self.request.user) & Q(recipient_delete=False))
        return messages

    def get_context_data(self, **kwargs):
        data = super(MyReceiveMessage, self).get_context_data(**kwargs)
        data['url'] = "/message/see/receive"
        data['option'] = "받은 쪽지함"
        data['url2'] = "/message/see/send/"
        data['option2'] = "보낸 쪽지함"
        return data


class MySendMessage(MyReceiveMessage):
    def get_queryset(self):
        messages = Message.objects.filter(Q(sender=self.request.user) & Q(sender_delete=False))
        return messages

    def get_context_data(self, **kwargs):
        data = super(MySendMessage, self).get_context_data(**kwargs)
        data['url'] = "/message/see/send/"
        data['option'] = "보낸 쪽지함"
        data['url2'] = "/message/see/receive"
        data['option2'] = "받은 쪽지함"
        return data


class DetailMessage(DetailView):
    model = Message
    template_name = 'message/detail_message.html'


class DeleteMessage(View):
    def post(self, request, message_pk):
        message = Message.objects.get(pk=message_pk)
        if request.user == message.sender:
            message.sender_delete = True
            message.save()
            return redirect('message:my_send_message')
        elif request.user == message.recipient:
            message.recipient_delete = True
            message.save()
            return redirect('message:my_receive_message')

        return Http404
