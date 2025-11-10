
# ------------------------------
# README.md 简短说明
# ------------------------------
"""
项目骨架说明：
1. 在项目根目录创建虚拟环境并激活
2. pip install -r requirements.txt
3. python manage.py migrate
4. python manage.py createsuperuser
5. python manage.py runserver

模块：accounts, blog, comments
"""

#用户名：admin
#密码：ceshi111


PythonClassProject/                       <-- Django 项目根目录
│
├── manage.py                     <-- Django 管理命令
├── db.sqlite3                     <-- SQLite 数据库（开发用）
├── requirements.txt               <-- 项目依赖包列表
├── static/                        <-- 静态资源（前端组员D）
│   ├── css/
│   │   └── main.css               <-- 全局样式
│   └── js/
│       ├── like.js                <-- 点赞功能 JS
│       └── comment.js             <-- 评论功能 JS
│
├── templates/                     <-- 全局模板
│   ├── base.html                  <-- 基础模板（前端组员D）
│   ├── accounts/                  <-- 用户模块模板（组员A）
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile_edit.html
│   └── blog/                      <-- 博客模块模板（组员B + 交互组C）
│       ├── post_list.html
│       ├── post_detail.html
│       └── post_form.html         <-- 新建/编辑文章
│
├── myproject/                     <-- Django 配置目录（队长）
│   ├── __init__.py
│   ├── settings.py                <-- 项目配置（数据库、静态、模板）
│   ├── urls.py                    <-- 总路由，包含 accounts、blog、comments
│   └── wsgi.py
│
├── accounts/                      <-- 用户模块（组员A）
│   ├── __init__.py
│   ├── models.py                  <-- Profile 模型
│   ├── views.py                   <-- login, logout, register, profile_edit
│   ├── urls.py                    <-- 登录、注册、登出路由
│   └── admin.py
│
├── blog/                          <-- 博客模块（组员B）
│   ├── __init__.py
│   ├── models.py                  <-- Post 模型
│   ├── views.py                   <-- post_list, post_detail, post_create
│   ├── urls.py                    <-- 博客路由
│   └── admin.py
│
└── comments/                      <-- 评论模块（组员C）
    ├── __init__.py
    ├── models.py                  <-- Comment 模型
    ├── views.py                   <-- 评论处理视图
    ├── urls.py                    <-- 评论相关路由
    └── admin.py

