from django.db import models

# Create your models here.

class UserInfo(models.Model):
    name = models.CharField(max_length=20, unique=True)
    sex = models.CharField(max_length=4)
    birthday = models.CharField(max_length=20)
    email = models.EmailField(default="00000@qq.com")
    phone = models.TextField(default="")
    ai_hao = models.TextField()  # 爱好
    def __str__(self):
        return self.name
class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    last_login_in = models.DateField()
    img = models.ImageField(default="")
    userInfo = models.ForeignKey(UserInfo, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.username
class Music(models.Model):
    geming = models.CharField(max_length=20, unique=True)  # 歌名
    gechi = models.TextField()  # 歌词
    author = models.CharField(max_length=10)
    beizhu = models.TextField(default="")  # 备注
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.gechi
class Music_list(models.Model):
    list_name = models.CharField(max_length=20, unique=True)  # 歌单名
    numbers = models.IntegerField()  # 数量
    bo_fang_liang = models.IntegerField(default=0)   # 播放量
    def __str__(self):
        return self.list_name
