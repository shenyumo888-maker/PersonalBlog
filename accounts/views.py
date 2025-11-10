from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from blog.models import Post # 导入你的 Post 模型

def register_view(request):
    """
    处理用户注册的视图
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # 创建新用户对象，但暂时不保存到数据库
            new_user = user_form.save(commit=False)
            # 设置用户密码（进行哈希处理）
            new_user.set_password(user_form.cleaned_data['password'])
            # 保存用户对象
            new_user.save()
            messages.success(request, '注册成功！现在您可以登录了。')
            return redirect('accounts:login')
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': user_form})

@login_required
def profile_edit_view(request):
    """
    处理用户编辑个人资料的视图
    """
    if request.method == 'POST':
        # request.FILES 用于接收上传的文件数据
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '个人资料更新成功！')
            return redirect('accounts:user_profile', username=request.user.username)
        else:
            messages.error(request, '表单内容有误，请检查。')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'accounts/profile_edit.html', {'u_form': user_form, 'p_form': profile_form})

def user_profile_view(request, username):
    """
    展示用户个人主页及其发布的所有文章
    """
    # 获取指定用户，如果不存在则返回 404
    user = get_object_or_404(User, username=username)
    # 获取该用户的所有文章
    post_list = user.posts.all() # 'posts' 来自于 Post 模型中 author 字段的 related_name

    # 设置分页，每页显示 5 篇文章
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # 如果 page 参数不是整数，返回第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果 page 参数超出范围，返回最后一页
        posts = paginator.page(paginator.num_pages)
        
    context = {
        'profile_user': user,
        'page_obj': posts
    }
    return render(request, 'accounts/user_profile.html', context)