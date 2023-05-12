

# 项目3 Web应用程序

## 一 Django入门

### 1 创建项目

```bash
django-admin.exe startproject learning_log .
```

### 2 创建数据库

```bash
python manage.py migrate
```
### 3 运行项目
```
python manage.py runserver
```

![image-20230512144825457](README.assets/image-20230512144825457.png)



### 4 创建应用程序

```bash
python manage.py startapp learning_logs
```

### 5 定义模型

```python
# model.py
from django.contrib.auth.models import User
from django.db import models

class Topic(models.Model):
    """主题"""
    text = models.CharField(max_length=200)  # 由字符或文本组成的数据
    date_added = models.DateTimeField(auto_now_add=True)  # 记录日期和时间的数据

    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # 外键参考User

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text
    
    
class Entry(models.Model):
    """条目"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # 外键参考Topic

    text = models.TextField()  # TextField实例
    date_added = models.DateTimeField(auto_now_add=True)

    # Meta存储用于管理模型的额外信息
    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text[:50] + "..."
```

### 6 激活模型

```python
# settings.py
INSTALLED_APPS = [

    # 我的应用程序
    'learning_logs',
        
    # --skip--
]
```

```bash
python manage.py makemigrations learning_logs
python manage.py migrate
```

### 7 Django管理网站

#### 1. 创建超级用户

```bash
python manage.py createsuperuser
```

> ll_admin admin

#### 2. 向管理网站注册模型

```python
# admin.py
from learning_logs.models import Topic, Entry

from learning_logs.models import Topic
admin.site.register(Topic)
```

#### 3. 添加主题

### 8 Django shell

```python
from learning_logs.models import Topic
Topic.objects.all()
```

## 二 创建网页：学习笔记主页

### 1 映射URL

```python
"""定义learning_log的URL模式"""

# urls.py 定义learning_log的URL模式

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path(r'', include('learning_logs.urls', namespace='learning_logs')),
]
```

#### 1 URL模式

```python
"""定义learning_logs的URL模式"""

# urls.py learning_logs

from django.conf.urls import url
from . import views

app_name = "learning_logs"

urlpatterns = [
    # 主页
    url(r'^$', views.index, name='index'),
]
```

#### 2 编写视图

```python
# view.py
from django.shortcuts import render

# Create your views here.
from learning_logs.models import Topic


def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')
```

### 2 模板继承

#### 1. 父模板

```html
<!--base.html-->
<body>
<p>
    <a href="{% url 'learning_logs:index' %}">诗文记录</a>
</p>

{% block content %}
    
{% endblock content %}
</body>
```

#### 2. 子模板
```html
<!--index.html-->
<body>

{% extends "learning_logs/base.html" %}

{% block content %}
<p>诗文学习记录可以帮助跟踪的学习情况。</p>
{% endblock content %}

</body>
```

### 3 显示所有主题的页面

#### 1 URL模式

```python
"""定义learning_logs的URL模式"""

# urls.py learning_logs

from django.conf.urls import url
from . import views

app_name = "learning_logs"

urlpatterns = [
	# --skip--
    

    # 显示所有的主题
    url(r'^topics/$', views.topics, name='topics'),
]
```
#### 2 视图

```python
# view.py

from django.shortcuts import render

# Create your views here.
from learning_logs.models import Topic


# --skip--


def topics(request):
    """显示所有的主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)
```

#### 3 模板

```html
<!--topics.html-->
<body>
    
{% extends "learning_logs/base.html" %}

{% block content %}
<p>主题</p>

<ul>
    {% for topic in topics %}
    <li><a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a></li>
    {% empty %}
    <li>No topics have been added yet.</li>
{% endfor %}
</ul>

{% endblock content %}
</body>
```

#### 4 修改base.html

```HTML
<!--base.html-->
<body>
<p>
    <a href="{% url 'learning_logs:index' %}">诗文记录</a>
    <a href="{% url 'learning_logs:topics' %}">主题</a>
</p>

{% block content %}

{% endblock content %}
```

### 4 显示特定主题的页面
#### 1 URL模式

```python
"""定义learning_logs的URL模式"""

# urls.py learning_logs

from django.conf.urls import url
from . import views

app_name = "learning_logs"

urlpatterns = [
    # --skip--

    
    # 特定主题的详细页面
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
]

```

#### 2 视图

```python
# view.py
from django.shortcuts import render

# Create your views here.
from learning_logs.models import Topic


# --skip--


def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
```

#### 3 模板

```html
<!--topic.html-->

<body>
    
{% extends "learning_logs/base.html" %}
    
<p>条目</p>
    
{% block content %}
<ul>
    {% for entry in entries %}
    <li>
        <p>{{ entry.date_added|date:'M d, Y H:i' }}</p>
        <p>{{ entry.text|linebreaks }}</p>
    </li>
    {% empty %}
    <li>
        There are no entries for this topic yet.
    </li>
    {% endfor %}
</ul>
{% endblock content %}
</body>
```

#### 4 修改topics.html

```html
<!--topics.html-->

<body>

{% extends "learning_logs/base.html" %}

{% block content %}
    
<p>主题</p>

<ul>
    {% for topic in topics %}
    <li><a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a></li>
    {% empty %}
    <li>No topics have been added yet.</li>
{% endfor %}
</ul>

{% endblock content %}
</body>
```

## 三 用户账户

### 1 添加新主题

#### 1 用于添加主题的表单

```python
# form.py

from django import forms
from .models import Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
```

#### 2 URL模式

```python
"""定义learning_logs的URL模式"""

# urls.py learning_logs

from django.conf.urls import url
from . import views

app_name = "learning_logs"

urlpatterns = [
    # --skip--
    
    
    # 用于添加新主题的网页
	url(r'^new_topic/$', views.new_topic, name='new_topic'),
]
```

#### 3 视图

```python
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from learning_logs.forms import TopicForm
from learning_logs.models import Topic


# --skip--


def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据,对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
```

#### 4 模板

```html
<!--new_topic.html-->

<body>
{% extends "learning_logs/base.html" %}

{% block content %}
    <form action="{% url 'learning_logs:new_topic' %}" method='post'>
    {% csrf_token %}
    {{ form.as_p }}
    <button name="submit">add topic</button>
    </form>
{% endblock content %}

</body>
```

#### 5 链接到页面topics.html

```html
<!--topics.html-->

<body>

{% extends "learning_logs/base.html" %}

{% block content %}
    <p>主题</p>

    <ul>
        {% for topic in topics %}
        <li><a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a></li>
        {% empty %}
        <li>No topics have been added yet.</li>
        {% endfor %}

    </ul>
    <a href="{% url 'learning_logs:new_topic' %}">Add a new topic:</a>

{% endblock content %}
</body>
```

### 2 添加新条目

#### 1 用于添加条目的表单

```python
# form.py

from django import forms
from .models import Topic, Entry


# --skip--


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
```
#### 2 URL模式

```python
"""定义learning_logs的URL模式"""

# urls.py learning_logs

from django.conf.urls import url
from . import views

app_name = "learning_logs"

urlpatterns = [
    # --skip--
    
    
    # 用于添加新条目的页面
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
]
```

#### 3 视图
```python
# view.py
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from learning_logs.forms import TopicForm
from learning_logs.models import Topic


# --skip--

    
def new_entry(request,topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # 未提交数据,创建一个空表单
        form = EntryForm()
    else:
        # POST提交的数据,对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
        new_entry = form.save(commit=False)
        new_entry.topic = topic
        new_entry.save()
        return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)
```

#### 4 模板

```html
<!--new_entry.html-->

<body>
{% extends "learning_logs/base.html" %}

{% block content %}
    <p>添加条目</p>
    <p><a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a></p>
    <form action="{% url 'learning_logs:new_entry' topic.id %}" method='post'>
        {% csrf_token %}
        {{ form.as_p }}
        <button name='submit'>add entry</button>
    </form>

{% endblock content %}
</body>
```

#### 5 链接到页面topic.html

```html
<!--topic.html-->

<body>

{% extends "learning_logs/base.html" %}

{% block content %}
    <p>条目</p>
<ul>
    {% for entry in entries %}
    <li>
        <p>{{ entry.date_added|date:'M d, Y H:i' }}</p>
        <p>{{ entry.text|linebreaks }}</p>
    </li>
    {% empty %}
    <li>
        There are no entries for this topic yet.
    </li>
    {% endfor %}
</ul>
    <p>
<a href="{% url 'learning_logs:new_entry' topic.id %}">add new entry</a>
</p>
{% endblock content %}
</body>
```

### 3 编辑条目

#### 1 URL模式

```python
"""定义learning_logs的URL模式"""

# urls.py learning_logs

from django.conf.urls import url
from . import views

app_name = "learning_logs"

urlpatterns = [
    # --skip--
    
    
    # 用于编辑条目的页面
	url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry,name='edit_entry'),
]
```

#### 2 视图

```python
# view.py
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from learning_logs.forms import TopicForm
from learning_logs.models import Topic


# --skip--

    
def edit_entry(request, entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
```

#### 3 模板

```html
<!--edit_entry.html-->

<body>
{% extends "learning_logs/base.html" %}

{% block content %}

    <p><a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a></p>
    <p>修改条目</p>


    <form action="{% url 'learning_logs:edit_entry' entry.id %}" method='post'>
    {% csrf_token %}
    {{ form.as_p }}
    <button name="submit">save changes</button>
    </form>
{% endblock content %}

</body>
```

#### 4 链接到页面topic.html

```html
<!--topic.html-->

<body>

{% extends "learning_logs/base.html" %}

{% block content %}
    <p>条目</p>
<ul>
    {% for entry in entries %}
    <li>
        <p>{{ entry.date_added|date:'M d, Y H:i' }}</p>
        <p>{{ entry.text|linebreaks }}</p>
    <p>
        <a href="{% url 'learning_logs:edit_entry' entry.id %}">修改条目</a>
    </p>
    </li>
    {% empty %}
    <li>
        There are no entries for this topic yet.
    </li>
    {% endfor %}
</ul>
    <p>
<a href="{% url 'learning_logs:new_entry' topic.id %}">add new entry</a>
</p>
{% endblock content %}
```

