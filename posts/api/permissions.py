# Django
from rest_framework.permissions import (BasePermission)
# Project

# Si es el Dueño
class IsOwnerOrReadOnly(BasePermission):
	message = 'No Tienes los permisos necesarios para modificar o eliminar un Post de otro usuario'

	def has_object_permission(self, request, view, obj):
		return obj.author == request.user