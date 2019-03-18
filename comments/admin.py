# Django
from django.contrib import admin

# Project
from .models import Comment

class CommentModelAdmin(admin.ModelAdmin):
	list_display        = ('author', 'post', 'content_type','timestamp')
	list_display_links  = ["post"]
	list_filter         = ["author", "post"]
	search_fields       = ["author", "post", 'content_type']

admin.site.register(Comment, CommentModelAdmin)