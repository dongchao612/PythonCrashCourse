from django.contrib.auth.models import User
from django.db import models


# Create your models here.
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
