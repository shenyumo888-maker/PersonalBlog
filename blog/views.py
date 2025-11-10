from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseForbidden
from django.urls import reverse
from .models import Post
from .forms import PostForm
from django.utils import timezone


def post_list(request):
    qs = Post.objects.filter(published=True)  # 只显示已发布文章
    paginator = Paginator(qs, 5)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'page_obj': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published = True                   # 自动设置为已发布
            post.published_date = timezone.now()    # 自动填充发布时间
            post.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not (request.user == post.author or request.user.is_staff):
        return HttpResponseForbidden("你没有权限编辑该文章。")
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            # 如果文章之前没有发布时间，设置为当前时间
            if not post.published_date:
                post.published_date = timezone.now()
            post.published = True   # 编辑完成后保证已发布
            post.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not (request.user == post.author or request.user.is_staff):
        return HttpResponseForbidden("你没有权限删除该文章。")
    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')
    return render(request, 'blog/post_delete_confirm.html', {'post': post})
