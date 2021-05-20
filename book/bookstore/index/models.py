from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name="书名")
    public = models.CharField(max_length=50, verbose_name="出版社")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="定价")
    def default_price(self):
        return "$30"
    retail_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="零售价", default=default_price)
    def __str__(self):
        return 'title:%s , public:%s, price:%s, retail_price:%s' % (self.title, self.public, self.price, self.retail_price)

class Author(models.Model):
    name = models.CharField(max_length=30, verbose_name="姓名")
    email = models.EmailField(verbose_name="邮箱")
    def __str__(self):
        return 'name:%s ' % self.name
class UserInfo(models.Model):
    username = models.CharField(max_length=24, verbose_name="用户名")
    password = models.CharField(max_length=24, verbose_name="密码")
    choices = (
        ('male', '男性'),
        ('female', '女性'),
    )
    gender = models.CharField(max_length=8, choices=choices, default='male', verbose_name="性别")
    def __str__(self):
        return 'username:%s' % self.username
