
# ------------------------------
# comments/views.py (简化示例)
# ------------------------------
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog.models import Post
from .models import Comment, Like
import json
from django.http import JsonResponse  # 新增导入


@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        
        # 增加一个简单的内容校验
        if not content or not content.strip():
            # 如果是 AJAX 请求，返回 JSON 错误
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': '评论内容不能为空'}, status=400)
            # 如果是普通请求，则重定向（虽然 AJAX 下基本不会触发）
            return redirect('blog:post_detail', slug=slug)

        parent = None
        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist:
                parent = None # parent_id 无效，忽略

        Comment.objects.create(post=post, user=request.user, content=content, parent=parent)

        # 检查这是否是一个 AJAX 请求
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # 如果是，返回一个 JSON 格式的成功响应
            return JsonResponse({'success': True})
    
    # 如果不是 POST 请求或 AJAX 请求，则重定向回详情页
    return redirect('blog:post_detail', slug=slug)

@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    # 验证权限：评论作者、文章作者或管理员可以删除
    if request.user == comment.user or request.user == comment.post.author or request.user.is_superuser:
        comment.delete()
    return redirect('blog:post_detail', slug=comment.post.slug)


@login_required
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        data = {
            'liked': False,
            'count': post.likes.count()
        }
    else:
        # 返回已点赞状态和最新数量
        data = {
            'liked': True,
            'count': post.likes.count()
        }
     # 如果是AJAX请求，返回JSON数据
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': created,  # created为True表示刚创建了点赞（已点赞）
            'count': post.likes.count()
        })
    return redirect('blog:post_detail', slug=slug)

