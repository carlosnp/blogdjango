# Django
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType

# Django External App
from markdown_deux import markdown

# Project
from .utils import get_read_time
from comments.models import Comment

# Filtro de la lista de post
# Post.objects.all()
# Post.objects.create(user=user, title="Some time")
class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draf=False).filter(publish__lte=timezone.now())

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
    height_field= models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content     = models.TextField("Contenido")
    draf        = models.BooleanField("Borrador", default=False)
    publish     = models.DateField("Publicar", auto_now=False, auto_now_add=False)
    read_time   = models.TimeField(blank=True, null=True)
    updated     = models.DateTimeField("Fecha de Actualización",auto_now=True, auto_now_add=False)
    timestamp   = models.DateTimeField("Fecha de creación",auto_now=False, auto_now_add=True)
    author      = models.ForeignKey( 
                settings.AUTH_USER_MODEL,
                default = 1,
                on_delete=models.CASCADE,
                verbose_name="Autor")

    # instanciamos el filtro
    objects = PostManager()

    def __unicode__(self):
        return self.title
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
    	# return "/posts/%s/"%(self.id)
    	return reverse("posts:detail", kwargs={"id":self.id})

    def get_markdown(self):
        content = self.content
        return mark_safe(markdown(content))
    
    class Meta:
        ordering = ["-id","-timestamp", "-updated"]

    # Propiedad Comentarios
    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(self)
        return qs
    
    # Crear Comentarios
    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

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

    if instance.content:
        html_string     = instance.get_markdown()
        read_time_var   = get_read_time(html_string)
        instance.read_time = read_time_var

pre_save.connect(pre_save_post_receiver, sender=Post)