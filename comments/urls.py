# -*- coding: utf-8 -*-
from django.urls import path

from .views import comment_detail

app_name = "comments"

urlpatterns = [
    path('<int:id>/', comment_detail, name="detail"),
    # path('<int:id>/delete/', comment_delete, name="delete"),
]