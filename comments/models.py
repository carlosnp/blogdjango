# Django
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Django External App

# Project
from posts.models import Post

class Comment(models.Model):
	author      	= models.ForeignKey(
					settings.AUTH_USER_MODEL, 
					default = 1, 
					on_delete=models.CASCADE, 
					verbose_name="Autor")
	post 			= models.ForeignKey(
					Post, 
					on_delete=models.CASCADE,)
	
	content_type 	= models.ForeignKey(
					ContentType, 
					on_delete=models.CASCADE,
					verbose_name="Tipo de Contenido",
					null=True,)
	object_id 	 	= models.PositiveIntegerField(
    				"ID", 
    				null=True,)
	content_object 	= GenericForeignKey(
    				'content_type', 
    				'object_id')

	content 		= models.TextField("Comentario")
	timestamp   	= models.DateTimeField(
					"Fecha de creación",
					auto_now=False, 
					auto_now_add=True)

	def __unicode__(self):
		return str(self.author.username)
	
	def __str__(self):
		return str(self.author.username)