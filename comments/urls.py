
# ------------------------------
# comments/urls.py
# ------------------------------
from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('post/<slug:slug>/like/', views.toggle_like, name='toggle_like'),
    path('delete/<int:id>/', views.delete_comment, name='delete_comment'),  # 新增
]
