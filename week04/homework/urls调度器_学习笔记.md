# Django 如何处理一个请求
当一个用户请求 Django 站点的一个页面：
1. 如果传入 HttpRequest 对象拥有 urlconf 属性（通过中间件设置），它的值将被用来代替
ROOT_URLCONF 设置。
2. Django 加载 URLconf 模块并寻找可用的 urlpatterns，Django 依次匹配每个 URL 模式，在与
请求的 URL 匹配的第一个模式停下来。
3. 一旦有 URL 匹配成功，Djagno 导入并调用相关的视图，视图会获得如下参数：
- 一个 HttpRequest 实例
- 一个或多个位置参数提供
4. 如果没有 URL 被匹配，或者匹配过程中出现了异常，Django 会调用一个适当的错误处理视图。

# urls 调度流程
## 增加项目 urls
```python
"""
1，
网页中输入字符，如：在 http://192.168.21.223:8000/ 后面输入 books
http://192.168.21.223:8000/books
runserver手动页面请求后，会去到 MyDjango/MyDjango/urls.py 中，
找到 urlpatterns 列表，逐条查看，直到找到books目标为止
"""
# MyDjango/MyDjango/urls.py
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
path('admin/', admin.site.urls),
path('',include('index.urls')),   # 找到include，会继续往 index的urls里面去找
]
```
## 增加 index 的 urls (app名叫 index)
```python
""" 
2，来到 index.urls，会继续在 urlpatterns 列表里面匹配 books，
直到找到第一个 books，如： path('books', views.books)
然后会再往 views.books 里面找，找到 books 方法，并执行
"""
# index/urls.py
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
path('', views.index),
# 展示books页面
path('books', views.books),
]
```

## 增加 index 的 views
```python
"""
3, 在 index.views 找到 books 方法，并执行里面的代码
"""
# index/views.py
from django.shortcuts import render
from django.http import HttpResponse
# 从models取数据传给template
from .models import Name

def index(request):
    return HttpResponse("Hello Django!")

def books(request):
    # 从models 取数据传给template
    n = Name.objects.all()
    return render(request, 'bookslist.html', locals())

```


