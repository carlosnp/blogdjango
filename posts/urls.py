# -*- coding: utf-8 -*-
from django.urls import path

from .views import posts_list, posts_list_user, posts_create, posts_detail, posts_update, posts_delete

app_name = "posts"

urlpatterns = [
    path('', posts_list, name="list"),
    path('user_post/', posts_list_user, name="list_user"),
    path('create/', posts_create, name="create"),
    path('<int:id>/', posts_detail, name="detail"),
    path('<int:id>/edit/', posts_update, name="update"),
    path('<int:id>/delete/', posts_delete, name="delete"),
]