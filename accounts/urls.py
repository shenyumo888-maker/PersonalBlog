from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # 注册
    path('register/', views.register_view, name='register'),

    # 使用 Django 内置的登录和登出视图
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # 这是新代码
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logged_out.html'), name='logout'),
    # 个人资料编辑
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),

    # 个人主页
    path('user/<str:username>/', views.user_profile_view, name='user_profile'),
]