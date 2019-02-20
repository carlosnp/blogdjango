# Django
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Project
from django.db import models

# Actualizar la imagen y guardarla en una carpeta con el id del usuario
def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    return "%s/%s"%(instance.id, filename)
    # return "%s/%s.%s"%(instance.id, instance.id, extension)

# Create your models here.
class Post(models.Model):
    title       = models.CharField("Titulo",max_length=120)
    slug        = models.SlugField(
                null=True, 
                blank=True,
                unique=True)
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

    def __unicode__(self):
        return self.title
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
    	# return "/posts/%s/"%(self.id)
    	return reverse("posts:detail", kwargs={"id":self.id})
    
    class Meta:
        ordering = ["-id","-timestamp", "-updated"]

# Slug funtions
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)