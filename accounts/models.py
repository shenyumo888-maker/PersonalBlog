from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """
    用户资料模型，用于扩展 Django 内置的 User 模型
    """
    # 使用 OneToOneField 与 User 模型建立一对一的关联
    # on_delete=models.CASCADE 表示当 User 被删除时，对应的 Profile 也一并删除
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # bio 字段用于存储用户简介，允许为空
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name='个人简介')
    
    # avatar 字段用于存储用户头像
    # upload_to='avatars/' 指定上传的图片将保存在 MEDIA_ROOT/avatars/ 目录下
    # default='avatars/default.png' 是为了防止用户没有上传头像时出错，需要你提供一张默认图片
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', verbose_name='头像')

    def __str__(self):
        return f'{self.user.username} 的资料'

# 使用 Django 信号 (Signal)
# 当一个 User 对象被创建后，自动创建一个与之关联的 Profile 对象
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

