# Django
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
# Django Rest Framework
from rest_framework.serializers import (ModelSerializer, 
                                        HyperlinkedIdentityField, 
                                        SerializerMethodField,
                                        ValidationError)

# Usuario
User = get_user_model()

# Create User
class UserCreateSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password',
		]
		extra_kwargs = {"password": {"write_only": True}
		}

	# Validacion de Datos del usuario al crearlo
	def create(self, validated_data):
		print(validated_data)
		username 	= validated_data['username']
		email 		= validated_data['email']
		password 	= validated_data['password']
		# Objeto usuario
		user_obj 	= User(username=username, email=email)
		# Para guardar correctamente la contraseña
		user_obj.set_password(password)
		user_obj.save()
		return validated_data