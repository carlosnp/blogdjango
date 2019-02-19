from django.db import models
from django.urls import reverse

# Actualizar la imagen y guardarla en una carpeta con el id del usuario
def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    return "%s/%s"%(instance.id, filename)
    # return "%s/%s.%s"%(instance.id, instance.id, extension)

# Create your models here.
class Post(models.Model):
    title       = models.CharField("Titulo",max_length=120)
    image       = models.ImageField("Imagen", 
                null=True,
                blank=True, 
                upload_to = upload_location,
                height_field="height_field", 
                width_field="width_field", 
                max_length=None)
    height_field=models.IntegerField(default=0)
    width_field =models.IntegerField(default=0)
    content     = models.TextField("Contenido")
    updated     = models.DateTimeField("Fecha de Actualizacion",auto_now=True, auto_now_add=False)
    timestamp   = models.DateTimeField("Fecha de creacion",auto_now=False, auto_now_add=True)
    author      = models.CharField("Autor",max_length=120)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
    	# return "/posts/%s/"%(self.id)
    	return reverse("posts:detail", kwargs={"id":self.id})
    
    class Meta:
        ordering = ["-id","-timestamp", "-updated"]