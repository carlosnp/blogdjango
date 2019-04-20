# Django
from django.db.models import Q
# Vistas Django Rest Framework
from rest_framework.generics import (ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, 
									RetrieveUpdateAPIView, RetrieveDestroyAPIView)
# Permisos Django Rest Framework
from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly)
# Filtros Django Rest Framework
from rest_framework.filters import (SearchFilter, OrderingFilter)
# Paginacion Django Rest Framework
from rest_framework.pagination import (LimitOffsetPagination, PageNumberPagination,)

# Project
from posts.models import Post
from .serializers import PostListSerializers, PostDetailSerializers, PostCreateUpdateSerializers
from .permissions import IsOwnerOrReadOnly
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination

# Lista de post
class PostListAPIView(ListAPIView):
	serializer_class = PostListSerializers
	# Filtros
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('author__username', 'author__first_name', 'author__last_name','title', 'content')
	ordering_fields = ('title', 'content')
	# Paginación
	pagination_class = PostPageNumberPagination
	# permission_classes = (AllowAny)

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
	# permission_classes = (AllowAny)
	
	def get_serializer_context(self):
		return {'request': self.request}

# Update post
class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializers
	#lookup_field = 'slug'
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	# permission_classes = (IsOwnerOrReadOnly)

	# Se coloca de autor al usuario que inicie sesion
	def perform_update(self, serializer):
		serializer.save(author=self.request.user)

# Destroy post
class PostDeleteAPIView(RetrieveDestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializers
	#lookup_field = 'slug'
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	# permission_classes = (IsOwnerOrReadOnly)