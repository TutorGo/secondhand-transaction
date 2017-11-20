import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView
from django.db.models import Q

from post.forms import SearchForm
from post.forms.post import PostRegist
from .models import Post
from time import sleep


# Create your views here.
class SellListView(LoginRequiredMixin, FormView):
    login_url = 'member:login'
    model = Post
    template_name = 'post/sell.html'
    form_class = SearchForm


class AjaxSell(View):
    def get(self, request):
        page = int(request.GET.get('offset', 8))
        category = request.GET.get('category', "")
        search_result = request.GET.get('search', "")
        if page == 8:
            page_min = 0
        else:
            page_min = page - 4
        if category:
            posts = Post.objects.filter(category=category)[page_min:page]
        elif search_result:
            posts = Post.objects.filter(Q(title__contains=search_result) \
                                        | Q(content__contains=search_result))[page_min:page]
        else:
            posts = Post.objects.all()[page_min:page]
        json_list = []
        for post in posts:
            json_list.append({'title': post.title, 'photo': post.image_1.url, 'pk': post.pk, \
                              'category': post.get_category_display(), 'price': post.price})

        data = json.dumps(json_list)
        return HttpResponse(data, content_type='application/json')

class AjaxDetail(LoginRequiredMixin, View):
    login_url = 'member:login'
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        photo_list = [post.image_1.url, post.image_2.url, post.image_3.url]

        json_post = {'title': post.title, 'photos': photo_list, 'pk': post.pk, \
                     'category': post.get_category_display(), 'price': post.price, 'content': post.content}
        data = json.dumps(json_post)
        return HttpResponse(data, content_type='application/json')

# def ajax_detail(request, post_id):
#     post = Post.objects.get(id=post_id)
#     photo_list = [post.image_1.url, post.image_2.url, post.image_3.url]
#
#     json_post = {'title': post.title, 'photos': photo_list, 'pk': post.pk, \
#                  'category': post.get_category_display(), 'price': post.price, 'content': post.content}
#     data = json.dumps(json_post)
#     return HttpResponse(data, content_type='application/json')


class PostRegister(LoginRequiredMixin, CreateView):
    login_url = 'member:login'
    template_name = 'post/post_register.html'
    form_class = PostRegist
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostRegister, self).form_valid(form)

