from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   path('',views.index,name='index'),
   path('signup',views.signup,name='signup'),
   path('loginuser',views.loginuser,name='loginuser'),
   path('logoutuser',views.logoutuser,name='logoutuser'),
]