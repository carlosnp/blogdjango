# Django
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Project
from .models import Comment
from comments.forms import CommentForm

# Eliminar comentario
def comment_delete(request, id):
	template_name 	= "comment_confirm_delete.html"
	#obj 			= get_object_or_404(Comment, id = id)

	# Delete Permissions
	#obj = Comment.objects.get(id=id)
	try:
		obj = Comment.objects.get(id=id)
	except:
		raise Http404

	if obj.author != request.user:
		# Metodo 1
		#messages.success(request, "No tienes permisos para ver esto.")
		#raise Http404
		# Metodo 2
		response = HttpResponse("No tienes permisos para ver esto.")
		response.status_code = 403
		return response
		#return render(request, template_name, context, status_code = 403)

	if request.method == "POST":
		parent_obj_url = obj.content_object.get_absolute_url()
		obj.delete()
		messages.success(request, "Ha sido Eliminado un comentario.")
		return HttpResponseRedirect(parent_obj_url)
	context = {
		"object": obj,
	}
	return render(request, template_name, context)

# Detalles de los comentarios
def comment_detail(request, id):
	template_name 	= 'comment_detail.html'
	#obj 			= get_object_or_404(Comment, id = id)

	# Delete Permissions
	#obj = Comment.objects.get(id=id)
	try:
		obj = Comment.objects.get(id=id)
	except:
		raise Http404

	#Si el objeto no es el padre
	if not obj.is_parent:
		obj = obj.parent

	content_object	= obj.content_object
	content_id		= obj.content_object.id

	# Base de Datos inicial
	initial_data 	= {
		"content_type": obj.content_type,
		"object_id": obj.object_id,
	}

	# Formulario de comentarios
	form = CommentForm(request.POST or None, initial=initial_data)
	# Si el formulario es valido
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
			messages.success(request, "Añadiste un comentario al POST")

		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	context = {
		"comment": obj,
		"form": form
	}
	return render(request, template_name, context)

