from django.urls import  path
from . import views
# 设置路径
urlpatterns = [
    path(r'', views.download_default_ge_ming),
    path(r'default/search', views.find_by_ge_ming),
    path(r'search', views.search_by_ge_ming),
    path(r'display', views.display_ge_ming),
    path(r'display/ge_ci', views.display_ge_ci),
    path(r'default', views.test),
    path(r'default/test', views.test_redirect),
    path(r'searchBody', views.get_ge_ming),
    path(r'temp', views.get_ge_ci),
]
