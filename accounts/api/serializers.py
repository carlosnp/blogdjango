# Django
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
# Django Rest Framework Serializers
from rest_framework.serializers import (# Serializer
										ModelSerializer,
										# Serializer Fields
										CharField,
										EmailField,
										# Serializer Fields Miscellaneous
                                        SerializerMethodField,
                                        # Serializer Relations
                                        HyperlinkedIdentityField,
                                        ValidationError)

# Usuario
User = get_user_model()

# Create User
class UserCreateSerializer(ModelSerializer):
	email = EmailField(label='Dirección de Correo Electrónico')
	email2 = EmailField(label='Confirme Dirección de Correo Electrónico')
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password',
		]
		extra_kwargs = {"password": {"write_only": True}
		}

	# Validando SI existe el correo electronico
	def validate(self, data):
		email = data['email']
		user_qs = User.objects.filter(email=email)
		if user_qs.exists():
			raise ValidationError("Esta dirección de Correo Electrónico YA fue registrada")
		return data

	# Validacion del correo electronico
	def validate_email2(self, value):
		data 	= self.get_initial()
		email1 	= data.get("email")
		email2 	= value
		if email1 != email2:
			raise ValidationError("La Dirección de Correo Electrónico NO coincide.")
		return value

	# Validacion de Datos del usuario al crearlo
	def create(self, validated_data):
		username 	= validated_data['username']
		email 		= validated_data['email']
		password 	= validated_data['password']
		# Objeto usuario
		user_obj 	= User(username=username, email=email)
		# Para guardar correctamente la contraseña
		user_obj.set_password(password)
		user_obj.save()
		return validated_data

# Login User
class UserLoginSerializer(ModelSerializer):
	# Para verificar con un token al usuario
	token	 = CharField(allow_blank=True, read_only=True)
	username = CharField(label='Nombre de Usuario', required=False, allow_blank=True)	
	email    = EmailField(label='Dirección de Correo Electrónico', required=False, allow_blank=True)
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password',
			'token'
		]
		extra_kwargs = {"password": {"write_only": True}
		}

	# Validando los campos del login
	def validate(self, data):
		# Declaramos los campos del usuario
		user_obj	= None
		email 		= data.get("email", None)
		username 	= data.get("username", None)
		password 	= data["password"]
		
		# Validamos que el usuario escriba el nombre y el correo electronico
		if not email or not username:	
			raise ValidationError("Se requiere un nombre de usuario o correo electrónico para iniciar sesión")

		# Buscamos y filtramos al usuario por nombre y correo electronico
		user 		= User.objects.filter(
						Q(email=email) |
						Q(username=username)
						).distinct() # 'distinct' elimina filas duplicadas de los resultados de la consulta
		# Excluimos los usuarios sin correo electronico
		user 		= user.exclude(email__isnull=True).exclude(email__iexact='')

		# Si el usuario existe y solo hay uno
		if user.exists() and user.count() == 1:
			user_obj = user.first()
		else:
			raise ValidationError("El nombre de usuario o el Correo Electronico NO son validos")			
		
		#
		if user_obj:
			# Validadmos la contraseña
			if not user_obj.check_password(password):
				raise ValidationError("Contraseña incorrecta!!!. Intentalo otra vez.")
		
		# Token
		data["token"] = "Token aleatorio"

		return data