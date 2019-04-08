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
    class Meta:
        model = Comment
        fields = [
            "Detail_url",
            "id",
            "object_id",
            "content_type",
            #"content_object",
            "parent",
            "content", 
            #"timestamp", 
            "author"]
    
    def get_author(self, obj):
        return str(obj.author.username)

class CommentDetailSerializers(ModelSerializer):
    author = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            "id",
            "object_id",
            "content_type",
            #"content_object",
            "parent",
            "content", 
            "timestamp", 
            "author"]
    
    def get_author(self, obj):
        return str(obj.author.username)