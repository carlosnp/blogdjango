# Django
from django.db import models
from django.conf import settings
from django.utils import timezone

# Django External App

# Project
from posts.models import Post

class Comment(models.Model):
	author      = models.ForeignKey(
				settings.AUTH_USER_MODEL, 
				default = 1, 
				on_delete=models.CASCADE, 
				verbose_name="Autor")
	post 		= models.ForeignKey(
				Post, 
				on_delete=models.CASCADE,)
	content 	= models.TextField("Comentario")
	timestamp   = models.DateTimeField(
				"Fecha de creación",
				auto_now=False, 
				auto_now_add=True)

	def __unicode__(self):
		return str(self.author.username)
	
	def __str__(self):
		return str(self.author.username)