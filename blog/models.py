# blog/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
import itertools
from django.utils import timezone

User = get_user_model()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def _generate_unique_slug(self, base):
        slug_candidate = slugify(base)[:200]
        if not slug_candidate:
            slug_candidate = slugify(str(self.title)) or 'post'
        original = slug_candidate
        for i in itertools.count(1):
            if not Post.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                return slug_candidate
            slug_candidate = f"{original}-{i}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug(self.title)
        else:
            self.slug = slugify(self.slug)[:255]
            if Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = self._generate_unique_slug(self.slug)

        # 创建时自动设置 published_date
        if self.published and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)
