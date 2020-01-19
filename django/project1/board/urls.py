from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'), path('list', views.list, name='list'),
    path('write', views.write, name='write'), path('edit', views.edit, name='edit'),
    path('delete', views.delete, name='delete'), path('son', views.son, name='son'),
    path('content', views.content, name='content')
    ]


# 현재 패키지에서 views 모듈을 가져옴