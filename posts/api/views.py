# Django
from django.db.models import Q
from rest_framework.generics import (ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, 
									RetrieveUpdateAPIView, RetrieveDestroyAPIView)
from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly)

# Project
from posts.models import Post
from .serializers import PostListSerializers, PostDetailSerializers, PostCreateUpdateSerializers
from .permissions import IsOwnerOrReadOnly

# Lista de post
class PostListAPIView(ListAPIView):
	serializer_class = PostListSerializers

	def get_queryset(self, *args, **kwargs):
		queryset_list = Post.objects.all()
		# queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)

		# Buscar en la lista de POST
		query = self.request.GET.get("q")
		if query:
			# Filtro de busqueda
			queryset_list = queryset_list.filter(
				Q(title__icontains=query) |
				Q(content__icontains=query) |
				Q(author__first_name__icontains=query) |
				Q(author__last_name__icontains=query) |
				Q(author__username__icontains=query)
				).distinct()
		return queryset_list


# Create post
class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializers
	#lookup_field = 'slug'
	permission_classes = (IsAuthenticated,)

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
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

	# Se coloca de autor al usuario que inicie sesion
	def perform_update(self, serializer):
		serializer.save(author=self.request.user)

# Destroy post
class PostDeleteAPIView(RetrieveDestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializers
	#lookup_field = 'slug'
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)