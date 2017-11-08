import json
from django.shortcuts import render,HttpResponse
from .models import Post
from time import sleep
# Create your views here.

def sell_page(request):
    category = request.GET.get('category', "")

    posts = Post.objects.all()[:4]
    context = {
        'posts': posts,
        'count': posts.count()
    }
    return render(request, 'post/sell.html', context)

def ajax_sell(request):
    page = int(request.GET.get('offset', 8))
    category = request.GET.get('category', "")
    print(category)
    if page == 8:
        page_min = 0
    else:
        page_min = page - 4
    if category:
        posts = Post.objects.filter(category=category)[page_min:page]
    else:
        posts = Post.objects.all()[page_min:page]
    json_list = []
    for post in posts:
        json_list.append({'title': post.category, 'photo': post.image_1.url, 'pk': post.pk})

    data = json.dumps(json_list)
    return HttpResponse(data, content_type='application/json')