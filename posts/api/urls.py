# -*- coding: utf-8 -*-
from django.urls import path

from posts.api.views import PostListAPIView, PostDetailAPIView, PostUpdateAPIView, PostDeleteAPIView


app_name = "posts_api"

urlpatterns = [
    path('', PostListAPIView.as_view(), name="list"),
    # path('create/', posts_create, name="create"),
    path('<int:pk>/', PostDetailAPIView.as_view(), name="detail"),
    path('<int:pk>/edit/', PostUpdateAPIView.as_view(), name="update"),
    path('<int:pk>/delete/', PostDeleteAPIView.as_view(), name="delete"),
]