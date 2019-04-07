# Django
from rest_framework.generics import (ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, 
									RetrieveUpdateAPIView)
# Project
from posts.models import Post
from .serializers import PostListSerializers, PostDetailSerializers, PostCreateUpdateSerializers

# Lista de post
class PostListAPIView(ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializers

# Create post
class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializers
	#lookup_field = 'slug'

	# Se coloca de autor al usuario que inicie sesion
	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

# Retrieve post
class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializers
	#lookup_field = 'slug'
	#lookup_url_kwarg = 'abc'

# Update post
class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializers
	#lookup_field = 'slug'

	# Se coloca de autor al usuario que inicie sesion
	def perform_update(self, serializer):
		serializer.save(author=self.request.user)

# Destroy post
class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializers
	#lookup_field = 'slug'