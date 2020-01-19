from django.contrib import admin

# Register your models here.
from .models import Item  #모든 모델을 불러옵니다.

admin.site.register(Item) #이거 추가