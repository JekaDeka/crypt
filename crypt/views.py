from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
import json


def main_page(request):
    tmpl_vars = {
        'all_posts': Post.objects.reverse(),
        'form': PostForm()
    }
    return render(request, 'crypt/index.html', tmpl_vars)


def decrypt_page(request):
    tmpl_vars = {
        'all_posts': Post.objects.reverse(),
        'form': PostForm()
    }
    return render(request, 'crypt/decrypt.html', tmpl_vars)


def history_page(request):
    tmpl_vars = {
        'all_posts': Post.objects.reverse(),
        'form': PostForm()
    }
    return render(request, 'crypt/history.html', tmpl_vars)


def create_post(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}

        post = Post(text=post_text)
        post.save()

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.pk
        response_data['text'] = post.text
        response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
