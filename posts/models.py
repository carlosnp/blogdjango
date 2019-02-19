from django.db import models
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title       = models.CharField("Titulo",max_length=120)
    content     = models.TextField("Contenido")
    updated     = models.DateTimeField("Fecha de Actualizacion",auto_now=True, auto_now_add=False)
    timestamp   = models.DateTimeField("Fecha de creacion",auto_now=False, auto_now_add=True)
    author      = models.CharField("Autor",max_length=120)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
    	# return "/posts/%s/"%(self.id)
    	return reverse("posts:detail", kwargs={"id":self.id})