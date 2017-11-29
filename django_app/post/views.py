import json

from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView, DeleteView
from django.db.models import Q

from post.decorators import post_owner
from post.forms import SearchForm
from post.forms.post import PostRegist, PostUpdate
from utils.custom_login import CustomRequiredLogin
from .models import Post


# Create your views here.
class PostListView(CustomRequiredLogin, FormView):
    login_url = 'member:login'
    model = Post
    template_name = 'post/sell.html'
    form_class = SearchForm


class AjaxSell(View):
    def get(self, request):
        page = int(request.GET.get('offset', 8))
        category = request.GET.get('category', "")
        search_result = request.GET.get('search', "")
        kinds = request.GET.get('kinds', "")
        if page == 8:
            page_min = 0
        else:
            page_min = page - 4
        if category:
            posts = Post.objects.filter(Q(sell_or_buy=kinds) & Q(category=category))[page_min:page]
        elif search_result:
            posts = Post.objects.filter(Q(sell_or_buy=kinds) & \
                                        (Q(title__contains=search_result) | Q(content__contains=search_result))) \
                [page_min:page]
        else:
            posts = Post.objects.filter(sell_or_buy=kinds)[page_min:page]
        json_list = []
        for post in posts:
            json_list.append({'title': post.title, 'photo': post.image_1.url, 'pk': post.pk, \
                              'category': post.get_category_display(), 'price': post.price})

        data = json.dumps(json_list)
        return HttpResponse(data, content_type='application/json')


class AjaxDetail(CustomRequiredLogin, View):
    login_url = 'member:login'

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        photo_list = [post.image_1.url, post.image_2.url, post.image_3.url]

        json_post = {'title': post.title, 'photos': photo_list, 'pk': post.pk, \
                     'category': post.get_category_display(), 'price': post.price, 'content': post.content,\
                     'nickname': post.author.nickname}
        data = json.dumps(json_post)
        return HttpResponse(data, content_type='application/json')


class PostRegister(CustomRequiredLogin, CreateView):
    login_url = 'member:login'
    template_name = 'post/post_register.html'
    form_class = PostRegist
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostRegister, self).form_valid(form)


@method_decorator(post_owner, name='dispatch')
class PostUpdate(CustomRequiredLogin, UpdateView):
    model = Post
    form_class = PostUpdate
    context_object_name = 'post'
    template_name = 'post/post_update.html'
    success_url = reverse_lazy('member:my_post')

    def get_initial(self):
        initial = super(PostUpdate, self).get_initial()
        post = self.get_object()
        price = post.price.replace(",", "").strip()
        initial['price'] = int(price)
        return initial


@method_decorator(post_owner, name='dispatch')
class PostDelete(CustomRequiredLogin, DeleteView):
    model = Post
    success_url = reverse_lazy('member:my_post')

