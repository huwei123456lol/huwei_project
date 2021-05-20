from django.contrib import admin
from index.models import  Author, UserInfo, Book
# Register your models here.
admin.site.register([Author, UserInfo, Book]),
