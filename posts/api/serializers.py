# Django
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
# Project
from posts.models import Post

POST_Detail_url = HyperlinkedIdentityField(view_name = 'posts_api:detail',lookup_field = 'pk')
POST_Delete_url = HyperlinkedIdentityField(view_name = 'posts_api:delete',lookup_field = 'pk')
POST_Edit_url   = HyperlinkedIdentityField(view_name = 'posts_api:update',lookup_field = 'pk')

class PostListSerializers(ModelSerializer):
    Detail_url = POST_Detail_url
    class Meta:
        model = Post
        fields = ["Detail_url","title", "content", "image", "draf", "publish","author"]

class PostDetailSerializers(ModelSerializer):
    Delete_url = POST_Delete_url
    Edit_url = POST_Edit_url
    class Meta:
        model = Post
        fields = ["Edit_url","Delete_url","id","title", "slug","content", "image", "draf", "timestamp", "publish", "updated", "read_time","author"]

class PostCreateUpdateSerializers(ModelSerializer):
	class Meta:
		model = Post
		fields = ["title", "content", "image", "draf", "publish"]

