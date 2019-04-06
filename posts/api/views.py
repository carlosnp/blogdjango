# Django
from rest_framework.generics import ListAPIView, RetrieveAPIView
# Project
from posts.models import Post
from .serializers import PostListSerializers, PostDetailSerializers

# Lista de post
class PostListAPIView(ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializers

# Detalles del post
class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializers
	#lookup_field = 'slug'
	#lookup_url_kwarg = 'abc'
