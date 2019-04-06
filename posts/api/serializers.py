# Django
from rest_framework.serializers import ModelSerializer
# Project
from posts.models import Post

class PostSerializers(ModelSerializer):
	class Meta:
		model = Post
		fields = ["id","title", "content", "image", "draf", "publish","author"]

