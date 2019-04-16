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
			'password',
			'email'
		]
		extra_kwargs = {"password":
							{"write_only": True}
		}