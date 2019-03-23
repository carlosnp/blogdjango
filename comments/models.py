# Django
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Django External App

# Project


class CommentManager(models.Manager):

	def filter_by_instance(self, instance):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		obj_id 		 = instance.id
		qs = super(CommentManager, self).filter(content_type = content_type, object_id = obj_id)
		return qs

class Comment(models.Model):
	author      	= models.ForeignKey(
					settings.AUTH_USER_MODEL, 
					default = 1, 
					on_delete=models.CASCADE, 
					verbose_name="Autor",)
	
	content_type 	= models.ForeignKey(
					ContentType, 
					on_delete=models.CASCADE,
					verbose_name="Tipo de Contenido",)
	object_id 	 	= models.PositiveIntegerField(
    				"ID",)
	content_object 	= GenericForeignKey(
    				'content_type', 
    				'object_id')

	content 		= models.TextField("Comentario")
	timestamp   	= models.DateTimeField(
					"Fecha de creación",
					auto_now=False, 
					auto_now_add=True)

	# Instanceamos el filtro
	objects = CommentManager()

	def __unicode__(self):
		return str(self.author.username)
	
	def __str__(self):
		return str(self.author.username)