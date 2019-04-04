# -*- coding: utf-8 -*-
from django.urls import path

from .views import loginView, registerView, logoutView

app_name = "accounts"

urlpatterns = [
    path('login', loginView, name="login"),
    path('logout/', logoutView, name="logout"),
    path('register/', registerView, name="register"),
]