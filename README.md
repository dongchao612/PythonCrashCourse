# PythonCrashCourse
Python编程 从入门到实践
## Part1基础知识

## Part2 项目
- 项目1 外星人入侵
- 项目2 数据可视化
- 项目3 Web应用程序

### 项目1 外星人入侵
### 项目2 数据可视化
### 项目3 Web应用程序
#### ch 18 Django入门
##### 18.1 建立项目
###### 18.1.2 建立虚拟环境
###### 18.1.5 安装Django
```bash
pip install Django
```
###### 18.1.6 在Django 中创建项目
```bash
django-admin.py startproject learning_log .
```
> 千万别忘了这个句点，否则部署应用程序时将遭遇一些配置问题

###### 18.1.7 创建数据库
```bash
python manage.py migrate
```
###### 18.1.8 查看项目
```bash
python manage.py runserver
```
##### 18.2 创建应用程序
```bash
python manage.py startapp learning_logs
```
看到其中新增了一个文件夹learning_logs,最重要的文件是models.py、admin.py和views.py。我们将使用models.py来定义我们
要在应用程序中管理的数据

###### 18.2.1 定义模型

```python
# models.py
class Topic(models.Model):
    """用户学习的主题"""
    text = models.CharField(max_length=200)  # 由字符或文本组成的数据
    date_added = models.DateTimeField(auto_now_add=True)  # 记录日期和时间的数据

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text
```
###### 18.2.2 激活模型
打开settings.py,将INSTALLED_APPS修改，将前面的应用程序添加到这个元组中
```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 我的应用程序
    'learning_logs',
]
```
```bash
python manage.py makemigrations learning_logs
```
需要让Django修改数据库，使其能够存储与模型Topic相关的信息

```bash
python manage.py makemigrations learning_logs
```
命令makemigrations让Django确定该如何修改数据库，使其能够存储与我们定义的新模型相关联的数据。

下面来应用这种迁移，让Django替我们修改数据库

```bash
python manage.py migrate
```
每当需要修改“学习笔记”管理的数据时，都采取如下三个步骤：修改models.py；对learning_logs调用makemigrations；让Django迁移项目。

###### 18.2.3 Django 管理网站
1.创建超级用户

```bash
python manage.py createsuperuser
```
> admin admin123
>
删除管理员
```python
from django.contrib.auth.models import User	# 引入管理员存放的数据库
user = User.objects.filter()	# 查找该数据库里有哪些用户
print(user)  # 列出用户名 <QuerySet [<User: admin>]> 
User.objects.get(username="admin", is_superuser=True).delete()
```

2.向管理网站注册模型

我们创建应用程序learning_logs时，Django在models.py所在的目录中创建了一个名为admin.py的文件：

```python
# admin.py
from learning_logs.models import Topic
admin.site.register(Topic)
```

3.添加主题

向管理网站注册Topic后，我们来添加第一个主题。为此，单击Topics进入主题网页，它几乎
是空的，这是因为我们还没有添加任何主题。单击Add，你将看到一个用于添加新主题的表单。
，在第一个方框中输入Chess再单击Save，这将返回到主题管理页面，其中包含刚创建的主题。
下面再创建一个主题，以便有更多的数据可供使用。再次单击Add，并创建另一个主题Rock
Climbing。当你单击Save时，将重新回到主题管理页面，其中包含主题Chess和Rock Climbing

###### 18.2.4 定义模型Entry

```python
# models.py
class Entry(models.Model):
    """学到的有关某个主题的具体知识"""
    topic = models.ForeignKey(Topic)  # ForeignKey实例
    text = models.TextField()# TextField实例
    date_added = models.DateTimeField(auto_now_add=True)
    
    # Meta存储用于管理模型的额外信息
    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text[:50] + "..."
```
###### 18.2.5 迁移模型Entry
```bash
python manage.py makemigrations learning_logs

python manage.py migrate
```
###### 18.2.6 向管理网站注册Entry

```python
# admin.py
from learning_logs.models import Topic, Entry
admin.site.register(Entry)
```
看到learning_logs下列出了Entries。单击Entries的Add链接，或者单击Entries再选择Add entry将看到一个下拉列表，能够选择要为哪个主
题创建条目，还有一个用于输入条目的文本框。从下拉列表中选择Chess，并添加一个条目。

###### 18.2.7 Django shell
输入一些数据后，就可通过交互式终端会话以编程方式查看这些数据了。这种交互式环境称为Django shell，是测试项目和排除其故障的理想之地

##### 18.3 创建网页：学习笔记主页
###### 18.3.1 映射URL
打开项目主文件夹learning_log中的文件urls.py，你将看到如下代码：
```python
# urls.py
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('learning_logs.urls', namespace='learning_logs')),
]
```
默认的urls.py包含在文件夹learning_log中，现在我们需要在文件夹learning_logs中创建另一个urls.py文件：

###### 18.3.2 编写视图
learning_logs中的文件views.py是你执行命令python manage.py startapp时自动生成的，当前其内容如下：
```python
# views.py
from django.shortcuts import render


# Create your views here.
def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')
```
#####  18.4 创建其他网页
###### 18.4.1 模板继承
1. 父模板
我们首先来创建一个名为base.html的模板，并将其存储在index.html所在的目录中。这个文件包含所有页面都有的元素；其他的模板都继承base.html。
```html
 <!-- base.html -->
<p>
    <a href="{% url 'learning_logs:index' %}">Learning Log</a>
    <!-- 生成一个URL，该URL与learning_logs/urls.py中定义的名为index的URL模式匹配  -->
</p>

{% block content %} {% endblock content %}

<!--插入了一对块标签。这个块名为content，是一个占位符，其中包含的信息将由子模板指定。-->
</body>
```
2.子模板
```html
<body>

{% extends "learning_logs/base.html" %}
<!--标题Learning Log替换成了从父模板那里继承的代码-->

{% block content %}

    <p>Learning Log helps you keep track of your learning, for any topic you're learning about.</p>

{% endblock content %}

</body>
```
###### 18.4.2 显示所有主题的页面
1.URL模式
首先，我们来定义显示所有主题的页面的URL。通常，使用一个简单的URL片段来指出网页显示的信息
```python
# urls.py
urlpatterns = [
    # 主页
    url(r'^$', views.index, name='index'),

    # 显示所有的主题
    url(r'^topics/$', views.topics, name='topics'),
]
```
2.视图
函数topics()需要从数据库中获取一些数据，并将其发送给模板。

```python
# views.py
def topics(request):
    """显示所有的主题"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)
```
3.模板
显示所有主题的页面的模板接受字典context，以便能够使用topics()提供的数据。
```html
<body>
{% extends "learning_logs/base.html" %}

{% block content %}
<p>Topics</p>
<ul>
    {% for topic in topics %}
    <li>{{ topic }}</li>
    {% empty %}
    <li>No topics have been added yet.</li>
    {% endfor %}
</ul>
{% endblock content %}
</body>
```
现在需要修改父模板，使其包含到显示所有主题的页面的链接：
```html
<!--base.html -->
<p>
    <a href="{% url 'learning_logs:index' %}">Learning Log</a>
    <a href="{% url 'learning_logs:topics' %}">Topics</a>
    <!-- 生成一个URL，该URL与learning_logs/urls.py中定义的名为index的URL模式匹配  -->
</p>
```
###### 18.4.3 显示特定主题的页面
1.URL模式
显示特定主题的页面的URL模式与前面的所有URL模式都稍有不同，因为它将使用主题的id属性来指出请求的是哪个主题
```python
# urls.py
urlpatterns = [
    # 主页
    url(r'^$', views.index, name='index'),

    # 显示所有的主题
    url(r'^topics/$', views.topics, name='topics'),

    # 特定主题的详细页面
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),

]
```
2.视图
```python
# views.py
def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
```
3.模板