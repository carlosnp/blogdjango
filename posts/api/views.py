# Django
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
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

# Actualizar el post
class PostUpdateAPIView(UpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializers
	#lookup_field = 'slug'

# Eliminar el post
class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializers
	#lookup_field = 'slug'