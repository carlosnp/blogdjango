from django.urls import path

from .views import posts_list, posts_create, posts_detail, posts_update, posts_delete

app_name = "posts"

urlpatterns = [
    path('', posts_list, name="list"),
    path('create/', posts_create, name="create"),
    path('<int:id>/', posts_detail, name="detail"),
    path('update/', posts_update, name="update"),
    path('delete/', posts_delete, name="delete"),
]