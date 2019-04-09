#-*- coding: utf-8 -*-
from django.urls import path

from .views import CommentListAPIView, CommentCreateAPIView, CommentDetailAPIView

app_name = "comments_api"

urlpatterns = [
    path('', CommentListAPIView.as_view(), name="list"),
    path('create/', CommentCreateAPIView.as_view(), name="create"),
    path('<int:pk>/', CommentDetailAPIView.as_view(), name="detail"),
    #path('<int:id>/delete/', comment_delete, name="delete"),
]