# blog/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import Post  # 绝对导入，避免相对导入问题

User = get_user_model()

class PostCreateLoginRequiredTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')

    def test_create_requires_login(self):
        url = reverse('post_create')
        response = self.client.get(url)
        # 未登录应该重定向到登录页（默认 status_code 302）
        self.assertEqual(response.status_code, 302)

class SlugUniquenessTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user2', password='pass')
        self.client.login(username='user2', password='pass')

    def test_slug_uniqueness_created(self):
        url = reverse('post_create')
        data1 = {'title': '同名标题', 'content': '内容1'}
        r1 = self.client.post(url, data1, follow=True)
        self.assertEqual(Post.objects.count(), 1)
        post1 = Post.objects.first()
        self.assertTrue(post1.slug)

        data2 = {'title': '同名标题', 'content': '内容2'}
        r2 = self.client.post(url, data2, follow=True)
        self.assertEqual(Post.objects.count(), 2)
        slugs = set(Post.objects.values_list('slug', flat=True))
        self.assertEqual(len(slugs), 2)  # 两个 slug 不相同
