# Django
from rest_framework.serializers import (ModelSerializer, 
                                        HyperlinkedIdentityField, 
                                        SerializerMethodField)
# Project
from posts.models import Post
from comments.models import Comment
from comments.api.serializers import CommentListSerializers

POST_Detail_url = HyperlinkedIdentityField(view_name = 'posts_api:detail',lookup_field = 'pk')
POST_Delete_url = HyperlinkedIdentityField(view_name = 'posts_api:delete',lookup_field = 'pk')
POST_Edit_url   = HyperlinkedIdentityField(view_name = 'posts_api:update',lookup_field = 'pk')

class PostListSerializers(ModelSerializer):
    Detail_url = POST_Detail_url
    author = SerializerMethodField()
    class Meta:
        model = Post
        fields = ["Detail_url", "title", "content", "image", "draf", "publish","author"]
    
    def get_author(self, obj):
        return str(obj.author.username)

class PostDetailSerializers(ModelSerializer):
    Detail_url  = POST_Detail_url
    Delete_url  = POST_Delete_url
    Edit_url    = POST_Edit_url
    author      = SerializerMethodField()
    image       = SerializerMethodField()
    html        = SerializerMethodField()
    comments    = SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ["Detail_url","Edit_url","Delete_url",
                  "html","id","title", "slug","content", 
                  "image", "draf", "timestamp", "publish", 
                  "updated", "read_time","author", "comments"]
    
    # Para usar la app markdown delcarada en el modelo
    def get_html(self, obj):
        return obj.get_markdown()
    
    # Aparece el nombre del autor en vez de un numero
    def get_author(self, obj):
        return str(obj.author.username)
    
    # para obtener la url de la imagen
    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        
        return image
    
    def get_comments(self, obj):
        #content_type    = obj.get_content_type
        #object_id       = obj.id
        commnets_qs     = Comment.objects.filter_by_instance(obj)
        comments        = CommentListSerializers(commnets_qs, many=True).data
        return comments

        pass

class PostCreateUpdateSerializers(ModelSerializer):
    author = SerializerMethodField()
    class Meta:
        model = Post
        fields = ["title", "content", "image", "draf", "publish", "author"]
    
    def get_author(self, obj):
        return str(obj.author.username)

