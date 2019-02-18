from django.shortcuts import render

# Create your views here.
from .models import Post
from django.http import HttpResponse
from django.views.generic import ListView

def posts_create(request):
    return HttpResponse("<h1>Crear</h1>")

def posts_detail(request):
	context = {
		"title": "Detalles"
	}
	return render(request, "post_list.html", context)

def posts_list(request):
	context = {
			"title": "Lista"
	}	
	# if request.user.is_authenticated:
	# 	context = {
	# 		"title": "Autenticado"
	# 	}
	# else:
	# 	context = {
	# 		"title": "Lista"
	# 	}
	return render(request, "post_list.html", context)

def posts_update(request):
    return HttpResponse("<h1>Actualizar</h1>")

def posts_delete(request):
    return HttpResponse("<h1>Borrar</h1>")

