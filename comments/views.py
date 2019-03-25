# Django
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Project
from .models import Comment
from comments.forms import CommentForm

def comment_detail(request, id):
	template_name = 'comment_detail.html'
	obj = get_object_or_404(Comment, id = id)
	form = CommentForm(request.POST or None)

	if form.is_valid():
		print(form.cleaned_data)
		c_type 			= form.cleaned_data.get("content_type")
		content_type 	= ContentType.objects.get(model=c_type)
		obj_id 			= form.cleaned_data.get("object_id")
		content_data 	= form.cleaned_data.get("content")
		
		# Verificamos si existe el padre de un comentario
		parent_obj		= None
		try:
			parent_id	= int(request.POST.get("parent_id"))
		except:
			parent_id	= None
		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs[0] #.first()

		# Creamos un comentario
		new_comment, created = Comment.objects.get_or_create(
										author = request.user,
										content_type = content_type,
										object_id= obj_id,
										content=content_data,
										parent = parent_obj
										)
		if created:
			messages.success(request, "Añadiste un comentario al POST: %s" % instance.title)

		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	context = {
		"comment": obj,
		"form": form
	}
	return render(request, template_name, context)

