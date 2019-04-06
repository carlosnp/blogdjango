# Django
from rest_framework.generics import ListAPIView
# Project
from posts.models import Post
from .serializers import PostSerializers

class PostListAPIView(ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializers
