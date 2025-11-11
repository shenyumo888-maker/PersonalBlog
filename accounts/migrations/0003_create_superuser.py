# accounts/migrations/0003_create_superuser.py

from django.db import migrations
import os

def create_superuser(apps, schema_editor):
    """
    创建一个超级管理员用户，并确保为其创建关联的 Profile。
    """
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('accounts', 'Profile') # <--- 1. 获取 Profile 模型

    USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'a_default_complex_password')

    if User.objects.filter(username=USERNAME).exists():
        print(f"用户 '{USERNAME}' 已存在，跳过创建。")
        # 检查这个已存在的用户是否有 profile，如果没有，则补上
        user = User.objects.get(username=USERNAME)
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)
            print(f"为已存在的用户 '{USERNAME}' 补上了 Profile。")
        return

    # 2. 创建用户，并把新创建的用户对象存到变量 new_user 中
    new_user = User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print(f"超级用户 '{USERNAME}' 创建成功。")
    
    # 3. 立刻为这个新用户创建一个 Profile
    Profile.objects.create(user=new_user)
    print(f"为新用户 '{USERNAME}' 创建 Profile 成功。")


class Migration(migrations.Migration):
    # ... dependencies 和 operations 保持不变 ...
    dependencies = [
        # 确保这里的依赖文件名是你项目里那个0002文件的真实名字
        ('accounts', '0002_alter_profile_avatar_alter_profile_bio_and_more'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'), # 依赖于上一个迁移文件
        ('accounts', '0002_alter_profile_avatar_alter_profile_bio_and_more'), # <--- 把这一行加进去！
    ]

    operations = [
        migrations.RunPython(create_superuser),

    ]


