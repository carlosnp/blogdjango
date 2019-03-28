# Django
from django.contrib import admin

# Project
from .models import Comment

class CommentModelAdmin(admin.ModelAdmin):
	list_display        = ('author', 'content_type','timestamp')
	list_display_links  = ["author"]
	list_filter         = ["author",]
	search_fields       = ["author", 'content_type']

admin.site.register(Comment, CommentModelAdmin)