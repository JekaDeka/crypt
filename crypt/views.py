from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
import json


def main_page(request):
    tmpl_vars = {
        'all_posts': Post.objects.reverse(),
        'post_form': PostForm(prefix="post"),
        'decrypt_form': PostForm(prefix="decrypt")
    }
    return render(request, 'crypt/index.html', tmpl_vars)


def history_page(request):
    tmpl_vars = {
        'all_posts': Post.objects.reverse(),
        'form': PostForm()
    }
    return render(request, 'crypt/history.html', tmpl_vars)


def create_post(request, pk):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}

        post = Post(text=post_text, crypted_type=int(pk))
        post.save()

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.pk
        response_data['text'] = post.text
        # response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
        response_data['type'] = post.crypted_type
        response_data['key'] = post.key
        response_data['crypted_text'] = post.crypted_text

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def decrypt_post(request, pk):
    if request.method == 'POST':
        crypted_text = request.POST.get('the_post')
        response_data = {}

        post = Post.objects.filter(crypted_text=crypted_text)
        if post:
            post = post[0]
            response_data['text'] = post.text
            response_data['privkey'] = post.privkey

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
