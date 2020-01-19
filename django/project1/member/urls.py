from django.urls import path

from . import views

urlpatterns = [path('index', views.index, name='index'), 
               path('join', views.join, name='join'), 
               path('list', views.list, name='list'),
               path('edit', views.edit, name='edit'),
               path('login', views.login, name='login'),
               path('logout', views.logout, name='logout')
               ]


# 현재 패키지에서 views 모듈을 가져옴