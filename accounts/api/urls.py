#-*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.urls import path

from .views import UserCreateApyView

app_name = "accounts_api"

urlpatterns = [
    #path('login', loginView, name="login"),
    #path('logout/', logoutView, name="logout"),
    path('register/', UserCreateApyView.as_view(), name="register"),
]