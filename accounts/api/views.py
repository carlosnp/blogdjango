# Django
from django.db.models import Q
from django.contrib.auth import get_user_model
# Vistas Django Rest Framework
from rest_framework.generics import (ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, 
									RetrieveUpdateAPIView, RetrieveDestroyAPIView)
# Django Rest Framework Response
from rest_framework.response import Response
# Django Rest Framework Status Codes
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
# Django Rest Framework Views
from rest_framework.views import APIView
# Permisos Django Rest Framework
from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly)
# Filtros Django Rest Framework
from rest_framework.filters import (SearchFilter, OrderingFilter)
# Paginacion Django Rest Framework
from rest_framework.pagination import (LimitOffsetPagination, PageNumberPagination,)
# Mixins
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin

# Project
from .serializers import (UserCreateSerializer, UserLoginSerializer)
from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination


# Usuario
User = get_user_model()

# View Create User
class UserCreateApyView(CreateAPIView):
	serializer_class = UserCreateSerializer
	queryset = User.objects.all()
	# permission_classes = (AllowAny,)

# View Create User
class UserLoginApyView(APIView):
	#queryset = User.objects.all()
	permission_classes = (AllowAny,)
	serializer_class = UserLoginSerializer

	def post(self, request, *args, **kwargs):
		data = request.data
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer.data
			return Response(new_data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
