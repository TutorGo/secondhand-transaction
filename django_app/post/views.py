import json
from django.shortcuts import render,HttpResponse
from django.views import View
from django.views.generic import ListView, FormView
from django.db.models import Q

from post.forms import SearchForm
from .models import Post
from time import sleep
# Create your views here.

class SellListView(FormView):
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
            posts = Post.objects.filter(Q(title__contains=search_result)\
                                        | Q(content__contains=search_result))[page_min:page]
        else:
            posts = Post.objects.all()[page_min:page]
        json_list = []
        for post in posts:
            json_list.append({'title': post.title, 'photo': post.image_1.url, 'pk': post.pk,\
                              'category': post.get_category_display(), 'price': post.price})

        data = json.dumps(json_list)
        return HttpResponse(data, content_type='application/json')