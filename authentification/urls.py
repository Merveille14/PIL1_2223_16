from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout"),
    path('forgot-password', views.forgot_password, name="password.forgot"),
    path('new-password/<str:token>', views.new_password, name="password.new"),
]
