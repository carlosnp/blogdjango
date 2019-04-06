# -*- coding: utf-8 -*-
from django.urls import path

from posts.api.views import PostListAPIView


app_name = "posts_api"

urlpatterns = [
    path('', PostListAPIView.as_view(), name="list"),
    # path('create/', posts_create, name="create"),
    # path('<int:id>/', posts_detail, name="detail"),
    # path('<int:id>/edit/', posts_update, name="update"),
    # path('<int:id>/delete/', posts_delete, name="delete"),
]