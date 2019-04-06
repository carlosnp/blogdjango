# Django
from rest_framework.serializers import ModelSerializer
# Project
from posts.models import Post

class PostListSerializers(ModelSerializer):
	class Meta:
		model = Post
		fields = ["id","title", "content", "image", "draf", "publish","author"]

class PostDetailSerializers(ModelSerializer):
	class Meta:
		model = Post
		fields = ["id","title", "slug","content", "image", "draf", "publish", "updated", "read_time","author"]

class PostCreateUpdateSerializers(ModelSerializer):
	class Meta:
		model = Post
		fields = ["title", "content", "image", "draf", "publish", "author"]

