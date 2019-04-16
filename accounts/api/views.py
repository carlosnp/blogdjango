# Django
from django.db.models import Q
from django.contrib.auth import get_user_model
# Vistas Django Rest Framework
from rest_framework.generics import (ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, 
									RetrieveUpdateAPIView, RetrieveDestroyAPIView)
# Django Rest Framework Response
from rest_framework.resonse import Response
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

# View Create User
class UserLoginApyView(APIView):
	serializer_class = UserLoginSerializer
	queryset = User.objects.all()
	permission_classes = (AllowAny,)