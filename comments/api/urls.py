#-*- coding: utf-8 -*-
from django.urls import path

from .views import (CommentListAPIView, 
	                CommentCreateAPIView, 
	                CommentDetailAPIView, 
	                #CommentEditAPIView
	                )

app_name = "comments_api"

urlpatterns = [
    path('', CommentListAPIView.as_view(), name="list"), # Lista de comentarios
    path('create/', CommentCreateAPIView.as_view(), name="create"), # Crea comentarios
    path('<int:pk>/', CommentDetailAPIView.as_view(), name="detail"), # Detalles de Comentarios (Edita y elimina)
    #path('<int:pk>/edit', CommentEditAPIView.as_view(), name="edit"), # Edita los comentarios
    #path('<int:id>/delete/', comment_delete, name="delete"), # Elimina los comentarios
]