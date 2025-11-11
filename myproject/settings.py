# ------------------------------
# myproject/settings.py
# (已为 Render.com 部署优化)
# ------------------------------
import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 生产环境核心配置 ---
# 从环境变量中获取 SECRET_KEY。如果找不到，则使用一个不安全的默认值（仅用于本地开发）。
# 在 Render 上，你必须设置 SECRET_KEY 环境变量！
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-insecure-key-for-dev')

# DEBUG 模式默认为 False。只有当环境变量 DEBUG=True 时才开启。
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# 设置允许访问的域名
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
# 如果你还有自己的域名，可以添加到这里
# ALLOWED_HOSTS.append('www.yourdomain.com')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 项目 apps
    'accounts.apps.AccountsConfig',
    'blog',
    'comments',
    'widget_tweaks', # <--- 把这行加在最后
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise 中间件，用于处理静态文件，必须放在 SecurityMiddleware 下面
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# --- 数据库配置 ---
# 使用 dj-database-url 自动配置数据库
# 它会读取 Render 提供的 DATABASE_URL 环境变量。
# 如果找不到该变量（例如在本地开发时），则回退到使用 SQLite。
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600 # 保持数据库长连接，提升性能
    )
}


# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [] # 为简化，保持为空


# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True


# --- 静态文件 (Static files) 和媒体文件 (Media files) 配置 ---

# 访问静态文件的 URL
STATIC_URL = '/static/'
# 本地开发时，Django 寻找静态文件的额外目录
STATICFILES_DIRS = [BASE_DIR / 'static']
# 运行 `collectstatic` 时，所有静态文件将被收集到这个目录
STATIC_ROOT = BASE_DIR / 'staticfiles'
# 使用 WhiteNoise 优化静态文件存储，支持压缩和缓存
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 媒体文件 (用户上传的文件)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- 认证和重定向 ---
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
