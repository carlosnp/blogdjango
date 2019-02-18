from django.urls import path

from .views import posts_list, posts_create, posts_detail, posts_update, posts_delete

urlpatterns = [
    path('', posts_list, name="post_list"),
    path('create/', posts_create, name="post_create"),
    path('detail/', posts_detail, name="post_detail"),
    path('update/', posts_update, name="post_update"),
    path('delete/', posts_delete, name="post_delete"),
]