# Django
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
# Django Rest Framework
from rest_framework.serializers import (ModelSerializer, 
                                        HyperlinkedIdentityField, 
                                        SerializerMethodField,
                                        ValidationError)
# Project
from comments.models import Comment

COMMENT_Detail_url = HyperlinkedIdentityField(view_name = 'comments_api:detail',lookup_field = 'pk')

# Usuario
User = get_user_model()

# Funcion para crear un comentario
def create_commnet_serializers(model_type='post', slug=None, parent_id=None, author=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                    "id",
                    #"parent",
                    "content",
                    "timestamp",        
                    # "author"
            ]
        # Inicializamos la funcion
        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if parent_id:
                # Verificamos si existe el elemento
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)
        
        # Validamos los datos
        def validate(self, data):
            # partimos de la dara inicializada en la funcion anterior
            model_type = self.model_type
            # Verificamos que existe
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("No es un tipo de contenido valido")
            # Verificamos si existe SLUG en el modelo
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("No es un slug valido")
            # Retornamos la data
            return data

        # Metodo para crear el comentario
        def create(self, validated_data):
            # Debemos tener todos los campos que se definieron en la funcion
            content     = validated_data.get("content")
            if author:
                main_user = author
            else:
                main_user = User.objects.all().first()
            model_type  = self.model_type
            slug        = self.slug
            parent_obj  = self.parent_obj
            comment     = Comment.objects.create_by_model_type(
                            model_type, slug, content,
                            main_user, parent_obj=parent_obj)
            # Regresamos el comentario
            return comment
    # Regresamos la clase
    return CommentCreateSerializer

class CommentListSerializers(ModelSerializer):
    #Detail_url = COMMENT_Detail_url
    author = SerializerMethodField()
    reply_count = SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            #"Detail_url",
            "id",
            #"object_id",
            #"content_type",
            #"content_object",
            #"parent",
            "content", 
            #"timestamp",
            "reply_count", 
            "author"]
    
    # Cuenta las replicas a un comentario
    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
    
    def get_author(self, obj):
        return str(obj.author.username)

class CommentChildSerializers(ModelSerializer):
    author = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            "id",
            "content", 
            "timestamp", 
            "author"]
    
    def get_author(self, obj):
        return str(obj.author.username)

class CommentDetailSerializers(ModelSerializer):
    author = SerializerMethodField()
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            "id",
            "object_id",
            "content_type",
            #"content_object",
            "content", 
            "timestamp",
            "author",
            "reply_count", 
            "replies",
        ]
    
    def get_author(self, obj):
        return str(obj.author.username)
    
    # Determina si hay replicas a un comentario
    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializers(obj.children(), many=True).data
        return None
    
    # Cuenta las replicas a un comentario
    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentEditSerializers(ModelSerializer):
    author = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            "id",
            "content", 
            "timestamp",
            "author",
        ]
    
    def get_author(self, obj):
        return str(obj.author.username)