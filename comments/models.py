# Django
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Django External App

# Project


class CommentManager(models.Manager):

	def all(self):
		qs = super(CommentManager, self).filter(parent=None)
		return qs

	def filter_by_instance(self, instance):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		obj_id 		 = instance.id
		qs = super(CommentManager, self).filter(content_type = content_type, object_id = obj_id).filter(parent=None)
		return qs
	
	def create_by_model_type(self, model_type, slug, content, user, parent_obj=None, author=None):
		model_qs = ContentType.objects.filter(model=model_type)
		# Si existe el modelo
		if model_qs.exists():
			Somemodel = model_qs.first().model_class()
			print(Somemodel)
			obj_qs = Somemodel.objects.filter(slug=slug)
			print(obj_qs)
			# si existe el objeo y es igual a uno
			if obj_qs.exists() and obj_qs.count() == 1:
				# Para crear el comentario
				instance 				= self.model()
				instance.content 		= content
				instance.author 		= user
				instance.content_type 	= model_qs.first()
				instance.object_id 		= obj_qs.first().id
				print(instance)
				# Si un objeto padre
				if parent_obj:
					instance.parent = parent_obj
				# Guardamos las instancias
				instance.save()
				return instance
		return None	

class Comment(models.Model):
	author      	= models.ForeignKey(
					settings.AUTH_USER_MODEL, 
					default = 1, 
					on_delete=models.CASCADE, 
					verbose_name='Autor',)
	
	content_type 	= models.ForeignKey(
					ContentType, 
					on_delete=models.CASCADE,
					verbose_name='Tipo de Contenido',)
	object_id 	 	= models.PositiveIntegerField(
    				'ID',)
	content_object 	= GenericForeignKey(
    				'content_type', 
    				'object_id')

	parent			= models.ForeignKey(
					'self',
					on_delete=models.CASCADE, 
					null=True,
					blank=True)
	
	content 		= models.TextField('Comentario')
	timestamp   	= models.DateTimeField(
					'Fecha de creación',
					auto_now=False, 
					auto_now_add=True)

	# Instanceamos el filtro
	objects = CommentManager()

	# Creamos una clase para ordenar los comentarios por fecha
	class Meta:
		ordering = ['-timestamp']

	def __unicode__(self):
		return str(self.author.username)
	
	def __str__(self):
		return str(self.author.username)
	
	# URL de los comentarios
	def get_absolute_url(self):
		return reverse("comments:detail", kwargs={"id":self.id})
	
	# URL para eliminar los comentarios	
	def get_delete_url(self):	
		return reverse("comments:delete", kwargs={"id":self.id})
	
	# Definimos los Hijos de los comentarios
	def children(self):
		return Comment.objects.filter(parent=self)
	
	# Verificamos si es el padre
	@property
	def is_parent(self):
		if self.parent is not None:
			return False
		return True