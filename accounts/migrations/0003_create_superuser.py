# accounts/migrations/0002_create_superuser.py

from django.db import migrations
import os # 导入 os 库来读取环境变量

def create_superuser(apps, schema_editor):
    """
    创建一个超级管理员用户。
    我们将从环境变量中读取用户名、邮箱和密码，这样更安全。
    """
    User = apps.get_model('auth', 'User')

    # 从环境变量获取管理员信息，如果找不到，则使用默认值
    # 这使得你可以在 Render 的后台安全地设置管理员密码
    USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'a_default_complex_password') # 请务必在服务器上设置这个环境变量！

    # 检查用户是否已存在
    if User.objects.filter(username=USERNAME).exists():
        print(f"用户 '{USERNAME}' 已存在，跳过创建。")
        return

    # 创建超级用户
    User.objects.create_superuser(
        username=admin,
        email=EMAIL,
        password=ceshi111
    )
    print(f"超级用户 '{USERNAME}' 创建成功。")


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'), # 依赖于上一个迁移文件
        ('accounts', '0002_alter_profile_avatar_alter_profile_bio_and_more'), # <--- 把这一行加进去！
    ]

    operations = [
        migrations.RunPython(create_superuser),

    ]
