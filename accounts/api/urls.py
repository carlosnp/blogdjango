#-*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.urls import path

from .views import UserCreateApyView, UserLoginApyView

app_name = "accounts_api"

urlpatterns = [
    path('login', UserLoginApyView.as_view(), name="login"),
    #path('logout/', logoutView, name="logout"),
    path('register/', UserCreateApyView.as_view(), name="register"),
]