from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Post
from django.http import HttpResponse

def posts_create(request):
    return HttpResponse("<h1>Crear</h1>")

def posts_detail(request, id):
	template_name = 'post_detail.html'
	# instance = Post.objects.all()
	instance = get_object_or_404(Post, id = id)
	context = {
		"title": "Detalles del Post",
		"instance": instance,
	}
	return render(request, template_name, context)

def posts_list(request):
	template_name = 'post_list.html'
	queryset = Post.objects.all()
	context = {
		"title": "Lista de Post",
		"object_list": queryset,
	}	
	# if request.user.is_authenticated:
	# 	context = {
	# 		"title": "Autenticado"
	# 	}
	# else:
	# 	context = {
	# 		"title": "Lista"
	# 	}
	return render(request, template_name, context)

def posts_update(request):
    return HttpResponse("<h1>Actualizar</h1>")

def posts_delete(request):
    return HttpResponse("<h1>Borrar</h1>")

