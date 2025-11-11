# accounts/apps.py

from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # 我们把“疗伤”逻辑加在这里
    def ready(self):
        """
        这个方法会在 Django 应用启动并准备就绪后自动运行。
        """
        # 把 import 放在这里，避免应用启动时出现问题
        from django.contrib.auth import get_user_model
        from .models import Profile

        User = get_user_model()
        
        # 找出所有还没有 Profile 的用户
        # 我们用 try...except 包裹，防止在早期迁移（Profile表还不存在时）出错
        try:
            users_without_profile = User.objects.filter(profile__isnull=True)
            
            # 为他们批量创建 Profile
            profiles_to_create = [
                Profile(user=user) for user in users_without_profile
            ]
            
            if profiles_to_create:
                Profile.objects.bulk_create(profiles_to_create)
                print(f"\n[Accounts App Ready] 为 {len(profiles_to_create)} 个用户成功创建了缺失的 Profile。")
        except Exception as e:
            # 在数据库还没准备好时，可能会报错，我们忽略它
            print(f"[Accounts App Ready] 检查 Profile 时出现临时错误: {e}")

