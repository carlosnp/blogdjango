# Django
from rest_framework.serializers import (ModelSerializer, 
                                        HyperlinkedIdentityField, 
                                        SerializerMethodField)

# Project
from comments.models import Comment

COMMENT_Detail_url = HyperlinkedIdentityField(view_name = 'comments_api:detail',lookup_field = 'pk')

class CommentListSerializers(ModelSerializer):
    Detail_url = COMMENT_Detail_url
    author = SerializerMethodField()
    reply_count = SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            "Detail_url",
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