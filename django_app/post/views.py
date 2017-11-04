import json
from django.shortcuts import render,HttpResponse
from .models import Post
from time import sleep
# Create your views here.

def sell_page(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'count': posts.count()
    }
    return render(request, 'post/sell.html', context)

def ajax_sell(request):
    page = int(request.GET.get('offset',""))
    if page == 4:
        min = 0
    else:
        min = page - 4
    posts = Post.objects.all()[min:page]
    print(posts)
    print(min,posts)
    json_list = []
    for post in posts:
        json_list.append({'title': post.title, 'photo':post.image_1.url, 'pk': post.pk})

    data = json.dumps(json_list)
    return HttpResponse(data, content_type='application/json')