# Django
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
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

# Retrieve post
class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializers
	#lookup_field = 'slug'
	#lookup_url_kwarg = 'abc'

# Update post
class PostUpdateAPIView(UpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializers
	#lookup_field = 'slug'

# Destroy post
class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializers
	#lookup_field = 'slug'