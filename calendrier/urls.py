from django.urls import path
from .import views 

urlpatterns = [
    path('',views.home,name='home'),
    path('inscription/',views.register,name='register'),
    path('inscription/login.html',views.login,name='login'),
    path('inscription/register.html',views.register,name='register'),
    path('connexion/',views.login,name='login'),
]