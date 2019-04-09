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
from comments.models import Comment
from .serializers import (CommentListSerializers, CommentDetailSerializers, 
						  create_commnet_serializers)
from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination

# Lista de Comentarios
class CommentListAPIView(ListAPIView):
	serializer_class = CommentListSerializers
	# Filtros
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('author__username', 'author__first_name', 'author__last_name', 'content')
	ordering_fields = ('content')
	# Paginación
	pagination_class = PostPageNumberPagination

	def get_queryset(self, *args, **kwargs):
		queryset_list = Comment.objects.all()
		# queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)

		# Buscar en la lista de POST
		query = self.request.GET.get("q")
		if query:
			# Filtro de busqueda
			queryset_list = queryset_list.filter(
				Q(content__icontains=query) |
				Q(author__first_name__icontains=query) |
				Q(author__last_name__icontains=query) |
				Q(author__username__icontains=query)
				).distinct()
		return queryset_list

# Create comentarios
class CommentCreateAPIView(CreateAPIView):
	queryset = Comment.objects.all()
	# serializer_class = CommentDetailSerializers
	permission_classes = (IsAuthenticated,)

	def get_serializer_class(self):
		model_type 	= self.request.GET.get("type")
		slug 		= self.request.GET.get("slug")
		parent_id 	= self.request.GET.get("parent_id", None)
		return create_commnet_serializers(model_type=model_type, 
										  slug=slug, 
										  parent_id=parent_id, 
										  author=self.request.user
										  )

	# Se coloca de autor al usuario que inicie sesion
	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

# Retrieve Comment
class CommentDetailAPIView(RetrieveAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentDetailSerializers