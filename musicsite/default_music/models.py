from django.db import models
import time

# Create your models here.


class Repeat(models.Model):
    repeat_name = models.CharField(max_length=10)  # 回复人名
    repeat_article = models.TextField()

    def __str__(self):
        return self.repeat_name


class Suggestion(models.Model):
    suggestion_title = models.CharField(max_length=20)
    suggestion_article = models.TextField()
    suggestion_author = models.CharField(max_length=20)
    suggestion_time = models.DateTimeField()  # 帖子发布时间
    suggestion_repeat = models.ForeignKey(Repeat, on_delete=models.CASCADE)
    def __str__(self):
        return self.suggestion_title


class Author(models.Model):
    author_name = models.CharField(max_length=50)
    author_birth = models.DateField(default=time.strftime('%Y-%m-%d'))  # 作者的出生日期
    author_dead_time = models.DateField(default=time.strftime('%Y-%m-%d'))  # 作者死亡时间，如果没有就不填
    author_major_exp = models.TextField(default="")  # 作者的生平事迹 或主要事迹
    author_bei_zhu = models.CharField(max_length=40, default="")

    def __str__(self):
        return self.author_name


class DefaultMusic(models.Model):
    music_name = models.CharField(max_length=50, unique=True)
    music_ge_chi = models.TextField()
    music_bei_zhu = models.TextField(default="")
    #last_time = models.DateTimeField(default='2000-10-1')  # 最近的更新内容时间
    bo_fang_liang = models.IntegerField(default=0)  # 播放量
    #suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    music_author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.music_name

class Ge_dan_list(models.Model):
    ge_dan_name = models.CharField(max_length=20)
    number = models.IntegerField(default=0)
    music = models.ForeignKey(DefaultMusic, on_delete=models.CASCADE)
    def __str__(self):
        return self.ge_dan_name
