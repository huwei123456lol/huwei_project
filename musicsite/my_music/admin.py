from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Music)
admin.site.register(models.Music_list)
admin.site.register(models.User)
admin.site.register(models.UserInfo)
