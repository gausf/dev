from unicodedata import name
from django.urls import path
from . import views

urlpatterns =[
    path('hot',views.hot,name='Hot'),
    path('index',views.index,name='index')
]