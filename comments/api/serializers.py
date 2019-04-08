# Django
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
# Django Rest Framework
from rest_framework.serializers import (ModelSerializer, 
                                        HyperlinkedIdentityField, 
                                        SerializerMethodField)
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
                    "parent",
                    "content",
                    "timestamp",        
                    "author"
            ]
        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if self.parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exist() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)
        
        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            
            if not model_qs.exist() or model_qs.count() != 1:
                raise ValidationError("No es un contenido valido")
            
            Somemodel = model_qs.first().model_class()
            obj_qs = Somemodel.objects.filter(slug=self.slug)
            
            if not obj_qs.exist() or obj_qs.count() != 1:
                raise ValidationError("No es un slug valido")
            
            return data

        def create(sefl, validated_data):
            content     = validated_data.get("content")
            user        = User.objects.all().first()
            model_type  = self.model_type
            slug        = self.slug
            parent_obj  = self.parent_obj
            comment     = Comment.objects.create_by_model_type(
                                            model_type=model_type, 
                                            slug = slug,
                                            content = content,
                                            author=user,
                                            parent_obj= parent_obj)
            return comment
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
            "replies"]
    
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