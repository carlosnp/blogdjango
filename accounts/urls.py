# -*- coding: utf-8 -*-
from django.urls import path

from .views import loginView, registerView, logoutView

app_name = "accounts"

urlpatterns = [
    path('', loginView, name="login"),
]