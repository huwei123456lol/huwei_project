from django.urls import path
from index import views


urlpatterns = [
    path('test', views.test2, name="test2"),
    path('', views.test, name='test'),
]